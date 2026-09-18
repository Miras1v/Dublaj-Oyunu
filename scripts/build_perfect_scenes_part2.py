import os
import sys

PERFECT_SCENES_2 = {}

# 21. Yenilmezler
PERFECT_SCENES_2["meme-565c56a384f3e6ca"] = {
    "title": "Yenilmezler - Zırhını Çıkarırsan Ne Kalır? (Tony vs Steve & Banner)",
    "description": "Avengers Helicarrier sahnesi: Steve Rogers ile Tony Stark atışması ve Bruce Banner'ın isyanı.",
    "characters": [
        {"id": "tony", "name": "Tony Stark (Demir Adam)", "color": "#dc2626", "avatar": "🤖"},
        {"id": "steve", "name": "Steve Rogers (Kaptan Amerika)", "color": "#2563eb", "avatar": "🛡️"},
        {"id": "banner", "name": "Bruce Banner (Hulk)", "color": "#16a34a", "avatar": "🧪"}
    ],
    "lines": [
        {"characterId": "steve", "startTime": 1.2, "endTime": 3.82, "text": "Kontrolden bahsedip kargaşaya davetiye çıkarıyorsun."},
        {"characterId": "tony", "startTime": 3.84, "endTime": 6.58, "text": "Çalışma tarzı bu değil mi? Neyiz biz, ekip mi?"},
        {"characterId": "tony", "startTime": 6.74, "endTime": 9.54, "text": "Hayır hayır, biz kargaşa yaratan kimyasal bir karışımız."},
        {"characterId": "tony", "startTime": 10.08, "endTime": 12.3, "text": "Biz... Biz saatli bombayız."},
        {"characterId": "steve", "startTime": 12.38, "endTime": 13.88, "text": "Ağır ol bakalım biraz."},
        {"characterId": "tony", "startTime": 14.24, "endTime": 16.18, "text": "Neden biraz deşarj olmasına izin vermiyoruz?"},
        {"characterId": "steve", "startTime": 16.2, "endTime": 18.04, "text": "Nedenini çok iyi biliyorsun. İşine bak sen."},
        {"characterId": "tony", "startTime": 18.64, "endTime": 19.92, "text": "Keşke beni buna zorlasan."},
        {"characterId": "steve", "startTime": 20.6, "endTime": 22.98, "text": "Evet. Zırh giymiş koca adam."},
        {"characterId": "steve", "startTime": 24.2, "endTime": 25.82, "text": "Öt bakalım nesin sen?"},
        {"characterId": "tony", "startTime": 26.32, "endTime": 28.6, "text": "Dahi, milyarder, playboy, hayırsever."},
        {"characterId": "steve", "startTime": 29.28, "endTime": 31.7, "text": "Bunlar olmadan da sana fark atacak kişiler biliyorum."},
        {"characterId": "steve", "startTime": 32.42, "endTime": 33.76, "text": "Ben bu filmi çok gördüm."},
        {"characterId": "steve", "startTime": 34.04, "endTime": 36.2, "text": "Uğruna gerçekten savaştığın tek şey kendinsin."},
        {"characterId": "steve", "startTime": 37.26, "endTime": 42.04, "text": "Fedakarlık edip dikenli telden geçecek ve üstünde sürünmelerine izin verecek biri değilsin."},
        {"characterId": "tony", "startTime": 42.12, "endTime": 43.4, "text": "Teli keserim olur biter."},
        {"characterId": "steve", "startTime": 46.46, "endTime": 47.9, "text": "Hep bir yolunu bulursun."},
        {"characterId": "steve", "startTime": 49.18, "endTime": 52.5, "text": "Tehdit olmayabilirsin ama kahramanmış gibi davranmayı da bırak artık!"},
        {"characterId": "tony", "startTime": 52.7, "endTime": 54.34, "text": "Kahraman mı? Senin gibi mi?"},
        {"characterId": "steve", "startTime": 55.02, "endTime": 57.2, "text": "Sen bir laboratuvar deneyisin Rogers."},
        {"characterId": "steve", "startTime": 57.48, "endTime": 60.22, "text": "Seni özel kılan her şey bir şişeden çıktı."},
        {"characterId": "tony", "startTime": 85.74, "endTime": 88.2, "text": "Hadi zırhını giy, birkaç raunt tutup kapışalım!"},
        {"characterId": "banner", "startTime": 97.42, "endTime": 99.48, "text": "Nereye? Odamı kiraya verdiniz."},
        {"characterId": "banner", "startTime": 101.26, "endTime": 104.64, "text": "Beni öldürmeniz gerekir diye... Ama yapamazsınız, biliyorum çünkü denedim!"},
        {"characterId": "banner", "startTime": 108.38, "endTime": 111.32, "text": "Bunalımdaydım, sonu yok diyordum..."},
        {"characterId": "banner", "startTime": 111.54, "endTime": 114.72, "text": "Ben de ağzıma bir kurşun sıktım ama diğer adam tükürüp çıkardı!"},
        {"characterId": "banner", "startTime": 116.2, "endTime": 120.52, "text": "Yaşamaya devam ettim, başkalarına yardım etmekle meşgul oldum."},
        {"characterId": "banner", "startTime": 120.66, "endTime": 124.18, "text": "Siz beni bu ucubelerin arasına sürükleyip buradakileri tehlikeye atana kadar!"},
        {"characterId": "banner", "startTime": 124.38, "endTime": 128.1, "text": "Sırrımı bilmek ister misiniz Ajan Romanoff? Nasıl sakin kaldığımı söyleyeyim mi?"},
        {"characterId": "steve", "startTime": 131.08, "endTime": 134.94, "text": "Doktor Banner... O asayı bırak."}
    ]
}

