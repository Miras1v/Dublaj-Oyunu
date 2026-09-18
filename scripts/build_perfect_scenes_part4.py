import os
import sys

PERFECT_SCENES_4 = {}

# 41. Sıfır Bir Mahmut Soyunma Odası
PERFECT_SCENES_4["meme-ac037f6b8ed128c4"] = {
    "title": "Sıfır Bir - Mahmut ve Çete Soyunma Odası Yüzleşmesi",
    "description": "Sıfır Bir Adana: Mahmut ve koğuştaki çete üyelerinin gerilimli diyalogu.",
    "characters": [
        {"id": "mahmut", "name": "Mahmut", "color": "#059669", "avatar": "👕"},
        {"id": "cete", "name": "Çete Lideri", "color": "#dc2626", "avatar": "🥊"}
    ],
    "lines": [
        {"characterId": "cete", "startTime": 0.0, "endTime": 3.46, "text": "Al Mahmut, bunlar bir süre senin misafirin olacak."},
        {"characterId": "cete", "startTime": 4.84, "endTime": 5.0, "text": "Geç!"},
        {"characterId": "mahmut", "startTime": 6.04, "endTime": 6.48, "text": "Bak hele."},
        {"characterId": "cete", "startTime": 6.96, "endTime": 7.3, "text": "Geç geç!"},
        {"characterId": "mahmut", "startTime": 7.44, "endTime": 10.18, "text": "Siz gelmezseniz bunların ensesine çökerim, rahat olun siz..."},
        {"characterId": "cete", "startTime": 10.5, "endTime": 12.38, "text": "Siz kafanızı yormayın kardeş."},
        {"characterId": "cete", "startTime": 13.8, "endTime": 16.42, "text": "Sağ salim gidin gelin inşallah."},
        {"characterId": "mahmut", "startTime": 16.94, "endTime": 18.52, "text": "İnşallah abi inşallah."},
        {"characterId": "mahmut", "startTime": 24.94, "endTime": 29.2, "text": "Kaşmerler sizi! Öyle plan etmekle olmuyor oğlum!"},
        {"characterId": "cete", "startTime": 32.06, "endTime": 34.74, "text": "Sakin ol Mahmut, bizim seninle bir işimiz yok."},
        {"characterId": "mahmut", "startTime": 37.26, "endTime": 43.24, "text": "Senin benimle işin yok da benim seninle işim var kahpe!"},
        {"characterId": "mahmut", "startTime": 44.94, "endTime": 47.32, "text": "Yiğitlik yapıyordunuz dışarıda oğlum, noldu?!"}
    ]
}

