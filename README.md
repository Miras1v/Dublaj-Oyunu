# 🎙️ Dublaj Partisi

**dublaj.io** mekaniğinde, $0 sunucu maliyetli **P2P WebRTC** mimarisiyle çalışan, gerçek videolar üzerinden arkadaşlarınızla ses kaydı yapıp birleştirebileceğiniz çok oyunculu parti oyunu.

---

## 📑 İçindekiler
1. [Özellikler](#-özellikler)
2. [Sistem Gereksinimleri](#-sistem-gereksinimleri)
3. [Hızlı Başlangıç (Kurulum)](#-hızlı-başlangıç-kurulum)
4. [Kullanıcı Girişi ve Admin Paneli](#-kullanıcı-girişi-ve-admin-paneli)
5. [Nasıl Oynanır? (Oyun Akışı)](#-nasıl-oynanır-oyun-akışı)
6. [Yeni Sahne ve Video Ekleme](#-yeni-sahne-ve-video-ekleme)
7. [Mimarisi & Güvenlik](#-mimari--güvenlik)
8. [Testleri Çalıştırma](#-testleri-çalıştırma)

---

## ✨ Özellikler

- **P2P WebRTC Oyun Motoru:** PeerJS ve WebRTC DataChannels üzerinden sunucuya hiçbir ses trafiği bindirmeden doğrudan oyuncular arası senkronizasyon.
- **56 Popüler Türk Meme Sahnesi:** Meta Demucs (HTDemucs) ile insan sesleri silinmiş, arka plan müzikleri ve beatleri korunmuş hazır sahne kütüphanesi (Kurtlar Vadisi, Ezel, Sıfır Bir, Kolpaçino, Technopat vb.).
- **HTTP 206 Partial Content Streaming:** `server.py` üzerinde çok iş parçacıklı (`ThreadingHTTPServer`) ve Range-Request desteği ile 10-50ms hızında kilitlenmesiz video akışı.
- **Kapalı Kullanıcı Sistemi (Auth):** Rastgele dış kayıt kapalı; yalnızca Admin tarafından tanımlanan kullanıcılar şifreleriyle girebilir.
- **İki Fazlı Dublaj Akışı:** Önce sahneyi izleme ve prova, ardından sessiz videoda mikrofona canlı dublaj kaydı.
- **Ritim & Karaoke HUD Barı:** Replik zamanlamasını milimetrik gösteren trafik ışığı (`HAZIRLAN` / `ŞİMDİ KONUŞ`) ve karaoke dolum barı.
- **Seyirci Modu & Prömiyer:** Kalabalık arkadaş grupları için kayıt gerektirmeyen seyirci modu ve Web Audio API ile tek tıkla videolu dublaj indirme.
- **3 Dinamik Koyu Tema:** Sinema/Netflix Kırmızı, Stüdyo Amber ve Cyberpunk Neon paletleri.

---

## 💻 Sistem Gereksinimleri

- **İşletim Sistemi:** Windows 10/11, macOS veya Linux (Ubuntu 20.04+ önerilir).
- **Python:** Python 3.8 veya daha güncel bir sürüm (Herhangi bir `pip install` paketine ihtiyaç duymaz, standart kütüphanelerle çalışır).
- **Tarayıcı:** Google Chrome, Brave, Edge veya Safari (Web Audio API ve WebRTC destekli modern tarayıcılar).
- **Mikrofon:** Dublaj kaydı yapacak oyuncular için bir mikrofon.

---

## 🚀 Hızlı Başlangıç (Kurulum)

### 1. Projeyi Klonlayın:
```bash
git clone https://github.com/Miras1v/Dublaj-Oyunu.git
cd Dublaj-Oyunu
```

### 2. Sunucuyu Başlatın:
**Windows için:**
```bash
start.bat
```
*(veya doğrudan terminalden)*
```bash
python server.py
```

### 3. Tarayıcınızda Açın:
Tarayıcınızı açıp şu adrese gidin:
```text
http://localhost:3000
```

---

## 🔑 Kullanıcı Girişi ve Admin Paneli
 
Sistem yetkisiz yabancıların erişimini engellemek için kapalı davet/auth mimarisiyle gelir. Güvenlik gereği kullanıcı veritabanı (`data/users.json`) Git reposuna dahil edilmemiştir (`.gitignore`).
 
### İlk Çalıştırma & Yönetici Hesabı:
Sunucuyu (`python server.py`) **ilk kez başlattığınızda**, `data/users.json` dosyası yoksa sistem otomatik olarak güvenli bir başlangıç yöneticisi oluşturur:
- **Kullanıcı Adı:** `admin`
- **Geçici Başlangıç Şifresi:** `admin123`
 
*(İsteğe bağlı olarak `data/users.example.json` dosyasını `data/users.json` olarak kopyalayarak da kendi kullanıcılarınızı tanımlayabilirsiniz).*

### Arkadaşlarınıza Hesap Açma:
1. Admin hesabınızla giriş yapın.
2. Sağ üstteki **`⚙️ Yönetim Paneli`** butonuna tıklayın.
3. **"Kullanıcı Yönetimi"** sekmesine geçin.
4. Arkadaşınız için bir `Kullanıcı Adı`, `Şifre` ve `Rol (Oyuncu)` belirleyip **"Hesap Oluştur"** deyin.
5. Arkadaşınız bu bilgilerle giriş yapabilir.

---

## 🎮 Nasıl Oynanır? (Oyun Akışı)

1. **Giriş Yapın:** Kullanıcı adı ve şifrenizle giriş yapın.
2. **Oyun Modunu Seçin:**
   - **🚀 Oyun Başlat (Host Ol):** Yeni bir oda kurar ve size özel bir `DUB-XXXX` oda kodu üretir.
   - **🎮 Oyuna Katıl:** Arkadaşınızın verdiği oda kodunu girerek lobiye bağlanın.
   - **🎯 Solo Mod:** Tek başınıza sahneleri açıp antrenman yapın.
3. **Rolünüzü Seçin:** Lobide yer alan karakterlerden birini seçin (Örn: Çakır, Testere Necmi).
4. **Sahneyi Seçin:** Host 56 popüler Türk meme sahnesinden birini başlatır.
5. **Aşama 1 (İzle & Dinle):** Orijinal video sesli şekilde oynar, repliklerin ritmine alışın.
6. **Aşama 2 (Sessiz Videoda Dublaj Yap):** Orijinal insan sesleri susturulur, arka plan beatleri çalar; HUD sizi yönlendirir:
   - `🟡 HAZIRLAN`: Sıradaki repliğe 1.8 saniye kala sarı ışık yanar.
   - `🔴 ŞİMDİ KONUŞ!`: Konuşma anında kırmızı kayıt rozeti ve karaoke barı dolar.
7. **Prömiyer Sineması:** Dublaj bittiğinde tüm oyuncuların sesleri birleştirilir ve ortaya çıkan yeni video birlikte izlenir.
8. **🎬 Videolu Dublajı İndir:** Beğendiğiniz performansı tarayıcı içinde birleştirip tek tıkla `.webm` veya `.mp4` olarak indirin.

---

## ⚙️ Yeni Sahne ve Video Ekleme

Kendi videolarınızı oyuna dahil etmek çok basittir:
1. Admin panelini açın (`⚙️ Yönetim Paneli`).
2. **"Sahne & Transkript"** sekmesine gelin.
3. Yeni MP4 videosunu yükleyin, replikleri ve saniyelerini girin.
4. **"📁 Klasöre Kalıcı Kaydet"** butonuna basın. Sunucu videoyu `assets/videos/` altına işler, `scenes.json` ve `scenes.js` dosyalarını otomatik günceller.

---

## 🛡️ Mimari & Güvenlik

- **Şifreleme:** Kullanıcı şifreleri `salt + hashlib.sha256` ile özetlenir. Düz metin şifre asla saklanmaz.
- **Timing-Attack Koruması:** Doğrulamalarda `secrets.compare_digest` kullanılır.
- **Oturumlar:** 32-byte (64 hex karakter) kriptografik Bearer token'lar.
- **Hafiflik:** Sıfır harici Python paketi. Düşük bellek tüketimi (~50-80 MB RAM).

---

## 🧪 Testleri Çalıştırma

Kod tabanının bütünlüğünü ve 11 kategorilik mimari standartları test etmek için:

```bash
node test_suite.js
```

---

## 📄 Lisans

Bu proje kişisel eğlence ve eğitim amaçlı geliştirilmiştir. Videolar ilgili hak sahiplerine aittir.