# 22. İsmail Kartal
PERFECT_SCENES_2["meme-5a992347adcc5220"] = {
    "title": "İsmail Kartal - Ferdi'yi Sol Bek Yapan Benim!",
    "description": "İsmail Kartal'ın efsanevi basın toplantısı: 'Ferdi'yi sol bek yapan benim!'",
    "characters": [
        {"id": "kartal", "name": "İsmail Kartal (Arap İsmail)", "color": "#eab308", "avatar": "👔"}
    ],
    "lines": [
        {"characterId": "kartal", "startTime": 0.0, "endTime": 3.52, "text": "Ferdi'yi sol bek yapan benim! Osayi'yi sağ bek yapan benim!"},
        {"characterId": "kartal", "startTime": 3.86, "endTime": 6.0, "text": "Szymanski'yi bir maç 6 numara, 8 numara..."},
        {"characterId": "kartal", "startTime": 6.0, "endTime": 8.02, "text": "Sağ kanatta oynatan benim! Niye kimse bunları konuşmuyor?"},
        {"characterId": "kartal", "startTime": 8.36, "endTime": 10.02, "text": "Serdar Dursun'u 10 numara oynatan benim!"}
    ]
}

# 23. Batu Abi Dalton Sandılar
PERFECT_SCENES_2["meme-5b819baf3f383a04"] = {
    "title": "Azar / TikTok Canlı Yayını - 'Batu Abi Dalton Sandılar Seni' Atışması",
    "description": "Batuhan Furkan canlı yayını: Konuğun 'Batu abi Dalton sandılar seni' trollemesi.",
    "characters": [
        {"id": "konuk", "name": "Yayın Konuğu", "color": "#3b82f6", "avatar": "👦"},
        {"id": "batu", "name": "Batuhan Furkan", "color": "#ef4444", "avatar": "🧔"}
    ],
    "lines": [
        {"characterId": "konuk", "startTime": 0.7, "endTime": 2.18, "text": "Bu ne çirkinlik ya?"},
        {"characterId": "batu", "startTime": 2.38, "endTime": 2.96, "text": "Bana mı dedin?"},
        {"characterId": "konuk", "startTime": 3.76, "endTime": 4.04, "text": "Evet."},
        {"characterId": "batu", "startTime": 4.48, "endTime": 5.04, "text": "Çirkinliğe bak!"},
        {"characterId": "konuk", "startTime": 8.32, "endTime": 9.64, "text": "Batu abi bir şey sorabilir miyim?"},
        {"characterId": "konuk", "startTime": 10.24, "endTime": 11.56, "text": "Özel birim misin yoksa?"},
        {"characterId": "batu", "startTime": 12.38, "endTime": 13.6, "text": "Özel birim doğrudur."},
        {"characterId": "konuk", "startTime": 14.26, "endTime": 14.58, "text": "Neyi?"},
        {"characterId": "batu", "startTime": 15.1, "endTime": 15.78, "text": "Özel biriyim."},
        {"characterId": "konuk", "startTime": 16.46, "endTime": 17.92, "text": "Tamam kankam nasıl, iyi misin?"},
        {"characterId": "konuk", "startTime": 19.3, "endTime": 20.34, "text": "Dalton sandılar seni reis!"},
        {"characterId": "batu", "startTime": 20.88, "endTime": 21.44, "text": "Efendim?"},
        {"characterId": "konuk", "startTime": 21.72, "endTime": 22.96, "text": "Kusura bakma Dalton sandılar, iyi misin?"},
        {"characterId": "batu", "startTime": 30.06, "endTime": 32.3, "text": "Haa, engelli sandılar beni öyle mi?!"}
    ]
}