# 42. Sıfır Bir Filozof
PERFECT_SCENES_4["meme-b65ba8effc3ba1fb"] = {
    "title": "Sıfır Bir - Özgür 'Sen Okuyacaksın Filozof' Sahnesi",
    "description": "Sıfır Bir Sokak Sahnesi: Özgür'ün küçük çocuğa (Filozof) okuma öğüdü verip sarılması.",
    "characters": [
        {"id": "filozof", "name": "Filozof (Çocuk)", "color": "#3b82f6", "avatar": "👓"},
        {"id": "ozgur", "name": "Özgür", "color": "#ef4444", "avatar": "🧔"},
        {"id": "berto", "name": "Berto", "color": "#f59e0b", "avatar": "🧢"}
    ],
    "lines": [
        {"characterId": "filozof", "startTime": 0.0, "endTime": 3.18, "text": "Ne yapayım Özgür abim, sizi gördüm bir selam vereyim dedim."},
        {"characterId": "ozgur", "startTime": 3.56, "endTime": 6.12, "text": "Adam ya! Büyümüş de küçülmüş fırıldak seni! Okul nasıl gidiyor?"},
        {"characterId": "filozof", "startTime": 7.62, "endTime": 9.0, "text": "Bu seneden sonra bırakacağım Özgür abi."},
        {"characterId": "ozgur", "startTime": 9.92, "endTime": 13.36, "text": "Niye oğlum? Mahalleyi sen kurtaracaksın oğlum, okusana!"},
        {"characterId": "filozof", "startTime": 13.96, "endTime": 16.04, "text": "Annemin durumu yok, o da artık bırak çalış diyor."},
        {"characterId": "ozgur", "startTime": 16.76, "endTime": 17.38, "text": "Olur mu oğlum?!"},
        {"characterId": "ozgur", "startTime": 18.82, "endTime": 23.12, "text": "Konuşalım lan bunun anasıyla! Senin gibi zeki bir çocuk okuldan mı alınır lan?!"},
        {"characterId": "ozgur", "startTime": 24.14, "endTime": 26.9, "text": "Bak biz okumadık ne oldu? Bari siz okuyun lan!"},
        {"characterId": "ozgur", "startTime": 26.9, "endTime": 31.98, "text": "Berto kardeş konuş anasıyla, okul masraflarını biz karşılarız!"},
        {"characterId": "ozgur", "startTime": 32.64, "endTime": 35.76, "text": "Kendilerinin de ihtiyacı olursa hallederiz, kafasını yormasın."},
        {"characterId": "berto", "startTime": 35.88, "endTime": 39.8, "text": "Tamam kardeş ben yarın gider konuşurum, Filozof'u okulsuz bırakmayız sen rahat ol."},
        {"characterId": "ozgur", "startTime": 40.58, "endTime": 43.44, "text": "Oğlum Filozof! Sen okuyacaksın lan!"},
        {"characterId": "ozgur", "startTime": 44.04, "endTime": 46.92, "text": "Doktor olacaksın, mühendis olacaksın, savcı olacaksın, hakim olacaksın!"},
        {"characterId": "ozgur", "startTime": 47.36, "endTime": 50.78, "text": "Bizim mahallemizden de böyle insanlar çıkabileceğini göstereceksin! Tamam mı aslanım?"},
        {"characterId": "filozof", "startTime": 51.14, "endTime": 51.82, "text": "Tamam abi sinirlenmeyin."},
        {"characterId": "ozgur", "startTime": 51.82, "endTime": 55.52, "text": "Allah'ını severim lan senin! Hadi gidelim."}
    ]
}

# 43. Nazif ÖSS
PERFECT_SCENES_4["meme-c0ba8b38a59eb9ef"] = {
    "title": "Viral Skeç - 'Nazif ÖSS'yi Kaçırdın!' Parodisi",
    "description": "Sosyal Medya Viral Skeci: Yatakta uyuyan gence ailesinin 'ÖSS'yi kaçırdın' şakası.",
    "characters": [
        {"id": "anne", "name": "Anne", "color": "#ec4899", "avatar": "👵"},
        {"id": "nazif", "name": "Nazif", "color": "#3b82f6", "avatar": "🛏️"}
    ],
    "lines": [
        {"characterId": "anne", "startTime": 0.0, "endTime": 3.24, "text": "Nazif! ÖSS'yi kaçırdın!"},
        {"characterId": "anne", "startTime": 5.4, "endTime": 7.52, "text": "ÖSS'yi kaçırdın Nazif kalk!"},
        {"characterId": "nazif", "startTime": 8.16, "endTime": 10.42, "text": "Ya alıştınız her sabah ya..."},
        {"characterId": "anne", "startTime": 11.92, "endTime": 14.54, "text": "Okuyup bir adam olamayacaksın Nazif!"},
        {"characterId": "anne", "startTime": 18.7, "endTime": 21.42, "text": "Nasıl kaçırırsın ÖSS'yi Nazif?!"},
        {"characterId": "nazif", "startTime": 22.8, "endTime": 24.74, "text": "Kaçta başlıyordu ki ha?"},
        {"characterId": "anne", "startTime": 25.14, "endTime": 26.18, "text": "Saat kaç?!"},
        {"characterId": "nazif", "startTime": 27.02, "endTime": 27.42, "text": "On bir."},
        {"characterId": "anne", "startTime": 30.78, "endTime": 31.88, "text": "Çalışmış mıydın bari nasıl?"},
        {"characterId": "nazif", "startTime": 34.36, "endTime": 37.38, "text": "Çok yoğun bir tanem çalıştım dört ay..."},
        {"characterId": "nazif", "startTime": 38.72, "endTime": 40.4, "text": "Gece gündüz çalıştım ya..."}
    ]
}

