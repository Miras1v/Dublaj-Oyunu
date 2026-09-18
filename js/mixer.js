// Dublaj Oyunu - Gerçek Video Destekli Prömiyer Sineması
// Orijinal video oynarken oyuncuların kaydettiği sesler tam senkron üzerine biner!
// Gelişmiş Timeline Oynatıcı: Play/Pause, Seek, Solo/Mute ve WAV İndirme Desteği

export class VirtualMixer {
  constructor(options = {}) {
    this.videoElement = options.videoElement; // <video id="premiere-video">
    this.transcriptBar = options.transcriptBar;
    this.transcriptSpeaker = options.transcriptSpeaker;
    this.transcriptText = options.transcriptText;

    this.audioContext = null;
    this.activeAudioNodes = [];
    this.characterGainNodes = new Map(); // charId -> GainNode
    this.characterVolumes = new Map();   // charId -> volume (0.0 to 2.0)
    this.mutedCharacters = new Set();    // Set of muted charIds
    this.soloCharacterId = null;         // Currently soloed charId, or null
    this.videoVolume = 0.35;             // Prömiyerde arka plan video/müzik seviyesi (%35 varsayılan)
    this.isVideoMuted = false;

    this.isPlaying = false;
    this.currentScene = null;
    this.audioTracks = {};
    this.decodedBuffers = new Map();

    this.onTimeUpdate = options.onTimeUpdate || (() => {});
    this.onEnd = options.onEnd || (() => {});
  }

  // Bireysel Karakter Sesini Ayarla (Volume Fader)
  setCharacterVolume(charId, volumePercent) {
    const vol = Math.max(0, Math.min(2.0, volumePercent / 100));
    this.characterVolumes.set(charId, vol);
    this._applyGainVolumes();
  }

  // Prömiyer Video (Dip Ses / Fon Müziği) Seviyesini Ayarla
  setVideoVolume(volumePercent) {
    this.videoVolume = Math.max(0, Math.min(1.0, volumePercent / 100));
    if (this.videoElement && !this.isVideoMuted) {
      this.videoElement.volume = this.videoVolume;
    }
  }

  // Karakter Mute Aç/Kapat
  toggleMute(charId) {
    if (this.mutedCharacters.has(charId)) {
      this.mutedCharacters.delete(charId);
    } else {
      this.mutedCharacters.add(charId);
    }
    this._applyGainVolumes();
    return this.mutedCharacters.has(charId);
  }

  // Karakter Solo Aç/Kapat
  toggleSolo(charId) {
    if (this.soloCharacterId === charId) {
      this.soloCharacterId = null; // Soloyu kaldır
    } else {
      this.soloCharacterId = charId; // Bu karakteri solo yap
    }
    this._applyGainVolumes();
    return this.soloCharacterId === charId;
  }

  // Video Sesi Mute Aç/Kapat
  toggleVideoMute() {
    this.isVideoMuted = !this.isVideoMuted;
    if (this.videoElement) {
      this.videoElement.volume = this.isVideoMuted ? 0 : this.videoVolume;
    }
    return this.isVideoMuted;
  }

  // Kazanç Değerlerini Hesapla ve GainNode'lara Uygula
  _applyGainVolumes() {
    if (!this.audioContext) return;
    const now = this.audioContext.currentTime;

    for (const [charId, gainNode] of this.characterGainNodes.entries()) {
      let effectiveVol = this.characterVolumes.has(charId) ? this.characterVolumes.get(charId) : 1.0;

      // Solo modu aktifse ve bu karakter solo değilse sesini kıs
      if (this.soloCharacterId !== null) {
        if (this.soloCharacterId !== charId) effectiveVol = 0;
      } else if (this.mutedCharacters.has(charId)) {
        // Mute ise sesini kıs
        effectiveVol = 0;
      }

      try {
        gainNode.gain.cancelScheduledValues(now);
        gainNode.gain.setValueAtTime(effectiveVol, now);
      } catch (e) {}
    }
  }

