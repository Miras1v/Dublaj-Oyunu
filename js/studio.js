// Dublaj Oyunu - İki Fazlı Stüdyo Motoru
// Faz 1 (İzleme): Video orijinal sesiyle oynar, kullanıcı izler
// Faz 2 (Dublaj): Video sessiz tekrar oynar, kullanıcı mikrofona konuşur

export class StudioEngine {
  constructor(options = {}) {
    this.videoElement = options.videoElement; // <video id="studio-video">
    this.transcriptBar = options.transcriptBar;
    this.transcriptSpeaker = options.transcriptSpeaker;
    this.transcriptText = options.transcriptText;
    this.transcriptTiming = options.transcriptTiming;
    this.transcriptInstruction = options.transcriptInstruction;
    this.roleTurnBanner = options.roleTurnBanner;
    this.vuMeterElement = options.vuMeterElement;
    this.karaokeProgressBar = options.karaokeProgressBar || (typeof document !== "undefined" ? document.getElementById("karaoke-progress-bar") : null);
    this.trafficLightBadge = options.trafficLightBadge || (typeof document !== "undefined" ? document.getElementById("transcript-traffic-light") : null);
    this.waveformCanvas = options.waveformCanvas || (typeof document !== "undefined" ? document.getElementById("studio-waveform-canvas") : null);
    this.signalDisplay = options.signalDisplay || (typeof document !== "undefined" ? document.getElementById("studio-db-display") : null);
    this.micStatusTag = options.micStatusTag || (typeof document !== "undefined" ? document.getElementById("studio-mic-status-tag") : null);

    this.currentScene = null;
    this.assignedRole = null;

    this.audioContext = null;
    this.mediaRecorder = null;
    this.recordedChunks = [];
    this.analyser = null;
    this.microphoneStream = null;
    this.micGainNode = null;
    this.micSourceNode = null;
    this.micDestination = null;
    this.currentDeviceId = null;
    this._pcmChunks = [];
    this._pcmScriptNode = null;
    this.micError = null;

    // Bireysel Ses Seviyeleri ve Müzik Kilidi
    this.micVolume = 1.0;
    this.videoVolume = 1.0;
    this.isMusicLocked = false;

    this.isPlaying = false;
    this.isRecording = false;
    this.currentTime = 0;

    // İki Fazlı Durum Makinesi
    this.phase = "idle"; // "idle" | "preview" | "rehearsal" | "recording" | "ready"

    this.roleCueIntervals = [];
    this.roleSegments = [];
    this.currentSegmentIndex = 0;
    this.segmentTimingLog = [];
    this.recordingStartTime = 0;
    this.currentSegMeta = null;
    this.isRoleSpeakingNow = false;

    this.onComplete = options.onComplete || (() => {});
    this.onTimeUpdate = options.onTimeUpdate || (() => {});
    this.onPhaseChange = options.onPhaseChange || (() => {});
  }

  // Bireysel Ses Ayarları
  setMicVolume(volumePercent) {
    this.micVolume = Math.max(0, Math.min(1.0, volumePercent / 100));
    if (this.micGainNode && this.audioContext && !this.isMusicLocked) {
      this.micGainNode.gain.setValueAtTime(this.micVolume, this.audioContext.currentTime);
    }
  }

  setVideoVolume(volumePercent) {
    this.videoVolume = Math.max(0, Math.min(1.0, volumePercent / 100));
    if (this.videoElement) {
      this.videoElement.volume = this.videoVolume;
      this.videoElement.muted = (this.videoVolume === 0);
    }
  }