# 24. Unlost Duvarı Delerim
PERFECT_SCENES_2["meme-638a5e3314df054c"] = {
    "title": "Cantuğ 'Unlost' - CS:GO Kasa Kumarında Duvarı Delen Çıldırma",
    "description": "Unlost'un CS:GO Live kasasında parayı batırınca komşuya ve duvara patladığı anlar.",
    "characters": [
        {"id": "unlost", "name": "Cantuğ (Unlost)", "color": "#ef4444", "avatar": "😡"}
    ],
    "lines": [
        {"characterId": "unlost", "startTime": 0.0, "endTime": 1.86, "text": "Son bir kez daha açayım, batacaksam orada batayım..."},
        {"characterId": "unlost", "startTime": 5.06, "endTime": 6.44, "text": "Ben bunu kalkıp döveceğim şimdi!"},
        {"characterId": "unlost", "startTime": 7.36, "endTime": 9.58, "text": "O ne oğlum lan, duvarı delecek adam!"},
        {"characterId": "unlost", "startTime": 14.48, "endTime": 16.08, "text": "Ne diye vuruyor, bağırmadım ki!"},
        {"characterId": "unlost", "startTime": 16.08, "endTime": 18.62, "text": "Ne diye vuruyor bağırmadım valla normal vuruyor!"},
        {"characterId": "unlost", "startTime": 22.74, "endTime": 23.98, "text": "Polis çağıracağım polis!"},
        {"characterId": "unlost", "startTime": 27.06, "endTime": 30.52, "text": "Ya gelsene vuruyor kapıya adam ya!"},
        {"characterId": "unlost", "startTime": 39.58, "endTime": 42.82, "text": "Ya var mı beyler böyle bir şey, bağırmıyorum amına koyayım ya!"}
    ]
}

# 25. Sıfır Bir Çıkmaz Sokak
PERFECT_SCENES_2["meme-6d951d7f55599703"] = {
    "title": "Sıfır Bir - Cio & Savaş Çıkmaz Sokak",
    "description": "Sıfır Bir Adana: Çıkmaz sokakta arabayı geri manevra yapmaya çalışan Cio ve Savaş.",
    "characters": [
        {"id": "cio", "name": "Cio Baba", "color": "#ef4444", "avatar": "🔫"},
        {"id": "savas", "name": "Savaş Satış", "color": "#3b82f6", "avatar": "🚗"}
    ],
    "lines": [
        {"characterId": "cio", "startTime": 0.0, "endTime": 2.72, "text": "Sıkıntı yok, hiçbir şekilde sıkıntı yok. Gel hele."},
        {"characterId": "savas", "startTime": 6.8, "endTime": 10.82, "text": "Yanınıza iki üç tane genç alın, bir dostumuzu karşılamaya gideceğiz."},
        {"characterId": "cio", "startTime": 16.0, "endTime": 19.34, "text": "Bak hele lan! Bu da kendini iyice Polat Alemdar zannetti ha!"},
        {"characterId": "cio", "startTime": 19.94, "endTime": 20.78, "text": "En son bozacağım!"},
        {"characterId": "savas", "startTime": 21.4, "endTime": 26.3, "text": "Bırak oğlum ya, abigil yolladıysa bir bildikleri vardır kafana takma böyle şeyleri."},
        {"characterId": "cio", "startTime": 26.64, "endTime": 29.58, "text": "Tamam da kardeş bize yapmasın! O yokken biz vardık!"},
        {"characterId": "savas", "startTime": 29.96, "endTime": 32.64, "text": "Ya boş koyalım, bu kadar işin içinde bir de bununla mı uğraşacağız ya?"},
        {"characterId": "cio", "startTime": 39.14, "endTime": 40.4, "text": "Lan bu yol çıkmıyor mu?!"},
        {"characterId": "savas", "startTime": 40.7, "endTime": 41.54, "text": "O yol çıkmıyor abi."},
        {"characterId": "cio", "startTime": 41.92, "endTime": 43.02, "text": "Niye söylemiyorsunuz oğlum?!"},
        {"characterId": "savas", "startTime": 43.28, "endTime": 44.02, "text": "Sormadın ki abi."},
        {"characterId": "savas", "startTime": 49.96, "endTime": 50.84, "text": "Bırak oğlum ya..."}
    ]
}

