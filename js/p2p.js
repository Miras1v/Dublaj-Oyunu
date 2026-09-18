// Dublaj Oyunu - P2P WebRTC Bağlantı Motoru (PeerJS)
// Sıfır Sunucu Maliyeti: Oda Kurucusu (Host) ve İstemciler (Clients)

export class P2PNetwork {
  constructor(options = {}) {
    this.peer = null;
    this.isHost = false;
    this.roomId = null;
    this.peerId = null;
    this.connections = new Map(); // Host için: peerId -> conn
    this.hostConnection = null;   // Client için: conn to host
    this.user = {
      name: options.name || "Oyuncu " + Math.floor(1000 + Math.random() * 9000),
      avatar: options.avatar || "🎙️",
      roleId: null,
      isReady: false
    };

    this.isAdmin = !!options.isAdmin;

    // Callback event handlers
    this.onStateChange = options.onStateChange || (() => {});
    this.onPeerJoin = options.onPeerJoin || (() => {});
    this.onPeerLeave = options.onPeerLeave || (() => {});
    this.onStartRecording = options.onStartRecording || (() => {});
    this.onStartPremiere = options.onStartPremiere || (() => {});
    this.onAudioReceived = options.onAudioReceived || (() => {});
    this.onRecordingsReady = options.onRecordingsReady || (() => {});
    this.onCustomSceneReceived = options.onCustomSceneReceived || (() => {});
    this.onTransferProgress = options.onTransferProgress || (() => {});
    this.onSceneUpdated = options.onSceneUpdated || (() => {});
    this.onCharactersUpdated = options.onCharactersUpdated || (() => {});
    this.onError = options.onError || ((err) => console.error(err));

    // WebRTC Chunk Transfer Havuzları (Büyük videoların 64KB SCTP sınırını aşmaması için)
    this.incomingTransfers = new Map(); // transferId -> { sceneMeta, totalChunks, receivedCount, chunks }
    this.cachedCustomVideos = new Map(); // sceneId -> base64Data

    // Global Room State (Host tarafından yönetilir - ASLA devasa video binary içermez!)
    this.state = {
      roomId: null,
      stage: "lobby", // 'lobby' | 'role_select' | 'recording' | 'mixing' | 'premiere'
      selectedSceneId: "sifir-bir-racon",
      players: [],
      audioTracks: {}, // characterId -> { audioUrl, duration }
      recordingsReady: false,
      allRecordingsCount: { current: 0, total: 0 },
      customScenes: [] // scene metadata only (hafif ve hızlı senkron)
    };
  }