  // 1. Mikrofon İzni ve AudioContext Başlatma (Cihaz Seçimi ve Donanımsal Bağlantı)
  async initAudio(deviceId = null) {
    try {
      if (deviceId) {
        this.currentDeviceId = deviceId;
      }

      if (this.microphoneStream) {
        if (!deviceId && this.microphoneStream.active) {
          if (this.audioContext && this.audioContext.state === "suspended") {
            await this.audioContext.resume().catch(() => {});
          }
          return true;
        }
        try {
          this.microphoneStream.getTracks().forEach(t => t.stop());
        } catch (e) {}
      }

      const audioConstraints = {
        echoCancellation: true,
        noiseSuppression: true,
        autoGainControl: true
      };
      if (this.currentDeviceId) {
        audioConstraints.deviceId = { exact: this.currentDeviceId };
      }

      this.microphoneStream = await navigator.mediaDevices.getUserMedia({
        audio: audioConstraints
      });

      if (!this.audioContext || this.audioContext.state === "closed") {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (this.audioContext.state === "suspended") {
        await this.audioContext.resume().catch(() => {});
      }

      if (this.micSourceNode) {
        try { this.micSourceNode.disconnect(); } catch (e) {}
      }
      this.micSourceNode = this.audioContext.createMediaStreamSource(this.microphoneStream);

      if (!this.micGainNode) {
        this.micGainNode = this.audioContext.createGain();
      }
      this.micGainNode.gain.value = this.micVolume;
      this.micSourceNode.connect(this.micGainNode);

      if (!this.analyser) {
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 256;
      }
      this.micGainNode.connect(this.analyser);

      // Web Audio Destination (MediaRecorder ve diğerleri için)
      this.micDestination = this.audioContext.createMediaStreamDestination();
      this.micGainNode.connect(this.micDestination);

      // PCM doğrudan ses kaydedici (ScriptProcessorNode)
      this._initPcmRecorder();

      this._startVUMeter();
      this.micError = null;

      const tagEl = this.micStatusTag || (typeof document !== "undefined" ? document.getElementById("studio-mic-status-tag") : null);
      if (tagEl) {
        tagEl.innerText = "AKTİF";
        tagEl.className = "px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 cursor-pointer";
        tagEl.title = "Mikrofon aktif ve ses algılıyor. Yenilemek için tıkla";
        tagEl.onclick = () => this.initAudio(this.currentDeviceId);
      }

      return true;
    } catch (err) {
      console.error("Mikrofon izni alınamadı:", err);
      this.micError = err.message || "İzin verilmedi";
      const tagEl = this.micStatusTag || (typeof document !== "undefined" ? document.getElementById("studio-mic-status-tag") : null);
      if (tagEl) {
        tagEl.innerText = "⚠️ İZİN VER (TIKLA)";
        tagEl.className = "px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-red-500/20 text-red-400 border border-red-500/40 cursor-pointer animate-pulse";
        tagEl.title = "Mikrofon izni reddedildi veya bulunamadı! İzin vermek için tıkla.";
        tagEl.onclick = async () => {
          try {
            await this.initAudio(this.currentDeviceId);
          } catch (e) {
            alert("Tarayıcınızın adres çubuğundaki kilit/izin simgesinden mikrofon erişimine izin verin!");
          }
        };
      }
      const signalEl = this.signalDisplay || (typeof document !== "undefined" ? document.getElementById("studio-db-display") : null);
      if (signalEl) {
        signalEl.innerText = "MİKROFON YOK";
        signalEl.className = "font-bold text-red-400";
      }
      throw new Error("Lütfen mikrofon erişimine izin verin!");
    }
  }

  // PCM doğrudan ses kaydedici (Kusursuz ses aktarımı ve yankısız yakalama)
  _initPcmRecorder() {
    if (this._pcmScriptNode) {
      try { this._pcmScriptNode.disconnect(); } catch (e) {}
    }
    if (!this.audioContext || !this.micGainNode) return;

    try {
      this._pcmScriptNode = this.audioContext.createScriptProcessor(4096, 1, 1);
      this._pcmChunks = [];

      this._pcmScriptNode.onaudioprocess = (e) => {
        // Çıktıyı hoparlöre verme (yankı/feedback olmaması için sıfırla)
        const out = e.outputBuffer.getChannelData(0);
        out.fill(0);

        if (!this.isRecording) return;

        const input = e.inputBuffer.getChannelData(0);
        const copy = new Float32Array(input.length);
        copy.set(input);
        this._pcmChunks.push(copy);
      };

      this.micGainNode.connect(this._pcmScriptNode);
      this._pcmScriptNode.connect(this.audioContext.destination);
    } catch (e) {
      console.warn("PCM ScriptProcessor başlatılamadı:", e);
    }
  }

  // Canlı Mikrofon Seviyesi & Dublaj.io Orijinal Ses Dalga Çizimi
  _startVUMeter() {
    if (!this.analyser) return;
    const bufferLength = this.analyser.frequencyBinCount;
    const freqData = new Uint8Array(bufferLength);
    const timeData = new Uint8Array(bufferLength);

    const canvas = this.waveformCanvas || (typeof document !== "undefined" ? document.getElementById("studio-waveform-canvas") : null);
    const canvasCtx = canvas ? canvas.getContext("2d") : null;

    const updateVU = () => {
      if (!this.analyser) return;
      this.analyser.getByteFrequencyData(freqData);
      this.analyser.getByteTimeDomainData(timeData);

      // 1. Ortalama seviye ve yüzde hesabı (Konuşma frekans bandı tepe & RMS enerjisi)
      let voiceSum = 0;
      let maxVal = 0;
      const voiceBins = Math.min(bufferLength, 32);
      for (let i = 0; i < voiceBins; i++) {
        voiceSum += freqData[i];
        if (freqData[i] > maxVal) maxVal = freqData[i];
      }
      const voiceAvg = voiceSum / Math.max(1, voiceBins);
      const rawPercent = Math.max((voiceAvg / 55) * 100, (maxVal / 150) * 100);
      const percent = this.isMusicLocked ? 0 : Math.min(100, Math.round(rawPercent * (this.micVolume || 1.0)));

      if (this.vuMeterElement) {
        this.vuMeterElement.style.width = percent + "%";
        if (this.phase === "recording" && this.isRoleSpeakingNow) {
          this.vuMeterElement.style.backgroundColor = "#10b981";
        } else if (this.phase === "recording") {
          this.vuMeterElement.style.backgroundColor = "#ef4444";
        } else {
          this.vuMeterElement.style.backgroundColor = percent > 5 ? "#38bdf8" : "#475569";
        }
      }

      // Sinyal Göstergesi (% SİNYAL)
      const signalEl = this.signalDisplay || (typeof document !== "undefined" ? document.getElementById("studio-db-display") : null);
      if (signalEl) {
        signalEl.innerText = `%${percent} SİNYAL`;
        signalEl.className = percent > 15 ? "font-bold text-emerald-400" : (percent > 0 ? "font-bold text-slate-300" : "font-bold text-slate-500");
      }

      // Mikrofon Durum Rozeti
      const tagEl = this.micStatusTag || (typeof document !== "undefined" ? document.getElementById("studio-mic-status-tag") : null);
      if (tagEl) {
        if (this.isMusicLocked) {
          tagEl.innerText = "🔒 SUSTURULDU";
          tagEl.className = "px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-amber-500/20 text-amber-300 border border-amber-500/40";
        } else if (this.phase === "recording") {
          tagEl.innerText = "🔴 KAYITTA";
          tagEl.className = "px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-red-500/20 text-red-400 border border-red-500/40 animate-pulse";
        } else {
          tagEl.innerText = "AKTİF";
          tagEl.className = "px-2 py-0.5 rounded text-[10px] font-extrabold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 cursor-pointer";
        }
      }

      // 2. Dublaj.io Orijinal Canlı Ses Dalgası (Canvas Waveform) Çizimi
      if (canvas && canvasCtx) {
        const width = canvas.width;
        const height = canvas.height;

        canvasCtx.clearRect(0, 0, width, height);

        // Koyu Stüdyo Arka Planı
        canvasCtx.fillStyle = "#020617";
        canvasCtx.fillRect(0, 0, width, height);

        // Frekans Spektrum Çubukları (Equalizer Bars)
        const barWidth = (width / bufferLength) * 1.5;
        let barX = 0;

        for (let i = 0; i < bufferLength; i++) {
          const barHeight = this.isMusicLocked 
            ? 0 
            : Math.min(height, (freqData[i] / 150) * height * 1.3 * (this.micVolume || 1.0));
          let barGrad = canvasCtx.createLinearGradient(0, height, 0, 0);

          if (this.phase === "recording" && this.isRoleSpeakingNow) {
            barGrad.addColorStop(0, "rgba(16, 185, 129, 0.2)");
            barGrad.addColorStop(0.7, "rgba(52, 211, 153, 0.8)");
            barGrad.addColorStop(1, "rgba(251, 191, 36, 0.95)");
          } else if (this.phase === "recording") {
            barGrad.addColorStop(0, "rgba(239, 68, 68, 0.15)");
            barGrad.addColorStop(0.7, "rgba(239, 68, 68, 0.7)");
            barGrad.addColorStop(1, "rgba(244, 63, 94, 0.9)");
          } else {
            barGrad.addColorStop(0, "rgba(59, 130, 246, 0.15)");
            barGrad.addColorStop(0.7, "rgba(96, 165, 250, 0.65)");
            barGrad.addColorStop(1, "rgba(168, 85, 247, 0.85)");
          }

          canvasCtx.fillStyle = barGrad;
          canvasCtx.fillRect(barX, height - barHeight, barWidth - 1, barHeight);
          barX += barWidth;
        }

        // Canlı Zaman Alanı Dalga Eğrisi (Oscilloscope Waveform)
        canvasCtx.lineWidth = 2;
        canvasCtx.strokeStyle = this.phase === "recording" && this.isRoleSpeakingNow
          ? "#34d399"
          : (this.phase === "recording" ? "#ef4444" : (percent > 8 ? "#38bdf8" : "#334155"));

        canvasCtx.beginPath();
        const sliceWidth = width / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
          const deviation = (timeData[i] - 128) / 128.0;
          const amp = this.isMusicLocked ? 0 : Math.max(-1, Math.min(1, deviation * 4.5 * (this.micVolume || 1.0)));
          const y = (height / 2) + (amp * (height / 2) * 0.85);

          if (i === 0) {
            canvasCtx.moveTo(x, y);
          } else {
            canvasCtx.lineTo(x, y);
          }
          x += sliceWidth;
        }
        canvasCtx.stroke();
      }

      requestAnimationFrame(updateVU);
    };
    updateVU();
  }