# 26. Kolpaçino Şahin Çoluk Çocuk
PERFECT_SCENES_2["meme-701778ed8f454ba0"] = {
    "title": "Kolpaçino - Şahin Çoluk Çocuğun Elinde Kaldık Raconu",
    "description": "Kolpaçino orman sahnesi: Şahin'in Özgür ve Sabri'ye 'Bak donum görünüyor' fırçası.",
    "characters": [
        {"id": "sahin", "name": "Şahin", "color": "#dc2626", "avatar": "🔫"},
        {"id": "ozgur", "name": "Özgür", "color": "#f59e0b", "avatar": "😰"}
    ],
    "lines": [
        {"characterId": "sahin", "startTime": 0.0, "endTime": 5.44, "text": "Bu ne iş ya? Birine telefon gelir dur, biri kolonyayla kendini yakmak ister dur!"},
        {"characterId": "sahin", "startTime": 5.66, "endTime": 8.74, "text": "Biri ormana dalar... Çoluk çocuğun elinde oyuncak olduk Tayfun!"},
        {"characterId": "ozgur", "startTime": 9.64, "endTime": 12.62, "text": "Abi ormandan sonrası deniz ya, istersen atıp kurtulalım mı?"},
        {"characterId": "sahin", "startTime": 12.74, "endTime": 13.58, "text": "Yavaş yapın lan!"},
        {"characterId": "ozgur", "startTime": 14.04, "endTime": 18.36, "text": "Sabri Bey, kız arkadaşım aradı durmak zorundaydım yani kusura bakmayın."},
        {"characterId": "ozgur", "startTime": 18.96, "endTime": 22.56, "text": "Ayriyeten içinde bulunduğumuz durumdan da ben de pek memnun değilim yani."},
        {"characterId": "sahin", "startTime": 22.84, "endTime": 23.84, "text": "Sen ne diyorsun ya?"},
        {"characterId": "ozgur", "startTime": 24.1, "endTime": 29.5, "text": "Yani diyorum ki gece gece iki ceset altı adam ayakaltı bir yerdeyiz yani..."},
        {"characterId": "sahin", "startTime": 29.5, "endTime": 30.72, "text": "Ne gülüyorsun lan?!"},
        {"characterId": "ozgur", "startTime": 30.94, "endTime": 31.52, "text": "Bilmiyorum abi."},
        {"characterId": "sahin", "startTime": 31.64, "endTime": 32.26, "text": "Ne gülüyorsun lan?!"},
        {"characterId": "ozgur", "startTime": 32.64, "endTime": 33.32, "text": "Bilmiyorum abi."},
        {"characterId": "sahin", "startTime": 33.7, "endTime": 35.94, "text": "Yavrum sen kaç yaşındasın?"},
        {"characterId": "ozgur", "startTime": 36.04, "endTime": 37.42, "text": "Otuz dört yaşındayım, ne oldu ki?"},
        {"characterId": "sahin", "startTime": 37.78, "endTime": 43.26, "text": "Bak kardeşim sen güzel bir kardeşe benziyorsun. Benim yaşım elli."},
        {"characterId": "sahin", "startTime": 44.28, "endTime": 47.26, "text": "Bak pantolonuma, bak iyi bak..."},
        {"characterId": "sahin", "startTime": 48.24, "endTime": 54.34, "text": "Ha? Donum görünüyor! Donum olmasa bizzat götümün kendisi görünecek!"}
    ]
}

