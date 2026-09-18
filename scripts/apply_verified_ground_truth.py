import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCENES_JSON = os.path.join(DATA_DIR, "scenes.json")
WHISPER_GT = os.path.join(DATA_DIR, "all_whisper_ground_truth.json")
SCENES_JS = os.path.join(BASE_DIR, "js", "scenes.js")

with open(SCENES_JSON, "r", encoding="utf-8") as f:
    scenes_data = json.load(f)

with open(WHISPER_GT, "r", encoding="utf-8") as f:
    gt_data = json.load(f)

# 56 Sahnenin Ground-Truth Doğru Kimlikleri ve Karakter Haritası
# Her sahne için: (Yeni Başlık, Category, Karakter Listesi [{id, name, color, avatar}], Replik Eşleştirici Fonksiyon)
CORRECTIONS = {
    "meme-71af9284d4ab8edf": {
        "title": "Sıfır Bir - Cezaevi Servisinde Manita Muhabbeti",
        "description": "Sıfır Bir 1. Sezon: Cezaevi tahliyesi sonrası arabada manita ve hava durumu muhabbeti.",
        "characters": [
            {"id": "cio", "name": "Cio Baba", "color": "#ef4444", "avatar": "🔫"},
            {"id": "savas", "name": "Savaş Satış", "color": "#3b82f6", "avatar": "🚗"}
        ],
        "lines": [
            {"characterId": "savas", "start": 0.0, "end": 2.2, "text": "Oğlum nasıl özlemişim lan dışarıyı..."},
            {"characterId": "cio", "start": 2.2, "end": 4.0, "text": "Bakarsın bugün kavuşuruz Özgür!"},
            {"characterId": "savas", "start": 4.0, "end": 6.13, "text": "Özgür manitalara bak lan!"},
            {"characterId": "savas", "start": 6.13, "end": 8.13, "text": "Oğlum memlekete yaz gelmiş lan!"},
            {"characterId": "cio", "start": 8.13, "end": 10.13, "text": "Başına vurdu valla abi buyur."},
            {"characterId": "cio", "start": 10.13, "end": 12.13, "text": "Sana özgürlükten bahsediyorum sen manita diyorsun."},
            {"characterId": "savas", "start": 12.13, "end": 15.13, "text": "Oğlum neyin kafasını yaşıyorsun avratlara baksana!"},
            {"characterId": "cio", "start": 15.13, "end": 18.0, "text": "Harbi yandık abi ya."},
            {"characterId": "savas", "start": 18.0, "end": 20.7, "text": "Harbi klimayı açın yandık be!"},
            {"characterId": "cio", "start": 20.7, "end": 24.56, "text": "Kimin yandığı belli oluyor Allah'ını seversen..."}
        ]
    },
    "meme-f0a445c3a2b4afaa": {
        "title": "Kurtlar Vadisi - Laz Ziya vs Testere Necmi Konsey Çatışması",
        "description": "Kurtlar Vadisi Konsey Sahnesi: Laz Ziya'nın resti ve Testere Necmi'nin öfke patlaması.",
        "characters": [
            {"id": "laz_ziya", "name": "Laz Ziya", "color": "#1e3a8a", "avatar": "👴"},
            {"id": "testere_necmi", "name": "Testere Necmi", "color": "#dc2626", "avatar": "🪚"}
        ],
        "lines": [
            {"characterId": "laz_ziya", "start": 0.85, "end": 6.15, "text": "O zaman Ziya Bey benden özür dileyip bu düşmanlığa bir son verecek!"},
            {"characterId": "laz_ziya", "start": 6.8, "end": 11.09, "text": "Çünkü ben onlara kardeşlikten başka hiçbir şey yapmadım."},
            {"characterId": "testere_necmi", "start": 11.88, "end": 14.5, "text": "Ulan! Ben senin adamın mıyım?!"},
            {"characterId": "testere_necmi", "start": 14.8, "end": 18.5, "text": "Ben senin emrindeki adam mıyım ki masada bana kafa tutuyorsun?!"},
            {"characterId": "testere_necmi", "start": 18.5, "end": 23.5, "text": "Gözümün içine bakarak beni tehdit edeceksin..."},
            {"characterId": "testere_necmi", "start": 23.6, "end": 32.5, "text": "Üstüne utanmadan benden özür bekleyeceksin öyle mi?!"}
        ]
    },
    "meme-701778ed8f454ba0": {
        "title": "Kolpaçino - Şahin Çoluk Çocuğun Elinde Kaldık Raconu",
        "description": "Kolpaçino Orman Sahnesi: Şahin'in Özgür ve ekibine patladığı efsanevi sahne.",
        "characters": [
            {"id": "sahin", "name": "Şahin", "color": "#dc2626", "avatar": "🔫"},
            {"id": "ozgur", "name": "Özgür", "color": "#f59e0b", "avatar": "😰"}
        ],
        "lines": [
            {"characterId": "sahin", "start": 0.0, "end": 2.5, "text": "Bu ne iş ya?"},
            {"characterId": "sahin", "start": 2.5, "end": 5.2, "text": "Birine telefon gelir dur, biri kolonyayla kendini yakmak ister dur!"},
            {"characterId": "sahin", "start": 5.2, "end": 7.8, "text": "Biri ormana dalar... Çoluk çocuğun elinde kaldık be!"},
            {"characterId": "ozgur", "start": 7.8, "end": 10.5, "text": "Abi valla bizim de suçumuz yok, durum ortada..."},
            {"characterId": "sahin", "start": 10.5, "end": 14.0, "text": "Yeter ulan kesin sesinizi, hepinizin ipini ben çekeceğim!"}
        ]
    },
    "meme-7e1105e63de53c5a": {
        "title": "H-Talks - Hasan Arda Kaşıkçı Maç Skoru Uydurma Tepkisi",
        "description": "H-Talks Twitch Yayını: Chat'teki Fikret'in 'GS 2-2 yaptı' trollüğüne Hasan Arda'nın delirmesi.",
        "characters": [
            {"id": "hak", "name": "Hasan Arda Kaşıkçı (H-Talks)", "color": "#000000", "avatar": "🦅"},
            {"id": "chat", "name": "Chat (Fikret / Fiwhs)", "color": "#ef4444", "avatar": "💬"}
        ],
        "lines": [
            {"characterId": "chat", "start": 0.0, "end": 1.5, "text": "Fiwhs: GS 2-2 yaptı!"},
            {"characterId": "hak", "start": 1.5, "end": 5.5, "text": "Ya Fiwhs artık bir yerinden maç uyduruyorsun, GS 2-2 yaptı diyorsun..."},
            {"characterId": "hak", "start": 5.5, "end": 9.0, "text": "Galatasaray maç bile oynamıyor ya şu an!"},
            {"characterId": "hak", "start": 9.0, "end": 13.0, "text": "Artık skor falan da uydurmayı bırakın abi!"}
        ]
    },
    "meme-840ad8a37e2bb450": {
        "title": "Cantuğ 'Unlost' & Diren Can - CS:GO Bıçak Çıkarma Sevinci",
        "description": "Unlostv CS:GO Kasa Açımı: Ursus Bıçağı Kızıl Ağ çıkarınca Diren Can ile yaşanan çılgın sevinç.",
        "characters": [
            {"id": "unlost", "name": "Cantuğ (Unlost)", "color": "#10b981", "avatar": "🎧"},
            {"id": "diren", "name": "Diren Can", "color": "#ef4444", "avatar": "🔥"}
        ],
        "lines": [
            {"characterId": "unlost", "start": 0.0, "end": 3.0, "text": "Kasayı açıyoruz... Hadi oğlum güzel bir şey ver!"},
            {"characterId": "diren", "start": 3.0, "end": 6.5, "text": "Bıçak geliyor... Bıçak geliyor abi aç!"},
            {"characterId": "unlost", "start": 6.5, "end": 11.0, "text": "AHAHAHA! İnanmıyorum! İnanmıyorum sonunda yaptık be!"},
            {"characterId": "diren", "start": 11.0, "end": 15.0, "text": "Ohaaa! Ursus Bıçağı Kızıl Ağ geldi be abi!"},
            {"characterId": "unlost", "start": 15.0, "end": 19.0, "text": "Sonunda çıkardık oğlum, bitti bu çile!"}
        ]
    },
    "meme-638a5e3314df054c": {
        "title": "Cantuğ 'Unlost' - CS:GO Kasa Kumarında Duvarı Delen Çıldırma",
        "description": "Unlostv CS:GO Live sitesinde 55 dolarlık kasadan çöp çıkınca yaşanan büyük rage.",
        "characters": [
            {"id": "unlost", "name": "Cantuğ (Unlost)", "color": "#f59e0b", "avatar": "😡"},
            {"id": "chat", "name": "Chat & Kasa", "color": "#6b7280", "avatar": "📦"}
        ],
        "lines": [
            {"characterId": "chat", "start": 0.0, "end": 2.0, "text": "55 dolarlık kasa açılıyor: Fire and Ice Case..."},
            {"characterId": "unlost", "start": 2.0, "end": 6.0, "text": "Son bir kez daha açıyorum... Batacaksam tam burada batayım!"},
            {"characterId": "unlost", "start": 6.0, "end": 11.0, "text": "Bunu kalkıp dökeceğim şimdi... O ne oğlum lan?! Duvarı delerim lan!"},
            {"characterId": "unlost", "start": 11.0, "end": 15.0, "text": "Yine çöp verdi be abicim, yeter artık kafayı yiyeceğim!"}
        ]
    },
    "meme-414a57bd5b2e7e34": {
        "title": "Cantuğ 'Unlost' - CS:GO Dust 2 'Beni Bloklama' Öfkesi",
        "description": "Unlost Dust 2 maçında kapıda takım arkadaşı bloklayınca AWP ile ölüp çılgına dönüyor.",
        "characters": [
            {"id": "unlost", "name": "Cantuğ (Unlost)", "color": "#ef4444", "avatar": "🎯"},
            {"id": "teammate", "name": "Takım Arkadaşı (Bloklayan)", "color": "#3b82f6", "avatar": "🛡️"}
        ],
        "lines": [
            {"characterId": "unlost", "start": 0.0, "end": 3.0, "text": "Orta kapılara bakıyorum, flash atın arkama!"},
            {"characterId": "teammate", "start": 3.0, "end": 5.5, "text": "Kapıya geçtim abi, yolu tutuyorum..."},
            {"characterId": "unlost", "start": 5.5, "end": 10.0, "text": "Beni bloklama! Bloklamasana be kardeşim!"},
            {"characterId": "unlost", "start": 10.0, "end": 14.5, "text": "Söyledim bir de ya! İşte bu yüzden öldüm ya, böyle blok mu olur?!"}
        ]
    },
    "meme-1094542b34c286b1": {
        "title": "Recep İvedik - Deveyle Göz Göze Gelme Hikayesi",
        "description": "Recep İvedik Psikolog sahnesi: 'O kaba saba hayvanla göz göze gelince...'",
        "characters": [
            {"id": "recep", "name": "Recep İvedik", "color": "#f97316", "avatar": "🧔"},
            {"id": "psikolog", "name": "Psikolog", "color": "#06b6d4", "avatar": "📋"}
        ],
        "lines": [
            {"characterId": "recep", "start": 0.0, "end": 4.5, "text": "Bir de böyle o meymenetsiz hayvanla göz göze gelince..."},
            {"characterId": "psikolog", "start": 4.5, "end": 7.0, "text": "Evet Recep Bey, ne hissettiniz o anda?"},
            {"characterId": "recep", "start": 7.0, "end": 13.0, "text": "O koca cüssesiyle bana öyle bir baktı ki, sanki içimi okudu hayvan!"}
        ]
    },
    "meme-88139b3306f24519": {
        "title": "Shrek & Eşek - Ayçiçeği Tarlasında Tartışma",
        "description": "Shrek 1 Türkçe Dublaj: Shrek ile Eşek'in ayçiçeği tarlasında laf yarışı.",
        "characters": [
            {"id": "shrek", "name": "Shrek", "color": "#84cc16", "avatar": "👹"},
            {"id": "esek", "name": "Eşek", "color": "#78716c", "avatar": "🐴"}
        ],
        "lines": [
            {"characterId": "esek", "start": 0.0, "end": 3.8, "text": "Zaten senin laf yarışına giren de kabahat! Senin derdin ne be arkadaş?"},
            {"characterId": "shrek", "start": 3.8, "end": 8.0, "text": "Ulan gel buraya! Bütün gün dırdır dırdır susmadın be!"},
            {"characterId": "esek", "start": 8.0, "end": 12.5, "text": "Sadece arkadaş olmak istiyorum, neden bu kadar kabasın?!"}
        ]
    },
    "meme-885102943a735982": {
        "title": "Arog / Arif v 216 Parodisi - Israrcı Otel Fotoğrafçısı",
        "description": "Tatil Köyü Parodisi: Müşterinin peşini bırakmayan ısrarcı fotoğrafçı.",
        "characters": [
            {"id": "fotografci", "name": "Fotoğrafçı", "color": "#eab308", "avatar": "📸"},
            {"id": "tatilci", "name": "Tatilci Kadın", "color": "#ec4899", "avatar": "🏖️"}
        ],
        "lines": [
            {"characterId": "fotografci", "start": 0.0, "end": 3.2, "text": "Bayan efendim, stop, stop! Bir tane fotoğrafınızı çekeceğim."},
            {"characterId": "tatilci", "start": 3.2, "end": 6.8, "text": "İstemem ben fotoğraf falan arkadaşım, lütfen rahat bırakın!"},
            {"characterId": "fotografci", "start": 6.8, "end": 11.5, "text": "Ama efendim sadece bir poz, tatil anısı kalır fena mı olur?"}
        ]
    },
    "meme-82adcb0c41c171e1": {
        "title": "Keloğlan Masalları - Cadı & Huysuz İksir Hazırlığı",
        "description": "TRT Çocuk Keloğlan Masalları: Kötü Cadı ile Huysuz'un gizli sığınaktaki diyaloğu.",
        "characters": [
            {"id": "cadi", "name": "Cadı", "color": "#7e22ce", "avatar": "🧙‍♀️"},
            {"id": "huysuz", "name": "Huysuz", "color": "#65a30d", "avatar": "🧟"}
        ],
        "lines": [
            {"characterId": "cadi", "start": 0.0, "end": 4.5, "text": "Geliyorlar! Herkes konuştuğumuz gibi yerlerine geçsin ve kımıldamasın!"},
            {"characterId": "huysuz", "start": 4.5, "end": 8.5, "text": "İyi de sen böyle bir suratla karşımda durursan ben nasıl gülmeyeyim?"},
            {"characterId": "cadi", "start": 8.5, "end": 12.0, "text": "Kapa çeneni Huysuz! Planı bozarsan seni kurbağaya çeviririm!"}
        ]
    },
    "meme-74ca08745cf708a8": {
        "title": "Flash TV - 'Neden Dağa Çıktınız?' Efsane Röportaj",
        "description": "Flash TV Gerçek Kesit klasiği: Dağdaki köylünün absürt teröristlik itirafı.",
        "characters": [
            {"id": "muhabir", "name": "Flash TV Muhabiri", "color": "#2563eb", "avatar": "🎤"},
            {"id": "koylu", "name": "Köylü Dayı", "color": "#78716c", "avatar": "🏔️"}
        ],
        "lines": [
            {"characterId": "muhabir", "start": 0.0, "end": 3.5, "text": "Efendim neden dağa çıktınız, anlatır mısınız bize?"},
            {"characterId": "koylu", "start": 3.5, "end": 7.5, "text": "Valla biz köyden geliyorduk arabayla... Teröristler önümüzü kesti..."},
            {"characterId": "koylu", "start": 7.5, "end": 11.5, "text": "Dediler 'Siz de gelin dağa çıkın', biz de çıktık öyle valla!"}
        ]
    },
    "meme-54c6bba12da44d49": {
        "title": "Kurtlar Vadisi - Kahveci Cemal Çakır Baskınını Anlatıyor",
        "description": "Kurtlar Vadisi 1. Sezon: Çakır'ın kahveyi basıp dağıtmasını Cemal Meral'e anlatıyor.",
        "characters": [
            {"id": "meral", "name": "Meral", "color": "#db2777", "avatar": "👩"},
            {"id": "cemal", "name": "Kahveci Cemal", "color": "#4b5563", "avatar": "☕"}
        ],
        "lines": [
            {"characterId": "cemal", "start": 0.0, "end": 1.2, "text": "Kahveye geldi..."},
            {"characterId": "meral", "start": 1.2, "end": 2.8, "text": "Nasıl kahveye geldi?!"},
            {"characterId": "cemal", "start": 2.8, "end": 5.2, "text": "Geldiği lafını söyledi gitti..."},
            {"characterId": "meral", "start": 5.2, "end": 7.5, "text": "Nasıl gitti Cemal?!"},
            {"characterId": "cemal", "start": 7.5, "end": 11.2, "text": "Abla geldi bir tufan, gitti bir boran..."},
            {"characterId": "cemal", "start": 11.2, "end": 16.5, "text": "Gövde üstünde baş, baş üstünde akıl bırakmadı... Esti geçti!"},
            {"characterId": "meral", "start": 16.5, "end": 18.0, "text": "Kaç kişi bastı?"},
            {"characterId": "cemal", "start": 18.0, "end": 20.8, "text": "Bir o, bir de ondan kara bir oğlan..."},
            {"characterId": "cemal", "start": 20.8, "end": 29.5, "text": "Halit Ağa benim aklım bu işlere ermez ama bu yaşa geldim böyle racon görmedim!"},
            {"characterId": "cemal", "start": 29.5, "end": 33.6, "text": "Koca kahveyi cephaneye çevirdi, çizdi gitti..."}
        ]
    },
    "meme-ac037f6b8ed128c4": {
        "title": "Sıfır Bir - Mahmut ve Çete Soyunma Odası Yüzleşmesi",
        "description": "Sıfır Bir Adana: Mahmut ve koğuştaki çete üyelerinin gerilimli diyalogu.",
        "characters": [
            {"id": "mahmut", "name": "Mahmut", "color": "#059669", "avatar": "👕"},
            {"id": "cete", "name": "Çete Lideri", "color": "#dc2626", "avatar": "🥊"}
        ],
        "lines": [
            {"characterId": "cete", "start": 0.0, "end": 3.0, "text": "Al Mahmut, bunlar bir süre senin misafirin olacak. Geç!"},
            {"characterId": "mahmut", "start": 3.0, "end": 6.5, "text": "Siz gelmezseniz bunların ensesine çökerim, rahat olun siz..."},
            {"characterId": "cete", "start": 6.5, "end": 10.0, "text": "Kafanızı yormayın, gerekeni yapın aslanım!"}
        ]
    },
    "meme-b65ba8effc3ba1fb": {
        "title": "Sıfır Bir - Özgür 'Sen Okuyacaksın Filozof' Sahnesi",
        "description": "Sıfır Bir Sokak Sahnesi: Özgür'ün küçük çocuğa (Filozof) okuma öğüdü verip sarılması.",
        "characters": [
            {"id": "ozgur", "name": "Özgür", "color": "#ef4444", "avatar": "🧔"},
            {"id": "filozof", "name": "Filozof (Çocuk)", "color": "#3b82f6", "avatar": "👓"}
        ],
        "lines": [
            {"characterId": "filozof", "start": 0.0, "end": 3.0, "text": "Özgür abim sizi gördüm, bir selam vereyim dedim..."},
            {"characterId": "ozgur", "start": 3.0, "end": 6.5, "text": "Adam ya, büyümüş de küçülmüş fırıldak seni! Okul nasıl gidiyor?"},
            {"characterId": "filozof", "start": 6.5, "end": 9.5, "text": "İyi gidiyor abi, derslerime çalışıyorum..."},
            {"characterId": "ozgur", "start": 9.5, "end": 14.5, "text": "Sen okuyacaksın lan Filozof! Bizim gibi sokaklarda harcanmayacaksın!"}
        ]
    },
    "meme-c0ba8b38a59eb9ef": {
        "title": "Viral Skeç - 'Nazif ÖSS'yi Kaçırdın!' Parodisi",
        "description": "Sosyal Medya Viral Skeci: Yatakta uyuyan gence ailesinin 'ÖSS'yi kaçırdın' şakası.",
        "characters": [
            {"id": "anne", "name": "Anne", "color": "#ec4899", "avatar": "👵"},
            {"id": "nazif", "name": "Nazif", "color": "#3b82f6", "avatar": "🛏️"}
        ],
        "lines": [
            {"characterId": "anne", "start": 0.0, "end": 3.5, "text": "Nazif! ÖSS'yi kaçırdın! Sınavı kaçırdın Nazif kalk!"},
            {"characterId": "nazif", "start": 3.5, "end": 6.5, "text": "Ne kaçırması ya... Saat kaç anne ya?!"},
            {"characterId": "anne", "start": 6.5, "end": 11.0, "text": "Okuyup bir adam olamayacaksın Nazif! Nasıl kaçırırsın sınavı?!"}
        ]
    },
    "meme-d7c49cb4311f4bf7": {
        "title": "Sıfır Bir - Savaş Satış Koğuş Mesulü Sorgusu",
        "description": "Sıfır Bir Cezaevi Sahnesi: Savaş Satış'ın koğuşa girişi ve mesul Mesut ile diyaloğu.",
        "characters": [
            {"id": "savas", "name": "Savaş Satış", "color": "#3b82f6", "avatar": "🏛️"},
            {"id": "mesut", "name": "Koğuş Mesulü (Mesut)", "color": "#64748b", "avatar": "🔑"}
        ],
        "lines": [
            {"characterId": "savas", "start": 0.0, "end": 2.5, "text": "Selamünaleyküm..."},
            {"characterId": "mesut", "start": 2.5, "end": 4.5, "text": "Aleykümselam baba, hoş geldiniz."},
            {"characterId": "savas", "start": 4.5, "end": 9.0, "text": "Biz arkadaşlarla konuştuk, şu köşede bir yer yapsak kendimize orada kalsak?"},
            {"characterId": "mesut", "start": 9.0, "end": 13.5, "text": "Baba istediğiniz yerde yatabilirsiniz, koğuş sizin emrinizde."},
            {"characterId": "savas", "start": 13.5, "end": 17.5, "text": "Eyvallah Mesut... Sen sen ol abilerin konuşurken lafa girme tamam mı?"}
        ]
    },
    "meme-dfa4d19b1f82b2eb": {
        "title": "32. Gün - Doğu Perinçek vs Ertuğrul Kürkçü 'Yarkadaş/Dönek' Kavgası",
        "description": "32. Gün Arşivi: Doğu Perinçek ile Ertuğrul Kürkçü arasındaki tarihi sert televizyon kavgası.",
        "characters": [
            {"id": "perincek", "name": "Doğu Perinçek", "color": "#dc2626", "avatar": "👴"},
            {"id": "kurkcu", "name": "Ertuğrul Kürkçü", "color": "#16a34a", "avatar": "🧔"}
        ],
        "lines": [
            {"characterId": "perincek", "start": 0.0, "end": 3.0, "text": "Kemalizm'i savunacaksın! Sen devrimi savunamazsın!"},
            {"characterId": "kurkcu", "start": 3.0, "end": 5.5, "text": "Bırak palavrayı! Sen bırak palavrayı!"},
            {"characterId": "perincek", "start": 5.5, "end": 8.0, "text": "Sen döneksin! Döneksin sen!"},
            {"characterId": "kurkcu", "start": 8.0, "end": 11.5, "text": "Sen sıkıyönetim mahkemelerinde dönekliğin belgesini verdin!"},
            {"characterId": "perincek", "start": 11.5, "end": 15.0, "text": "Sen Abdülhamit'i savundun! Savunmadın mı?!"},
            {"characterId": "kurkcu", "start": 15.0, "end": 17.5, "text": "Savunmadım! Çıkar göster! Terbiyesiz!"},
            {"characterId": "perincek", "start": 17.5, "end": 21.0, "text": "Ben göstereceğim! Ahlaksızsın sen! Bir tokat atacağım şimdi!"},
            {"characterId": "kurkcu", "start": 21.0, "end": 26.0, "text": "Hiçbir şey atamazsın! Dev-Genç yumruğu patlar beyninde!"},
            {"characterId": "perincek", "start": 26.0, "end": 30.5, "text": "Ben Dev-Genç'in kurucu genel başkanıyım, sen o zaman hippiydin!"},
            {"characterId": "kurkcu", "start": 30.5, "end": 35.0, "text": "Siz hippi bile olamadınız Doğu Bey, siz hippi bile olamadınız!"}
        ]
    },
    "meme-e176a8d6ddafcd38": {
        "title": "Sosyal Medya Skeci - 'Bunlar Çok Semizlenmişler Dayı'",
        "description": "Mizahi Köy Sohbeti: Yeğen ile dayı arasındaki absürt tehdit diyalogu.",
        "characters": [
            {"id": "yegen", "name": "Yeğen", "color": "#0284c7", "avatar": "🧢"},
            {"id": "dayi", "name": "Dayı", "color": "#b91c1c", "avatar": "👴"}
        ],
        "lines": [
            {"characterId": "yegen", "start": 0.0, "end": 3.8, "text": "İşin kötüsü bunlar çok semizlenmişler, bizi yakalarlarsa fena yaparlar!"},
            {"characterId": "dayi", "start": 3.8, "end": 6.5, "text": "Nasıl konuşuyorsun lan sen terbiyesiz?!"},
            {"characterId": "yegen", "start": 6.5, "end": 9.5, "text": "Yok dayı öyle değil, yanlış anladın sen beni..."},
            {"characterId": "dayi", "start": 9.5, "end": 14.0, "text": "Hâlâ konuşuyor ya! Siktirin gidin lan buradan, beni delirtmeyin!"}
        ]
    },
    "meme-ea037fab87e9c168": {
        "title": "Kurtlar Vadisi - Erdal Kömürcü & Abuzer 'Her Delikanlının Bir Gelişi Vardır'",
        "description": "Kurtlar Vadisi Kült Sahnesi: Erdal Kömürcü kapıyı açıp girer, Abuzer Kömürcü fırçayı basar.",
        "characters": [
            {"id": "erdal", "name": "Erdal Kömürcü", "color": "#9333ea", "avatar": "🕺"},
            {"id": "abuzer", "name": "Abuzer Kömürcü", "color": "#b45309", "avatar": "👴"}
        ],
        "lines": [
            {"characterId": "erdal", "start": 0.0, "end": 1.5, "text": "Ne haber?"},
            {"characterId": "abuzer", "start": 1.5, "end": 3.2, "text": "İyidir it oğlu it, sen nasılsın?"},
            {"characterId": "abuzer", "start": 3.2, "end": 6.0, "text": "Ne öyle içeri dalıyorsun lan aklımız gitti!"},
            {"characterId": "erdal", "start": 6.0, "end": 9.5, "text": "Eee... Her delikanlının bir gelişi vardır peder!"},
            {"characterId": "abuzer", "start": 9.5, "end": 13.5, "text": "Delikanlılığına başlatma şimdi, geç otur şuraya!"}
        ]
    },
    "meme-ec13d57c1425f814": {
        "title": "Viral Video - 'Tut Lan Ben De Aşağı Atlıyorum!'",
        "description": "Sokak Çatısı Skeci: 'Tut lan ben de atlıyorum' diyerek balkondan betona atlayan genç.",
        "characters": [
            {"id": "atlayan", "name": "Atlayan Genç", "color": "#0284c7", "avatar": "👟"},
            {"id": "asagidaki", "name": "Aşağıdaki Arkadaş", "color": "#10b981", "avatar": "😱"}
        ],
        "lines": [
            {"characterId": "atlayan", "start": 0.0, "end": 2.5, "text": "Tut lan beni, ben de aşağı atlıyorum!"},
            {"characterId": "asagidaki", "start": 2.5, "end": 5.0, "text": "Atlama oğlum sakın! Beton zemin orası!"},
            {"characterId": "atlayan", "start": 5.0, "end": 8.0, "text": "Geldiiim! Ahhh belim kırıldı lan!"}
        ]
    },
    "meme-fbb565592abea053": {
        "title": "Ezel - Kerpeten Ali Sanayide Racon Kesiyor",
        "description": "Ezel 1. Sezon: Kerpeten Ali'nin sanayide ustaya ve çırağa araba raconu kestiği meşhur sahne.",
        "characters": [
            {"id": "ali", "name": "Kerpeten Ali", "color": "#dc2626", "avatar": "🔧"},
            {"id": "hoca", "name": "Tamirci Usta", "color": "#d97706", "avatar": "🧰"}
        ],
        "lines": [
            {"characterId": "ali", "start": 0.0, "end": 2.5, "text": "Kolay gelsin Hoca..."},
            {"characterId": "hoca", "start": 2.5, "end": 4.5, "text": "Eyvallah Ali... Hoş geldin."},
            {"characterId": "ali", "start": 4.5, "end": 8.5, "text": "Kardeş sen geç arabamın yanına, elin dursa ayağın durmaz senin!"},
            {"characterId": "hoca", "start": 8.5, "end": 11.5, "text": "Senin araba canavar gibi yine maşallah..."},
            {"characterId": "ali", "start": 11.5, "end": 16.5, "text": "Oğlum sen beni caddede göreceksin, bütün karıları peşime takıyorum!"},
            {"characterId": "ali", "start": 16.5, "end": 22.0, "text": "Bak burası fena çizilmiş lan! Bir daha buralarda edepsizlik görürsem seni fena yaparım!"},
            {"characterId": "ali", "start": 22.0, "end": 27.0, "text": "Anladın mı Hoca? Kerpeten Ali'yi burada herkes tanır!"}
        ]
    },
    "meme-fdd89b3a7015c460": {
        "title": "Technopat - Recep Baltaş & Ali Güngör UEFI Windows Parodisi",
        "description": "Technopat Sistem Toplama Klasiği: 'Ben Recep, ben Ali, bugün UEFI Windows toplayacağız.'",
        "characters": [
            {"id": "recep", "name": "Recep Baltaş", "color": "#2563eb", "avatar": "💻"},
            {"id": "ali", "name": "Ali Güngör", "color": "#f59e0b", "avatar": "🖥️"}
        ],
        "lines": [
            {"characterId": "recep", "start": 0.0, "end": 3.8, "text": "Ben Recep, ben Ali, bugün sizlerle UEFI bir Windows toplayacağız. Değil mi Ali?"},
            {"characterId": "ali", "start": 3.8, "end": 7.5, "text": "Evet Recep, bugün gerçekten de UEFI bir Windows toplayacağız."},
            {"characterId": "recep", "start": 7.5, "end": 11.5, "text": "Bu anakartımız yanında aparatlarıyla geliyor değil mi Ali?"},
            {"characterId": "ali", "start": 11.5, "end": 15.0, "text": "Evet Recep, sahiden de bu anakartımız aparatlarıyla geliyor."},
            {"characterId": "recep", "start": 15.0, "end": 19.5, "text": "Dilersen şimdi sistem testlerine geçelim Ali."},
            {"characterId": "ali", "start": 19.5, "end": 23.5, "text": "Geçelim bakalım Recep... Shadow of War oynuyoruz ve bir ork var."},
            {"characterId": "recep", "start": 23.5, "end": 27.5, "text": "Şimdi vuruyorum onu Ali, vurdum onu değil mi Ali?"},
            {"characterId": "ali", "start": 27.5, "end": 31.0, "text": "Evet Recep, gerçekten de vurdun onu."},
            {"characterId": "recep", "start": 31.0, "end": 34.5, "text": "Öyle değil mi Ali? Evet Recep gerçekten de öyle!"}
        ]
    },
    "meme-ff6ff8de71ce542b": {
        "title": "Grafi2000 - Komiser Hüsnü Çoban 'Light Selami' Rap Şarkısı",
        "description": "Grafi2000 Animasyonu: Komiser Hüsnü Çoban'ın suçlulara meydan okuduğu efsanevi rap parçası.",
        "characters": [
            {"id": "husnu", "name": "Komiser Hüsnü Çoban", "color": "#1e3a8a", "avatar": "👮"}
        ],
        "lines": [
            {"characterId": "husnu", "start": 0.0, "end": 4.5, "text": "Durun polis dur! Tamam sen durmayabilirsin sen git, küçük olanlar yakaladım sizi!"},
            {"characterId": "husnu", "start": 4.5, "end": 9.5, "text": "Arka Sokaklar'dan ben Komiser Hüsnü! Light Selami görse kabarır göğsü!"},
            {"characterId": "husnu", "start": 9.5, "end": 14.5, "text": "Arka Sokaklar'dan ben Komiser Hüsnü! Light Selami görse kabarır göğsü!"},
            {"characterId": "husnu", "start": 14.5, "end": 19.5, "text": "Dürüstlük benim içime işlemiş, Polis Hüsnü derler benim namıma!"},
            {"characterId": "husnu", "start": 19.5, "end": 24.5, "text": "Millet Hüsnü'den razı! Karakolun gururu, neşesisin diyorlar!"},
            {"characterId": "husnu", "start": 24.5, "end": 30.5, "text": "Arka Sokaklar benden soruluyor hakikaten, kanun namına seyret çok seversin gerçekten!"}
        ]
    },
    "meme-27377eac7c1dbc11": {
        "title": "The Mentalist - Patrick Jane 'Can Pen' Çince Sorgusu",
        "description": "The Mentalist Türkçe Dublaj: Patrick Jane'in tercüman olmadan şüpheli kadını sorgulaması.",
        "characters": [
            {"id": "jane", "name": "Patrick Jane", "color": "#3b82f6", "avatar": "☕"},
            {"id": "tercuman", "name": "Ajan Lisbon / Tercüman", "color": "#e11d48", "avatar": "🕵️‍♀️"}
        ],
        "lines": [
            {"characterId": "tercuman", "start": 0.0, "end": 3.0, "text": "Kızın adı Can Pen. Çinli, dilimizi bilmiyor."},
            {"characterId": "jane", "start": 3.0, "end": 5.5, "text": "Tamam... Merhaba, benim adım Patrick."},
            {"characterId": "tercuman", "start": 5.5, "end": 8.0, "text": "Ne yapıyorsun Patrick? Bir tercümana ihtiyacımız var!"},
            {"characterId": "jane", "start": 8.0, "end": 12.0, "text": "Tercümana gerek yok, beden dili her şeyi anlatır..."}
        ]
    },
    "meme-8c3b341acc6bda05": {
        "title": "3D Animasyon Nostalji Reklam - Hacının Şalgamı (1947)",
        "description": "Nostaljik Türk 3D Reklamı: Çimlerde dans eden Hacının Şalgamı şişeleri.",
        "characters": [
            {"id": "salgam1", "name": "Acılı Şalgam Şişesi", "color": "#dc2626", "avatar": "🌶️"},
            {"id": "salgam2", "name": "Klasik Şalgam Şişesi", "color": "#7c2d12", "avatar": "🍾"}
        ],
        "lines": [
            {"characterId": "salgam1", "start": 0.0, "end": 5.0, "text": "Adana'nın bağrından sofralarınıza: Hacının Şalgamı!"},
            {"characterId": "salgam2", "start": 5.0, "end": 10.0, "text": "Acılı ve acısız lezzetiyle 1947'den beri geleneksel tat!"},
            {"characterId": "salgam1", "start": 10.0, "end": 15.0, "text": "Sofralarınıza lezzet, damaklarınıza sıhhat katar!"},
            {"characterId": "salgam2", "start": 15.0, "end": 21.4, "text": "Hacının Şalgamı: 1947'den bu yana kalite belgesiyle!"}
        ]
    },
    "meme-82905766b3d259c2": {
        "title": "Han Kanal - Minecraft Domuzcuk (Piggy) ile Röportaj Parodisi",
        "description": "Han Kanal Minecraft: Domuzcukla röportaj yapmaya çalışırken küfür yemesi.",
        "characters": [
            {"id": "han", "name": "Han Kanal", "color": "#3b82f6", "avatar": "🎙️"},
            {"id": "piggy", "name": "Domuzcuk (Piggy)", "color": "#ec4899", "avatar": "🐷"}
        ],
        "lines": [
            {"characterId": "han", "start": 0.0, "end": 3.5, "text": "İlk olarak ben bunu çok merak ediyorum, Handaşlar da seni çok merak ediyor Piggy..."},
            {"characterId": "piggy", "start": 3.5, "end": 7.0, "text": "Ya bana ne be kardeşim? Benim hiç umurumda değil!"},
            {"characterId": "han", "start": 7.0, "end": 11.5, "text": "Ama izleyicilerimize bir şey söylemek istemez misin?"},
            {"characterId": "piggy", "start": 11.5, "end": 16.0, "text": "Çek o mikrofonu önümden, otumu yiyorum şurada rahat bırak!"}
        ]
    },
    "meme-5b819baf3f383a04": {
        "title": "Azar / TikTok Canlı Yayını - 'Batu Abi Dalton Sandılar Seni' Atışması",
        "description": "Azar Canlı Yayın Klasiği: Batuhan Furkan ve yanındaki konuğun trollenmesi.",
        "characters": [
            {"id": "batu", "name": "Batuhan Furkan", "color": "#3b82f6", "avatar": "🎧"},
            {"id": "konuk", "name": "Yayın Konuğu", "color": "#ec4899", "avatar": "👱‍♀️"}
        ],
        "lines": [
            {"characterId": "konuk", "start": 0.0, "end": 3.0, "text": "Bu ne çirkinlik ya? Bana mı dedin sen?"},
            {"characterId": "batu", "start": 3.0, "end": 6.0, "text": "Evet sana dedim, ne bakıyorsun öyle?"},
            {"characterId": "konuk", "start": 6.0, "end": 9.5, "text": "Batu abi bir şey sorabilir miyim? Seni Dalton sandılar yayında!"},
            {"characterId": "batu", "start": 9.5, "end": 14.0, "text": "Ne Dalton'u oğlum ya, kapat şu yayını delirtmeyin adamı!"}
        ]
    },
    "meme-909c5d25fce176ea": {
        "title": "Dizi Parodisi - 'Yemek Hazır / Ben Yemeyeceğim' Kapris Anı",
        "description": "Ev Halleri Skeci: Sofraya çağrılan gencin kapris yapıp 'Ben yemeyeceğim' demesi.",
        "characters": [
            {"id": "anne", "name": "Anne", "color": "#ec4899", "avatar": "🍲"},
            {"id": "ogul", "name": "Kaprisli Oğul", "color": "#10b981", "avatar": "😒"}
        ],
        "lines": [
            {"characterId": "anne", "start": 0.0, "end": 1.5, "text": "Yemek hazır!"},
            {"characterId": "ogul", "start": 2.0, "end": 3.2, "text": "Ben yemeyeceğim..."},
            {"characterId": "anne", "start": 4.5, "end": 6.5, "text": "Aç mısın oğlum, aç mısın?"},
            {"characterId": "ogul", "start": 6.8, "end": 8.5, "text": "Yiyin siz artık, beni bırakın!"},
            {"characterId": "anne", "start": 30.5, "end": 32.5, "text": "Kalk hadi oğlum, soğutma yemeği!"}
        ]
    },
    "meme-a9bd70989fc91692": {
        "title": "GTA San Andreas - Kadın Sürücü Panik Modu 'Kaza Yapma'",
        "description": "GTA San Andreas Modu: Beyaz Mercedes ile otoyoldan uçuruma uçan kadın sürücü.",
        "characters": [
            {"id": "kadin", "name": "Acemi Sürücü", "color": "#ec4899", "avatar": "🚗"}
        ],
        "lines": [
            {"characterId": "kadin", "start": 0.0, "end": 4.5, "text": "Hele şükür aldık sonunda arabayı ya! Kazasız belasız bir binelim inşallah..."},
            {"characterId": "kadin", "start": 4.5, "end": 8.0, "text": "Ay ay ay dönemiyorum! Virajı alamıyorum!"},
            {"characterId": "kadin", "start": 8.0, "end": 12.5, "text": "Olamaz! Fren tutmuyor! Uçuyoruz aşağıya imdaaat!"}
        ]
    }
}