  // 2. Sahneyi ve Gerçek Videoyu Yükle
  loadScene(scene, assignedRole) {
    this.currentScene = scene;
    this.assignedRole = assignedRole;
    this.currentTime = 0;
    this.isPlaying = false;
    this.isRecording = false;
    this.phase = "idle";

    // Kullanıcının replik aralıklarını çıkar
    const lines = this.currentScene.lines || [];
    this.roleCueIntervals = lines
      .filter(l => l.characterId === this.assignedRole)
      .map(l => ({ start: l.startTime, end: l.endTime }));

    // Gerçek videoyu yükle
    if (this.videoElement) {
      this.videoElement.src = scene.videoSrc;
      this.videoElement.currentTime = 0;
      this.videoElement.load();
    }

    this._updateTranscriptDisplay(0);
  }

  // ╔══════════════════════════════════════════╗
  // ║  FAZ 1: İZLEME (PREVIEW)                ║
  // ║  Video orijinal sesiyle oynar            ║
  // ║  Kullanıcı izler, transkript görür       ║
  // ║  Video bitince "Hazırım" butonu çıkar    ║
  // ╚══════════════════════════════════════════╝
  startPreview() {
    if (!this.currentScene || !this.videoElement) return;

    this.phase = "preview";
    this.currentTime = 0;
    this.isPlaying = true;
    this.isRecording = false;
    this.onPhaseChange("preview");

    // Video orijinal sesiyle oynar (İzleme Modu)
    if (this.videoElement.src !== this.currentScene.videoSrc && !this.videoElement.src.endsWith(this.currentScene.videoSrc)) {
      this.videoElement.src = this.currentScene.videoSrc;
    }
    this.videoElement.currentTime = 0;
    this.videoElement.volume = 1.0; // TAM SES - orijinal diyalogları duy
    this.videoElement.muted = false;
    this.videoElement.play();

    // Banner'ı güncelle
    this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-blue-900/90 text-blue-200 border border-blue-500 shadow-lg";
    this.roleTurnBanner.innerHTML = "👁️ İZLEME MODU — Sahneyi İzle ve Replikleri Öğren";

    this.videoElement.ontimeupdate = () => {
      this.currentTime = this.videoElement.currentTime;
      this.onTimeUpdate(this.currentTime, this.videoElement.duration || this.currentScene.duration);
      this._updateTranscriptDisplay(this.currentTime, "preview");
    };

    this.videoElement.onended = () => {
      this.isPlaying = false;
      this.phase = "ready";
      this.onPhaseChange("ready");

      // "Hazırım" banner'ı göster
      this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-3 px-4 rounded-xl text-center font-black text-base uppercase tracking-widest bg-emerald-600/90 text-white border-2 border-emerald-400 shadow-2xl shadow-emerald-500/30 animate-pulse";
      this.roleTurnBanner.innerHTML = "✅ Sahneyi Gördün! Aşağıdaki Butona Bas ve Dublaja Başla!";
    };
  }

  // ╔══════════════════════════════════════════╗
  // ║  BİREYSEL PROVA: SADECE KENDİ ROLÜNÜ İZLE ║
  // ║  Yalnızca kullanıcının kendi repliklerini ║
  // ║  sesli olarak izletir ve alıştırma yaptırır║
  // ╚══════════════════════════════════════════╝
  // Kullanıcının rolüne ait sahneleri/replik segmentlerini çıkarır (Hatalı süreleri otomatik onarır)
  _getRoleSegments() {
    if (!this.roleCueIntervals || this.roleCueIntervals.length === 0) return [];
    
    // Her bir aralığı temizle ve ters girilmişse / hatalıysa düzelt
    const sanitized = this.roleCueIntervals.map(c => {
      let s = parseFloat(c.start);
      let e = parseFloat(c.end);
      if (isNaN(s)) s = 0;
      if (isNaN(e)) e = s + 3.0;
      if (s < 0) s = 0;

      if (e <= s) {
        // Eğer bitiş başlangıçtan küçükse (örn: start 18, end 14):
        // Ters girildiyse (14 ile 18 kastedilmiş)
        if (e > 0 && e < s) {
          const tmp = s;
          s = e;
          e = tmp;
        } else {
          e = s + 3.0;
        }
      }
      return { start: s, end: e };
    });

    const sorted = sanitized.sort((a, b) => a.start - b.start);
    const segments = [];
    let cur = { start: sorted[0].start, end: sorted[0].end };

    for (let i = 1; i < sorted.length; i++) {
      const next = sorted[i];
      // 1.5 saniyeden az ara varsa aynı sahne parçası olarak birleştir
      if (next.start - cur.end <= 1.5) {
        cur.end = Math.max(cur.end, next.end);
      } else {
        segments.push(cur);
        cur = { start: next.start, end: next.end };
      }
    }
    segments.push(cur);
    return segments;
  }

