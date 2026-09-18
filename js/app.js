import { SCENES } from "./scenes.js";
import { P2PNetwork } from "./p2p.js";
import { StudioEngine } from "./studio.js";
import { VirtualMixer } from "./mixer.js";
import { auth } from "./auth.js";

class DublajApp {
  constructor() {
    this.network = null;
    this.studio = null;
    this.mixer = null;
    this.auth = auth;
    this.selectedScene = SCENES[0];
    this.isSoloMode = false;
    this.searchQuery = "";
    this._editorPreviewTargetEnd = null;
    this._isUserScrubbingEditorVideo = false;

    this.selectedMicDeviceId = null;
    this._lobbyVuInterval = null;

    // Admin Yetkisi (Miraç) - İlk girişte kimse admin başlamaz!
    // Yalnızca şifre girilip doğrulandıktan sonra oturum bazında aktif olur.
    this.isAdmin = false;
    if (typeof localStorage !== "undefined") {
      try { localStorage.removeItem("miracos_dublaj_admin"); } catch (e) {}
    }

    this.dom = {
      screens: {
        login: document.getElementById("screen-login"),
        home: document.getElementById("screen-home"),
        lobby: document.getElementById("screen-lobby"),
        studio: document.getElementById("screen-studio"),
        premiere: document.getElementById("screen-premiere")
      },
      inputs: {
        playerName: document.getElementById("input-player-name"),
        roomCode: document.getElementById("input-room-code")
      },
      header: {
        logo: document.getElementById("app-header-logo"),
        themeSelect: document.getElementById("select-theme"),
        adminBadge: document.getElementById("btn-admin-badge"),
        openTranscriptEditorBtn: document.getElementById("btn-open-transcript-editor"),
        adminLogoutBtn: document.getElementById("btn-admin-logout")
      },
      headerUser: {
        section: document.getElementById("header-user-section"),
        badge: document.getElementById("header-user-badge"),
        icon: document.getElementById("header-user-icon"),
        name: document.getElementById("header-user-name"),
        adminPanelBtn: document.getElementById("btn-header-admin-panel"),
        logoutBtn: document.getElementById("btn-user-logout")
      },
      login: {
        screen: document.getElementById("screen-login"),
        form: document.getElementById("form-login"),
        usernameInput: document.getElementById("input-login-username"),
        passwordInput: document.getElementById("input-login-password"),
        submitBtn: document.getElementById("btn-login-submit"),
        submitBtnText: document.getElementById("btn-login-text"),
        errorBox: document.getElementById("login-error-msg"),
        errorText: document.getElementById("login-error-text")
      },
      homeWelcome: {
        name: document.getElementById("home-welcome-name"),
        badge: document.getElementById("home-welcome-badge"),
        badgeIcon: document.getElementById("home-welcome-badge-icon"),
        badgeText: document.getElementById("home-welcome-badge-text"),
        adminCard: document.getElementById("home-admin-card"),
        adminPanelBtn: document.getElementById("btn-home-admin-panel"),
        openJoinModalBtn: document.getElementById("btn-open-join-modal")
      },
      joinModal: {
        modal: document.getElementById("modal-join-room"),
        input: document.getElementById("modal-input-room-code"),
        closeBtn: document.getElementById("btn-close-join-modal"),
        cancelBtn: document.getElementById("btn-cancel-join-modal"),
        submitBtn: document.getElementById("btn-submit-join-modal")
      },
      adminPanel: {
        modal: document.getElementById("modal-admin-panel"),
        closeBtn: document.getElementById("btn-close-admin-panel"),
        closeBottomBtn: document.getElementById("btn-admin-panel-close-bottom"),
        tabUsersBtn: document.getElementById("tab-btn-admin-users"),
        tabScenesBtn: document.getElementById("tab-btn-admin-scenes"),
        contentUsers: document.getElementById("tab-content-admin-users"),
        contentScenes: document.getElementById("tab-content-admin-scenes"),
        newUsernameInput: document.getElementById("admin-input-new-username"),
        newPasswordInput: document.getElementById("admin-input-new-password"),
        newRoleSelect: document.getElementById("admin-select-new-role"),
        createUserBtn: document.getElementById("btn-admin-submit-create-user"),
        userFeedback: document.getElementById("admin-user-feedback"),
        userCountBadge: document.getElementById("admin-user-count-badge"),
        refreshUsersBtn: document.getElementById("btn-admin-refresh-users"),
        usersListContainer: document.getElementById("admin-users-list-container"),
        sceneSelectDropdown: document.getElementById("admin-scene-select-dropdown"),
        launchEditorBtn: document.getElementById("btn-admin-launch-editor"),
        saveDiskBtn: document.getElementById("btn-admin-save-current-scene-disk"),
        openUploadBtn: document.getElementById("btn-admin-open-upload-modal")
      },
      lobby: {
        codeDisplay: document.getElementById("lobby-code-display"),
        playerList: document.getElementById("lobby-player-list"),
        sceneGrid: document.getElementById("lobby-scene-grid"),
        roleContainer: document.getElementById("lobby-role-container"),
        startBtn: document.getElementById("lobby-start-btn"),
        sceneTitle: document.getElementById("lobby-selected-scene-title"),
        categoryTabs: document.getElementById("category-tabs"),
        syncBar: document.getElementById("lobby-sync-bar"),
        syncTitle: document.getElementById("lobby-sync-title"),
        syncProgress: document.getElementById("lobby-sync-progress"),
        openUploadBtn: document.getElementById("btn-open-upload-modal"),
        micSelect: document.getElementById("lobby-mic-device-select"),
        micTestBtn: document.getElementById("btn-lobby-test-mic"),
        micTestBtnText: document.getElementById("lobby-test-mic-text"),
        micVuBar: document.getElementById("lobby-mic-vu-bar"),
        micStatusBadge: document.getElementById("lobby-mic-status-badge"),
        micPct: document.getElementById("lobby-mic-pct")
      },
      studio: {
        container: document.getElementById("studio-video-container"),
        video: document.getElementById("studio-video"),
        transcriptBar: document.getElementById("video-transcript-bar"),
        transcriptSpeaker: document.getElementById("transcript-speaker"),
        transcriptText: document.getElementById("transcript-text"),
        transcriptTiming: document.getElementById("transcript-timing"),
        transcriptInstruction: document.getElementById("transcript-instruction"),
        karaokeProgressBar: document.getElementById("karaoke-progress-bar"),
        trafficLightBadge: document.getElementById("transcript-traffic-light"),
        roleTurnBanner: document.getElementById("role-turn-banner"),
        vuMeter: document.getElementById("studio-vu-bar"),
        waveformCanvas: document.getElementById("studio-waveform-canvas"),
        signalDisplay: document.getElementById("studio-db-display"),
        micStatusTag: document.getElementById("studio-mic-status-tag"),
        timer: document.getElementById("studio-timer"),
        roleBadge: document.getElementById("studio-role-badge"),
        phaseBadge: document.getElementById("studio-phase-badge"),
        actionButtons: document.getElementById("studio-action-buttons"),
        skipPreviewBtn: document.getElementById("btn-skip-preview"),
        replayPreviewBtn: document.getElementById("btn-replay-preview"),
        rehearseRoleBtn: document.getElementById("btn-rehearse-role"),
        startDubbingBtn: document.getElementById("btn-start-dubbing"),
        premiereReadyBox: document.getElementById("studio-premiere-ready-box"),
        reRecordBtn: document.getElementById("btn-re-record"),
        recordingsStatusText: document.getElementById("studio-recordings-status-text"),
        hostLaunchPremiereBtn: document.getElementById("btn-host-launch-premiere"),
        clientWaitingMsg: document.getElementById("studio-client-waiting-msg"),
        videoVolume: document.getElementById("studio-video-volume"),
        videoVolumeVal: document.getElementById("studio-video-volume-val"),
        micVolume: document.getElementById("studio-mic-volume"),
        micVolumeVal: document.getElementById("studio-mic-volume-val")
      },
      premiere: {
        video: document.getElementById("premiere-video"),
        transcriptBar: document.getElementById("premiere-transcript-bar"),
        transcriptSpeaker: document.getElementById("premiere-speaker"),
        transcriptText: document.getElementById("premiere-text"),
        timer: document.getElementById("premiere-timer"),
        currentTimeEl: document.getElementById("premiere-current-time"),
        totalTimeEl: document.getElementById("premiere-total-time"),
        seekSlider: document.getElementById("premiere-seek-slider"),
        playPauseBtn: document.getElementById("premiere-play-pause-btn"),
        playPauseIcon: document.getElementById("premiere-play-pause-icon"),
        playPauseText: document.getElementById("premiere-play-pause-text"),
        replayBtn: document.getElementById("premiere-replay-btn"),
        downloadAudioBtn: document.getElementById("premiere-download-audio-btn"),
        downloadVideoBtn: document.getElementById("premiere-download-video-btn"),
        newLobbyBtn: document.getElementById("premiere-new-lobby-btn"),
        videoVolume: document.getElementById("premiere-video-volume"),
        videoVolumeVal: document.getElementById("premiere-video-volume-val"),
        videoMuteBtn: document.getElementById("premiere-video-mute-btn"),
        characterVolumes: document.getElementById("premiere-character-volumes")
      },
      modals: {
        adminLogin: document.getElementById("modal-admin-login"),
        adminPassInput: document.getElementById("admin-password-input"),
        adminSubmitBtn: document.getElementById("btn-admin-submit"),
        adminCancelBtn: document.getElementById("btn-admin-cancel"),

        adminEditor: document.getElementById("modal-admin-editor"),
        editorTitle: document.getElementById("editor-scene-title"),
        tabLinesBtn: document.getElementById("tab-btn-lines"),
        tabCharactersBtn: document.getElementById("tab-btn-characters"),
        tabLinesContent: document.getElementById("tab-content-lines"),
        tabCharactersContent: document.getElementById("tab-content-characters"),
        editorLinesContainer: document.getElementById("editor-lines-container"),
        editorCharactersContainer: document.getElementById("editor-characters-container"),
        editorSortTimeBtn: document.getElementById("btn-editor-sort-time"),
        editorPreviewToggleBtn: document.getElementById("btn-editor-preview-toggle"),
        editorPreviewToggleText: document.getElementById("editor-preview-toggle-text"),
        editorVideoPreviewBox: document.getElementById("editor-video-preview-box"),
        editorPreviewVideo: document.getElementById("editor-preview-video"),
        editorLiveTimeDisplay: document.getElementById("editor-live-time-display"),
        editorTotalTimeDisplay: document.getElementById("editor-total-time-display"),
        editorVideoSlider: document.getElementById("editor-video-slider"),
        editorPlayPauseBtn: document.getElementById("btn-editor-play-pause"),
        editorPlayIcon: document.getElementById("editor-play-icon"),
        editorPlayText: document.getElementById("editor-play-text"),
        editorStepBackBtn: document.getElementById("btn-editor-step-back"),
        editorStepFwdBtn: document.getElementById("btn-editor-step-fwd"),
        editorLineCountBadge: document.getElementById("editor-line-count-badge"),
        editorAddLineBtn: document.getElementById("btn-editor-add-line"),
        editorAddMusicBtn: document.getElementById("btn-editor-add-music"),
        editorAddCharacterBtn: document.getElementById("btn-editor-add-character"),
        editorSavePermanentBtn: document.getElementById("btn-editor-save-permanent"),
        editorSaveBtn: document.getElementById("btn-editor-save"),
        editorCancelBtn: document.getElementById("btn-editor-cancel"),
        editorCloseBtn: document.getElementById("btn-close-transcript-editor"),

        upload: document.getElementById("modal-upload-video"),
        uploadFileInput: document.getElementById("custom-video-file-input"),
        uploadPreviewWrapper: document.getElementById("custom-video-preview-wrapper"),
        uploadPreviewVideo: document.getElementById("custom-video-preview"),
        uploadTitle: document.getElementById("custom-video-title"),
        uploadCategory: document.getElementById("custom-video-category"),
        uploadSubmitBtn: document.getElementById("btn-upload-submit"),
        uploadCancelBtn: document.getElementById("btn-upload-cancel"),
        uploadCloseBtn: document.getElementById("btn-close-upload-modal")
      }
    };
  }

  async init() {
    this._initTheme();
    this._initEngines();
    this._initLobbyMicrophone();
    this._bindEvents();
    this._bindAuthEvents();
    this._checkAdminState();
    this._renderCategories();
    this._renderHomeFeatured();
    this._renderScenes();
    this._checkAutoJoinRoom();

    // Oturum Kontrolü (Token varsa doğrula, yoksa ekranı kilitleyip login göster)
    await this._checkInitialAuth();

    // URL'de ?admin varsa doğrudan yetki verme, şifre doğrulama modalını aç!
    if (typeof window !== "undefined" && new URLSearchParams(window.location.search).has("admin")) {
      this._openAdminLoginModal();
      try {
        const cleanUrl = window.location.pathname;
        window.history.replaceState({}, document.title, cleanUrl);
      } catch (e) {}
    }
  }

  _initTheme() {
    if (typeof window === "undefined") return;
    try {
      const saved = localStorage.getItem("miracos_theme") || "cinema";
      this._setTheme(saved, false);
    } catch (e) {
      this._setTheme("cinema", false);
    }
  }

  _setTheme(themeName, showToast = true) {
    const validThemes = ["cinema", "studio", "cyber"];
    const theme = validThemes.includes(themeName) ? themeName : "cinema";
    if (typeof document !== "undefined") {
      document.documentElement.setAttribute("data-theme", theme);
      if (this.dom.header && this.dom.header.themeSelect) {
        this.dom.header.themeSelect.value = theme;
      }
    }
    try {
      localStorage.setItem("miracos_theme", theme);
    } catch (e) {}

    if (showToast) {
      const labels = {
        cinema: "🎬 Sinema & Netflix (Kırmızı/Siyah)",
        studio: "🎙️ Ses Stüdyosu (Amber/Antrasit)",
        cyber: "👾 Cyber Gece (Neon/OLED Siyah)"
      };
      this._showNotification(`Tema güncellendi: ${labels[theme]}`, "info");
    }
  }