  async preparePremiere(scene, audioTracks) {
    this.currentScene = scene;
    this.audioTracks = audioTracks || {};
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.decodedBuffers = new Map();
    this.characterGainNodes = new Map();
    this.mutedCharacters.clear();
    this.soloCharacterId = null;

    // Sesleri decode et
    for (const [charId, track] of Object.entries(this.audioTracks)) {
      if (!track || !track.audioData) continue;
      try {
        const audioBuffer = await this._base64ToAudioBuffer(track.audioData);
        this.decodedBuffers.set(charId, audioBuffer);
      } catch (e) {
        console.warn(`${charId} sesi çözülemedi:`, e);
      }
    }

    // Videoyu hazırla (Temiz enstrümantal dublaj videosu varsa onu çal, yoksa orijinal video)
    if (this.videoElement) {
      this.videoElement.src = scene.cleanVideoSrc || scene.videoSrc;
      this.videoElement.currentTime = 0;
      this.videoElement.volume = this.isVideoMuted ? 0 : this.videoVolume;
      this.videoElement.load();
    }
  }

  async _base64ToAudioBuffer(base64Data) {
    const res = await fetch(base64Data);
    const arrayBuffer = await res.arrayBuffer();
    return await this.audioContext.decodeAudioData(arrayBuffer);
  }

  // Baştan Oynat
  play() {
    this.seek(0);
    this.resume();
  }