  // ╔══════════════════════════════════════════╗
  // ║  BİREYSEL PROVA: SADECE KENDİ ROLÜNÜ İZLE ║
  // ║  Yalnızca kullanıcının kendi sahnelerini  ║
  // ║  sesli olarak izletir ve alıştırma yaptırır║
  // ╚══════════════════════════════════════════╝
  playRoleRehearsal() {
    if (!this.currentScene || !this.videoElement) return;

    this.roleSegments = this._getRoleSegments();
    if (this.roleSegments.length === 0) {
      alert("Bu sahne için seçili rolüne ait replik bulunamadı veya rol seçilmedi.");
      return;
    }

    this.phase = "rehearsal";
    this.isPlaying = true;
    this.isRecording = false;
    this.currentSegmentIndex = 0;
    this.onPhaseChange("rehearsal");

    this._playCurrentRehearsalSegment();
  }

  _playCurrentRehearsalSegment() {
    const seg = this.roleSegments[this.currentSegmentIndex];
    if (!seg) {
      this.phase = "ready";
      this.onPhaseChange("ready");
      return;
    }

    const startPos = Math.max(0, seg.start - 0.8);
    const maxDur = this.videoElement.duration || this.currentScene.duration || 9999;
    let endPos = Math.min(maxDur, seg.end + 0.4);
    if (endPos <= startPos + 0.8) {
      endPos = startPos + 2.0;
    }

    this.videoElement.currentTime = startPos;
    this.videoElement.volume = this.videoVolume || 1.0;
    this.videoElement.muted = (this.videoVolume === 0);
    this.videoElement.play();

    this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-purple-900/90 text-purple-200 border border-purple-500 shadow-lg animate-pulse";
    this.roleTurnBanner.innerHTML = `🎯 ROL PROVASI — Sadece Kendi Sahnelerini Dinliyorsun (${this.currentSegmentIndex + 1}/${this.roleSegments.length})`;

    this.videoElement.ontimeupdate = () => {
      this.currentTime = this.videoElement.currentTime;
      this.onTimeUpdate(this.currentTime, this.videoElement.duration || this.currentScene.duration);
      this._updateTranscriptDisplay(this.currentTime, "rehearsal");

      if (this.currentTime >= endPos) {
        this.videoElement.ontimeupdate = null;
        if (this.currentSegmentIndex < this.roleSegments.length - 1) {
          this.currentSegmentIndex++;
          this._playCurrentRehearsalSegment();
        } else {
          this.videoElement.pause();
          this.isPlaying = false;
          this.phase = "ready";
          this.onPhaseChange("ready");

          this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-3 px-4 rounded-xl text-center font-black text-base uppercase tracking-widest bg-emerald-600/90 text-white border-2 border-emerald-400 shadow-2xl shadow-emerald-500/30 animate-pulse";
          this.roleTurnBanner.innerHTML = "🎯 Prova Bitti! Dublaj için hazırsan Başla butonuna bas!";
        }
      }
    };
  }