  _checkAutoJoinRoom() {
    if (typeof window === "undefined") return;
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const room = urlParams.get("room") || urlParams.get("oda");
      if (room && this.dom.inputs.roomCode) {
        const cleanRoom = room.trim().toUpperCase();
        this.dom.inputs.roomCode.value = cleanRoom;
        this.dom.inputs.roomCode.classList.add("border-indigo-400", "bg-indigo-950/40");
        this._showNotification(`🔗 ${cleanRoom} odasına davet edildin! İsim yazıp tek tıkla katılabilirsin.`, "info");
      }
    } catch (e) {}
  }

  _initEngines() {
    this.studio = new StudioEngine({
      videoElement: this.dom.studio.video,
      transcriptBar: this.dom.studio.transcriptBar,
      transcriptSpeaker: this.dom.studio.transcriptSpeaker,
      transcriptText: this.dom.studio.transcriptText,
      transcriptTiming: this.dom.studio.transcriptTiming,
      transcriptInstruction: this.dom.studio.transcriptInstruction,
      karaokeProgressBar: this.dom.studio.karaokeProgressBar,
      trafficLightBadge: this.dom.studio.trafficLightBadge,
      roleTurnBanner: this.dom.studio.roleTurnBanner,
      vuMeterElement: this.dom.studio.vuMeter,
      waveformCanvas: this.dom.studio.waveformCanvas,
      signalDisplay: this.dom.studio.signalDisplay,
      micStatusTag: this.dom.studio.micStatusTag,
      onTimeUpdate: (current, total) => {
        this.dom.studio.timer.innerText = `${current.toFixed(1)}s / ${total.toFixed(0)}s`;
      },
      onComplete: (data) => {
        console.log("Kayıt tamamlandı:", data);
        if (this.isSoloMode) {
          const audioTracks = {};
          if (data.characterId) {
            audioTracks[data.characterId] = {
              characterId: data.characterId,
              audioData: data.audioBase64,
              playerName: this.network ? this.network.user.name : "Sen"
            };
          }
          this._startPremiereScreen(audioTracks);
        } else {
          if (data.characterId && data.characterId !== "spectator") {
            this.network.sendVoiceRecording(data.characterId, data.audioBase64);
          }
          this.dom.studio.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-3 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-indigo-900/90 text-white border border-indigo-500 animate-pulse";
          this.dom.studio.roleTurnBanner.innerHTML = (data.characterId && data.characterId !== "spectator")
            ? "⏳ Sesin Kaydedildi! Diğer oyuncular bekleniyor..."
            : "🍿 Seyirci Yayını Tamam! Oyuncuların dublajı bekleniyor...";

          // Bekleme kutusunu göster ve durumu güncelle
          this.dom.studio.actionButtons?.classList.add("hidden");
          this.dom.studio.premiereReadyBox?.classList.remove("hidden");
          this._updateStudioPremiereState(this.network.state);
        }
      },
      onPhaseChange: (phase) => {
        this._updatePhaseUI(phase);
      }
    });

    this.mixer = new VirtualMixer({
      videoElement: this.dom.premiere.video,
      transcriptBar: this.dom.premiere.transcriptBar,
      transcriptSpeaker: this.dom.premiere.transcriptSpeaker,
      transcriptText: this.dom.premiere.transcriptText,
      onTimeUpdate: (current, total) => {
        if (this.dom.premiere.timer) {
          this.dom.premiere.timer.innerText = `${current.toFixed(1)}s / ${total.toFixed(0)}s`;
        }
        if (this.dom.premiere.currentTimeEl) {
          this.dom.premiere.currentTimeEl.innerText = `${current.toFixed(1)}s`;
        }
        if (this.dom.premiere.totalTimeEl) {
          this.dom.premiere.totalTimeEl.innerText = `${total.toFixed(1)}s`;
        }
        if (this.dom.premiere.seekSlider) {
          this.dom.premiere.seekSlider.max = total || 15;
          this.dom.premiere.seekSlider.value = current;
        }
      },
      onEnd: () => {
        console.log("Prömiyer gösterimi bitti!");
        if (this.dom.premiere.playPauseIcon) this.dom.premiere.playPauseIcon.innerText = "▶️";
        if (this.dom.premiere.playPauseText) this.dom.premiere.playPauseText.innerText = "Oynat";
      }
    });
  }

  _bindEvents() {
    // 0. TEMA DEĞİŞTİRİCİ (3 SİYAH AĞIRLIKLI PALET)
    if (this.dom.header && this.dom.header.themeSelect) {
      this.dom.header.themeSelect.addEventListener("change", (e) => {
        this._setTheme(e.target.value, true);
      });
    }

    // 1. ODA OLUŞTUR (HOST)
    document.getElementById("btn-create-room").addEventListener("click", async () => {
      const name = this.dom.inputs.playerName.value.trim() || "Oyuncu " + Math.floor(Math.random() * 900);
      this.isSoloMode = false;
      this._setupNetwork(name);
      const roomCode = await this.network.createRoom();
      this.dom.lobby.codeDisplay.innerText = roomCode;
      this._switchScreen("lobby");
    });

    // 2. ODAYA KATIL (CLIENT)
    document.getElementById("btn-join-room").addEventListener("click", async () => {
      const name = this.dom.inputs.playerName.value.trim() || "Oyuncu " + Math.floor(Math.random() * 900);
      const code = this.dom.inputs.roomCode.value.trim().toUpperCase();
      if (!code) {
        alert("Lütfen 6 haneli oda kodunu girin!");
        return;
      }
      this.isSoloMode = false;
      this._setupNetwork(name);
      try {
        await this.network.joinRoom(code);
        this.dom.lobby.codeDisplay.innerText = code;
        this._switchScreen("lobby");
      } catch (err) {
        alert("Odaya bağlanılamadı. Kodu kontrol edin!");
      }
    });

    // 3. TEK KİŞİLİK ANTRENMAN (SOLO MOD)
    document.getElementById("btn-solo-mode").addEventListener("click", async () => {
      this.isSoloMode = true;
      const name = this.dom.inputs.playerName.value.trim() || "Sen";
      this._setupNetwork(name);
      this.dom.lobby.codeDisplay.innerText = "SOLO";
      this.network.state.players = [{
        id: "solo-user",
        name: name,
        avatar: "🎙️",
        isHost: true,
        roleId: null,
        isReady: true
      }];
      this._switchScreen("lobby");
      this._updateLobbyUI(this.network.state);
    });

    // 3.5. LOBİ SAHNE ARAMA ÇUBUĞU
    const sceneSearchInput = document.getElementById("lobby-scene-search");
    if (sceneSearchInput) {
      sceneSearchInput.addEventListener("input", (e) => {
        this.searchQuery = e.target.value;
        this._renderScenes();
      });
    }

    // 4. LOBİ BAŞLAT BUTONU
    this.dom.lobby.startBtn.addEventListener("click", async () => {
      // En az bir gerçek konuşmacı karakter seçilmiş mi kontrol et
      const hasAnyActor = this.isSoloMode 
        ? (this.selectedRole && this.selectedRole !== "spectator")
        : (this.network && this.network.state && this.network.state.players.some(p => p.roleId && p.roleId !== "spectator"));

      if (!hasAnyActor) {
        alert("Dublajı başlatabilmek için odadaki en az 1 oyuncunun konuşmacı rolü seçmesi gerekir!");
        return;
      }

      if (!this.selectedRole) {
        alert("Lütfen bir karakter seçin veya 'Seyirci / İzleyici' koltuğuna geçin!");
        return;
      }

      if (this.selectedRole !== "spectator") {
        try {
          await this.studio.initAudio(this.selectedMicDeviceId);
        } catch (e) {
          alert("Dublaj yapabilmek için mikrofon erişimine izin vermelisiniz!");
          return;
        }
      }

      if (this.isSoloMode) {
        this._startStudioScreen(this.selectedScene.id, this.selectedRole);
      } else {
        this.network.startDubbingCountdown();
      }
    });

    // 5. ODA KODU & DAVET LİNKİ KOPYALA
    document.getElementById("btn-copy-code")?.addEventListener("click", () => {
      const code = this.dom.lobby.codeDisplay.innerText.trim();
      const inviteUrl = `${window.location.origin}${window.location.pathname}?room=${encodeURIComponent(code)}`;
      navigator.clipboard.writeText(inviteUrl);
      this._showNotification(`🔗 Davet Linki Kopyalandı!\nArkadaşına atarak tek tıkla odaya alabilirsin.`, "success");
    });

    // 6. PRÖMİYER YENİDEN OYNAT VE GELİŞMİŞ SES/TIMELINE KONTROLLERİ
    this.dom.premiere.playPauseBtn?.addEventListener("click", () => {
      const isPlaying = this.mixer.togglePlayPause();
      if (this.dom.premiere.playPauseIcon) this.dom.premiere.playPauseIcon.innerText = isPlaying ? "⏸️" : "▶️";
      if (this.dom.premiere.playPauseText) this.dom.premiere.playPauseText.innerText = isPlaying ? "Durdur" : "Oynat";
    });

    this.dom.premiere.replayBtn?.addEventListener("click", () => {
      this.mixer.play();
      if (this.dom.premiere.playPauseIcon) this.dom.premiere.playPauseIcon.innerText = "⏸️";
      if (this.dom.premiere.playPauseText) this.dom.premiere.playPauseText.innerText = "Durdur";
    });

    this.dom.premiere.seekSlider?.addEventListener("input", (e) => {
      const targetTime = parseFloat(e.target.value);
      this.mixer.seek(targetTime);
    });

    this.dom.premiere.downloadAudioBtn?.addEventListener("click", () => {
      this.mixer.exportMixedAudio();
    });

    this.dom.premiere.downloadVideoBtn?.addEventListener("click", async () => {
      const btn = this.dom.premiere.downloadVideoBtn;
      if (!btn) return;
      const originalHTML = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = `<span>⏺️</span><span>Video Kaydediliyor (%0)...</span>`;
      try {
        await this.mixer.exportMixedVideo((pct) => {
          btn.innerHTML = `<span>⏺️</span><span>Video Kaydediliyor (%${pct})...</span>`;
        });
      } catch (err) {
        console.error("Video export hatası:", err);
      } finally {
        btn.disabled = false;
        btn.innerHTML = originalHTML;
      }
    });

    this.dom.premiere.videoMuteBtn?.addEventListener("click", (e) => {
      const isMuted = this.mixer.toggleVideoMute();
      e.target.innerText = isMuted ? "🔇" : "🔊";
      e.target.classList.toggle("bg-red-900/60", isMuted);
    });

    this.dom.premiere.videoVolume?.addEventListener("input", (e) => {
      const val = parseInt(e.target.value, 10);
      if (this.dom.premiere.videoVolumeVal) this.dom.premiere.videoVolumeVal.innerText = `%${val}`;
      this.mixer.setVideoVolume(val);
    });

    // 7. LOBİYE DÖN
    this.dom.premiere.newLobbyBtn.addEventListener("click", () => {
      this.mixer.stop();
      this._switchScreen("lobby");
    });

    // 8. EMOJİ REAKSİYONLARI
    document.querySelectorAll(".reaction-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        this._spawnFloatingEmoji(e.target.innerText);
      });
    });

    // 8.1 STÜDYO BİREYSEL SES KONTROLLERİ
    this.dom.studio.videoVolume?.addEventListener("input", (e) => {
      const val = parseInt(e.target.value, 10);
      if (this.dom.studio.videoVolumeVal) this.dom.studio.videoVolumeVal.innerText = `%${val}`;
      this.studio.setVideoVolume(val);
    });

    this.dom.studio.micVolume?.addEventListener("input", (e) => {
      const val = parseInt(e.target.value, 10);
      if (this.dom.studio.micVolumeVal) this.dom.studio.micVolumeVal.innerText = `%${val}`;
      this.studio.setMicVolume(val);
    });

    // 9. STÜDYO BUTONLARI
    // "İzlemeyi Geç (Doğrudan Hazır Ol)"
    document.getElementById("btn-skip-preview")?.addEventListener("click", () => {
      this.studio.skipPreview();
    });

    // "Tekrar İzle (Tümü)"
    document.getElementById("btn-replay-preview")?.addEventListener("click", () => {
      this.dom.studio.actionButtons?.classList.add("hidden");
      this.studio.startPreview();
    });

    // "Rolümü Prova Et (Sadece Kendi Repliklerini Dinle)"
    document.getElementById("btn-rehearse-role")?.addEventListener("click", () => {
      this.dom.studio.actionButtons?.classList.add("hidden");
      this.studio.playRoleRehearsal();
    });

    // "Hazırım, Dublaja Başla!"
    document.getElementById("btn-start-dubbing")?.addEventListener("click", async () => {
      if (!this.studio.microphoneStream) {
        try {
          await this.studio.initAudio(this.selectedMicDeviceId);
        } catch (e) {
          alert("Dublaj yapabilmek için mikrofon erişimine izin vermelisiniz!");
          return;
        }
      }
      if (this.studio.audioContext && this.studio.audioContext.state === "suspended") {
        await this.studio.audioContext.resume().catch(() => {});
      }

      this.dom.studio.actionButtons?.classList.add("hidden");
      this._showCountdownOverlay(() => {
        this.studio.startRecording();
      }, "Şimdi Sen Konuşuyorsun! Dublaj Başlıyor!");
    });

    // "Dublajı Beğenmedim, Tekrar Kaydet"
    document.getElementById("btn-re-record")?.addEventListener("click", () => {
      this._handleReRecord();
    });

    // 10. HOST / ADMİN: FİLMİ BAŞLAT (PRÖMİYER)
    this.dom.studio.hostLaunchPremiereBtn?.addEventListener("click", () => {
      if (this.network) {
        this.network.launchPremiere();
      }
    });

    // 11. GİZLİ ADMİN GİRİŞİ (Logo'ya 3 tık)
    let logoClicks = 0;
    let logoTimer = null;
    this.dom.header.logo?.addEventListener("click", () => {
      logoClicks++;
      clearTimeout(logoTimer);
      logoTimer = setTimeout(() => { logoClicks = 0; }, 1200);
      if (logoClicks >= 3) {
        logoClicks = 0;
        this._openAdminLoginModal();
      }
    });

    // Admin Şifre Onayla / İptal
    this.dom.modals.adminSubmitBtn?.addEventListener("click", () => {
      this._verifyAdminPassword();
    });
    this.dom.modals.adminPassInput?.addEventListener("keypress", (e) => {
      if (e.key === "Enter") this._verifyAdminPassword();
    });
    this.dom.modals.adminCancelBtn?.addEventListener("click", () => {
      this.dom.modals.adminLogin?.classList.add("hidden");
    });

    // Admin Rozetine Tıklayınca Bilgi
    this.dom.header.adminBadge?.addEventListener("click", () => {
      alert("👑 Admin Yetkisi Aktif!\nSahne transkriptlerini düzenleyebilir ve odayı yönetebilirsiniz.");
    });

    // Admin Oturumunu Kapat / Kilitle
    this.dom.header.adminLogoutBtn?.addEventListener("click", () => {
      this.isAdmin = false;
      localStorage.removeItem("miracos_dublaj_admin");
      if (this.network) this.network.isAdmin = false;
      this._checkAdminState();
      alert("🔒 Admin yetkisi kapatıldı. Standart oyuncu moduna dönüldü.");
    });

    // 12. GELİŞMİŞ TRANSKRİPT & KARAKTER EDİTÖRÜ
    this.dom.header.openTranscriptEditorBtn?.addEventListener("click", () => {
      this._openTranscriptEditor();
    });
    this.dom.modals.editorCloseBtn?.addEventListener("click", () => {
      this._closeTranscriptEditor();
    });
    this.dom.modals.editorCancelBtn?.addEventListener("click", () => {
      this._closeTranscriptEditor();
    });
    this.dom.modals.tabLinesBtn?.addEventListener("click", () => {
      this._switchEditorTab("lines");
    });
    this.dom.modals.tabCharactersBtn?.addEventListener("click", () => {
      this._switchEditorTab("characters");
    });
    this.dom.modals.editorSortTimeBtn?.addEventListener("click", () => {
      this._sortTranscriptLinesByTime();
    });
    this.dom.modals.editorPreviewToggleBtn?.addEventListener("click", () => {
      this._toggleEditorVideoPreview();
    });

    // Editör Canlı Video Oynatıcı Kontrolleri
    this.dom.modals.editorPlayPauseBtn?.addEventListener("click", () => {
      const vid = this.dom.modals.editorPreviewVideo;
      if (!vid) return;
      if (vid.paused) {
        this._editorPreviewTargetEnd = null;
        vid.play().catch(() => {});
      } else {
        vid.pause();
      }
    });

    this.dom.modals.editorPreviewVideo?.addEventListener("click", () => {
      const vid = this.dom.modals.editorPreviewVideo;
      if (!vid) return;
      if (vid.paused) {
        this._editorPreviewTargetEnd = null;
        vid.play().catch(() => {});
      } else {
        vid.pause();
      }
    });

    this.dom.modals.editorVideoSlider?.addEventListener("input", (e) => {
      this._isUserScrubbingEditorVideo = true;
      const val = parseFloat(e.target.value);
      if (this.dom.modals.editorPreviewVideo) {
        this.dom.modals.editorPreviewVideo.currentTime = val;
      }
      if (this.dom.modals.editorLiveTimeDisplay) {
        this.dom.modals.editorLiveTimeDisplay.innerText = `${val.toFixed(2)}s`;
      }
    });

    this.dom.modals.editorVideoSlider?.addEventListener("change", () => {
      this._isUserScrubbingEditorVideo = false;
    });

    this.dom.modals.editorStepBackBtn?.addEventListener("click", () => {
      const vid = this.dom.modals.editorPreviewVideo;
      if (!vid) return;
      vid.currentTime = Math.max(0, vid.currentTime - 0.5);
    });

    this.dom.modals.editorStepFwdBtn?.addEventListener("click", () => {
      const vid = this.dom.modals.editorPreviewVideo;
      if (!vid) return;
      const maxDur = vid.duration || 999;
      vid.currentTime = Math.min(maxDur, vid.currentTime + 0.5);
    });

    // Hız butonları (0.5x, 0.75x, 1.0x)
    document.querySelectorAll(".editor-speed-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const speed = parseFloat(btn.dataset.speed);
        if (this.dom.modals.editorPreviewVideo) {
          this.dom.modals.editorPreviewVideo.playbackRate = speed;
        }
        document.querySelectorAll(".editor-speed-btn").forEach(b => {
          b.classList.remove("bg-amber-500/20", "text-amber-300");
          b.classList.add("text-slate-400");
        });
        btn.classList.remove("text-slate-400");
        btn.classList.add("bg-amber-500/20", "text-amber-300");
      });
    });

    // Spacebar tuşu ile videoyu durdurup oynatma (kullanıcı girdi alanında değilse)
    window.addEventListener("keydown", (e) => {
      if (e.code === "Space" && !this.dom.modals.adminEditor?.classList.contains("hidden")) {
        const activeTag = document.activeElement?.tagName?.toLowerCase();
        if (activeTag !== "input" && activeTag !== "textarea" && activeTag !== "select") {
          e.preventDefault();
          this.dom.modals.editorPlayPauseBtn?.click();
        }
      }
    });

    this.dom.modals.editorAddLineBtn?.addEventListener("click", () => {
      this._addTranscriptLine();
    });
    this.dom.modals.editorAddMusicBtn?.addEventListener("click", () => {
      this._addMusicLockLine();
    });
    this.dom.modals.editorAddCharacterBtn?.addEventListener("click", () => {
      this._addEditorCharacter();
    });
    this.dom.modals.editorSavePermanentBtn?.addEventListener("click", () => {
      this._savePermanentSceneToDisk();
    });
    this.dom.modals.editorSaveBtn?.addEventListener("click", () => {
      this._saveTranscriptEditor();
    });

    // 13. ÖZEL VİDEO YÜKLEME
    this.dom.lobby.openUploadBtn?.addEventListener("click", () => {
      this._openUploadModal();
    });
    this.dom.modals.uploadCloseBtn?.addEventListener("click", () => {
      this.dom.modals.upload?.classList.add("hidden");
    });
    this.dom.modals.uploadCancelBtn?.addEventListener("click", () => {
      this.dom.modals.upload?.classList.add("hidden");
    });
    this.dom.modals.uploadFileInput?.addEventListener("change", (e) => {
      this._handleCustomVideoSelection(e.target.files[0]);
    });
    this.dom.modals.uploadSubmitBtn?.addEventListener("click", () => {
      this._submitCustomVideo();
    });
  }

  _setupNetwork(name) {
    this.network = new P2PNetwork({
      name,
      isAdmin: this.isAdmin,
      onStateChange: (state) => {
        this._updateLobbyUI(state);
        this._updateStudioPremiereState(state);
      },
      onRecordingsReady: (state) => {
        this._updateStudioPremiereState(state);
      },
      onCustomSceneReceived: (scene) => {
        this._handleNewCustomScene(scene);
      },
      onTransferProgress: ({ sceneTitle, percent, isReceiving }) => {
        this._showSyncProgress(sceneTitle, percent >= 100, percent, isReceiving);
      },
      onSceneUpdated: (sceneId, lines) => {
        this._handleSceneLinesUpdated(sceneId, lines);
      },
      onCharactersUpdated: (sceneId, characters) => {
        this._handleSceneCharactersUpdated(sceneId, characters);
      },
      onStartRecording: (sceneId) => {
        const charId = this.selectedRole;
        this._startStudioScreen(sceneId, charId);
      },
      onStartPremiere: (audioTracks) => {
        this._startPremiereScreen(audioTracks);
      },
      onError: (err) => console.error("Ağ Hatası:", err)
    });
  }

  _switchScreen(screenName) {
    Object.keys(this.dom.screens).forEach(name => {
      if (name === screenName) {
        this.dom.screens[name].classList.remove("hidden");
      } else {
        this.dom.screens[name].classList.add("hidden");
      }
    });

    if (screenName === "lobby") {
      this._populateAudioDevices();
      if (this.studio && this.studio.microphoneStream && this.studio.microphoneStream.active) {
        this._startLobbyVUMonitor();
      }
    } else {
      if (this._lobbyVuInterval) {
        clearInterval(this._lobbyVuInterval);
        this._lobbyVuInterval = null;
      }
    }
  }

  _initLobbyMicrophone() {
    const testBtn = this.dom.lobby.micTestBtn;
    const deviceSelect = this.dom.lobby.micSelect;

    testBtn?.addEventListener("click", async () => {
      await this._testLobbyMicAction();
    });

    deviceSelect?.addEventListener("change", async (e) => {
      this.selectedMicDeviceId = e.target.value || null;
      try {
        await this.studio.initAudio(this.selectedMicDeviceId);
        this._showNotification("🎙️ Mikrofon girişi değiştirildi!", "info");
      } catch (err) {
        console.warn("Cihaz değiştirme hatası:", err);
      }
    });
  }

  async _testLobbyMicAction() {
    const badge = this.dom.lobby.micStatusBadge;
    const btnText = this.dom.lobby.micTestBtnText;

    if (btnText) btnText.innerText = "Mikrofon Başlatılıyor...";
    try {
      await this.studio.initAudio(this.selectedMicDeviceId);
      if (badge) {
        badge.innerText = "✅ AKTİF";
        badge.className = "px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
      }
      if (btnText) btnText.innerText = "✅ Mikrofon Bağlandı (Tekrar Test Et)";

      await this._populateAudioDevices();
      this._startLobbyVUMonitor();
      this._showNotification("🎙️ Mikrofon başarıyla bağlandı! Konuşarak yeşil sinyal barını görebilirsin.", "success");
    } catch (err) {
      if (badge) {
        badge.innerText = "❌ İZİN VERİLMEDİ";
        badge.className = "px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-red-500/20 text-red-400 border border-red-500/40";
      }
      if (btnText) btnText.innerText = "⚠️ İzin Ver & Yeniden Dene";
      alert("Lütfen tarayıcınızın adres çubuğundaki kilit simgesine tıklayarak mikrofon iznini 'İzin Ver' olarak ayarlayın.");
    }
  }

  async _populateAudioDevices() {
    if (typeof navigator === "undefined" || !navigator.mediaDevices || !navigator.mediaDevices.enumerateDevices) return;
    try {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const audioInputs = devices.filter(d => d.kind === "audioinput");
      const select = this.dom.lobby.micSelect;
      if (!select) return;

      const currentVal = this.selectedMicDeviceId || select.value;
      select.innerHTML = `<option value="">🎙️ Varsayılan Mikrofon</option>`;
      audioInputs.forEach((dev, idx) => {
        const opt = document.createElement("option");
        opt.value = dev.deviceId;
        opt.innerText = dev.label || `Mikrofon Girişi ${idx + 1}`;
        if (dev.deviceId === currentVal) opt.selected = true;
        select.appendChild(opt);
      });
    } catch (e) {
      console.warn("Ses aygıtları listelenemedi:", e);
    }
  }

  _startLobbyVUMonitor() {
    if (this._lobbyVuInterval) clearInterval(this._lobbyVuInterval);
    if (!this.studio || !this.studio.analyser) return;

    const analyser = this.studio.analyser;
    const bufLen = analyser.frequencyBinCount;
    const data = new Uint8Array(bufLen);

    this._lobbyVuInterval = setInterval(() => {
      if (this.dom.screens.lobby && this.dom.screens.lobby.classList.contains("hidden")) {
        clearInterval(this._lobbyVuInterval);
        this._lobbyVuInterval = null;
        return;
      }

      analyser.getByteFrequencyData(data);
      let sum = 0;
      let maxVal = 0;
      const count = Math.min(bufLen, 32);
      for (let i = 0; i < count; i++) {
        sum += data[i];
        if (data[i] > maxVal) maxVal = data[i];
      }
      const avg = sum / Math.max(1, count);
      const rawPct = Math.max((avg / 55) * 100, (maxVal / 150) * 100);
      const pct = Math.min(100, Math.round(rawPct));

      if (this.dom.lobby.micVuBar) {
        this.dom.lobby.micVuBar.style.width = pct + "%";
      }
      if (this.dom.lobby.micPct) {
        this.dom.lobby.micPct.innerText = `%${pct} SİNYAL`;
        this.dom.lobby.micPct.className = pct > 15 
          ? "font-mono font-bold text-emerald-400" 
          : "font-mono font-bold text-slate-400";
      }
    }, 60);
  }

  _renderCategories() {
    const totalCount = SCENES.length;
    const memeCount = SCENES.filter(s => s.category === "meme").length;
    const classicCount = SCENES.filter(s => s.category !== "meme").length;

    const categories = [
      { id: "all", name: `Tümü (${totalCount})` },
      { id: "meme", name: `🔥 Türk Memeleri (${memeCount})` },
      { id: "dizi-film", name: `🎬 Dizi & Film (${classicCount})` },
      { id: "ozel", name: "⭐ Özel Sahneler" }
    ];

    const currentCat = this.currentCategory || "all";

    this.dom.lobby.categoryTabs.innerHTML = categories.map((cat) => `
      <button class="cat-tab-btn px-3.5 py-1 rounded-full text-xs font-bold transition-all ${
        cat.id === currentCat ? 'bg-indigo-600 text-white shadow-md shadow-indigo-500/30' : 'bg-slate-800/90 text-slate-300 hover:bg-slate-700 hover:text-white'
      }" data-cat="${cat.id}">
        ${cat.name}
      </button>
    `).join("");

    this.dom.lobby.categoryTabs.querySelectorAll(".cat-tab-btn").forEach(btn => {
      btn.addEventListener("click", (e) => {
        this.dom.lobby.categoryTabs.querySelectorAll(".cat-tab-btn").forEach(b => {
          b.classList.remove("bg-indigo-600", "text-white", "shadow-md", "shadow-indigo-500/30");
          b.classList.add("bg-slate-800/90", "text-slate-300");
        });
        btn.classList.add("bg-indigo-600", "text-white", "shadow-md", "shadow-indigo-500/30");
        btn.classList.remove("bg-slate-800/90", "text-slate-300");
        this.currentCategory = btn.dataset.cat;
        this._renderScenes(this.currentCategory);
      });
    });
  }

  _renderHomeFeatured() {
    const container = document.getElementById("home-featured-scenes");
    if (!container) return;

    // Öne çıkan 6 popüler sahne
    const featuredIds = [
      "meme-kolpacino-saatli-bomba",
      "meme-sonuc-ne-soru-cevap",
      "meme-artist-ne-arar",
      "meme-cikar-telefonunu",
      "sifir-bir-cio",
      "kv-pala"
    ];

    let featuredScenes = featuredIds
      .map(id => SCENES.find(s => s.id === id))
      .filter(Boolean);

    if (featuredScenes.length < 6) {
      for (const s of SCENES) {
        if (!featuredScenes.some(fs => fs.id === s.id)) {
          featuredScenes.push(s);
          if (featuredScenes.length >= 6) break;
        }
      }
    }

    container.innerHTML = featuredScenes.map(scene => {
      const isSelected = scene.id === this.selectedScene.id;
      const thumb = scene.thumbnail || `assets/thumbnails/${scene.id}.jpg`;
      return `
        <div class="home-featured-card group relative p-2 rounded-2xl bg-slate-950/80 border ${
          isSelected ? 'border-indigo-500 ring-2 ring-indigo-500/40 bg-indigo-950/40' : 'border-slate-800/90 hover:border-indigo-500/60'
        } cursor-pointer transition-all duration-200 hover:-translate-y-1 hover:shadow-xl hover:shadow-indigo-500/10" data-id="${scene.id}">
          <div class="relative w-full aspect-video rounded-xl overflow-hidden bg-slate-900 mb-1.5 border border-slate-800/80">
            <img src="${thumb}" 
                 alt="${scene.title}" 
                 loading="lazy" 
                 class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                 onerror="this.onerror=null; this.src='data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'480\' height=\'270\' viewBox=\'0 0 480 270\'><rect width=\'480\' height=\'270\' fill=\'%230f172a\'/><text x=\'50%25\' y=\'50%25\' dominant-baseline=\'middle\' text-anchor=\'middle\' fill=\'%2364748b\' font-size=\'32\' font-family=\'sans-serif\'>🎬 DUBLAJ</text></svg>'"/>
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20 pointer-events-none"></div>
            
            <span class="absolute top-1 left-1 px-1.5 py-0.5 rounded bg-black/75 backdrop-blur-md text-amber-300 font-bold text-[9px] border border-amber-500/30">
              ${scene.category === 'meme' ? '🔥 Meme' : '🎬 Sahne'}
            </span>

            <span class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-black/80 text-white font-mono font-bold text-[10px]">
              ⏱️ ${scene.duration}s
            </span>

            ${isSelected ? `
              <div class="absolute inset-0 bg-indigo-950/40 border-2 border-indigo-400 rounded-xl flex items-center justify-center">
                <span class="px-2 py-0.5 rounded-full bg-indigo-600 text-white font-black text-[10px] shadow-lg flex items-center space-x-1">
                  <span>✅</span>
                  <span>SEÇİLDİ</span>
                </span>
              </div>
            ` : ''}
          </div>

          <h5 class="font-bold text-white text-xs line-clamp-1 group-hover:text-indigo-300 transition-colors" title="${scene.title}">
            ${scene.title}
          </h5>
          <p class="text-[10px] text-slate-400 font-mono mt-0.5">
            👥 ${scene.characters ? scene.characters.length : 1} Karakter
          </p>
        </div>
      `;
    }).join("");

    container.querySelectorAll(".home-featured-card").forEach(card => {
      card.addEventListener("click", () => {
        const sceneId = card.dataset.id;
        this.selectedScene = SCENES.find(s => s.id === sceneId) || SCENES[0];
        this._showNotification(`🎬 "${this.selectedScene.title}" seçildi! Şimdi oda kur veya solo başla.`, "success");
        this._renderHomeFeatured();
        if (this.dom.inputs.playerName && !this.dom.inputs.playerName.value.trim()) {
          this.dom.inputs.playerName.focus();
        }
      });
    });
  }

  _renderScenes(category = null) {
    if (category) this.currentCategory = category;
    const cat = this.currentCategory || "all";
    const query = (this.searchQuery || "").trim().toLowerCase();

    let filtered = SCENES;
    if (cat === "meme") {
      filtered = filtered.filter(s => s.category === "meme");
    } else if (cat === "dizi-film") {
      filtered = filtered.filter(s => s.category !== "meme");
    } else if (cat === "ozel") {
      filtered = filtered.filter(s => s.category === "ozel" || String(s.id).startsWith("custom-"));
    }

    if (query) {
      filtered = filtered.filter(s => {
        const titleMatch = s.title && s.title.toLowerCase().includes(query);
        const descMatch = s.description && s.description.toLowerCase().includes(query);
        const charMatch = s.characters && s.characters.some(c => c.name && c.name.toLowerCase().includes(query));
        const lineMatch = s.lines && s.lines.some(l => l.text && l.text.toLowerCase().includes(query));
        return titleMatch || descMatch || charMatch || lineMatch;
      });
    }

    if (filtered.length === 0) {
      this.dom.lobby.sceneGrid.innerHTML = `
        <div class="col-span-1 sm:col-span-2 py-12 text-center text-slate-400 space-y-2">
          <span class="text-4xl block">🔍</span>
          <p class="font-bold text-white text-sm">"${this.searchQuery}" ile eşleşen video bulunamadı.</p>
          <p class="text-xs">Farklı bir arama terimi deneyebilir veya kategoriyi değiştirebilirsin.</p>
        </div>
      `;
      return;
    }

    this.dom.lobby.sceneGrid.innerHTML = filtered.map(scene => {
      const isSelected = scene.id === this.selectedScene.id;
      const thumb = scene.thumbnail || `assets/thumbnails/${scene.id}.jpg`;
      const charBadges = (scene.characters || []).map(c => `
        <span class="px-2 py-0.5 text-[10px] sm:text-[11px] rounded-full bg-slate-900/90 text-slate-200 border border-slate-700/80 flex items-center space-x-1 shadow-sm">
          <span>${c.avatar || '🎭'}</span>
          <span class="font-medium truncate max-w-[85px]">${c.name}</span>
        </span>
      `).join("");

      return `
        <div class="scene-card group relative p-3 rounded-2xl border cursor-pointer transition-all duration-200 hover:-translate-y-1 ${
          isSelected 
            ? 'border-indigo-500 bg-indigo-950/40 ring-2 ring-indigo-500/60 shadow-lg shadow-indigo-500/20' 
            : 'border-slate-800/90 bg-slate-900/70 hover:border-slate-700 hover:bg-slate-900/90 hover:shadow-md'
        }" data-id="${scene.id}">
          
          <!-- Küçük Resim / Thumbnail (16:9) -->
          <div class="relative w-full aspect-video rounded-xl overflow-hidden bg-slate-950 mb-2.5 border border-slate-800/80 shadow-inner group-hover:border-indigo-500/40 transition-colors">
            <img src="${thumb}" 
                 alt="${scene.title}" 
                 loading="lazy"
                 class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                 onerror="this.onerror=null; this.src='data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'480\' height=\'270\' viewBox=\'0 0 480 270\'><rect width=\'480\' height=\'270\' fill=\'%230f172a\'/><text x=\'50%25\' y=\'50%25\' dominant-baseline=\'middle\' text-anchor=\'middle\' fill=\'%2364748b\' font-size=\'32\' font-family=\'sans-serif\'>🎬 DUBLAJ</text></svg>'"/>
            
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/30 pointer-events-none"></div>

            <!-- Sol Üst: Kategori -->
            <span class="absolute top-2 left-2 px-2 py-0.5 rounded-md bg-black/80 backdrop-blur-md text-amber-300 font-black text-[10px] uppercase tracking-wider border border-amber-500/40 shadow-sm flex items-center space-x-1">
              <span>${scene.category === 'meme' ? '🔥' : '🎬'}</span>
              <span>${scene.categoryName || (scene.category === 'meme' ? 'Meme' : 'Dizi/Film')}</span>
            </span>

            <!-- Sağ Üst: Karakter Sayısı -->
            <span class="absolute top-2 right-2 px-2 py-0.5 rounded-md bg-black/80 backdrop-blur-md text-slate-200 font-bold text-[10px] border border-slate-700/60 shadow-sm flex items-center space-x-1">
              <span>👥</span>
              <span>${scene.characters ? scene.characters.length : 1} Rol</span>
            </span>

            <!-- Sağ Alt: Süre -->
            <span class="absolute bottom-2 right-2 px-2 py-0.5 rounded-md bg-black/90 backdrop-blur-md text-white font-mono font-black text-[11px] border border-slate-700/80 shadow-md">
              ⏱️ ${scene.duration}s
            </span>

            <!-- Seçili Durumu Overlay -->
            ${isSelected ? `
              <div class="absolute inset-0 bg-indigo-950/40 border-2 border-indigo-400 rounded-xl flex items-center justify-center">
                <span class="px-3.5 py-1.5 rounded-full bg-indigo-600 text-white font-black text-xs shadow-2xl flex items-center space-x-1.5 tracking-wide border border-indigo-300 animate-pulse">
                  <span>✅</span>
                  <span>SEÇİLDİ</span>
                </span>
              </div>
            ` : `
              <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-black/30">
                <span class="w-10 h-10 rounded-full bg-indigo-600/80 backdrop-blur-md flex items-center justify-center text-white text-base shadow-xl border border-indigo-400/50 transform group-hover:scale-110 transition-transform">
                  ▶
                </span>
              </div>
            `}
          </div>

          <!-- Video Başlığı & Detaylar -->
          <div class="space-y-1.5">
            <h4 class="font-bold text-white text-sm line-clamp-1 group-hover:text-indigo-300 transition-colors" title="${scene.title}">
              ${scene.title}
            </h4>
            <p class="text-xs text-slate-400 line-clamp-1 font-normal">
              ${scene.description || ''}
            </p>
            <div class="flex flex-wrap items-center gap-1.5 pt-0.5">
              ${charBadges}
            </div>
          </div>
        </div>
      `;
    }).join("");

    this.dom.lobby.sceneGrid.querySelectorAll(".scene-card").forEach(card => {
      card.addEventListener("click", () => {
        const sceneId = card.dataset.id;
        this.selectedScene = SCENES.find(s => s.id === sceneId) || SCENES[0];
        if (this.network && this.network.isHost) {
          this.network.selectScene(sceneId);
        }
        this._updateRolesUI();
        this._renderScenes(category);
      });
    });

    this._updateRolesUI();
  }

  _renderLobbySceneGrid(category = null) {
    this._renderScenes(category);
  }

  _updateRolesUI() {
    this.dom.lobby.sceneTitle.innerText = this.selectedScene.title;
    const isSelectedSpectator = this.selectedRole === "spectator";

    const charactersHtml = (this.selectedScene.characters || []).map(char => {
      const isSelected = this.selectedRole === char.id;
      // Odada bu rolü başkası almış mı kontrol et
      const takenByPlayer = (this.network && this.network.state && this.network.state.players)
        ? this.network.state.players.find(p => p.roleId === char.id && (!this.network.peerId || p.id !== this.network.peerId))
        : null;

      return `
        <button class="role-select-btn p-3 rounded-xl border flex items-center justify-between transition-all ${
          isSelected 
            ? 'border-emerald-500 bg-emerald-950/30 ring-2 ring-emerald-500/40 text-white' 
            : (takenByPlayer ? 'border-slate-800/50 bg-slate-950/40 text-slate-500 opacity-75' : 'border-slate-800 bg-slate-900/50 hover:border-slate-700 text-slate-300')
        }" data-role="${char.id}" ${takenByPlayer && !isSelected ? 'title="' + takenByPlayer.name + ' bu rolü aldı"' : ''}>
          <div class="flex items-center space-x-2.5">
            <span class="text-2xl">${char.avatar}</span>
            <div class="text-left">
              <p class="font-bold text-sm" style="color: ${char.color}">${char.name}</p>
              <p class="text-xs ${takenByPlayer && !isSelected ? 'text-amber-400/80 font-medium' : 'text-slate-400'}">
                ${takenByPlayer && !isSelected ? `🔒 ${takenByPlayer.name} seçti` : 'Bu karakteri seslendir'}
              </p>
            </div>
          </div>
          ${isSelected ? '<span class="text-emerald-400 font-bold text-xs bg-emerald-500/20 px-2 py-1 rounded-md">SEÇTİN</span>' : (takenByPlayer ? '<span class="text-[10px] font-bold text-slate-500 bg-slate-800/60 px-2 py-0.5 rounded">DOLU</span>' : '')}
        </button>
      `;
    }).join("");

    const spectatorHtml = `
      <div class="pt-2 border-t border-slate-800/80">
        <button class="role-select-btn w-full p-3 rounded-xl border flex items-center justify-between transition-all ${
          isSelectedSpectator 
            ? 'border-amber-500 bg-amber-950/40 ring-2 ring-amber-500/40 text-white shadow-lg shadow-amber-500/10' 
            : 'border-slate-800/80 bg-slate-950/60 hover:border-slate-700 text-slate-400'
        }" data-role="spectator">
          <div class="flex items-center space-x-2.5">
            <span class="text-2xl">🍿</span>
            <div class="text-left">
              <p class="font-bold text-sm text-amber-300 flex items-center space-x-1.5">
                <span>Seyirci / İzleyici Koltuğu</span>
                <span class="text-[10px] uppercase font-extrabold px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">Sınırsız</span>
              </p>
              <p class="text-xs text-slate-400">Konuşma yapmaz, dublajı canlı izler ve prömiyerde güler</p>
            </div>
          </div>
          ${isSelectedSpectator ? '<span class="text-amber-400 font-bold text-xs bg-amber-500/20 px-2 py-1 rounded-md">SEYİRCİSİN</span>' : ''}
        </button>
      </div>
    `;

    this.dom.lobby.roleContainer.innerHTML = charactersHtml + spectatorHtml;

    this.dom.lobby.roleContainer.querySelectorAll(".role-select-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        this.selectedRole = btn.dataset.role;
        if (this.network) this.network.selectRole(this.selectedRole);
        this._updateRolesUI();
      });
    });
  }

  _updateLobbyUI(state) {
    if (!state) return;

    // Odadaki özel videoları yerel sahne listesine bağla ve eksik videoyu talep et
    if (state.customScenes && Array.isArray(state.customScenes)) {
      let hasNewCustom = false;
      state.customScenes.forEach(sceneMeta => {
        if (!SCENES.some(s => s.id === sceneMeta.id)) {
          SCENES.push({ ...sceneMeta, videoSrc: "" });
          hasNewCustom = true;
          if (this.network && !this.network.isHost) {
            this.network.requestCustomSceneVideo(sceneMeta.id);
          }
        }
      });
      if (hasNewCustom) {
        this._renderCategories();
        this._renderScenes();
      }
    }

    if (state.selectedSceneId && state.selectedSceneId !== this.selectedScene.id) {
      this.selectedScene = SCENES.find(s => s.id === state.selectedSceneId) || this.selectedScene;
      this._updateRolesUI();
    }

    this.dom.lobby.playerList.innerHTML = (state.players || []).map(p => {
      const isSpectator = p.roleId === "spectator";
      const assignedChar = (this.selectedScene.characters || []).find(c => c.id === p.roleId);
      return `
        <div class="flex items-center justify-between p-3 rounded-xl bg-slate-800/60 border border-slate-700/60">
          <div class="flex items-center space-x-3">
            <span class="text-2xl">${isSpectator ? '🍿' : p.avatar}</span>
            <div>
              <p class="font-bold text-sm text-white flex items-center space-x-1.5">
                <span>${p.name}</span>
                ${p.isHost ? '<span class="text-[10px] bg-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded font-semibold">HOST</span>' : ''}
              </p>
              <p class="text-xs ${isSpectator ? 'text-amber-300 font-semibold' : 'text-slate-400'}">
                ${isSpectator ? '🍿 Seyirci (İzleyici)' : (assignedChar ? `Rol: ${assignedChar.name}` : 'Rol seçiyor...')}
              </p>
            </div>
          </div>
          <span class="w-2.5 h-2.5 rounded-full ${p.roleId ? (isSpectator ? 'bg-amber-400 shadow-sm shadow-amber-400' : 'bg-emerald-400 shadow-sm shadow-emerald-400') : 'bg-slate-500'}"></span>
        </div>
      `;
    }).join("");
  }

  // ==========================================
  // KAPALI GİRİŞ VE KULLANICI DENEYİMİ (AUTH)
  // ==========================================
  async _checkInitialAuth() {
    if (this.auth.isAuthenticated()) {
      const user = await this.auth.verifySession();
      if (user) {
        this._applyAuthenticatedUser(user, false);
        return;
      }
    }
    this._showLoginScreen();
  }

  _showLoginScreen() {
    this.isAdmin = false;
    this._checkAdminState();
    this._switchScreen("login");
    this.dom.headerUser?.section?.classList.add("hidden");
    if (this.dom.login.errorBox) {
      this.dom.login.errorBox.classList.add("hidden");
    }
    if (this.dom.login.usernameInput) {
      setTimeout(() => this.dom.login.usernameInput.focus(), 150);
    }
  }

  _applyAuthenticatedUser(user, showWelcomeToast = true) {
    const username = user.username || "Oyuncu";
    const role = user.role || "user";
    const displayName = username.charAt(0).toUpperCase() + username.slice(1);

    this.isAdmin = (role === "admin");
    if (this.network) {
      this.network.isAdmin = this.isAdmin;
    }

    if (this.dom.inputs.playerName) {
      this.dom.inputs.playerName.value = displayName;
    }

    // Üst Bar Kullanıcı Rozeti & Butonları
    if (this.dom.headerUser.section) {
      this.dom.headerUser.section.classList.remove("hidden");
    }
    if (this.dom.headerUser.name) {
      this.dom.headerUser.name.innerText = this.isAdmin ? `${displayName} (Admin)` : `${displayName} (Oyuncu)`;
    }
    if (this.dom.headerUser.icon) {
      this.dom.headerUser.icon.innerText = this.isAdmin ? "👑" : "🎙️";
    }
    if (this.dom.headerUser.badge) {
      if (this.isAdmin) {
        this.dom.headerUser.badge.className = "px-3 py-1 rounded-full text-xs font-black bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center space-x-1.5 shadow-sm";
      } else {
        this.dom.headerUser.badge.className = "px-3 py-1 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 flex items-center space-x-1.5 shadow-sm";
      }
    }

    // Ana Ekran Karşılama Kartı
    if (this.dom.homeWelcome.name) {
      this.dom.homeWelcome.name.innerText = displayName;
    }
    if (this.dom.homeWelcome.badge) {
      if (this.isAdmin) {
        this.dom.homeWelcome.badge.className = "px-2.5 py-1 rounded-xl text-xs font-black bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center space-x-1";
        if (this.dom.homeWelcome.badgeIcon) this.dom.homeWelcome.badgeIcon.innerText = "👑";
        if (this.dom.homeWelcome.badgeText) this.dom.homeWelcome.badgeText.innerText = "Admin";
      } else {
        this.dom.homeWelcome.badge.className = "px-2.5 py-1 rounded-xl text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 flex items-center space-x-1";
        if (this.dom.homeWelcome.badgeIcon) this.dom.homeWelcome.badgeIcon.innerText = "🎙️";
        if (this.dom.homeWelcome.badgeText) this.dom.homeWelcome.badgeText.innerText = "Oyuncu";
      }
    }

    this._checkAdminState();
    this._switchScreen("home");

    if (showWelcomeToast) {
      this._showNotification(`Hoş Geldin, ${displayName}! 🎙️`, "success");
    }
  }

  async _handleLoginSubmit() {
    const username = (this.dom.login.usernameInput?.value || "").trim();
    const password = (this.dom.login.passwordInput?.value || "").trim();

    if (!username || !password) {
      this._showLoginError("Lütfen kullanıcı adı ve şifrenizi girin.");
      return;
    }

    const btn = this.dom.login.submitBtn;
    const btnText = this.dom.login.submitBtnText;
    if (btn) {
      btn.disabled = true;
      btn.classList.add("opacity-75", "cursor-wait");
    }
    if (btnText) btnText.innerText = "Giriş Yapılıyor...";

    const res = await this.auth.login(username, password);

    if (btn) {
      btn.disabled = false;
      btn.classList.remove("opacity-75", "cursor-wait");
    }
    if (btnText) btnText.innerText = "Giriş Yap";

    if (res.success && res.user) {
      if (this.dom.login.errorBox) this.dom.login.errorBox.classList.add("hidden");
      if (this.dom.login.passwordInput) this.dom.login.passwordInput.value = "";
      this._applyAuthenticatedUser(res.user, true);
    } else {
      this._showLoginError(res.error || "Kullanıcı adı veya şifre hatalı!");
    }
  }

  _showLoginError(message) {
    if (this.dom.login.errorBox && this.dom.login.errorText) {
      this.dom.login.errorText.innerText = message;
      this.dom.login.errorBox.classList.remove("hidden");
    }
  }

  async _handleUserLogout() {
    await this.auth.logout();
    this._showLoginScreen();
    this._showNotification("Oturum başarıyla kapatıldı.", "info");
  }

  // ==========================================
  // ODAYA KATIL (JOIN MODAL)
  // ==========================================
  _openJoinModal() {
    this.dom.joinModal.modal?.classList.remove("hidden");
    if (this.dom.joinModal.input) {
      this.dom.joinModal.input.value = this.dom.inputs.roomCode?.value || "";
      setTimeout(() => this.dom.joinModal.input.focus(), 120);
    }
  }

  _closeJoinModal() {
    this.dom.joinModal.modal?.classList.add("hidden");
  }

  async _handleJoinModalSubmit() {
    const code = (this.dom.joinModal.input?.value || "").trim().toUpperCase();
    if (!code) {
      this._showNotification("Lütfen oda kodunu girin (örn: DUB-XXXX)", "warning");
      return;
    }
    this._closeJoinModal();
    if (this.dom.inputs.roomCode) {
      this.dom.inputs.roomCode.value = code;
    }
    const name = this.dom.inputs.playerName.value.trim() || (this.auth?.getDisplayName ? this.auth.getDisplayName() : "Oyuncu " + Math.floor(Math.random() * 900));
    this.isSoloMode = false;
    this._setupNetwork(name);
    try {
      await this.network.joinRoom(code);
      this.dom.lobby.codeDisplay.innerText = code;
      this._switchScreen("lobby");
    } catch (err) {
      this._showNotification("Odaya bağlanılamadı. Kodu kontrol edin!", "error");
    }
  }

  // ==========================================
  // ADMİN YÖNETİM PANELİ (MİRAÇ / ADMIN)
  // ==========================================
  _openAdminPanel() {
    if (!this.isAdmin) {
      this._showNotification("Bu alana erişim için admin yetkisi gereklidir!", "warning");
      return;
    }
    this._populateAdminSceneDropdown();
    this._switchAdminPanelTab("users");
    this._loadAdminUsers();
    this.dom.adminPanel.modal?.classList.remove("hidden");
  }

  _closeAdminPanel() {
    this.dom.adminPanel.modal?.classList.add("hidden");
  }

  _switchAdminPanelTab(tabName) {
    if (tabName === "users") {
      this.dom.adminPanel.tabUsersBtn?.classList.add("border-amber-500", "text-amber-400");
      this.dom.adminPanel.tabUsersBtn?.classList.remove("border-transparent", "text-slate-400");
      this.dom.adminPanel.tabScenesBtn?.classList.remove("border-amber-500", "text-amber-400");
      this.dom.adminPanel.tabScenesBtn?.classList.add("border-transparent", "text-slate-400");

      this.dom.adminPanel.contentUsers?.classList.remove("hidden");
      this.dom.adminPanel.contentScenes?.classList.add("hidden");
    } else {
      this.dom.adminPanel.tabScenesBtn?.classList.add("border-amber-500", "text-amber-400");
      this.dom.adminPanel.tabScenesBtn?.classList.remove("border-transparent", "text-slate-400");
      this.dom.adminPanel.tabUsersBtn?.classList.remove("border-amber-500", "text-amber-400");
      this.dom.adminPanel.tabUsersBtn?.classList.add("border-transparent", "text-slate-400");

      this.dom.adminPanel.contentScenes?.classList.remove("hidden");
      this.dom.adminPanel.contentUsers?.classList.add("hidden");
    }
  }

  _populateAdminSceneDropdown() {
    const dropdown = this.dom.adminPanel.sceneSelectDropdown;
    if (!dropdown) return;
    dropdown.innerHTML = SCENES.map(scene => `
      <option value="${scene.id}" ${this.selectedScene && this.selectedScene.id === scene.id ? "selected" : ""}>
        ${scene.title} (${scene.duration}s - ${scene.categoryName || scene.category})
      </option>
    `).join("");
  }

  async _loadAdminUsers() {
    const container = this.dom.adminPanel.usersListContainer;
    if (!container) return;
    container.innerHTML = `
      <div class="text-center py-6 text-slate-400 text-xs flex items-center justify-center space-x-2">
        <span class="w-3 h-3 rounded-full bg-amber-400 animate-ping"></span>
        <span>Kullanıcı listesi yükleniyor...</span>
      </div>
    `;

    const res = await this.auth.getAdminUsers();
    if (res.success && Array.isArray(res.users)) {
      if (this.dom.adminPanel.userCountBadge) {
        this.dom.adminPanel.userCountBadge.innerText = `${res.users.length} Kullanıcı`;
      }
      if (res.users.length === 0) {
        container.innerHTML = `<div class="text-center py-4 text-slate-500 text-xs">Henüz kayıtlı kullanıcı bulunmuyor.</div>`;
        return;
      }
      const currentUsername = this.auth.getUsername();
      container.innerHTML = res.users.map(u => {
        const isCurrent = u.username === currentUsername;
        const isAdminRole = u.role === "admin";
        const dateStr = u.created_at ? new Date(u.created_at * 1000).toLocaleDateString("tr-TR") : "-";
        return `
          <div class="flex items-center justify-between p-3 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition-colors">
            <div class="flex items-center space-x-3">
              <span class="text-xl">${isAdminRole ? "👑" : "🎙️"}</span>
              <div>
                <div class="font-bold text-xs text-white flex items-center space-x-2">
                  <span>${u.username}</span>
                  ${isCurrent ? '<span class="text-[9px] bg-indigo-500/30 text-indigo-300 px-1.5 py-0.2 rounded font-semibold">SEN</span>' : ''}
                </div>
                <div class="text-[10px] text-slate-400">Kayıt: ${dateStr}</div>
              </div>
            </div>
            <div class="flex items-center space-x-2.5">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${isAdminRole ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'bg-slate-800 text-slate-300 border border-slate-700'}">
                ${isAdminRole ? 'Yönetici (Admin)' : 'Oyuncu'}
              </span>
              <button class="btn-delete-user px-2.5 py-1 text-red-400 hover:text-white hover:bg-red-950/60 border border-red-500/30 rounded-lg text-xs transition-all ${isCurrent ? 'opacity-40 cursor-not-allowed' : ''}" 
                      data-username="${u.username}" 
                      title="${isCurrent ? 'Kendinizi silemezsiniz' : 'Kullanıcıyı Sil'}" 
                      ${isCurrent ? 'disabled' : ''}>
                🗑️
              </button>
            </div>
          </div>
        `;
      }).join("");

      container.querySelectorAll(".btn-delete-user:not([disabled])").forEach(btn => {
        btn.addEventListener("click", () => {
          const targetUser = btn.dataset.username;
          this._handleDeleteAdminUser(targetUser);
        });
      });
    } else {
      container.innerHTML = `
        <div class="text-center py-4 text-rose-400 text-xs">
          ${res.error || "Kullanıcılar listelenemedi."}
        </div>
      `;
    }
  }

  async _handleCreateAdminUser() {
    const username = (this.dom.adminPanel.newUsernameInput?.value || "").trim();
    const password = (this.dom.adminPanel.newPasswordInput?.value || "").trim();
    const role = this.dom.adminPanel.newRoleSelect?.value || "user";
    const feedback = this.dom.adminPanel.userFeedback;

    if (!username || !password) {
      if (feedback) {
        feedback.className = "text-xs font-semibold text-rose-400";
        feedback.innerText = "⚠️ Kullanıcı adı ve şifre zorunludur.";
      }
      return;
    }

    if (feedback) {
      feedback.className = "text-xs font-semibold text-slate-400";
      feedback.innerText = "Kullanıcı oluşturuluyor...";
    }

    const res = await this.auth.createAdminUser(username, password, role);

    if (res.success) {
      if (feedback) {
        feedback.className = "text-xs font-semibold text-emerald-400";
        feedback.innerText = `✅ '${username}' kullanıcısı oluşturuldu!`;
      }
      if (this.dom.adminPanel.newUsernameInput) this.dom.adminPanel.newUsernameInput.value = "";
      if (this.dom.adminPanel.newPasswordInput) this.dom.adminPanel.newPasswordInput.value = "";
      this._loadAdminUsers();
      setTimeout(() => {
        if (feedback) feedback.innerText = "";
      }, 4000);
    } else {
      if (feedback) {
        feedback.className = "text-xs font-semibold text-rose-400";
        feedback.innerText = `❌ ${res.error || "Hata oluştu."}`;
      }
    }
  }

  async _handleDeleteAdminUser(targetUsername) {
    if (!targetUsername) return;
    const ok = confirm(`'${targetUsername}' kullanıcısını silmek istediğinize emin misiniz?`);
    if (!ok) return;

    const res = await this.auth.deleteAdminUser(targetUsername);
    if (res.success) {
      this._showNotification(`'${targetUsername}' kullanıcısı silindi.`, "info");
      this._loadAdminUsers();
    } else {
      this._showNotification(res.error || "Kullanıcı silinemedi.", "error");
    }
  }

  _bindAuthEvents() {
    // Giriş Formu
    this.dom.login.form?.addEventListener("submit", (e) => {
      e.preventDefault();
      this._handleLoginSubmit();
    });
    this.dom.login.submitBtn?.addEventListener("click", () => {
      this._handleLoginSubmit();
    });
    this.dom.login.passwordInput?.addEventListener("keydown", (e) => {
      if (e.key === "Enter") this._handleLoginSubmit();
    });
    this.dom.login.usernameInput?.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        if (this.dom.login.passwordInput?.value) {
          this._handleLoginSubmit();
        } else {
          this.dom.login.passwordInput?.focus();
        }
      }
    });

    // Oturum Kapatma
    this.dom.headerUser.logoutBtn?.addEventListener("click", () => {
      this._handleUserLogout();
    });

    // Admin Paneli Açma Butonları (Header & Ana Ekran)
    this.dom.headerUser.adminPanelBtn?.addEventListener("click", () => {
      this._openAdminPanel();
    });
    this.dom.homeWelcome.adminPanelBtn?.addEventListener("click", () => {
      this._openAdminPanel();
    });

    // Admin Paneli Kapatma & Sekmeler
    this.dom.adminPanel.closeBtn?.addEventListener("click", () => {
      this._closeAdminPanel();
    });
    this.dom.adminPanel.closeBottomBtn?.addEventListener("click", () => {
      this._closeAdminPanel();
    });
    this.dom.adminPanel.tabUsersBtn?.addEventListener("click", () => {
      this._switchAdminPanelTab("users");
    });
    this.dom.adminPanel.tabScenesBtn?.addEventListener("click", () => {
      this._switchAdminPanelTab("scenes");
    });

    // Admin Kullanıcı Ekleme & Yenileme
    this.dom.adminPanel.createUserBtn?.addEventListener("click", () => {
      this._handleCreateAdminUser();
    });
    this.dom.adminPanel.refreshUsersBtn?.addEventListener("click", () => {
      this._loadAdminUsers();
    });

    // Admin Sahne Seçimi & Butonlar
    this.dom.adminPanel.sceneSelectDropdown?.addEventListener("change", (e) => {
      const sceneId = e.target.value;
      const targetScene = SCENES.find(s => s.id === sceneId);
      if (targetScene) {
        this.selectedScene = targetScene;
        this._updateRolesUI();
      }
    });
    this.dom.adminPanel.launchEditorBtn?.addEventListener("click", () => {
      this._closeAdminPanel();
      this._openTranscriptEditor();
    });
    this.dom.adminPanel.saveDiskBtn?.addEventListener("click", () => {
      this._savePermanentScene();
    });
    this.dom.adminPanel.openUploadBtn?.addEventListener("click", () => {
      this._closeAdminPanel();
      this.dom.modals.upload?.classList.remove("hidden");
    });

    // Odaya Katıl Modal Bağlantıları
    this.dom.homeWelcome.openJoinModalBtn?.addEventListener("click", () => {
      this._openJoinModal();
    });
    this.dom.joinModal.closeBtn?.addEventListener("click", () => {
      this._closeJoinModal();
    });
    this.dom.joinModal.cancelBtn?.addEventListener("click", () => {
      this._closeJoinModal();
    });
    this.dom.joinModal.submitBtn?.addEventListener("click", () => {
      this._handleJoinModalSubmit();
    });
    this.dom.joinModal.input?.addEventListener("keydown", (e) => {
      if (e.key === "Enter") this._handleJoinModalSubmit();
    });
  }

  // --- ADMİN YETKİSİ YÖNETİMİ ---
  _checkAdminState() {
    if (this.isAdmin) {
      this.dom.header.adminBadge?.classList.remove("hidden");
      this.dom.header.openTranscriptEditorBtn?.classList.remove("hidden");
      this.dom.header.adminLogoutBtn?.classList.remove("hidden");
      this.dom.headerUser?.adminPanelBtn?.classList.remove("hidden");
      this.dom.homeWelcome?.adminCard?.classList.remove("hidden");
    } else {
      this.dom.header.adminBadge?.classList.add("hidden");
      this.dom.header.openTranscriptEditorBtn?.classList.add("hidden");
      this.dom.header.adminLogoutBtn?.classList.add("hidden");
      this.dom.headerUser?.adminPanelBtn?.classList.add("hidden");
      this.dom.homeWelcome?.adminCard?.classList.add("hidden");
    }
  }

  _openAdminLoginModal() {
    this.dom.modals.adminLogin?.classList.remove("hidden");
    if (this.dom.modals.adminPassInput) {
      this.dom.modals.adminPassInput.value = "";
      this.dom.modals.adminPassInput.focus();
    }
  }

  _verifyAdminPassword() {
    const entered = (this.dom.modals.adminPassInput?.value || "").trim();
    if (entered === "dubSex" || entered.toLowerCase() === "dubsex") {
      this.isAdmin = true;
      if (this.network) this.network.isAdmin = true;
      this._checkAdminState();
      this.dom.modals.adminLogin?.classList.add("hidden");
      alert("👑 Hoş geldin Miraç! Admin yetkileri tanımlandı.");
    } else {
      alert("❌ Hatalı şifre! Erişim reddedildi.");
      if (this.dom.modals.adminPassInput) this.dom.modals.adminPassInput.value = "";
    }
  }

  // --- GELİŞMİŞ TRANSKRİPT & KARAKTER EDİTÖRÜ (ADMIN) ---
  _openTranscriptEditor() {
    if (!this.selectedScene) return;
    this.dom.modals.editorTitle.innerText = `${this.selectedScene.title} (${this.selectedScene.duration}s)`;
    
    // Önizleme videosunu hazırla ve sesini aç
    const vid = this.dom.modals.editorPreviewVideo;
    if (vid) {
      vid.src = this.selectedScene.videoSrc;
      vid.currentTime = 0;
      vid.playbackRate = 1.0;
      vid.muted = false;
      this._editorPreviewTargetEnd = null;

      vid.onloadedmetadata = () => {
        const dur = vid.duration || this.selectedScene.duration || 0;
        if (this.dom.modals.editorTotalTimeDisplay) {
          this.dom.modals.editorTotalTimeDisplay.innerText = `${dur.toFixed(2)}s`;
        }
        if (this.dom.modals.editorVideoSlider) {
          this.dom.modals.editorVideoSlider.max = dur;
          this.dom.modals.editorVideoSlider.value = 0;
        }
      };

      vid.ontimeupdate = () => {
        const cur = vid.currentTime;
        if (this.dom.modals.editorLiveTimeDisplay) {
          this.dom.modals.editorLiveTimeDisplay.innerText = `${cur.toFixed(2)}s`;
        }
        if (this.dom.modals.editorVideoSlider && !this._isUserScrubbingEditorVideo) {
          this.dom.modals.editorVideoSlider.value = cur;
        }

        // Eğer belirli bir repliği dinliyorsak bitiş saniyesinde durdur
        if (this._editorPreviewTargetEnd !== null && cur >= this._editorPreviewTargetEnd) {
          vid.pause();
          this._editorPreviewTargetEnd = null;
        }

        // Aktif repliği vurgula
        this._highlightActiveEditorLine(cur);
      };

      vid.onplay = () => {
        if (this.dom.modals.editorPlayIcon) this.dom.modals.editorPlayIcon.innerText = "⏸️";
        if (this.dom.modals.editorPlayText) this.dom.modals.editorPlayText.innerText = "Durdur";
      };

      vid.onpause = () => {
        if (this.dom.modals.editorPlayIcon) this.dom.modals.editorPlayIcon.innerText = "▶";
        if (this.dom.modals.editorPlayText) this.dom.modals.editorPlayText.innerText = "Oynat";
      };

      vid.onended = () => {
        if (this.dom.modals.editorPlayIcon) this.dom.modals.editorPlayIcon.innerText = "▶";
        if (this.dom.modals.editorPlayText) this.dom.modals.editorPlayText.innerText = "Oynat";
        this._editorPreviewTargetEnd = null;
      };
    }

    this._switchEditorTab("lines");
    this._renderTranscriptEditorLines();
    this._renderTranscriptEditorCharacters();
    this.dom.modals.adminEditor?.classList.remove("hidden");
  }

  _closeTranscriptEditor() {
    this.dom.modals.adminEditor?.classList.add("hidden");
    if (this.dom.modals.editorPreviewVideo) {
      this.dom.modals.editorPreviewVideo.pause();
    }
    this._editorPreviewTargetEnd = null;
  }

  _switchEditorTab(tabName) {
    if (tabName === "lines") {
      this.dom.modals.tabLinesBtn?.classList.add("border-amber-500", "text-amber-400");
      this.dom.modals.tabLinesBtn?.classList.remove("border-transparent", "text-slate-400");
      this.dom.modals.tabCharactersBtn?.classList.remove("border-amber-500", "text-amber-400");
      this.dom.modals.tabCharactersBtn?.classList.add("border-transparent", "text-slate-400");

      this.dom.modals.tabLinesContent?.classList.remove("hidden");
      this.dom.modals.tabCharactersContent?.classList.add("hidden");
    } else {
      this.dom.modals.tabCharactersBtn?.classList.add("border-amber-500", "text-amber-400");
      this.dom.modals.tabCharactersBtn?.classList.remove("border-transparent", "text-slate-400");
      this.dom.modals.tabLinesBtn?.classList.remove("border-amber-500", "text-amber-400");
      this.dom.modals.tabLinesBtn?.classList.add("border-transparent", "text-slate-400");

      this.dom.modals.tabCharactersContent?.classList.remove("hidden");
      this.dom.modals.tabLinesContent?.classList.add("hidden");
    }
  }

  _toggleEditorVideoPreview() {
    // Yan yana stüdyo düzeninde video daima görünür durumdadır
    const vid = this.dom.modals.editorPreviewVideo;
    if (vid) {
      if (vid.paused) vid.play().catch(() => {});
      else vid.pause();
    }
  }

  _highlightActiveEditorLine(cur) {
    const rows = this.dom.modals.editorLinesContainer?.querySelectorAll(".editor-line-row");
    if (!rows) return;
    rows.forEach(row => {
      const start = parseFloat(row.querySelector(".line-start-input")?.value) || parseFloat(row.dataset.start) || 0;
      const end = parseFloat(row.querySelector(".line-end-input")?.value) || parseFloat(row.dataset.end) || 0;
      const indicator = row.querySelector(".line-playing-indicator");
      if (cur >= start && cur <= end) {
        row.classList.add("border-amber-400", "bg-amber-500/20", "shadow-lg", "shadow-amber-500/10");
        indicator?.classList.remove("hidden");
      } else {
        row.classList.remove("border-amber-400", "bg-amber-500/20", "shadow-lg", "shadow-amber-500/10");
        indicator?.classList.add("hidden");
      }
    });
  }

  _renderTranscriptEditorLines() {
    const lines = this.selectedScene.lines || [];
    const characters = this.selectedScene.characters || [];

    if (this.dom.modals.editorLineCountBadge) {
      this.dom.modals.editorLineCountBadge.innerText = `${lines.length} Replik`;
    }

    this.dom.modals.editorLinesContainer.innerHTML = lines.map((line, index) => {
      const isMusic = line.type === "music" || line.isMusic;
      const duration = (line.endTime - line.startTime).toFixed(1);
      return `
      <div class="editor-line-row p-3.5 rounded-2xl transition-all duration-200 ${isMusic ? 'bg-amber-950/25 border-2 border-amber-500/50' : 'bg-slate-950/70 border border-slate-800'} space-y-2.5" data-index="${index}" data-start="${line.startTime}" data-end="${line.endTime}" data-type="${isMusic ? 'music' : 'dialogue'}">
        <!-- Üst Kontrol Barı -->
        <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-2">
          <div class="flex items-center space-x-2">
            <!-- Sıralama Butonları -->
            <div class="flex items-center bg-slate-900 border border-slate-700 rounded-lg overflow-hidden">
              <button class="btn-line-up px-2 py-1 hover:bg-slate-800 text-slate-300 hover:text-white text-xs" title="Yukarı Taşı">⬆️</button>
              <button class="btn-line-down px-2 py-1 hover:bg-slate-800 text-slate-300 hover:text-white text-xs border-l border-slate-700" title="Aşağı Taşı">⬇️</button>
            </div>

            <!-- Karakter / Müzik Seçimi -->
            <select class="line-char-select px-2.5 py-1 ${isMusic ? 'bg-amber-950/80 border-amber-500/60 text-amber-300 font-black' : 'bg-slate-900 border-slate-700 text-white font-bold'} border rounded-xl text-xs focus:outline-none">
              <option value="__music__" ${isMusic ? 'selected' : ''}>🎵 [MÜZİK / MİKROFON KİLİDİ]</option>
              ${characters.map(c => `
                <option value="${c.id}" ${(!isMusic && c.id === line.characterId) ? 'selected' : ''}>
                  ${c.avatar || "🎭"} ${c.name}
                </option>
              `).join("")}
            </select>

            <!-- Çalıyor İndikatörü -->
            <span class="line-playing-indicator hidden px-2 py-0.5 bg-amber-500/20 border border-amber-500/40 text-amber-300 rounded-full text-[10px] font-black animate-pulse flex items-center space-x-1">
              <span>🔊</span>
              <span>Çalıyor</span>
            </span>
          </div>

          <!-- Dinle & Sil Butonları -->
          <div class="flex items-center space-x-1.5">
            <button class="btn-preview-line px-2.5 py-1 bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-amber-300 hover:text-amber-200 font-bold rounded-lg text-xs transition-all flex items-center space-x-1" title="Videonun bu replik aralığını oynat ve dinle">
              <span>▶</span>
              <span>Dinle</span>
            </button>
            <button class="btn-delete-line p-1 text-red-400 hover:text-red-300 hover:bg-red-950/40 rounded-lg transition-colors ml-1" title="Repliği Sil">
              🗑️
            </button>
          </div>
        </div>

        <!-- Zaman Çizelgesi Kontrolleri -->
        <div class="flex flex-wrap items-center justify-between gap-2 bg-slate-900/60 p-2 rounded-xl border border-slate-800/60">
          <div class="flex items-center space-x-1">
            <span class="text-[11px] font-semibold text-slate-400">Başla:</span>
            <button class="btn-grab-start px-2 py-0.5 bg-indigo-600/30 hover:bg-indigo-600/50 border border-indigo-500/50 text-indigo-300 rounded text-[11px] font-bold transition-all" title="Videonun şu anki saniyesini başlangıç yap">📍 Başla</button>
            <button class="nudge-btn px-1.5 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px]" data-action="sub-start">-0.2</button>
            <input type="number" step="0.1" value="${line.startTime}" class="line-start-input w-16 px-1.5 py-0.5 bg-slate-900 border border-slate-700 rounded text-center text-xs font-mono text-indigo-300 font-bold">
            <button class="nudge-btn px-1.5 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px]" data-action="add-start">+0.2</button>
          </div>

          <div class="flex items-center space-x-1">
            <span class="text-[11px] font-semibold text-slate-400">Bitir:</span>
            <button class="btn-grab-end px-2 py-0.5 bg-emerald-600/30 hover:bg-emerald-600/50 border border-emerald-500/50 text-emerald-300 rounded text-[11px] font-bold transition-all" title="Videonun şu anki saniyesini bitiş yap">📍 Bitir</button>
            <button class="nudge-btn px-1.5 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px]" data-action="sub-end">-0.2</button>
            <input type="number" step="0.1" value="${line.endTime}" class="line-end-input w-16 px-1.5 py-0.5 bg-slate-900 border border-slate-700 rounded text-center text-xs font-mono text-emerald-300 font-bold">
            <button class="nudge-btn px-1.5 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px]" data-action="add-end">+0.2</button>
          </div>

          <div class="text-[10px] text-slate-400 font-mono">
            Süre: <span class="line-duration-display text-white font-bold">${duration}s</span>
          </div>
        </div>

        <!-- Replik / Müzik Metni -->
        <div>
          <input type="text" value="${(line.text || '').replace(/"/g, '&quot;')}" placeholder="${isMusic ? 'Müzik/efekt adı...' : 'Replik metni...'}" 
                 class="line-text-input w-full px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-xl text-white text-xs font-medium focus:border-amber-500 focus:outline-none">
        </div>

        <!-- Duygu / İpucu -->
        <div>
          <input type="text" value="${line.emotion || (isMusic ? 'Fon Müziği / Edit' : '')}" placeholder="Duygu / Yönerge (Örn: Öfkeli bağırış)" 
                 class="line-emotion-input w-full px-3 py-1 bg-slate-900/60 border border-slate-800 rounded-lg text-slate-300 text-[11px] italic focus:outline-none">
        </div>
      </div>
    `;
    }).join("");

    // Event Bağlantıları (Dinle, Canlı Alma, Nudge, Sıralama ve Silme)
    this.dom.modals.editorLinesContainer.querySelectorAll(".editor-line-row").forEach(row => {
      const startInput = row.querySelector(".line-start-input");
      const endInput = row.querySelector(".line-end-input");
      const durEl = row.querySelector(".line-duration-display");

      const updateDuration = () => {
        const s = parseFloat(startInput.value) || 0;
        const e = parseFloat(endInput.value) || 0;
        if (e <= s) {
          if (durEl) durEl.innerHTML = `<span class="text-rose-400 font-bold animate-pulse text-[10px]" title="Bitiş süresi başlangıçtan büyük olmalıdır!">⚠️ Bitiş ≤ Başla (${(e - s).toFixed(1)}s)</span>`;
          endInput.classList.add("border-rose-500", "text-rose-400", "bg-rose-950/30");
        } else {
          if (durEl) durEl.innerHTML = `<span class="text-white font-bold">${(e - s).toFixed(1)}s</span>`;
          endInput.classList.remove("border-rose-500", "text-rose-400", "bg-rose-950/30");
        }
        row.dataset.start = s;
        row.dataset.end = e;
      };

      startInput.addEventListener("input", updateDuration);
      endInput.addEventListener("input", updateDuration);

      // Bu Repliği Dinle & Önizle (Sadece o repliğin aralığını oynatıp durur)
      row.querySelector(".btn-preview-line")?.addEventListener("click", () => {
        const vid = this.dom.modals.editorPreviewVideo;
        if (!vid) return;
        const start = parseFloat(startInput.value) || 0;
        let end = parseFloat(endInput.value) || (start + 2.0);
        if (end <= start) end = start + 2.0;
        this._editorPreviewTargetEnd = end;
        vid.currentTime = Math.max(0, start);
        vid.play().catch(() => {});
      });

      // Yukarı Taşı
      row.querySelector(".btn-line-up")?.addEventListener("click", () => {
        if (row.previousElementSibling) {
          row.previousElementSibling.before(row);
          this._syncLinesFromDOM();
        }
      });

      // Aşağı Taşı
      row.querySelector(".btn-line-down")?.addEventListener("click", () => {
        if (row.nextElementSibling) {
          row.nextElementSibling.after(row);
          this._syncLinesFromDOM();
        }
      });

      // Videodan Başlangıç Saniyesi Yakala
      row.querySelector(".btn-grab-start")?.addEventListener("click", () => {
        const vid = this.dom.modals.editorPreviewVideo;
        if (vid) {
          startInput.value = vid.currentTime.toFixed(2);
          // Eğer bitiş saniyesi başlangıçtan küçük kaldıysa otomatik güncelle
          const s = parseFloat(startInput.value) || 0;
          const e = parseFloat(endInput.value) || 0;
          if (e <= s) {
            endInput.value = (s + 2.5).toFixed(2);
          }
          updateDuration();
          this._syncLinesFromDOM();
          const btn = row.querySelector(".btn-grab-start");
          btn.classList.add("bg-emerald-500", "text-slate-950");
          setTimeout(() => btn.classList.remove("bg-emerald-500", "text-slate-950"), 250);
        }
      });

      // Videodan Bitiş Saniyesi Yakala
      row.querySelector(".btn-grab-end")?.addEventListener("click", () => {
        const vid = this.dom.modals.editorPreviewVideo;
        if (vid) {
          const s = parseFloat(startInput.value) || 0;
          let endVal = vid.currentTime;
          if (endVal <= s) {
            endVal = s + 2.0;
          }
          endInput.value = endVal.toFixed(2);
          updateDuration();
          this._syncLinesFromDOM();
          const btn = row.querySelector(".btn-grab-end");
          btn.classList.add("bg-emerald-500", "text-slate-950");
          setTimeout(() => btn.classList.remove("bg-emerald-500", "text-slate-950"), 250);
        }
      });

      // Nudge butonları
      row.querySelectorAll(".nudge-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const action = btn.dataset.action;
          if (action === "sub-start") startInput.value = Math.max(0, (parseFloat(startInput.value) - 0.2)).toFixed(2);
          if (action === "add-start") startInput.value = (parseFloat(startInput.value) + 0.2).toFixed(2);
          if (action === "sub-end") endInput.value = Math.max(0, (parseFloat(endInput.value) - 0.2)).toFixed(2);
          if (action === "add-end") endInput.value = (parseFloat(endInput.value) + 0.2).toFixed(2);
          updateDuration();
          this._syncLinesFromDOM();
        });
      });

      // Satır Sil (Hemen DOM'dan ve veriden siler, diğer replikleri bozmaz)
      row.querySelector(".btn-delete-line")?.addEventListener("click", () => {
        row.remove();
        this._syncLinesFromDOM();
        if (this.dom.modals.editorLineCountBadge) {
          const count = this.dom.modals.editorLinesContainer.querySelectorAll(".editor-line-row").length;
          this.dom.modals.editorLineCountBadge.innerText = `${count} Replik`;
        }
      });

      // Metin ve Duygu değiştiğinde anında senkron et
      row.querySelector(".line-text-input")?.addEventListener("input", () => this._syncLinesFromDOM());
      row.querySelector(".line-emotion-input")?.addEventListener("input", () => this._syncLinesFromDOM());
      row.querySelector(".line-char-select")?.addEventListener("change", () => this._syncLinesFromDOM());
    });
  }

  // Kronolojik Zamana Göre Sırala
  _sortTranscriptLinesByTime() {
    this._syncLinesFromDOM();
    if (!this.selectedScene || !this.selectedScene.lines) return;
    this.selectedScene.lines.sort((a, b) => (a.startTime || 0) - (b.startTime || 0));
    this._renderTranscriptEditorLines();
  }

  // --- KARAKTER YÖNETİMİ ---
  _renderTranscriptEditorCharacters() {
    const characters = this.selectedScene.characters || [];
    this.dom.modals.editorCharactersContainer.innerHTML = characters.map(char => `
      <div class="editor-char-row bg-slate-950/80 border border-slate-800 rounded-2xl p-4 flex flex-wrap items-center justify-between gap-3" data-id="${char.id}">
        <div class="flex items-center space-x-3">
          <input type="text" value="${char.avatar || '🎭'}" maxlength="2" title="Avatar Emoji" 
                 class="char-avatar-input w-12 h-12 text-center text-2xl bg-slate-900 border border-slate-700 rounded-xl focus:outline-none focus:border-amber-500">
          <div>
            <label class="block text-[10px] text-slate-400 font-semibold uppercase tracking-wider mb-1">Karakter Adı</label>
            <input type="text" value="${char.name || ''}" placeholder="Karakter adı..." 
                   class="char-name-input px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-xl text-white text-xs font-bold focus:border-amber-500 focus:outline-none w-48">
          </div>
        </div>

        <div class="flex items-center space-x-3">
          <div>
            <label class="block text-[10px] text-slate-400 font-semibold uppercase tracking-wider mb-1">Rol Rengi</label>
            <input type="color" value="${char.color || '#6366f1'}" 
                   class="char-color-input w-10 h-8 rounded-lg bg-transparent border-0 cursor-pointer">
          </div>

          <button class="btn-delete-char p-2 text-red-400 hover:text-red-300 hover:bg-red-950/40 rounded-xl transition-colors ml-2" title="Karakteri Sil">
            🗑️
          </button>
        </div>
      </div>
    `).join("");

    this.dom.modals.editorCharactersContainer.querySelectorAll(".editor-char-row").forEach(row => {
      row.querySelector(".btn-delete-char")?.addEventListener("click", () => {
        const totalChars = this.dom.modals.editorCharactersContainer.querySelectorAll(".editor-char-row").length;
        if (totalChars <= 1) {
          alert("Sahnede en az 1 karakter kalmalıdır!");
          return;
        }
        row.remove();
        // Replik listesindeki dropdown'ları güncellemek için satırları yeniden oku
        this._syncCharactersFromDOM();
        this._renderTranscriptEditorLines();
      });
    });
  }

  _addEditorCharacter() {
    const newId = "char-" + Date.now();
    if (!this.selectedScene.characters) this.selectedScene.characters = [];
    this.selectedScene.characters.push({
      id: newId,
      name: `Karakter ${this.selectedScene.characters.length + 1}`,
      color: "#8b5cf6",
      avatar: "🎭"
    });
    this._renderTranscriptEditorCharacters();
    this._renderTranscriptEditorLines();
  }

  _syncCharactersFromDOM() {
    const charRows = this.dom.modals.editorCharactersContainer.querySelectorAll(".editor-char-row");
    const updated = [];
    charRows.forEach((row, idx) => {
      const id = row.dataset.id || ("char-" + (idx + 1));
      const name = row.querySelector(".char-name-input").value.trim() || `Karakter ${idx + 1}`;
      const avatar = row.querySelector(".char-avatar-input").value.trim() || "🎭";
      const color = row.querySelector(".char-color-input").value || "#6366f1";
      updated.push({ id, name, avatar, color });
    });
    this.selectedScene.characters = updated;
    return updated;
  }

  _syncLinesFromDOM() {
    if (!this.dom.modals.editorLinesContainer) return this.selectedScene?.lines || [];
    const rows = this.dom.modals.editorLinesContainer.querySelectorAll(".editor-line-row");
    if (!rows || rows.length === 0) return this.selectedScene?.lines || [];

    const updated = [];
    rows.forEach((row, i) => {
      const charSelect = row.querySelector(".line-char-select");
      const charVal = charSelect ? charSelect.value : "";
      const isMusic = charVal === "__music__" || row.dataset.type === "music";
      const startInput = row.querySelector(".line-start-input");
      const endInput = row.querySelector(".line-end-input");
      const textInput = row.querySelector(".line-text-input");
      const emotionInput = row.querySelector(".line-emotion-input");

      let startTime = startInput ? (parseFloat(startInput.value) || 0) : 0;
      let endTime = endInput ? (parseFloat(endInput.value) || (startTime + 2)) : (startTime + 2);
      if (startTime < 0) startTime = 0;
      if (endTime <= startTime) {
        if (endTime > 0 && endTime < startTime) {
          const tmp = startTime;
          startTime = endTime;
          endTime = tmp;
        } else {
          endTime = startTime + 2.0;
        }
      }
      const text = textInput ? textInput.value : "";
      const emotion = emotionInput ? emotionInput.value : "";

      if (isMusic) {
        updated.push({
          id: i + 1,
          type: "music",
          isMusic: true,
          characterId: null,
          startTime: startTime,
          endTime: endTime,
          text: text || "🎵 [Fon Müziği / Edit]",
          emotion: emotion || "Kayıt Kilitli"
        });
      } else {
        updated.push({
          id: i + 1,
          characterId: charVal,
          startTime: startTime,
          endTime: endTime,
          text: text,
          emotion: emotion
        });
      }
    });

    if (this.selectedScene) {
      this.selectedScene.lines = updated;
    }
    return updated;
  }

  _addTranscriptLine() {
    // 1. ÖNCE EKRANDA YAZILI OLAN TÜM REPLİKLERİ VE SÜRELERİ KORU
    this._syncLinesFromDOM();

    const characters = this.selectedScene.characters || [];
    const defaultChar = characters[0] ? characters[0].id : "";
    const lines = this.selectedScene.lines || [];
    const lastLine = lines[lines.length - 1];
    const newStart = lastLine ? (lastLine.endTime + 0.5).toFixed(1) : "0.0";
    const newEnd = (parseFloat(newStart) + 3.0).toFixed(1);

    lines.push({
      id: Date.now(),
      characterId: defaultChar,
      startTime: parseFloat(newStart),
      endTime: parseFloat(newEnd),
      text: "Yeni replik metni",
      emotion: "Doğal ton"
    });
    this._renderTranscriptEditorLines();

    // Yeni eklenen repliğe otomatik odaklan ve kaydır
    setTimeout(() => {
      if (this.dom.modals.editorLinesContainer) {
        this.dom.modals.editorLinesContainer.scrollTop = this.dom.modals.editorLinesContainer.scrollHeight;
        const lastInput = this.dom.modals.editorLinesContainer.querySelector(".editor-line-row:last-child .line-text-input");
        if (lastInput) {
          lastInput.focus();
          lastInput.select();
        }
      }
    }, 50);
  }

  _addMusicLockLine() {
    // 1. ÖNCE EKRANDA YAZILI OLAN TÜM REPLİKLERİ VE SÜRELERİ KORU
    this._syncLinesFromDOM();

    const lines = this.selectedScene.lines || [];
    const lastLine = lines[lines.length - 1];
    const newStart = lastLine ? (lastLine.endTime + 0.2).toFixed(1) : "0.0";
    const newEnd = (parseFloat(newStart) + 4.0).toFixed(1);

    lines.push({
      id: Date.now(),
      type: "music",
      isMusic: true,
      characterId: null,
      startTime: parseFloat(newStart),
      endTime: parseFloat(newEnd),
      text: "🎵 [Fon Müziği / Edit — Mikrofon Kilitli]",
      emotion: "Müzik / Edit"
    });
    this._renderTranscriptEditorLines();

    setTimeout(() => {
      if (this.dom.modals.editorLinesContainer) {
        this.dom.modals.editorLinesContainer.scrollTop = this.dom.modals.editorLinesContainer.scrollHeight;
      }
    }, 50);
  }

  _saveTranscriptEditor() {
    // 1. Karakterleri kaydet
    const updatedCharacters = this._syncCharactersFromDOM();

    // 2. Replikleri topla (Kullanıcının belirlediği DOM sırasına göre!)
    const updatedLines = this._syncLinesFromDOM();

    this.selectedScene.characters = updatedCharacters;
    this.selectedScene.lines = updatedLines;

    // Lobi rol listesini anında yenile
    this._updateRolesUI();

    // Eğer P2P aktifse tüm odaya senkronize et
    if (this.network) {
      this.network.broadcastUpdatedLines(this.selectedScene.id, updatedLines);
      if (this.network.broadcastUpdatedCharacters) {
        this.network.broadcastUpdatedCharacters(this.selectedScene.id, updatedCharacters);
      }
    }

    this._closeTranscriptEditor();
    alert("✅ Karakterler ve transkript başarıyla güncellendi ve odaya dağıtıldı!");
  }

  // --- ADMİN: SAHNEYİ VE VİDEOYU PROJEYE KALICI OLARAK KAYDET (DİSKE YAZ) ---
  async _savePermanentSceneToDisk() {
    if (!this.selectedScene) return;

    // 1. DOM'daki en güncel karakter ve replik bilgilerini senkronize et
    const updatedCharacters = this._syncCharactersFromDOM();
    const updatedLines = this._syncLinesFromDOM();

    this.selectedScene.characters = updatedCharacters;
    this.selectedScene.lines = updatedLines;

    const btn = this.dom.modals.editorSavePermanentBtn;
    const oldHtml = btn ? btn.innerHTML : "";
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = `<span>⏳</span><span>Klasöre Kaydediliyor...</span>`;
    }

    try {
      let videoBase64 = null;
      const isCustomBlob = this.selectedScene.videoSrc && (
        this.selectedScene.videoSrc.startsWith("blob:") || 
        this.selectedScene.videoSrc.startsWith("data:")
      );

      // Eğer özel yüklenmiş video ise (blob/data URL) Base64'e çevir
      if (isCustomBlob) {
        const response = await fetch(this.selectedScene.videoSrc);
        const blob = await response.blob();
        videoBase64 = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result);
          reader.onerror = reject;
          reader.readAsDataURL(blob);
        });
      }

      // Sahne payload'u hazırla
      const payload = {
        password: "dubSex",
        scene: {
          id: this.selectedScene.id,
          title: this.selectedScene.title,
          category: this.selectedScene.category || "ozel",
          categoryName: this.selectedScene.categoryName || "Özel Sahneler",
          duration: parseFloat(this.selectedScene.duration) || 30.0,
          videoSrc: this.selectedScene.videoSrc,
          difficulty: this.selectedScene.difficulty || "Orta",
          description: this.selectedScene.description || "Admin tarafından eklenen sahne.",
          characters: updatedCharacters,
          lines: updatedLines
        },
        videoBase64: videoBase64
      };

      // Python yerel sunucusuna (/api/save-permanent-scene) POST et
      const res = await fetch("/api/save-permanent-scene", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error(`Sunucu yanıt kodu: HTTP ${res.status}`);
      }

      const result = await res.json();
      if (result.success) {
        if (result.scene && result.scene.videoSrc) {
          this.selectedScene.videoSrc = result.scene.videoSrc;
        }

        // Yerel SCENES dizisini de güncelle veya ekle
        const existIdx = SCENES.findIndex(s => s.id === this.selectedScene.id);
        if (existIdx >= 0) {
          SCENES[existIdx] = { ...this.selectedScene };
        } else {
          SCENES.push({ ...this.selectedScene });
        }

        // Lobi listesini ve rollerini güncelle
        this._updateRolesUI();
        this._renderScenes();
        this._renderHomeFeatured();

        // Eğer P2P varsa odaya da dağıt
        if (this.network) {
          this.network.broadcastUpdatedLines(this.selectedScene.id, updatedLines);
          if (this.network.broadcastUpdatedCharacters) {
            this.network.broadcastUpdatedCharacters(this.selectedScene.id, updatedCharacters);
          }
        }

        this._closeTranscriptEditor();
        alert("🎉 TEBRİKLER!\n\nBu sahne ve videosu doğrudan projenin kalıcı klasörüne (`assets/videos/` ve `scenes.js`) kaydedildi!\n\nArtık bu proje klasörünü arkadaşlarına zipleyip attığında, sahne sende olduğu gibi onlarda da kalıcı olarak yer alacak ve sorunsuzca oynanabilecektir!");
      } else {
        alert("❌ Hata: " + (result.error || "Bilinmeyen sunucu hatası."));
      }

    } catch (err) {
      console.error("Kalıcı kaydetme hatası:", err);
      alert("⚠️ Kalıcı Kaydetme Bilgisi:\n\nProjeye kalıcı olarak kaydedebilmek için yerel Python sunucusunun açık olması gerekir (start.bat ile başlatılmalıdır).\n\nHata: " + err.message);
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = oldHtml;
      }
    }
  }

  _handleSceneLinesUpdated(sceneId, lines) {
    const scene = SCENES.find(s => s.id === sceneId);
    if (scene) {
      scene.lines = lines;
      console.log(`[P2P] ${scene.title} replikleri admin tarafından güncellendi.`);
    }
  }

  _handleSceneCharactersUpdated(sceneId, characters) {
    const scene = SCENES.find(s => s.id === sceneId);
    if (scene) {
      scene.characters = characters;
      if (this.selectedScene && this.selectedScene.id === sceneId) {
        this.selectedScene.characters = characters;
        this._updateRolesUI();
      }
      console.log(`[P2P] ${scene.title} karakterleri admin tarafından güncellendi.`);
    }
  }

  // --- KENDİ VİDEONU YÜKLE (CUSTOM SCENE) ---
  _openUploadModal() {
    this.dom.modals.upload?.classList.remove("hidden");
    if (this.dom.modals.uploadTitle) this.dom.modals.uploadTitle.value = "";
    if (this.dom.modals.uploadFileInput) this.dom.modals.uploadFileInput.value = "";
    this.dom.modals.uploadPreviewWrapper?.classList.add("hidden");
    this.uploadedCustomVideoData = null;
  }

  _handleCustomVideoSelection(file) {
    if (!file) return;
    const objectUrl = URL.createObjectURL(file);
    const preview = this.dom.modals.uploadPreviewVideo;
    if (preview) preview.src = objectUrl;
    this.dom.modals.uploadPreviewWrapper?.classList.remove("hidden");

    const submitBtn = document.getElementById("btn-upload-submit");
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `<span>⏳</span><span>Video Hazırlanıyor...</span>`;
      submitBtn.classList.add("opacity-75", "cursor-not-allowed");
    }

    // Dosyayı Base64'e dönüştür (P2P senkron için)
    const reader = new FileReader();
    reader.onload = (e) => {
      this.uploadedCustomVideoData = {
        name: file.name,
        size: file.size,
        base64: e.target.result,
        objectUrl: objectUrl
      };
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<span>🚀</span><span>Odaya Yükle ve Dağıt</span>`;
        submitBtn.classList.remove("opacity-75", "cursor-not-allowed");
      }
    };
    reader.onerror = () => {
      alert("Video dosyası okunamadı!");
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<span>🚀</span><span>Odaya Yükle ve Dağıt</span>`;
        submitBtn.classList.remove("opacity-75", "cursor-not-allowed");
      }
    };
    reader.readAsDataURL(file);

    if (this.dom.modals.uploadTitle && !this.dom.modals.uploadTitle.value) {
      this.dom.modals.uploadTitle.value = file.name.replace(/\.[^/.]+$/, "");
    }
  }

  async _submitCustomVideo() {
    if (!this.uploadedCustomVideoData) {
      alert("Lütfen bir video dosyası seçin veya dosyanın hazırlanmasını bekleyin!");
      return;
    }

    const title = this.dom.modals.uploadTitle.value.trim() || "Özel Video";
    const category = this.dom.modals.uploadCategory.value || "ozel";
    const duration = Math.ceil(this.dom.modals.uploadPreviewVideo?.duration || 15);

    // Karakterleri al
    const charInputs = this.dom.modals.upload.querySelectorAll(".custom-char-name");
    const colorInputs = this.dom.modals.upload.querySelectorAll(".custom-char-color");
    const characters = [];

    charInputs.forEach((input, idx) => {
      const name = input.value.trim() || `Karakter ${idx + 1}`;
      const color = colorInputs[idx] ? colorInputs[idx].value : "#6366f1";
      characters.push({
        id: "char-" + (idx + 1),
        name: name,
        color: color,
        avatar: idx === 0 ? "🎙️" : "🎬"
      });
    });

    const newScene = {
      id: "custom-" + Date.now(),
      title: title,
      category: category,
      categoryName: "Özel Video",
      duration: duration,
      videoSrc: this.uploadedCustomVideoData.objectUrl,
      videoData: this.uploadedCustomVideoData.base64,
      difficulty: "Özel",
      description: "Lobi tarafından yüklenen özel sahne.",
      characters: characters,
      lines: [
        {
          id: 1,
          characterId: characters[0].id,
          startTime: 0.0,
          endTime: Math.min(5.0, duration),
          text: "Senin repliğin! Mikrofon sende.",
          emotion: "Doğal"
        }
      ]
    };

    const existingIndex = SCENES.findIndex(s => s.id === newScene.id || (s.title === newScene.title && s.duration === newScene.duration));
    if (existingIndex !== -1) {
      SCENES[existingIndex] = newScene;
    } else {
      SCENES.push(newScene);
    }
    this.selectedScene = newScene;

    this.currentCategory = "ozel";
    this._renderCategories();
    this._renderScenes("ozel");
    this._updateRolesUI();
    this.dom.modals.upload?.classList.add("hidden");

    // P2P ile odadaki herkese dağıt (WebRTC chunk stream)
    if (this.network) {
      this._showSyncProgress(newScene.title, false, 0, false);
      await this.network.broadcastCustomScene(newScene);
    }
  }

  _handleNewCustomScene(sceneData) {
    const existingIndex = SCENES.findIndex(s => s.id === sceneData.id);
    if (existingIndex !== -1) {
      if (sceneData.videoData && !SCENES[existingIndex].videoSrc) {
        fetch(sceneData.videoData)
          .then(res => res.blob())
          .then(blob => {
            SCENES[existingIndex].videoSrc = URL.createObjectURL(blob);
            SCENES[existingIndex].videoData = sceneData.videoData;
            this._renderCategories();
            this._renderScenes();
            this._showSyncProgress(sceneData.title, true, 100, true);
          });
      }
      return;
    }

    if (sceneData.videoData) {
      fetch(sceneData.videoData)
        .then(res => res.blob())
        .then(blob => {
          sceneData.videoSrc = URL.createObjectURL(blob);
          SCENES.push(sceneData);
          this.selectedScene = sceneData;
          this.currentCategory = "ozel";
          this._renderCategories();
          this._renderScenes("ozel");
          this._updateRolesUI();
          this._showSyncProgress(sceneData.title, true, 100, true);
        })
        .catch(err => {
          console.error("Özel video blob çevirme hatası:", err);
          SCENES.push(sceneData);
          this._renderCategories();
          this._renderScenes();
        });
    } else {
      SCENES.push(sceneData);
      this._renderCategories();
      this._renderScenes();
    }
  }

  _showSyncProgress(title, isCompleted = false, percent = null, isReceiving = false) {
    const bar = this.dom.lobby.syncBar;
    const progressEl = this.dom.lobby.syncProgress;
    const titleEl = this.dom.lobby.syncTitle;
    if (!bar) return;

    bar.classList.remove("hidden");
    const actionText = isReceiving ? "indiriliyor ve hazırlanıyor" : "odadaki oyunculara aktarılıyor";
    if (titleEl) titleEl.innerText = `🎬 ${title} ${actionText}...`;

    if (percent !== null) {
      if (progressEl) progressEl.innerText = `%${percent}`;
    }

    if (isCompleted || (percent !== null && percent >= 100)) {
      if (titleEl) titleEl.innerText = `✅ ${title} hazır!`;
      if (progressEl) progressEl.innerText = `%100`;
      setTimeout(() => {
        bar.classList.add("hidden");
      }, 2500);
    }
  }

  // --- STÜDYO EKRANI ---
  async _startStudioScreen(sceneId, assignedRole) {
    const scene = SCENES.find(s => s.id === sceneId) || this.selectedScene;
    this._switchScreen("studio");

    const isSpectator = assignedRole === "spectator";
    const char = (scene.characters || []).find(c => c.id === assignedRole);
    this.dom.studio.roleBadge.innerHTML = isSpectator
      ? `<span class="text-amber-300 font-black flex items-center space-x-1.5"><span class="text-sm">🍿</span><span class="tracking-wide">Seyirci Koltuğu</span><span class="text-[10px] uppercase font-extrabold tracking-wider px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 ml-1">Canlı İzleyici</span></span>`
      : (char 
        ? `<span class="text-white font-black flex items-center space-x-1.5"><span class="text-sm">${char.avatar}</span><span class="tracking-wide">${char.name}</span><span class="text-[10px] uppercase font-extrabold tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 ml-1">Senin Rolün</span></span>`
        : `<span class="text-slate-400">Rol seçilmedi</span>`);

    // Butonları ve bekleme kutularını sıfırla
    this.dom.studio.actionButtons?.classList.add("hidden");
    this.dom.studio.premiereReadyBox?.classList.add("hidden");
    this.dom.studio.hostLaunchPremiereBtn?.classList.add("hidden");
    this.dom.studio.clientWaitingMsg?.classList.add("hidden");

    // Mikrofonu stüdyo açılır açılmaz anında hazırla (seyirciler hariç)
    if (!isSpectator) {
      if (!this.studio.microphoneStream) {
        this.studio.initAudio(this.selectedMicDeviceId).catch((err) => {
          console.warn("Mikrofon otomatik açılamadı:", err);
        });
      } else if (this.studio.audioContext && this.studio.audioContext.state === "suspended") {
        this.studio.audioContext.resume().catch(() => {});
      }
    }

    this.studio.loadScene(scene, assignedRole);

    // Önce İZLEME fazı başlar
    this._showCountdownOverlay(() => {
      this.studio.startPreview();
    }, "Sahneyi İzle ve Replikleri Öğren!");
  }

  _playBeep(freq = 520, duration = 0.12, type = "sine") {
    try {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return;
      if (!this._beepCtx) {
        this._beepCtx = new AudioContextClass();
      }
      if (this._beepCtx.state === "suspended") {
        this._beepCtx.resume();
      }
      const osc = this._beepCtx.createOscillator();
      const gain = this._beepCtx.createGain();
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this._beepCtx.currentTime);
      gain.gain.setValueAtTime(0.18, this._beepCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this._beepCtx.currentTime + duration);
      osc.connect(gain);
      gain.connect(this._beepCtx.destination);
      osc.start();
      osc.stop(this._beepCtx.currentTime + duration);
    } catch (e) {}
  }

  _showCountdownOverlay(callback) {
    const overlay = document.createElement("div");
    overlay.className = "fixed inset-0 z-50 flex flex-col items-center justify-center bg-black/90 backdrop-blur-md";
    overlay.innerHTML = `
      <div class="text-center">
        <h3 id="countdown-title" class="text-2xl font-black text-slate-300 uppercase tracking-widest mb-4">HAZIRLAN</h3>
        <div id="countdown-number" class="text-8xl sm:text-9xl font-black bg-gradient-to-br from-indigo-400 to-pink-500 bg-clip-text text-transparent animate-bounce">
          3
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    let count = 3;
    const numEl = overlay.querySelector("#countdown-number");
    const titleEl = overlay.querySelector("#countdown-title");

    // İlk '3' bipi
    this._playBeep(520, 0.12, "sine");

    const interval = setInterval(() => {
      count--;
      if (count > 0) {
        if (numEl) numEl.innerText = count;
        this._playBeep(520, 0.12, "sine");
      } else if (count === 0) {
        if (titleEl) titleEl.innerText = "KAYIT";
        if (numEl) {
          numEl.innerText = "BAŞLA!";
          numEl.className = "text-6xl sm:text-8xl font-black text-emerald-400 animate-pulse";
        }
        this._playBeep(920, 0.25, "triangle");
      } else {
        clearInterval(interval);
        overlay.remove();
        callback();
      }
    }, 1000);
  }

  _updatePhaseUI(phase) {
    const badge = this.dom.studio.phaseBadge;
    const actionBtns = this.dom.studio.actionButtons;
    const skipBtn = this.dom.studio.skipPreviewBtn;
    const videoContainer = this.dom.studio.container || document.getElementById("studio-video-container");

    if (videoContainer) {
      if (phase === "recording") {
        videoContainer.classList.add("recording-on-air");
        videoContainer.classList.remove("border-slate-800", "border-purple-500");
      } else if (phase === "rehearsal") {
        videoContainer.classList.remove("recording-on-air", "border-slate-800");
        videoContainer.classList.add("border-purple-500");
      } else {
        videoContainer.classList.remove("recording-on-air", "border-purple-500");
        videoContainer.classList.add("border-slate-800");
      }
    }

    if (!badge) return;

    if (skipBtn) {
      if (phase === "preview") {
        skipBtn.classList.remove("hidden");
      } else {
        skipBtn.classList.add("hidden");
      }
    }

    switch (phase) {
      case "preview":
        badge.className = "inline-flex items-center px-4 py-2 rounded-full text-sm font-bold border border-blue-500 bg-blue-950/60 text-blue-300";
        badge.innerHTML = `<span class="w-2 h-2 rounded-full mr-2 bg-blue-400 animate-pulse"></span><span>👁️ Faz 1: İzleme — Sahneyi Oku</span>`;
        actionBtns?.classList.add("hidden");
        break;

      case "rehearsal":
        badge.className = "inline-flex items-center px-4 py-2 rounded-full text-sm font-bold border border-purple-500 bg-purple-950/60 text-purple-300";
        badge.innerHTML = `<span class="w-2 h-2 rounded-full mr-2 bg-purple-400 animate-pulse"></span><span>🎯 Faz: Rol Provası — Kendi Repliklerini Dinle</span>`;
        actionBtns?.classList.add("hidden");
        break;

      case "ready":
        badge.className = "inline-flex items-center px-4 py-2 rounded-full text-sm font-bold border-2 border-emerald-400 bg-emerald-950/60 text-emerald-300 animate-pulse";
        badge.innerHTML = `<span class="w-2 h-2 rounded-full mr-2 bg-emerald-400"></span><span>✅ Hazır — Prova Yap veya Dublaja Geç!</span>`;
        actionBtns?.classList.remove("hidden");
        break;

      case "recording":
        badge.className = "inline-flex items-center px-4 py-2 rounded-full text-sm font-bold border border-red-500 bg-red-950/60 text-red-300";
        badge.innerHTML = `<span class="w-3 h-3 rounded-full mr-2 bg-red-500 animate-ping"></span><span>🔴 Faz 2: Kayıt — Şimdi Dubla!</span>`;
        actionBtns?.classList.add("hidden");
        break;

      case "idle":
      default:
        badge.className = "inline-flex items-center px-4 py-2 rounded-full text-sm font-bold border border-slate-700 bg-slate-900/60 text-slate-400";
        badge.innerHTML = `<span class="w-2 h-2 rounded-full mr-2 bg-slate-500"></span><span>⏸️ Bekleniyor</span>`;
        break;
    }
  }

  _handleReRecord() {
    if (!this.studio) return;
    this.studio.resetRecording();
    this.dom.studio.premiereReadyBox?.classList.add("hidden");
    this.dom.studio.actionButtons?.classList.remove("hidden");
    if (this.dom.studio.roleTurnBanner) {
      this.dom.studio.roleTurnBanner.className = "hidden";
      this.dom.studio.roleTurnBanner.innerHTML = "";
    }
    this._showNotification("Önceki kaydın temizlendi. Dublaj butonları tekrar hazır!", "info");
  }

  // --- YALNIZCA HOST/ADMİN PRÖMİYER YETKİSİ VE BEKLEME EKRANI ---
  _updateStudioPremiereState(state) {
    if (!state) return;
    const readyBox = this.dom.studio.premiereReadyBox;
    const statusText = this.dom.studio.recordingsStatusText;
    const launchBtn = this.dom.studio.hostLaunchPremiereBtn;
    const clientWaitingMsg = this.dom.studio.clientWaitingMsg;

    if (!readyBox || readyBox.classList.contains("hidden")) return;

    const isHostOrAdmin = this.network && (this.network.isHost || this.network.isAdmin);
    const { current, total } = state.allRecordingsCount || { current: 0, total: 0 };

    if (state.recordingsReady) {
      if (statusText) statusText.innerText = "🎉 Tüm oyuncuların sesleri tamamlandı!";
      if (isHostOrAdmin) {
        launchBtn?.classList.remove("hidden");
        clientWaitingMsg?.classList.add("hidden");
      } else {
        launchBtn?.classList.add("hidden");
        clientWaitingMsg?.classList.remove("hidden");
      }
    } else {
      if (statusText) statusText.innerText = `⏳ Sesin kaydedildi! Diğer oyuncular bekleniyor (${current}/${total})...`;
      launchBtn?.classList.add("hidden");
      clientWaitingMsg?.classList.add("hidden");
    }
  }

  async _startPremiereScreen(audioTracks) {
    this._switchScreen("premiere");
    this._renderPremiereCharacterFaders();
    await this.mixer.preparePremiere(this.selectedScene, audioTracks);
    // Varsayılan video fon sesi seviyesini miksere senkronla
    const defaultVidVol = this.dom.premiere.videoVolume ? parseInt(this.dom.premiere.videoVolume.value, 10) : 70;
    this.mixer.setVideoVolume(defaultVidVol);
    this.mixer.play();
  }

  _renderPremiereCharacterFaders() {
    const container = this.dom.premiere.characterVolumes;
    if (!container || !this.selectedScene) return;
    const characters = this.selectedScene.characters || [];

    container.innerHTML = characters.map(char => `
      <div class="bg-slate-950/60 border border-slate-800/80 rounded-xl p-2.5 flex items-center justify-between" data-char="${char.id}">
        <div class="flex items-center space-x-2">
          <span class="text-sm">${char.avatar || "🎭"}</span>
          <div>
            <div class="font-bold text-xs text-slate-200">${char.name}</div>
            <div class="text-[10px] text-indigo-400 font-medium">Dublaj Parçası</div>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <!-- Mute & Solo Butonları -->
          <button class="btn-char-mute px-2 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px] font-bold transition-colors" data-char="${char.id}" title="Sustur (Mute)">M</button>
          <button class="btn-char-solo px-2 py-0.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px] font-bold transition-colors" data-char="${char.id}" title="Tek Başına Dinle (Solo)">S</button>
          <input type="range" min="0" max="150" value="100" class="char-vol-slider w-20 accent-indigo-500 cursor-pointer" data-char="${char.id}">
          <span class="char-vol-val font-mono text-indigo-300 font-bold text-xs w-8 text-right">%100</span>
        </div>
      </div>
    `).join("");

    container.querySelectorAll(".char-vol-slider").forEach(slider => {
      slider.addEventListener("input", (e) => {
        const charId = e.target.dataset.char;
        const val = parseInt(e.target.value, 10);
        const valSpan = e.target.parentElement.querySelector(".char-vol-val");
        if (valSpan) valSpan.innerText = `%${val}`;
        this.mixer.setCharacterVolume(charId, val);
      });
    });

    container.querySelectorAll(".btn-char-mute").forEach(btn => {
      btn.addEventListener("click", () => {
        const charId = btn.dataset.char;
        const isMuted = this.mixer.toggleMute(charId);
        btn.classList.toggle("bg-red-900", isMuted);
        btn.classList.toggle("text-red-200", isMuted);
      });
    });

    container.querySelectorAll(".btn-char-solo").forEach(btn => {
      btn.addEventListener("click", () => {
        const charId = btn.dataset.char;
        const isSolo = this.mixer.toggleSolo(charId);
        container.querySelectorAll(".btn-char-solo").forEach(b => {
          b.classList.remove("bg-amber-600", "text-black");
        });
        if (isSolo) {
          btn.classList.add("bg-amber-600", "text-black");
        }
      });
    });
  }

  _spawnFloatingEmoji(emoji) {
    const el = document.createElement("div");
    el.innerText = emoji;
    el.className = "fixed bottom-24 pointer-events-none text-4xl animate-float-up z-50";
    el.style.left = (20 + Math.random() * 60) + "%";
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2500);
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const app = new DublajApp();
  app.init();
});