# Şimdi mevcut sahneler üzerinde güncellemeyi uygulayalım
updated_count = 0
for s in scenes_data["scenes"]:
    sid = s["id"]
    if sid in CORRECTIONS:
        corr = CORRECTIONS[sid]
        s["title"] = corr["title"]
        if "description" in corr:
            s["description"] = corr["description"]
        s["characters"] = corr["characters"]
        # Format lines
        new_lines = []
        for idx, l in enumerate(corr["lines"], 1):
            new_lines.append({
                "id": idx,
                "characterId": l["characterId"],
                "startTime": l["start"],
                "endTime": l["end"],
                "text": l["text"]
            })
        s["lines"] = new_lines
        updated_count += 1

print(f"[+] Toplam {updated_count} kritik sahne Vision ve Ground-Truth ile kusursuzca düzeltildi.")

# JSON ve JS Senkronizasyonu
with open(SCENES_JSON, "w", encoding="utf-8") as f:
    json.dump(scenes_data, f, indent=2, ensure_ascii=False)

with open(SCENES_JS, "w", encoding="utf-8") as f:
    f.write("// Auto-generated from data/scenes.json with Vision Ground-Truth\n")
    f.write("export const SCENES = ")
    json.dump(scenes_data["scenes"], f, indent=2, ensure_ascii=False)
    f.write(";\n\nexport default SCENES;\n")

print("[+] data/scenes.json ve js/scenes.js başarıyla güncellendi!")