# 44. Sıfır Bir Koğuş Mesulü
PERFECT_SCENES_4["meme-d7c49cb4311f4bf7"] = {
    "title": "Sıfır Bir - Savaş Satış Koğuş Mesulü Sorgusu",
    "description": "Sıfır Bir Cezaevi: Savaş'ın koğuş mesulü Mesut ile ranza yeri konuşması ve raconu.",
    "characters": [
        {"id": "savas", "name": "Savaş Satış", "color": "#3b82f6", "avatar": "🧔"},
        {"id": "mesut", "name": "Koğuş Mesulü (Mesut)", "color": "#10b981", "avatar": "👔"},
        {"id": "mahkum", "name": "Müdahale Eden Mahkum", "color": "#ef4444", "avatar": "😠"}
    ],
    "lines": [
        {"characterId": "savas", "startTime": 1.02, "endTime": 1.54, "text": "Selamünaleyküm."},
        {"characterId": "mesut", "startTime": 1.86, "endTime": 2.58, "text": "Aleykümselam baba."},
        {"characterId": "savas", "startTime": 3.22, "endTime": 5.34, "text": "Abi biz arkadaşlarla kendi aramızda da konuştuk..."},
        {"characterId": "savas", "startTime": 5.66, "endTime": 8.42, "text": "Şu köşede bir yer yapsak, biz orada kalsak kendimize?"},
        {"characterId": "mahkum", "startTime": 9.94, "endTime": 12.58, "text": "Direksiyon başına sonra yatın! Bir de yer mi beğeneceğiz size?!"},
        {"characterId": "savas", "startTime": 13.68, "endTime": 14.74, "text": "Mesut sensin değil mi?"},
        {"characterId": "mesut", "startTime": 14.84, "endTime": 15.66, "text": "Mesut benim baba."},
        {"characterId": "savas", "startTime": 16.12, "endTime": 17.1, "text": "Bu kardeş niye konuşuyor?"},
        {"characterId": "mesut", "startTime": 17.4, "endTime": 18.9, "text": "Bu kardeş bir daha konuşamaz."},
        {"characterId": "mesut", "startTime": 19.18, "endTime": 20.52, "text": "Sen konuşma, son uyarım!"},
        {"characterId": "mesut", "startTime": 21.58, "endTime": 24.5, "text": "Baba istediğiniz yerde yatabilirsiniz kafanıza göre."},
        {"characterId": "savas", "startTime": 24.76, "endTime": 25.14, "text": "Eyvallah."},
        {"characterId": "savas", "startTime": 26.24, "endTime": 29.14, "text": "Sen sen ol, abilerin konuşurken lafa girme tamam mı?"}
    ]
}