  // Rastgele 6 haneli havalı oda kodu üretir
  _generateRoomCode() {
    const chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
    let code = "DUB-";
    for (let i = 0; i < 4; i++) {
      code += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return code;
  }

  // 1. ODA OLUŞTUR (HOST MODU)
  createRoom(customCode) {
    return new Promise((resolve, reject) => {
      const roomCode = customCode || this._generateRoomCode();
      this.isHost = true;
      this.roomId = roomCode;

      // PeerJS Cloud (Ücretsiz Public STUN/TURN el sıkışma sunucusu)
      this.peer = new window.Peer(roomCode, {
        debug: 1,
        config: {
          iceServers: [
            { urls: "stun:stun.l.google.com:19302" },
            { urls: "stun:global.stun.twilio.com:3478" }
          ]
        }
      });

      this.peer.on("open", (id) => {
        this.peerId = id;
        this.state.roomId = id;
        this.state.players = [{
          id: id,
          name: this.user.name,
          avatar: this.user.avatar,
          isHost: true,
          roleId: null,
          isReady: true
        }];
        this.onStateChange(this.state);
        resolve(id);
      });

      this.peer.on("connection", (conn) => {
        this._setupHostConnection(conn);
      });

      this.peer.on("error", (err) => {
        if (err.type === "unavailable-id") {
          // Kod çakışması olursa yeni kod dene
          this.peer.destroy();
          this.createRoom().then(resolve).catch(reject);
        } else {
          this.onError(err);
          reject(err);
        }
      });
    });
  }

  // Host: Yeni oyuncu bağlantısını karşıla
  _setupHostConnection(conn) {
    conn.on("open", () => {
      this.connections.set(conn.peer, conn);

      conn.on("data", (data) => {
        this._handleHostMessage(conn.peer, data);
      });

      conn.on("close", () => {
        this.connections.delete(conn.peer);
        this.state.players = this.state.players.filter(p => p.id !== conn.peer);
        this._broadcastState();
        this.onPeerLeave(conn.peer);
      });
    });
  }

  // Host: Gelen veri paketlerini işle
  _handleHostMessage(peerId, data) {
    switch (data.type) {
      case "JOIN": {
        const newPlayer = {
          id: peerId,
          name: data.name,
          avatar: data.avatar,
          isHost: false,
          roleId: null,
          isReady: false
        };
        this.state.players.push(newPlayer);
        this._broadcastState();
        this.onPeerJoin(newPlayer);

        // Yeni katılan oyuncuya lobide önceden yüklenmiş özel sahneleri otomatik stream et
        if (this.state.customScenes && this.state.customScenes.length > 0) {
          const conn = this.connections.get(peerId);
          if (conn && conn.open) {
            this.state.customScenes.forEach(sceneMeta => {
              const videoBase64 = this.cachedCustomVideos.get(sceneMeta.id);
              if (videoBase64) {
                const transferId = "join-vid-" + Date.now() + "-" + sceneMeta.id;
                this._sendChunkedVideo(conn, transferId, sceneMeta, videoBase64);
              }
            });
          }
        }
        break;
      }

      case "SELECT_ROLE": {
        const player = this.state.players.find(p => p.id === peerId);
        if (player) {
          player.roleId = data.roleId;
          this._broadcastState();
        }
        break;
      }

      case "TOGGLE_READY": {
        const readyPlayer = this.state.players.find(p => p.id === peerId);
        if (readyPlayer) {
          readyPlayer.isReady = !readyPlayer.isReady;
          this._broadcastState();
        }
        break;
      }

      case "AUDIO_UPLOAD":
        // Oyuncudan gelen ses kaydı (base64 veya blob)
        this.state.audioTracks[data.characterId] = {
          characterId: data.characterId,
          audioData: data.audioData,
          playerName: data.playerName
        };
        this.onAudioReceived(data);
        this._checkAllRecordingsDone();
        break;

      case "VIDEO_CHUNK_START":
        this._handleIncomingChunkStart(data);
        break;

      case "VIDEO_CHUNK_DATA":
        this._handleIncomingChunkData(data);
        break;

      case "VIDEO_CHUNK_END": {
        const completed = this._handleIncomingChunkEnd(data);
        if (completed) {
          const { sceneMeta, videoBase64 } = completed;
          this.cachedCustomVideos.set(sceneMeta.id, videoBase64);
          if (!this.state.customScenes) this.state.customScenes = [];
          const existingIdx = this.state.customScenes.findIndex(s => s.id === sceneMeta.id);
          if (existingIdx >= 0) {
            this.state.customScenes[existingIdx] = sceneMeta;
          } else {
            this.state.customScenes.push(sceneMeta);
          }
          this.state.selectedSceneId = sceneMeta.id;
          this._broadcastState();

          // Diğer tüm istemcilere stream et
          const relayId = "relay-" + Date.now();
          for (const [id, c] of this.connections) {
            if (id !== peerId && c.open) {
              this._sendChunkedVideo(c, relayId, sceneMeta, videoBase64);
            }
          }

          const fullScene = { ...sceneMeta, videoData: videoBase64 };
          this.onCustomSceneReceived(fullScene);
        }
        break;
      }

      case "REQUEST_CUSTOM_SCENE_VIDEO": {
        const videoBase64 = this.cachedCustomVideos.get(data.sceneId);
        const sceneMeta = (this.state.customScenes || []).find(s => s.id === data.sceneId);
        const conn = this.connections.get(peerId);
        if (conn && conn.open && videoBase64 && sceneMeta) {
          const transferId = "req-vid-" + Date.now() + "-" + data.sceneId;
          this._sendChunkedVideo(conn, transferId, sceneMeta, videoBase64);
        }
        break;
      }

      case "UPLOAD_CUSTOM_SCENE": {
        // Fallback / legacy
        const sceneMeta = { ...data.scene };
        const videoBase64 = data.scene.videoData;
        delete sceneMeta.videoData;

        if (videoBase64) this.cachedCustomVideos.set(sceneMeta.id, videoBase64);
        if (!this.state.customScenes) this.state.customScenes = [];
        this.state.customScenes.push(sceneMeta);
        this.state.selectedSceneId = sceneMeta.id;
        this._broadcastState();

        if (videoBase64) {
          const transferId = "upload-vid-" + Date.now();
          for (const [_, c] of this.connections) {
            if (c.open) this._sendChunkedVideo(c, transferId, sceneMeta, videoBase64);
          }
        }
        this.onCustomSceneReceived(data.scene);
        break;
      }

      case "ADMIN_UPDATE_LINES":
        this._broadcast({ type: "SCENE_LINES_UPDATED", sceneId: data.sceneId, lines: data.lines });
        this.onSceneUpdated(data.sceneId, data.lines);
        break;

      case "ADMIN_UPDATE_CHARACTERS":
        this._broadcast({ type: "SCENE_CHARACTERS_UPDATED", sceneId: data.sceneId, characters: data.characters });
        this.onCharactersUpdated(data.sceneId, data.characters);
        break;

      case "ADMIN_FORCE_LAUNCH_PREMIERE":
        this.launchPremiere();
        break;

      default:
        console.warn("Bilinmeyen host mesajı:", data);
    }
  }

  // 2. ODAYA KATIL (CLIENT MODU)
  joinRoom(targetRoomId) {
    return new Promise((resolve, reject) => {
      this.isHost = false;
      this.roomId = targetRoomId.toUpperCase().trim();

      this.peer = new window.Peer({
        debug: 1,
        config: {
          iceServers: [
            { urls: "stun:stun.l.google.com:19302" },
            { urls: "stun:global.stun.twilio.com:3478" }
          ]
        }
      });

      this.peer.on("open", (id) => {
        this.peerId = id;
        const conn = this.peer.connect(this.roomId, { reliable: true });

        conn.on("open", () => {
          this.hostConnection = conn;
          // Katılım isteği gönder
          conn.send({
            type: "JOIN",
            name: this.user.name,
            avatar: this.user.avatar
          });
          resolve(this.roomId);
        });

        conn.on("data", (data) => {
          this._handleClientMessage(data);
        });

        conn.on("close", () => {
          this.onError(new Error("Oda kurucusuyla bağlantı kesildi."));
        });
      });

      this.peer.on("error", (err) => {
        this.onError(err);
        reject(err);
      });
    });
  }

  // Client: Host'tan gelen veri paketlerini işle
  _handleClientMessage(data) {
    switch (data.type) {
      case "STATE_UPDATE":
        this.state = data.state;
        this.onStateChange(this.state);
        break;

      case "START_RECORDING":
        this.onStartRecording(data.sceneId, data.assignedRole);
        break;

      case "START_PREMIERE":
        this.onStartPremiere(data.audioTracks);
        break;

      case "VIDEO_CHUNK_START":
        this._handleIncomingChunkStart(data);
        break;

      case "VIDEO_CHUNK_DATA":
        this._handleIncomingChunkData(data);
        break;

      case "VIDEO_CHUNK_END": {
        const completed = this._handleIncomingChunkEnd(data);
        if (completed) {
          const { sceneMeta, videoBase64 } = completed;
          if (!this.state.customScenes) this.state.customScenes = [];
          const existingIdx = this.state.customScenes.findIndex(s => s.id === sceneMeta.id);
          if (existingIdx >= 0) {
            this.state.customScenes[existingIdx] = sceneMeta;
          } else {
            this.state.customScenes.push(sceneMeta);
          }
          const fullScene = { ...sceneMeta, videoData: videoBase64 };
          this.onCustomSceneReceived(fullScene);
        }
        break;
      }

      case "NEW_CUSTOM_SCENE":
        if (!this.state.customScenes) this.state.customScenes = [];
        this.state.customScenes.push(data.scene);
        this.onCustomSceneReceived(data.scene);
        break;

      case "SCENE_LINES_UPDATED":
        this.onSceneUpdated(data.sceneId, data.lines);
        break;

      case "SCENE_CHARACTERS_UPDATED":
        this.onCharactersUpdated(data.sceneId, data.characters);
        break;

      default:
        console.warn("Bilinmeyen client mesajı:", data);
    }
  }

  // --- ORTAK / YARDIMCI EYLEMLER ---

  // Host: Sahne değiştir
  selectScene(sceneId) {
    if (!this.isHost) return;
    this.state.selectedSceneId = sceneId;
    // Rolleri sıfırla
    this.state.players.forEach(p => p.roleId = null);
    this.state.audioTracks = {};
    this.state.recordingsReady = false;
    this._broadcastState();
  }

  // Rol Seç (Host veya Client)
  selectRole(roleId) {
    if (this.isHost) {
      const hostPlayer = this.state.players.find(p => p.isHost);
      if (hostPlayer) hostPlayer.roleId = roleId;
      this._broadcastState();
    } else if (this.hostConnection) {
      this.hostConnection.send({ type: "SELECT_ROLE", roleId });
    }
  }

  // Kayıt Başlat (Sadece Host)
  startDubbingCountdown() {
    if (!this.isHost) return;
    this.state.stage = "recording";
    this.state.audioTracks = {};
    this.state.recordingsReady = false;
    this._broadcastState();

    // Tüm istemcilere anlık senkron komutu yolla
    this._broadcast({
      type: "START_RECORDING",
      sceneId: this.state.selectedSceneId
    });
    this.onStartRecording(this.state.selectedSceneId);
  }

  // Kaydedilen Sesi Gönder (Client veya Host)
  sendVoiceRecording(characterId, audioBase64) {
    const payload = {
      type: "AUDIO_UPLOAD",
      characterId,
      audioData: audioBase64,
      playerName: this.user.name
    };

    if (this.isHost) {
      this._handleHostMessage(this.peerId, payload);
    } else if (this.hostConnection) {
      this.hostConnection.send(payload);
    }
  }

  // Host: Tüm sesler geldi mi kontrol et (Seyirci/İzleyiciler ses göndermek zorunda değildir)
  _checkAllRecordingsDone() {
    if (!this.isHost) return;
    const assignedRoles = this.state.players
      .filter(p => p.roleId && p.roleId !== "spectator")
      .map(p => p.roleId);
    const recordedRoles = Object.keys(this.state.audioTracks);

    const isComplete = assignedRoles.length > 0 && assignedRoles.every(role => recordedRoles.includes(role));
    this.state.recordingsReady = isComplete;
    this.state.allRecordingsCount = { current: recordedRoles.length, total: assignedRoles.length };

    this._broadcastState();
    if (isComplete) {
      this.onRecordingsReady(this.state);
    }
  }

  // YALNIZCA HOST / ADMİN YETKİSİ: Filmi Başlat (Prömiyer)
  launchPremiere() {
    if (!this.isHost && !this.isAdmin) {
      console.warn("Yalnızca Oda Kurucusu (Host) veya Admin filmi başlatabilir!");
      return false;
    }

    if (this.isHost) {
      this.state.stage = "premiere";
      this._broadcastState();
      this._broadcast({
        type: "START_PREMIERE",
        audioTracks: this.state.audioTracks
      });
      this.onStartPremiere(this.state.audioTracks);
    } else if (this.hostConnection && this.isAdmin) {
      this.hostConnection.send({ type: "ADMIN_FORCE_LAUNCH_PREMIERE" });
    }
    return true;
  }

  // --- WebRTC Chunked Video Transfer Motoru (64KB Sınırını Aşan Büyük Dosyalar İçin) ---
  _handleIncomingChunkStart(data) {
    this.incomingTransfers.set(data.transferId, {
      sceneMeta: data.sceneMeta,
      totalChunks: data.totalChunks,
      receivedCount: 0,
      chunks: new Array(data.totalChunks)
    });
    this.onTransferProgress({
      sceneTitle: data.sceneMeta.title,
      percent: 0,
      isReceiving: true
    });
  }

  _handleIncomingChunkData(data) {
    const transfer = this.incomingTransfers.get(data.transferId);
    if (!transfer) return;
    transfer.chunks[data.index] = data.chunk;
    transfer.receivedCount++;
    const pct = Math.min(99, Math.round((transfer.receivedCount / transfer.totalChunks) * 100));
    this.onTransferProgress({
      sceneTitle: transfer.sceneMeta.title,
      percent: pct,
      isReceiving: true
    });
  }

  _handleIncomingChunkEnd(data) {
    const transfer = this.incomingTransfers.get(data.transferId);
    if (!transfer) return null;
    this.incomingTransfers.delete(data.transferId);
    const videoBase64 = transfer.chunks.join("");
    this.onTransferProgress({
      sceneTitle: transfer.sceneMeta.title,
      percent: 100,
      isReceiving: true
    });
    return {
      sceneMeta: transfer.sceneMeta,
      videoBase64
    };
  }

  async _sendChunkedVideo(conn, transferId, sceneMeta, videoBase64) {
    if (!conn || !conn.open || !videoBase64) return;
    const CHUNK_SIZE = 16384; // 16 KB (WebRTC SCTP güvenli parça boyutu)
    const totalChunks = Math.ceil(videoBase64.length / CHUNK_SIZE);

    try {
      // 1. Transfer Başlat
      conn.send({
        type: "VIDEO_CHUNK_START",
        transferId,
        sceneMeta,
        totalChunks,
        totalSize: videoBase64.length
      });

      // 2. Parçaları Sırayla Gönder
      for (let i = 0; i < totalChunks; i++) {
        if (!conn.open) break;
        const chunk = videoBase64.substring(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE);
        conn.send({
          type: "VIDEO_CHUNK_DATA",
          transferId,
          index: i,
          chunk
        });

        if (i % 5 === 0 || i === totalChunks - 1) {
          const pct = Math.min(99, Math.round(((i + 1) / totalChunks) * 100));
          this.onTransferProgress({
            sceneTitle: sceneMeta.title,
            percent: pct,
            isReceiving: false
          });
        }

        // WebRTC SCTP buffer dolmasını önlemek için her 10 parçada 8ms nefes al
        if (i % 10 === 0) {
          await new Promise(r => setTimeout(r, 8));
        }
      }

      // 3. Transfer Bitiş
      if (conn.open) {
        conn.send({
          type: "VIDEO_CHUNK_END",
          transferId,
          sceneId: sceneMeta.id
        });
        this.onTransferProgress({
          sceneTitle: sceneMeta.title,
          percent: 100,
          isReceiving: false
        });
      }
    } catch (err) {
      console.error("Video chunk transfer hatası:", err);
    }
  }

  // Özel Video Sahnesi Yayınla (Chunked Stream ile Sıfır Senkron Kayması)
  async broadcastCustomScene(sceneData) {
    const videoBase64 = sceneData.videoData;
    const sceneMeta = { ...sceneData };
    delete sceneMeta.videoData; // Global state içine devasa base64 koyma (64KB sınırını patlatmamak için)

    if (videoBase64) {
      this.cachedCustomVideos.set(sceneMeta.id, videoBase64);
    }

    if (this.isHost) {
      if (!this.state.customScenes) this.state.customScenes = [];
      const existingIdx = this.state.customScenes.findIndex(s => s.id === sceneMeta.id);
      if (existingIdx >= 0) {
        this.state.customScenes[existingIdx] = sceneMeta;
      } else {
        this.state.customScenes.push(sceneMeta);
      }
      this.state.selectedSceneId = sceneMeta.id;
      this._broadcastState();

      // Odadaki tüm istemcilere chunked stream ile gönder
      const transferId = "host-vid-" + Date.now() + "-" + sceneMeta.id;
      for (const [_, conn] of this.connections) {
        if (conn.open && videoBase64) {
          this._sendChunkedVideo(conn, transferId, sceneMeta, videoBase64);
        }
      }

      this.onCustomSceneReceived(sceneData);
    } else if (this.hostConnection && this.hostConnection.open) {
      const transferId = "client-vid-" + Date.now() + "-" + sceneMeta.id;
      if (videoBase64) {
        await this._sendChunkedVideo(this.hostConnection, transferId, sceneMeta, videoBase64);
      }
    }
  }

  requestCustomSceneVideo(sceneId) {
    if (this.hostConnection && this.hostConnection.open) {
      this.hostConnection.send({
        type: "REQUEST_CUSTOM_SCENE_VIDEO",
        sceneId
      });
    }
  }

  // Transkript Değişikliklerini Yayınla
  broadcastUpdatedLines(sceneId, lines) {
    if (this.isHost) {
      this._broadcast({ type: "SCENE_LINES_UPDATED", sceneId, lines });
      this.onSceneUpdated(sceneId, lines);
    } else if (this.hostConnection) {
      this.hostConnection.send({ type: "ADMIN_UPDATE_LINES", sceneId, lines });
    }
  }

  // Karakter & Rol Değişikliklerini Yayınla
  broadcastUpdatedCharacters(sceneId, characters) {
    if (this.isHost) {
      this._broadcast({ type: "SCENE_CHARACTERS_UPDATED", sceneId, characters });
      this.onCharactersUpdated(sceneId, characters);
    } else if (this.hostConnection) {
      this.hostConnection.send({ type: "ADMIN_UPDATE_CHARACTERS", sceneId, characters });
    }
  }

  // Host: Tüm odadaki kullanıcılara durumu yay
  _broadcastState() {
    if (!this.isHost) return;
    this._broadcast({ type: "STATE_UPDATE", state: this.state });
    this.onStateChange(this.state);
  }

  _broadcast(data) {
    if (!this.isHost) return;
    for (const [_, conn] of this.connections) {
      if (conn.open) {
        try {
          conn.send(data);
        } catch (err) {
          console.error("P2P broadcast gönderim hatası:", err);
        }
      }
    }
  }
}