# 27. Sıfır Bir Manita
PERFECT_SCENES_2["meme-71af9284d4ab8edf"] = {
    "title": "Sıfır Bir - Cezaevi Servisinde Manita Muhabbeti",
    "description": "Sıfır Bir 1. Sezon: Cezaevi tahliyesi sonrası arabada manita ve hava durumu muhabbeti.",
    "characters": [
        {"id": "cio", "name": "Cio Baba", "color": "#ef4444", "avatar": "🔫"},
        {"id": "savas", "name": "Savaş Satış", "color": "#3b82f6", "avatar": "🚗"}
    ],
    "lines": [
        {"characterId": "savas", "startTime": 0.0, "endTime": 1.5, "text": "Oğlum nasıl özlemişim lan dışarıyı..."},
        {"characterId": "cio", "startTime": 2.02, "endTime": 3.94, "text": "Bakarsın bugün kavuşuruz Özgür!"},
        {"characterId": "savas", "startTime": 4.4, "endTime": 5.66, "text": "Özgür manitalara bak lan!"},
        {"characterId": "savas", "startTime": 6.22, "endTime": 7.7, "text": "Oğlum memlekete yaz gelmiş lan!"},
        {"characterId": "cio", "startTime": 8.16, "endTime": 9.54, "text": "Başına vurdu valla abi buyur."},
        {"characterId": "cio", "startTime": 9.78, "endTime": 11.72, "text": "Sana özgürlükten bahsediyorum sen manita diyorsun."},
        {"characterId": "savas", "startTime": 12.22, "endTime": 14.96, "text": "Oğlum neyin kafasını yaşıyorsun avratlara baksana!"},
        {"characterId": "cio", "startTime": 17.24, "endTime": 18.72, "text": "Harbi yandık abi ya."},
        {"characterId": "savas", "startTime": 19.08, "endTime": 20.34, "text": "Harbi klimayı açın yandık be!"},
        {"characterId": "cio", "startTime": 22.66, "endTime": 24.54, "text": "Kimin yandığı belli oluyor Allah'ını seversen..."}
    ]
}

# 28. Flash TV Neden Dağa Çıktınız
PERFECT_SCENES_2["meme-74ca08745cf708a8"] = {
    "title": "Flash TV - 'Neden Dağa Çıktınız?' Efsane Röportaj",
    "description": "Flash TV Gerçek Kesit klasiği: Dağdaki köylünün absürt teröristlik itirafı.",
    "characters": [
        {"id": "muhabir", "name": "Flash TV Muhabiri", "color": "#2563eb", "avatar": "🎤"},
        {"id": "koylu", "name": "Köylü Dayı", "color": "#78716c", "avatar": "🏔️"}
    ],
    "lines": [
        {"characterId": "muhabir", "startTime": 0.0, "endTime": 3.08, "text": "Efendim neden terörist oldunuz, anlatır mısınız bize?"},
        {"characterId": "koylu", "startTime": 3.86, "endTime": 6.14, "text": "Valla biz köyden geliyorduk arabayla..."},
        {"characterId": "koylu", "startTime": 6.24, "endTime": 11.76, "text": "Bizden birileri teröristler önümüze geldi, dedik dağa geleceksin, ben dedim gelmiyorum, o dedi geleceksin, biz mecbur kaldık gittik."},
        {"characterId": "koylu", "startTime": 12.28, "endTime": 19.68, "text": "Biz dağa gittik elime silah verdi çatışacaksın, ben dedim çatışmıyorum, o dedi çatışacaksın, biz mecbur kaldık çatıştık."},
        {"characterId": "koylu", "startTime": 20.6, "endTime": 25.96, "text": "Valla tam o esnada bir bomba patladı gümm! Bir parça geldi benim kafama vurdu danng!"},
        {"characterId": "koylu", "startTime": 26.74, "endTime": 30.56, "text": "Valla ben köyümü kaybetmişim, iki gün köyü aradım bulamadım..."},
        {"characterId": "koylu", "startTime": 30.98, "endTime": 34.68, "text": "Sonra biz devlet güçlerine teslim olduk, ne mutlu Türküm diyene!"}
    ]
}