# 45. 32. Gün Perinçek vs Kürkçü
PERFECT_SCENES_4["meme-dfa4d19b1f82b2eb"] = {
    "title": "32. Gün - Doğu Perinçek vs Ertuğrul Kürkçü 'Yarkadaş/Dönek' Kavgası",
    "description": "32. Gün Türk televizyon tarihinin en ikonik kavgası: Doğu Perinçek ve Ertuğrul Kürkçü.",
    "characters": [
        {"id": "perincek", "name": "Doğu Perinçek", "color": "#dc2626", "avatar": "👴"},
        {"id": "kurkcu", "name": "Ertuğrul Kürkçü", "color": "#2563eb", "avatar": "👓"}
    ],
    "lines": [
        {"characterId": "perincek", "startTime": 0.0, "endTime": 3.2, "text": "Kemalizm'i savunacağız! Sen Kemalist devrimi savunamazsın!"},
        {"characterId": "kurkcu", "startTime": 3.44, "endTime": 5.16, "text": "Bırak palavrayı! Sen bırak palavrayı!"},
        {"characterId": "perincek", "startTime": 5.24, "endTime": 7.56, "text": "Sen döneksin! Sen döneksin! Döneksin!"},
        {"characterId": "kurkcu", "startTime": 7.88, "endTime": 10.92, "text": "Sen sıkıyönetim mahkemelerinde çıkıp dönekliğin belgesini verdin mi?!"},
        {"characterId": "perincek", "startTime": 10.92, "endTime": 11.82, "text": "Sen ne dedin?!"},
        {"characterId": "kurkcu", "startTime": 12.28, "endTime": 15.66, "text": "Sen 12 Eylül mahkemelerini göreceksin! Göreceksin!"},
        {"characterId": "perincek", "startTime": 15.92, "endTime": 17.0, "text": "Sen Abdülhamit'i savundun!"},
        {"characterId": "kurkcu", "startTime": 17.24, "endTime": 17.84, "text": "Savunmadım!"},
        {"characterId": "perincek", "startTime": 18.1, "endTime": 20.02, "text": "Sen mürtecileri savundun! Sen savundun!"},
        {"characterId": "kurkcu", "startTime": 20.08, "endTime": 22.24, "text": "Terbiyesiz! Savunmadım!"},
        {"characterId": "kurkcu", "startTime": 22.7, "endTime": 23.26, "text": "Çıkar göster!"},
        {"characterId": "perincek", "startTime": 23.68, "endTime": 24.56, "text": "Ben göstereceğim!"},
        {"characterId": "kurkcu", "startTime": 26.96, "endTime": 28.5, "text": "Puşt! Terbiyesiz!"},
        {"characterId": "perincek", "startTime": 30.92, "endTime": 32.72, "text": "Ahlaksızsın sen! Bir tokat atacağım şimdi!"},
        {"characterId": "kurkcu", "startTime": 32.84, "endTime": 36.6, "text": "Hiçbir şey atamazsın! Bak sen görürsün Dev-Genç yumruğu patlar beyninde!"},
        {"characterId": "perincek", "startTime": 37.98, "endTime": 41.2, "text": "Ben Dev-Genç'in ismini koyan kurucu genel başkanıyım senin!"},
        {"characterId": "kurkcu", "startTime": 41.2, "endTime": 45.08, "text": "Sen FKF'nin başkanısın, Dev-Genç'in değil!"},
        {"characterId": "perincek", "startTime": 45.22, "endTime": 49.18, "text": "Hippiydin o zaman! Hippiydin! 18 yaşında hippiydin!"},
        {"characterId": "kurkcu", "startTime": 49.3, "endTime": 52.26, "text": "Doğu Bey, siz hippi bile olamadınız biliyor musunuz?!"}
    ]
}

# 46. Bunlar Çok Semizlenmişler Dayı
PERFECT_SCENES_4["meme-e176a8d6ddafcd38"] = {
    "title": "Sosyal Medya Skeci - 'Bunlar Çok Semizlenmişler Dayı'",
    "description": "Köy evinde yeğen ile dayının argo kelime yanlış anlaması üzerine atışması.",
    "characters": [
        {"id": "yegen", "name": "Yeğen", "color": "#3b82f6", "avatar": "👦"},
        {"id": "dayi", "name": "Dayı", "color": "#ef4444", "avatar": "👴"}
    ],
    "lines": [
        {"characterId": "yegen", "startTime": 0.0, "endTime": 2.82, "text": "İşin kötüsü bunlar çok semizlenmişler..."},
        {"characterId": "yegen", "startTime": 3.04, "endTime": 4.74, "text": "Bizi yakalarlarsa skeç çekeceklermiş!"},
        {"characterId": "dayi", "startTime": 5.08, "endTime": 6.84, "text": "Nasıl konuşuyorsun lan sen terbiyesiz?!"},
        {"characterId": "yegen", "startTime": 7.36, "endTime": 9.76, "text": "Yok dayı öyle değil yanlış anladın ya!"},
        {"characterId": "yegen", "startTime": 10.18, "endTime": 13.16, "text": "Bizi bulurlarsa skeç yapacaklarmış anlamında söyledim!"},
        {"characterId": "yegen", "startTime": 14.78, "endTime": 18.68, "text": "Valla öyle, her yerde konuşurlarmış bunlara skeç çekeceğiz diye!"},
        {"characterId": "dayi", "startTime": 19.16, "endTime": 21.44, "text": "Hâlâ konuşuyor ya yavşağa bak!"},
        {"characterId": "dayi", "startTime": 22.36, "endTime": 26.88, "text": "Beni delirtmeyeceksiniz lan! Cahiller siktirin gidin lan buradan!"}
    ]
}