  // Oynat/Durdur Geçişi
  togglePlayPause() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.resume();
    }
    return this.isPlaying;
  }

  // Duraklat (Pause)
  pause() {
    this.isPlaying = false;
    if (this.videoElement) {
      this.videoElement.pause();
    }
    this._stopActiveAudioSources();
  }

  // Devam Et (Resume)
  resume() {
    if (!this.currentScene || !this.videoElement || !this.audioContext) return;
    if (this.audioContext.state === "suspended") {
      this.audioContext.resume();
    }

    const currentPos = this.videoElement.currentTime || 0;
    this.isPlaying = true;
    this._stopActiveAudioSources();

    const nowAudioTime = this.audioContext.currentTime;

    // Her karakter için buffer'ı offset'ten başlat
    for (const [charId, buffer] of this.decodedBuffers.entries()) {
      if (currentPos >= buffer.duration) continue;

      const source = this.audioContext.createBufferSource();
      source.buffer = buffer;

      const gainNode = this.audioContext.createGain();
      this.characterGainNodes.set(charId, gainNode);

      source.connect(gainNode);
      gainNode.connect(this.audioContext.destination);

      // Offset ile senkron başlat
      source.start(nowAudioTime, currentPos);
      this.activeAudioNodes.push(source);
    }

    this._applyGainVolumes();

    this.videoElement.play();

    this.videoElement.ontimeupdate = () => {
      const cur = this.videoElement.currentTime;
      const dur = this.videoElement.duration || this.currentScene.duration;
      this.onTimeUpdate(cur, dur);
      this._updatePremiereTranscript(cur);
    };

    this.videoElement.onended = () => {
      this.pause();
      this.onEnd();
    };
  }

  // İstenen Saniyeye Sar (Seek)
  seek(targetTime) {
    if (!this.videoElement) return;
    const dur = this.videoElement.duration || (this.currentScene ? this.currentScene.duration : 15);
    const clampedTime = Math.max(0, Math.min(dur, targetTime));

    const wasPlaying = this.isPlaying;
    this.pause();
    this.videoElement.currentTime = clampedTime;
    this.onTimeUpdate(clampedTime, dur);
    this._updatePremiereTranscript(clampedTime);

    if (wasPlaying) {
      this.resume();
    }
  }

  _stopActiveAudioSources() {
    this.activeAudioNodes.forEach(node => {
      try { node.stop(); } catch (e) {}
    });
    this.activeAudioNodes = [];
  }

  stop() {
    this.pause();
    if (this.videoElement) {
      this.videoElement.currentTime = 0;
      this.videoElement.ontimeupdate = null;
      this.videoElement.onended = null;
    }
  }

  _updatePremiereTranscript(time) {
    if (!this.currentScene || !this.transcriptBar) return;
    const lines = this.currentScene.lines || [];
    const activeCue = lines.find(l => time >= l.startTime && time <= l.endTime);

    // Müzik aralığı gösterimi
    if (activeCue && (activeCue.type === "music" || activeCue.isMusic)) {
      this.transcriptBar.classList.remove("opacity-0");
      this.transcriptBar.classList.add("opacity-100");
      this.transcriptSpeaker.innerText = "🎵 [FON MÜZİĞİ & EDİT GEÇİŞİ]";
      this.transcriptSpeaker.style.color = "#f59e0b";
      this.transcriptText.innerText = activeCue.text;
      return;
    }

    const activeChar = activeCue 
      ? (this.currentScene.characters || []).find(c => c.id === activeCue.characterId) 
      : null;

    if (activeCue && activeChar) {
      const track = this.audioTracks[activeChar.id];
      const dubberName = track ? track.playerName : "Sen";

      this.transcriptBar.classList.remove("opacity-0");
      this.transcriptBar.classList.add("opacity-100");
      this.transcriptSpeaker.innerText = `🎙️ ${activeChar.avatar} ${activeChar.name} (Seslendiren: ${dubberName})`;
      this.transcriptSpeaker.style.color = activeChar.color;
      this.transcriptText.innerText = `"${activeCue.text}"`;
    } else {
      this.transcriptBar.classList.remove("opacity-100");
      this.transcriptBar.classList.add("opacity-0");
    }
  }

  // Tüm Kayıtları Tek Birleşik WAV Olarak İndir (Export Mixed Audio)
  async exportMixedAudio() {
    if (!this.currentScene || this.decodedBuffers.size === 0) {
      alert("İndirilecek ses kaydı bulunamadı!");
      return;
    }

    const duration = this.currentScene.duration || 15;
    const sampleRate = 44100;
    const offlineCtx = new (window.OfflineAudioContext || window.webkitOfflineAudioContext)(2, duration * sampleRate, sampleRate);

    // Tüm kanalları offline context'e ekle
    for (const [charId, buffer] of this.decodedBuffers.entries()) {
      let vol = this.characterVolumes.has(charId) ? this.characterVolumes.get(charId) : 1.0;
      if (this.mutedCharacters.has(charId)) vol = 0;
      if (this.soloCharacterId !== null && this.soloCharacterId !== charId) vol = 0;

      const source = offlineCtx.createBufferSource();
      source.buffer = buffer;

      const gain = offlineCtx.createGain();
      gain.gain.value = vol;

      source.connect(gain);
      gain.connect(offlineCtx.destination);
      source.start(0);
    }

    const renderedBuffer = await offlineCtx.startRendering();
    const wavBlob = this._audioBufferToWavBlob(renderedBuffer);

    // Dosyayı indir
    const url = URL.createObjectURL(wavBlob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `dublaj_${this.currentScene.id}_${Date.now()}.wav`;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { a.remove(); URL.revokeObjectURL(url); }, 2000);
  }

  // Videolu Dublajı İndir (.webm / .mp4 - Tarayıcı İçi Sıfır Maliyetli Muxing)
  async exportMixedVideo(progressCallback = () => {}) {
    if (!this.currentScene || this.decodedBuffers.size === 0) {
      alert("İndirilecek dublaj kaydı bulunamadı!");
      return;
    }

    const vid = this.videoElement;
    if (!vid) return;

    // Tarayıcı captureStream desteği
    const stream = vid.captureStream ? vid.captureStream() : (vid.mozCaptureStream ? vid.mozCaptureStream() : null);
    if (!stream) {
      alert("Tarayıcınız video akış kaydını (captureStream) desteklemiyor!");
      return;
    }

    // Dublaj ses mikseri çıkış akışı
    const audioStreamDest = this.audioContext.createMediaStreamDestination();

    // Ses kanallarını audioStreamDest'e bağla
    for (const [charId, buffer] of this.decodedBuffers.entries()) {
      let vol = this.characterVolumes.has(charId) ? this.characterVolumes.get(charId) : 1.0;
      if (this.mutedCharacters.has(charId)) vol = 0;
      if (this.soloCharacterId !== null && this.soloCharacterId !== charId) vol = 0;

      const src = this.audioContext.createBufferSource();
      src.buffer = buffer;
      const gain = this.audioContext.createGain();
      gain.gain.value = vol;
      src.connect(gain);
      gain.connect(audioStreamDest);
      src.start(this.audioContext.currentTime);
      this.activeAudioNodes.push(src);
    }

    // Kombine Video + Mixed Audio Akışı
    const videoTracks = stream.getVideoTracks();
    const audioTracks = audioStreamDest.stream.getAudioTracks();
    const combinedStream = new MediaStream([...videoTracks, ...audioTracks]);

    const mimeTypes = [
      "video/webm;codecs=vp9,opus",
      "video/webm;codecs=vp8,opus",
      "video/webm",
      "video/mp4"
    ];
    const chosenMime = mimeTypes.find(t => MediaRecorder.isTypeSupported(t)) || "";

    const recorder = new MediaRecorder(combinedStream, chosenMime ? { mimeType: chosenMime } : {});
    const recordedChunks = [];

    recorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) recordedChunks.push(e.data);
    };

    const duration = vid.duration || this.currentScene.duration || 15;

    return new Promise((resolve) => {
      recorder.onstop = () => {
        const blob = new Blob(recordedChunks, { type: chosenMime || "video/webm" });
        const ext = chosenMime.includes("mp4") ? "mp4" : "webm";
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `dublaj_videolu_${this.currentScene.id}_${Date.now()}.${ext}`;
        document.body.appendChild(a);
        a.click();
        setTimeout(() => { a.remove(); URL.revokeObjectURL(url); }, 2500);
        this.stop();
        resolve();
      };

      // Başa sarıp kaydı başlat
      vid.currentTime = 0;
      recorder.start(250);
      vid.play();

      vid.ontimeupdate = () => {
        const cur = vid.currentTime;
        const pct = Math.min(100, Math.round((cur / duration) * 100));
        progressCallback(pct);
      };

      vid.onended = () => {
        recorder.stop();
      };
    });
  }

  _audioBufferToWavBlob(buffer) {
    const numChannels = buffer.numberOfChannels;
    const sampleRate = buffer.sampleRate;
    const format = 1; // PCM
    const bitDepth = 16;
    const bytesPerSample = bitDepth / 8;
    const blockAlign = numChannels * bytesPerSample;

    let interleaved;
    if (numChannels === 2) {
      const left = buffer.getChannelData(0);
      const right = buffer.getChannelData(1);
      interleaved = new Float32Array(left.length + right.length);
      for (let i = 0, j = 0; i < left.length; i++) {
        interleaved[j++] = left[i];
        interleaved[j++] = right[i];
      }
    } else {
      interleaved = buffer.getChannelData(0);
    }

    const bufferLength = 44 + interleaved.length * 2;
    const arrayBuffer = new ArrayBuffer(bufferLength);
    const view = new DataView(arrayBuffer);

    // RIFF chunk descriptor
    this._writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + interleaved.length * 2, true);
    this._writeString(view, 8, 'WAVE');
    // FMT sub-chunk
    this._writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, format, true);
    view.setUint16(22, numChannels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * blockAlign, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, bitDepth, true);
    // data sub-chunk
    this._writeString(view, 36, 'data');
    view.setUint32(40, interleaved.length * 2, true);

    // Write samples
    let offset = 44;
    for (let i = 0; i < interleaved.length; i++, offset += 2) {
      let s = Math.max(-1, Math.min(1, interleaved[i]));
      view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }

    return new Blob([view], { type: 'audio/wav' });
  }

  _writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  }
}