# 29. H-Talks Hasan Arda
PERFECT_SCENES_2["meme-7e1105e63de53c5a"] = {
    "title": "H-Talks - Hasan Arda Kaşıkçı Maç Skoru Uydurma Tepkisi",
    "description": "H-Talks Twitch Yayını: Chat'teki Fikret'in 'GS 2-2 yaptı' trollüğüne Hasan Arda'nın delirmesi.",
    "characters": [
        {"id": "hak", "name": "Hasan Arda Kaşıkçı (H-Talks)", "color": "#000000", "avatar": "🦅"}
    ],
    "lines": [
        {"characterId": "hak", "startTime": 0.8, "endTime": 3.84, "text": "Ya Fiwhs artık bir yerinden maç uyduruyorsun!"},
        {"characterId": "hak", "startTime": 3.98, "endTime": 5.16, "text": "GS 2-2 yaptı diyorsun..."},
        {"characterId": "hak", "startTime": 5.34, "endTime": 7.26, "text": "Galatasaray maç bile oynamıyor ya şu an!"},
        {"characterId": "hak", "startTime": 9.22, "endTime": 14.46, "text": "Artık skor uydurdun uydurdun uydurdun, artık beni çileden çıkarmak için bir yerinden maç uyduruyorsun ya!"},
        {"characterId": "hak", "startTime": 18.68, "endTime": 23.16, "text": "Şu an inanmıyorum sana ki bir yerde Galatasaray 2-2 yapmış olsun ya!"},
        {"characterId": "hak", "startTime": 24.84, "endTime": 27.22, "text": "Bir de basketmiş amına koyayım!"},
        {"characterId": "hak", "startTime": 30.0, "endTime": 33.68, "text": "Bir de basketmiş özrü kabahatinden büyük ya!"},
        {"characterId": "hak", "startTime": 37.68, "endTime": 40.74, "text": "Basket maçıymış yüzümü yolacağım tırnaklarımla ya!"}
    ]
}

# 30. Han Kanal Domuzcuk
PERFECT_SCENES_2["meme-82905766b3d259c2"] = {
    "title": "Han Kanal - Minecraft Domuzcuk (Piggy) ile Röportaj Parodisi",
    "description": "Han Kanal Minecraft parodisi: Domuz Piggy'nin sahibine isyanı.",
    "characters": [
        {"id": "han", "name": "Han Kanal", "color": "#3b82f6", "avatar": "🎙️"},
        {"id": "piggy", "name": "Domuzcuk (Piggy)", "color": "#ec4899", "avatar": "🐷"}
    ],
    "lines": [
        {"characterId": "han", "startTime": 0.0, "endTime": 2.0, "text": "İlk olarak ben bunu çok merak ediyorum."},
        {"characterId": "han", "startTime": 2.78, "endTime": 4.6, "text": "Handaşlar da seni çok merak ediyor Piggy."},
        {"characterId": "piggy", "startTime": 4.68, "endTime": 7.14, "text": "Ya bana ne be kardeşim? Benim hiç umurumda değil!"},
        {"characterId": "piggy", "startTime": 7.3, "endTime": 8.48, "text": "Bana yemek ver ne olur!"},
        {"characterId": "piggy", "startTime": 9.04, "endTime": 11.44, "text": "Ben açlıktan ölüyorum ya sahibim yüzünden!"},
        {"characterId": "han", "startTime": 11.7, "endTime": 15.92, "text": "Evet Piggy sahibinden memnun mu, lütfen bunu da merak ediyor Handaşlar?"},
        {"characterId": "piggy", "startTime": 17.86, "endTime": 20.86, "text": "Ya ne yaptın evime be adam, evimi yıktın!"},
        {"characterId": "piggy", "startTime": 21.2, "endTime": 23.82, "text": "Sahibimden memnun değilim, transfer olmak istiyorum!"}
    ]
}

print(f"Bölüm 2 hazırlandı: {len(PERFECT_SCENES_2)} sahne.")