# 47. Toteme Çorba Yazmışlar
PERFECT_SCENES_4["meme-e826a1eb54f96a91"] = {
    "title": "Viral - Toteme Çorba Yazmışlar Rant",
    "description": "Yol kenarında sadece mercimek çorbası bulan aç sürücünün efsanevi öfke patlaması.",
    "characters": [
        {"id": "sofor", "name": "Aç Kalan Sürücü", "color": "#f97316", "avatar": "🚗"}
    ],
    "lines": [
        {"characterId": "sofor", "startTime": 0.88, "endTime": 5.68, "text": "Yollardayım ben, gidiyorum. Yolun kenarına kocaman çorba yazmış!"},
        {"characterId": "sofor", "startTime": 6.04, "endTime": 10.46, "text": "Hayvan gibi toteme çorba yazmış, içeri giriyorum ne çorbası var diyorum..."},
        {"characterId": "sofor", "startTime": 10.92, "endTime": 15.5, "text": "Mercimek! Ananı sikeyim hayallerimle oynadın be adam!"},
        {"characterId": "sofor", "startTime": 15.5, "endTime": 21.94, "text": "Ayak lazım, paça lazım, işkembe lazım! Mercimekle avradını sikeyim madem yok..."},
        {"characterId": "sofor", "startTime": 22.28, "endTime": 26.38, "text": "Neden oraya kocaman çorba yazıyorsun be vicdansız?!"},
        {"characterId": "sofor", "startTime": 26.38, "endTime": 27.04, "text": "Çorba!"}
    ]
}

# 48. Buzdolabı Işığı
PERFECT_SCENES_4["meme-e8c99d3f73f2c634"] = {
    "title": "Meme - Buzdolabı Işığı ve Şabat İcadı",
    "description": "Buzdolabı kapağındaki ışığı kapatmak yerine önünü kapatan icat parodisi.",
    "characters": [
        {"id": "anlatan", "name": "Buluşu Anlatan Adam", "color": "#3b82f6", "avatar": "💡"},
        {"id": "dinleyen", "name": "Şüpheci Arkadaş", "color": "#10b981", "avatar": "🤔"}
    ],
    "lines": [
        {"characterId": "anlatan", "startTime": 0.0, "endTime": 2.48, "text": "İşte Yahudi aklı buna bir çözüm bulmuş."},
        {"characterId": "anlatan", "startTime": 3.16, "endTime": 3.88, "text": "Bup!"},
        {"characterId": "dinleyen", "startTime": 4.32, "endTime": 5.56, "text": "Ama ışık açık değil mi?"},
        {"characterId": "anlatan", "startTime": 5.72, "endTime": 7.36, "text": "Işık açık, onu kapatmadın."},
        {"characterId": "anlatan", "startTime": 7.58, "endTime": 11.1, "text": "Sadece önünü kapatıp ışığı engelleyebilirsin Yahudi aklı..."},
        {"characterId": "anlatan", "startTime": 11.12, "endTime": 12.26, "text": "Bunu da icat etmiş."},
        {"characterId": "dinleyen", "startTime": 14.74, "endTime": 20.04, "text": "Yani dondurucuyu her açtığınızda abi ışık yanmayacak, ışığı açmış olmayacaksın!"}
    ]
}