  // ╔══════════════════════════════════════════╗
  // ║  FAZ 2: DUBLAJ (RECORDING)              ║
  // ║  SADECE KENDİ SAHNELERİ OYNAR            ║
  // ║  Mikrofon kayıt başlar                   ║
  // ║  Sadece kendi rolünün transkripti çıkar  ║
  // ╚══════════════════════════════════════════╝
  startRecording() {
    if (!this.currentScene || !this.videoElement) return;

    // Seyirci / İzleyici Modu: Mikrofon kaydı yapmaz, video canlı oynatılır
    if (this.assignedRole === "spectator") {
      this.phase = "recording";
      this.isPlaying = true;
      this.isRecording = false;
      this.recordedChunks = [];
      this._pcmChunks = [];
      const dur = this.videoElement.duration || this.currentScene.duration || 20;
      this.roleSegments = [{ start: 0, end: dur }];
      this.currentSegmentIndex = 0;
      this.recordingStartTime = Date.now();
      this.onPhaseChange("recording");
      this._playCurrentRecordingSegment();
      return;
    }

    this.roleSegments = this._getRoleSegments();
    if (this.roleSegments.length === 0) {
      alert("Bu sahne için seçili rolüne ait replik bulunamadı!");
      return;
    }

    if (this.audioContext && this.audioContext.state === "suspended") {
      this.audioContext.resume().catch(() => {});
    }

    this.phase = "recording";
    this.isPlaying = true;
    this.isRecording = true;
    this.recordedChunks = [];
    this._pcmChunks = [];
    this.currentSegmentIndex = 0;
    this.recordingStartTime = Date.now();
    this.segmentTimingLog = [];
    this.onPhaseChange("recording");

    // Mikrofon kaydını başlat (MediaStreamDestination veya raw stream)
    const recordStream = (this.micDestination && this.micDestination.stream) 
      ? this.micDestination.stream 
      : this.microphoneStream;

    if (recordStream) {
      try {
        let mimeType = "";
        if (typeof MediaRecorder !== "undefined") {
          const types = [
            "audio/webm;codecs=opus",
            "audio/webm",
            "audio/ogg;codecs=opus",
            "audio/mp4"
          ];
          for (const t of types) {
            if (MediaRecorder.isTypeSupported(t)) {
              mimeType = t;
              break;
            }
          }
        }
        this.mediaRecorder = new MediaRecorder(recordStream, mimeType ? { mimeType } : {});
        this.mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) this.recordedChunks.push(e.data);
        };
        this.mediaRecorder.start(100);
      } catch (e) {
        console.warn("MediaRecorder hatası:", e);
      }
    }

    // Dublaj kaydı: Varsa temiz enstrümantal video oynat (müzik duyulur, orijinal ses susar)
    const recSrc = this.currentScene.cleanVideoSrc || this.currentScene.videoSrc;
    if (this.videoElement.src !== recSrc && !this.videoElement.src.endsWith(recSrc)) {
      this.videoElement.src = recSrc;
    }

    this._playCurrentRecordingSegment();
  }

  _playCurrentRecordingSegment() {
    const seg = this.roleSegments[this.currentSegmentIndex];
    if (!seg) {
      this.stopSession();
      return;
    }

    const startPos = Math.max(0, seg.start - 0.8);
    const maxDur = this.videoElement.duration || this.currentScene.duration || 9999;
    let endPos = Math.min(maxDur, seg.end + 0.4);
    // Güvenlik: endPos asla startPos'tan küçük veya eşit olamaz (en az 1.5 sn oynat)
    if (endPos <= startPos + 0.8) {
      endPos = startPos + 2.0;
    }

    const segWallStart = (Date.now() - this.recordingStartTime) / 1000;
    this.currentSegMeta = {
      videoStart: startPos,
      videoEnd: endPos,
      wallStart: segWallStart
    };

    this.videoElement.currentTime = startPos;
    // Kullanıcının dublaj yaparken video sesini duyabilmesi (ayarlanan seviye veya varsayılan %80)
    const vVol = (this.videoVolume !== undefined && this.videoVolume !== null) ? this.videoVolume : 0.8;
    this.videoElement.volume = Math.max(0, Math.min(1, vVol));
    this.videoElement.muted = (this.videoElement.volume === 0);
    this.videoElement.play();

    if (this.assignedRole === "spectator") {
      this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-amber-950/90 text-amber-200 border border-amber-500 shadow-lg animate-pulse";
      this.roleTurnBanner.innerHTML = "🍿 SEYİRCİ KOLTUĞU — Oyuncular Dublaj Yapıyor, Canlı İzliyorsun!";
    } else {
      this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-red-900/90 text-red-200 border border-red-500 shadow-lg animate-pulse";
      this.roleTurnBanner.innerHTML = `🔴 KAYIT — SADECE SENİN SAHNEN (${this.currentSegmentIndex + 1}/${this.roleSegments.length})`;
    }

    this.videoElement.ontimeupdate = () => {
      this.currentTime = this.videoElement.currentTime;
      this.onTimeUpdate(this.currentTime, this.videoElement.duration || this.currentScene.duration);
      this._updateTranscriptDisplay(this.currentTime, "recording");

      if (this.currentTime >= endPos) {
        this.videoElement.ontimeupdate = null;
        const segWallDur = Math.max(0.1, ((Date.now() - this.recordingStartTime) / 1000) - this.currentSegMeta.wallStart);
        this.segmentTimingLog.push({
          videoStart: this.currentSegMeta.videoStart,
          videoEnd: this.currentSegMeta.videoEnd,
          wallStart: this.currentSegMeta.wallStart,
          wallDuration: segWallDur
        });

        if (this.currentSegmentIndex < this.roleSegments.length - 1) {
          this.currentSegmentIndex++;
          this._playCurrentRecordingSegment();
        } else {
          this.stopSession();
        }
      }
    };

    this.videoElement.onended = () => {
      this.stopSession();
    };
  }

  // Baştaki İzlemeyi Geç (Doğrudan Hazır Durumuna Atla)
  skipPreview() {
    if (this.phase !== "preview") return;
    if (this.videoElement) {
      this.videoElement.pause();
      this.videoElement.ontimeupdate = null;
      this.videoElement.onended = null;
    }
    this.isPlaying = false;
    this.phase = "ready";
    this.onPhaseChange("ready");
  }

  // Dublajı Sıfırla / Tekrar Kaydetmeye Hazırla
  resetRecording() {
    this.recordedChunks = [];
    this._pcmChunks = [];
    this.recordedBlob = null;
    this.recordedAudioUrl = null;
    this.segmentTimingLog = [];
    this.currentSegmentIndex = 0;
    this.isPlaying = false;
    this.isRecording = false;
    this.isRoleSpeakingNow = false;

    if (this.videoElement) {
      this.videoElement.pause();
      this.videoElement.ontimeupdate = null;
      this.videoElement.onended = null;
      this.videoElement.currentTime = 0;
    }
    this.phase = "ready";
    this.onPhaseChange("ready");
  }

  // Eski startSession -> artık doğrudan preview başlatır
  startSession() {
    this.startPreview();
  }

  // Oturumu Durdur ve Kullanıcının Sesini İzole Et
  stopSession() {
    this.isPlaying = false;
    this.isRecording = false;
    this.isRoleSpeakingNow = false;

    if (this.videoElement) {
      this.videoElement.pause();
      this.videoElement.ontimeupdate = null;
      this.videoElement.onended = null;
    }

    if (this.currentSegMeta && this.segmentTimingLog) {
      const alreadyLogged = this.segmentTimingLog.some(s => s.videoStart === this.currentSegMeta.videoStart);
      if (!alreadyLogged) {
        const segWallDur = Math.max(0.1, ((Date.now() - this.recordingStartTime) / 1000) - this.currentSegMeta.wallStart);
        this.segmentTimingLog.push({
          videoStart: this.currentSegMeta.videoStart,
          videoEnd: this.currentSegMeta.videoEnd,
          wallStart: this.currentSegMeta.wallStart,
          wallDuration: segWallDur
        });
      }
    }

    if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
      this.mediaRecorder.stop();
      this.mediaRecorder.onstop = async () => {
        const fullBlob = new Blob(this.recordedChunks, { type: "audio/webm" });
        const processed = await this._processAssignedRoleAudio(fullBlob);
        this.phase = "idle";
        this.onPhaseChange("idle");
        this.onComplete({
          audioBlob: processed.blob,
          audioBase64: processed.base64,
          characterId: this.assignedRole,
          duration: this.currentTime
        });
      };
    } else {
      this.phase = "idle";
      this.onPhaseChange("idle");
      this.onComplete({
        audioBlob: null,
        audioBase64: null,
        characterId: this.assignedRole,
        duration: this.currentTime
      });
    }
  }

  // Transkript ve Canlı Altyazı Şeridini Güncelle
  // Transkript ve Canlı Altyazı Şeridini Güncelle (Karaoke Barı & Trafik Işığı Destekli)
  _updateTranscriptDisplay(time, currentPhase) {
    if (!this.currentScene || !this.transcriptBar) return;
    const lines = this.currentScene.lines || [];
    const activeCue = lines.find(l => time >= l.startTime && time <= l.endTime);
    // Yaklaşan replik kontrolü (1.8 saniye içinde başlayacak mı?)
    const upcomingCue = !activeCue ? lines.find(l => time < l.startTime && (l.startTime - time) <= 1.8) : null;

    // 1. MÜZİK VE EDİT KİLİDİ KONTROLÜ:
    const isMusicCue = activeCue && (activeCue.type === "music" || activeCue.isMusic);
    if (isMusicCue) {
      this.isMusicLocked = true;
      this.isRoleSpeakingNow = false;

      // Donanımsal mikrofon susturma (Zero-gain mute)
      if (this.micGainNode && this.audioContext) {
        this.micGainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
      }

      this.transcriptBar.classList.remove("opacity-0");
      this.transcriptBar.classList.add("opacity-100");
      this.transcriptBar.style.borderColor = "#f59e0b";
      this.transcriptBar.style.boxShadow = "0 0 25px rgba(245, 158, 11, 0.4)";

      this.transcriptSpeaker.innerText = "🎵 Müzik / Edit";
      this.transcriptSpeaker.style.backgroundColor = "#d97706";
      this.transcriptTiming.innerText = `${activeCue.startTime.toFixed(1)}s - ${activeCue.endTime.toFixed(1)}s`;
      this.transcriptText.innerText = activeCue.text;
      this.transcriptInstruction.innerText = "🔒 Müzik çalıyor — Mikrofon kilitlendi, sessiz kal!";

      if (this.trafficLightBadge) {
        this.trafficLightBadge.className = "text-[11px] font-black uppercase tracking-widest px-3 py-0.5 rounded-full bg-amber-950 text-amber-300 border border-amber-500 flex items-center space-x-1.5 shadow-sm";
        this.trafficLightBadge.innerHTML = "<span>🔒</span><span>MÜZİK KİLİTLİ</span>";
      }

      if (this.karaokeProgressBar) {
        const mDur = Math.max(0.1, activeCue.endTime - activeCue.startTime);
        const mElapsed = time - activeCue.startTime;
        const mPct = Math.min(100, Math.max(0, (mElapsed / mDur) * 100));
        this.karaokeProgressBar.style.width = `${mPct}%`;
        this.karaokeProgressBar.className = "h-full bg-amber-500 transition-all duration-75";
      }

      this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2.5 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-gradient-to-r from-amber-600 to-orange-600 text-white border-2 border-amber-300 shadow-2xl shadow-amber-500/40 animate-pulse";
      this.roleTurnBanner.innerHTML = "🎵 [MÜZİK ÇALIYOR] — MİKROFON KİLİTLENDİ (MÜZİĞİ DİNLE!)";
      return;
    } else {
      this.isMusicLocked = false;
      if (this.micGainNode && this.audioContext) {
        this.micGainNode.gain.setValueAtTime(this.micVolume, this.audioContext.currentTime);
      }
    }

    const activeChar = activeCue 
      ? (this.currentScene.characters || []).find(c => c.id === activeCue.characterId) 
      : null;

    const isMyTurn = activeCue && activeCue.characterId === this.assignedRole;
    this.isRoleSpeakingNow = isMyTurn;

    // 2. AKTİF REPLİK VARSA (ŞİMDİ KONUŞ EVRESİ)
    if (activeCue && activeChar) {
      const cueDur = Math.max(0.1, activeCue.endTime - activeCue.startTime);
      const elapsed = time - activeCue.startTime;
      const progressPct = Math.min(100, Math.max(0, (elapsed / cueDur) * 100));

      if (this.karaokeProgressBar) {
        this.karaokeProgressBar.style.width = `${progressPct}%`;
        this.karaokeProgressBar.className = isMyTurn 
          ? "h-full bg-gradient-to-r from-emerald-400 to-teal-400 transition-all duration-75 shadow-sm"
          : "h-full bg-gradient-to-r from-indigo-400 to-blue-400 transition-all duration-75 shadow-sm";
      }

      if (currentPhase === "preview") {
        // İLK İZLEME: Herkes tüm sahneyi ve tüm replikleri görür
        this.transcriptBar.classList.remove("opacity-0");
        this.transcriptBar.classList.add("opacity-100");
        this.transcriptBar.style.borderColor = "#3b82f6";
        this.transcriptBar.style.boxShadow = "0 0 15px rgba(59, 130, 246, 0.3)";

        this.transcriptSpeaker.innerText = `${activeChar.avatar} ${activeChar.name}`;
        this.transcriptSpeaker.style.backgroundColor = activeChar.color;
        this.transcriptTiming.innerText = `${activeCue.startTime.toFixed(1)}s - ${activeCue.endTime.toFixed(1)}s`;
        this.transcriptText.innerText = `"${activeCue.text}"`;
        this.transcriptInstruction.innerText = activeCue.emotion ? `🎭 ${activeCue.emotion}` : "";

        if (this.trafficLightBadge) {
          this.trafficLightBadge.className = "text-[11px] font-bold uppercase tracking-widest px-3 py-0.5 rounded-full bg-blue-900/80 text-blue-200 border border-blue-500 flex items-center space-x-1.5 shadow-sm";
          this.trafficLightBadge.innerHTML = `<span>👁️</span><span>${activeChar.name}</span>`;
        }

        if (isMyTurn) {
          this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-purple-900/90 text-purple-100 border border-purple-400 shadow-lg";
          this.roleTurnBanner.innerHTML = `👁️ SENİN REPLİĞİN — Dinle ve ezberlemeye çalış!`;
        } else {
          this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-blue-900/90 text-blue-200 border border-blue-500";
          this.roleTurnBanner.innerHTML = `👁️ İZLEME MODU — ${activeChar.avatar} ${activeChar.name} Konuşuyor`;
        }
      } else {
        // PROVA VE NORMAL KAYIT (ŞİMDİ KONUŞ!)
        if (isMyTurn) {
          this.transcriptBar.classList.remove("opacity-0");
          this.transcriptBar.classList.add("opacity-100");
          this.transcriptBar.style.borderColor = currentPhase === "recording" ? "#10b981" : "#a855f7";
          this.transcriptBar.style.boxShadow = currentPhase === "recording" 
            ? "0 0 35px rgba(16, 185, 129, 0.55)" 
            : "0 0 20px rgba(168, 85, 247, 0.35)";

          this.transcriptSpeaker.innerText = `${activeChar.avatar} SEN (${activeChar.name})`;
          this.transcriptSpeaker.style.backgroundColor = activeChar.color;
          this.transcriptTiming.innerText = `${activeCue.startTime.toFixed(1)}s - ${activeCue.endTime.toFixed(1)}s`;
          this.transcriptText.innerText = `"${activeCue.text}"`;
          this.transcriptInstruction.innerText = activeCue.emotion ? `🎭 ${activeCue.emotion}` : "";

          if (this.trafficLightBadge) {
            this.trafficLightBadge.className = "text-[11px] font-black uppercase tracking-widest px-3 py-0.5 rounded-full bg-red-600 text-white border border-red-400 animate-pulse flex items-center space-x-1.5 shadow-lg";
            this.trafficLightBadge.innerHTML = "<span>🔴</span><span>ŞİMDİ KONUŞ!</span>";
          }

          if (currentPhase === "recording") {
            this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-emerald-600/95 text-white shadow-xl shadow-emerald-500/40 border-2 border-emerald-300 animate-pulse";
            this.roleTurnBanner.innerHTML = "🎙️ SENİN REPLİĞİN! ŞİMDİ VİDEOYA BAKIP KONUŞ!";
          }
        } else {
          // Başka karakterin repliği varsa gizle
          this.transcriptBar.classList.add("opacity-0");
          this.transcriptBar.classList.remove("opacity-100");
          if (this.karaokeProgressBar) this.karaokeProgressBar.style.width = "0%";
          this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-bold text-xs uppercase tracking-widest bg-slate-950/70 text-slate-400 border border-slate-800";
          this.roleTurnBanner.innerHTML = "🎬 SADECE SENİN SAHNEN — Replik Bekleniyor...";
        }
      }
    } else if (upcomingCue) {
      // 3. YAKLAŞAN REPLİK (1.8s İÇİNDE - SARI IŞIK / HAZIRLAN)
      const upcomingChar = (this.currentScene.characters || []).find(c => c.id === upcomingCue.characterId);
      const isMyUpcoming = upcomingCue.characterId === this.assignedRole;
      const remainingSec = (upcomingCue.startTime - time).toFixed(1);

      if (isMyUpcoming || currentPhase === "preview") {
        this.transcriptBar.classList.remove("opacity-0");
        this.transcriptBar.classList.add("opacity-100");
        this.transcriptBar.style.borderColor = "#f59e0b";
        this.transcriptBar.style.boxShadow = "0 0 25px rgba(245, 158, 11, 0.45)";

        this.transcriptSpeaker.innerText = `${upcomingChar ? upcomingChar.avatar : '🎭'} ${isMyUpcoming ? 'SEN (' + (upcomingChar ? upcomingChar.name : '') + ')' : (upcomingChar ? upcomingChar.name : '')}`;
        this.transcriptSpeaker.style.backgroundColor = upcomingChar ? upcomingChar.color : "#d97706";
        this.transcriptTiming.innerText = `${upcomingCue.startTime.toFixed(1)}s - ${upcomingCue.endTime.toFixed(1)}s`;
        this.transcriptText.innerText = `"${upcomingCue.text}"`;
        this.transcriptInstruction.innerText = upcomingCue.emotion ? `🎭 ${upcomingCue.emotion}` : "";

        if (this.trafficLightBadge) {
          this.trafficLightBadge.className = "text-[11px] font-black uppercase tracking-widest px-3 py-0.5 rounded-full bg-amber-500 text-slate-950 border border-amber-300 animate-pulse flex items-center space-x-1.5 shadow-md";
          this.trafficLightBadge.innerHTML = `<span>🟡</span><span>HAZIRLAN (${remainingSec}s)</span>`;
        }

        if (this.karaokeProgressBar) {
          this.karaokeProgressBar.style.width = "0%";
        }

        this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-black text-sm uppercase tracking-widest bg-amber-600/90 text-white shadow-lg shadow-amber-500/30 border border-amber-300 animate-pulse";
        this.roleTurnBanner.innerHTML = `🟡 HAZIRLAN! (${remainingSec}s sonra konuşuyorsun)`;
      } else {
        this.transcriptBar.classList.add("opacity-0");
        if (this.karaokeProgressBar) this.karaokeProgressBar.style.width = "0%";
      }
    } else {
      // 4. BOŞLUK / BEKLEME EVRESİ
      this.transcriptBar.classList.add("opacity-0");
      this.transcriptBar.classList.remove("opacity-100");
      if (this.karaokeProgressBar) this.karaokeProgressBar.style.width = "0%";

      if (this.trafficLightBadge) {
        this.trafficLightBadge.className = "text-[11px] font-bold uppercase tracking-widest px-3 py-0.5 rounded-full bg-slate-800 text-slate-400 border border-slate-700 flex items-center space-x-1.5";
        this.trafficLightBadge.innerHTML = "<span>⏸️</span><span>BEKLE</span>";
      }

      if (currentPhase === "preview") {
        this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-bold text-xs uppercase tracking-widest bg-blue-950/70 text-blue-300 border border-blue-800";
        this.roleTurnBanner.innerHTML = "👁️ İZLİYORSUN... Sahne Akıyor";
      } else {
        this.roleTurnBanner.className = "absolute top-4 left-4 right-4 py-2 px-4 rounded-xl text-center font-bold text-xs uppercase tracking-widest bg-slate-950/70 text-slate-400 border border-slate-800";
        this.roleTurnBanner.innerHTML = "🎬 SADECE SENİN SAHNEN — Replik Geliyor...";
      }
    }
  }

  // Rol İzolasyonu ve Müzik Kilidi Filtresi: Yalnızca kullanıcının kendi replik pencerelerini keser
  async _processAssignedRoleAudio(rawBlob) {
    if (!this.audioContext || this.roleCueIntervals.length === 0) {
      const base64 = await this._blobToBase64(rawBlob);
      return { blob: rawBlob, base64 };
    }

    try {
      if (this.audioContext.state === "suspended") {
        await this.audioContext.resume().catch(() => {});
      }

      let audioBuffer = null;

      // 1. Önce doğrudan yakalanan PCM tamponlarını kullan (Kusursuz, kayıpsız, WebM dekoderine bağımlı değil!)
      if (this._pcmChunks && this._pcmChunks.length > 0) {
        const totalSamples = this._pcmChunks.reduce((acc, c) => acc + c.length, 0);
        if (totalSamples > 0) {
          audioBuffer = this.audioContext.createBuffer(1, totalSamples, this.audioContext.sampleRate);
          const chData = audioBuffer.getChannelData(0);
          let offset = 0;
          for (const chunk of this._pcmChunks) {
            chData.set(chunk, offset);
            offset += chunk.length;
          }
        }
      }

      // 2. Fallback: Eğer PCM yoksa MediaRecorder Blob'unu çöz
      if (!audioBuffer && rawBlob) {
        const arrayBuffer = await rawBlob.arrayBuffer();
        audioBuffer = await this.audioContext.decodeAudioData(arrayBuffer);
      }

      if (!audioBuffer) {
        throw new Error("Ses verisi oluşturulamadı");
      }

      const sampleRate = audioBuffer.sampleRate;
      const numChannels = audioBuffer.numberOfChannels;
      const sceneDuration = this.currentScene.duration || 20;
      const totalLength = Math.ceil(sceneDuration * sampleRate);

      const cleanBuffer = this.audioContext.createBuffer(numChannels, totalLength, sampleRate);
      const musicCues = (this.currentScene.lines || []).filter(l => l.type === "music" || l.isMusic);

      for (let channel = 0; channel < numChannels; channel++) {
        const inputData = audioBuffer.getChannelData(channel);
        const outputData = cleanBuffer.getChannelData(channel);
        outputData.fill(0); // Sessizlik

        if (this.segmentTimingLog && this.segmentTimingLog.length > 0) {
          // Segmentli kayıt: Her bir sahne parçasını tam video saniyesine yerleştir
          this.segmentTimingLog.forEach(seg => {
            const wallStartSample = Math.floor(seg.wallStart * sampleRate);
            const wallDurSamples = Math.floor(seg.wallDuration * sampleRate);
            const videoStartSample = Math.floor(seg.videoStart * sampleRate);

            for (let i = 0; i < wallDurSamples; i++) {
              const srcIdx = wallStartSample + i;
              const dstIdx = videoStartSample + i;
              if (srcIdx < inputData.length && dstIdx < totalLength) {
                outputData[dstIdx] = inputData[srcIdx];
              }
            }
          });
        } else {
          // Fallback: Doğrudan aralık bazlı yerleştirme
          this.roleCueIntervals.forEach(inv => {
            const startSample = Math.max(0, Math.floor((inv.start - 0.2) * sampleRate));
            const endSample = Math.min(totalLength, Math.floor((inv.end + 0.35) * sampleRate));
            for (let i = startSample; i < endSample; i++) {
              if (i < inputData.length && i < totalLength) {
                outputData[i] = inputData[i];
              }
            }
          });
        }

        // 2. Müzik aralıklarını kesin olarak sıfırla (Müzik kilidi koruması)
        musicCues.forEach(m => {
          const mStart = Math.max(0, Math.floor(m.startTime * sampleRate));
          const mEnd = Math.min(totalLength, Math.floor(m.endTime * sampleRate));
          for (let i = mStart; i < mEnd; i++) {
            if (i < totalLength) outputData[i] = 0;
          }
        });
      }

      const wavBlob = this._audioBufferToWav(cleanBuffer);
      const base64 = await this._blobToBase64(wavBlob);
      return { blob: wavBlob, base64 };
    } catch (e) {
      console.warn("Ses filtreleme hatası, ham ses aktarılıyor:", e);
      const base64 = await this._blobToBase64(rawBlob);
      return { blob: rawBlob, base64 };
    }
  }

  _audioBufferToWav(buffer) {
    const numOfChan = buffer.numberOfChannels;
    const length = buffer.length * numOfChan * 2 + 44;
    const out = new DataView(new ArrayBuffer(length));
    let offset = 0;
    let pos = 0;

    function setUint16(data) { out.setUint16(pos, data, true); pos += 2; }
    function setUint32(data) { out.setUint32(pos, data, true); pos += 4; }

    setUint32(0x46464952); setUint32(length - 8); setUint32(0x45564157);
    setUint32(0x20746d66); setUint32(16); setUint16(1); setUint16(numOfChan);
    setUint32(buffer.sampleRate); setUint32(buffer.sampleRate * 2 * numOfChan);
    setUint16(numOfChan * 2); setUint16(16); setUint32(0x61746164); setUint32(length - pos - 4);

    const channels = [];
    for (let i = 0; i < buffer.numberOfChannels; i++) channels.push(buffer.getChannelData(i));

    while (offset < buffer.length) {
      for (let i = 0; i < numOfChan; i++) {
        let sample = Math.max(-1, Math.min(1, channels[i][offset]));
        sample = (0.5 + sample < 0 ? sample * 32768 : sample * 32767) | 0;
        out.setInt16(pos, sample, true);
        pos += 2;
      }
      offset++;
    }

    return new Blob([out.buffer], { type: "audio/wav" });
  }

  _blobToBase64(blob) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  }
}