# 49. Kuru Fasulyeci Ümit Usta
PERFECT_SCENES_4["meme-e93c45e8d6f4a3d8"] = {
    "title": "Meme - Kuru Fasulyeci Ümit Usta Parodisi",
    "description": "Kendi evinin altında dükkan açıp hiçbir zaman fasulye bırakmayan Ümit Usta parodisi.",
    "characters": [
        {"id": "musteri", "name": "Aç Müşteri", "color": "#3b82f6", "avatar": "🍲"},
        {"id": "umit", "name": "Ümit Usta", "color": "#f59e0b", "avatar": "👨‍🍳"}
    ],
    "lines": [
        {"characterId": "musteri", "startTime": 0.0, "endTime": 5.26, "text": "Çorba falan yapmıyor, kendi evinin altında 11 gibi açıyor 2 gibi kapatıyor zaten kalmıyor..."},
        {"characterId": "musteri", "startTime": 5.54, "endTime": 8.5, "text": "Efsane bir tat! Ümit Usta 2 kuru versene bize be!"},
        {"characterId": "umit", "startTime": 8.68, "endTime": 10.24, "text": "Kuru kalmadı oğlumuz."},
        {"characterId": "musteri", "startTime": 10.28, "endTime": 12.7, "text": "Yapma be abi... İyi yarın geliriz biz o zaman."},
        {"characterId": "umit", "startTime": 12.74, "endTime": 13.84, "text": "Yarın açmam."},
        {"characterId": "musteri", "startTime": 14.2, "endTime": 16.08, "text": "Hadi ya! İyi tamam Cuma geliriz ya."},
        {"characterId": "umit", "startTime": 16.22, "endTime": 17.24, "text": "Cuma da açmam."},
        {"characterId": "musteri", "startTime": 18.42, "endTime": 20.08, "text": "Haa Cuma gelemeyiz zaten toplantı var."},
        {"characterId": "umit", "startTime": 20.22, "endTime": 21.74, "text": "Cuma açarım o zaman!"},
        {"characterId": "musteri", "startTime": 22.26, "endTime": 23.74, "text": "Ümit Usta 2 kuru ver bize be!"},
        {"characterId": "umit", "startTime": 23.94, "endTime": 25.24, "text": "Kalmadı oğlumuz ya."},
        {"characterId": "musteri", "startTime": 25.54, "endTime": 27.94, "text": "Saat 11'de açmadın mı sen? 11'i 10 geçiyor ne ara bitti?!"},
        {"characterId": "umit", "startTime": 27.94, "endTime": 31.06, "text": "Ben bir kase yaptım kendime kadar, yedim onu yani."},
        {"characterId": "musteri", "startTime": 31.3, "endTime": 32.02, "text": "Yarın kaçta açacaksın?"},
        {"characterId": "umit", "startTime": 32.36, "endTime": 34.1, "text": "Sabahın 4.30'unda açarım."},
        {"characterId": "musteri", "startTime": 34.88, "endTime": 36.76, "text": "Ümit Usta bize 2 kuru versene."},
        {"characterId": "umit", "startTime": 36.92, "endTime": 38.54, "text": "Oğlumuz ne kurusu sabah sabah?!"},
        {"characterId": "musteri", "startTime": 38.86, "endTime": 40.9, "text": "Abi sen demedin mi sabah 4.30'da açacağım diye?!"},
        {"characterId": "umit", "startTime": 41.1, "endTime": 46.08, "text": "Açtım da kapatacağım camiye gideceğim, soğuk orada burada sıcağında abdest aldım."},
        {"characterId": "umit", "startTime": 47.0, "endTime": 47.88, "text": "11 gibi gelin."},
        {"characterId": "musteri", "startTime": 48.04, "endTime": 48.34, "text": "Bu ne?"},
        {"characterId": "umit", "startTime": 49.94, "endTime": 55.82, "text": "Narsist kişiliğime yenik düştüm ve zirvede bırakıyorum, siz bunu okuduğunuzda ben çoktan emekli olacağım."},
        {"characterId": "umit", "startTime": 55.82, "endTime": 58.34, "text": "Kurucu üye Ümit Usta."}
    ]
}

# 50. KV Erdal Kömürcü & Abuzer
PERFECT_SCENES_4["meme-ea037fab87e9c168"] = {
    "title": "Kurtlar Vadisi - Erdal Kömürcü & Abuzer 'Her Delikanlının Bir Gelişi Vardır'",
    "description": "Kurtlar Vadisi efsane ikili: Abuzer Kömürcü ile oğlu Erdal'ın kapı eşiğindeki diyaloğu.",
    "characters": [
        {"id": "erdal", "name": "Erdal Kömürcü", "color": "#3b82f6", "avatar": "🧪"},
        {"id": "abuzer", "name": "Abuzer Kömürcü", "color": "#ef4444", "avatar": "👴"}
    ],
    "lines": [
        {"characterId": "erdal", "startTime": 0.84, "endTime": 1.84, "text": "Ne haber?"},
        {"characterId": "abuzer", "startTime": 2.96, "endTime": 5.22, "text": "İyidir sahip, sen nasılsın?"},
        {"characterId": "abuzer", "startTime": 5.44, "endTime": 8.76, "text": "Ne diyorsun oğlum ya? Ne öyle geliyorsun aklımız gitti!"},
        {"characterId": "erdal", "startTime": 9.14, "endTime": 11.66, "text": "Eee her delikanlının bir gelişi vardır!"},
        {"characterId": "abuzer", "startTime": 12.12, "endTime": 14.88, "text": "Ne yaptın güzel kurup bir yer aldın mı içeriye?"}
    ]
}

print(f"Bölüm 4 hazırlandı: {len(PERFECT_SCENES_4)} sahne.")
