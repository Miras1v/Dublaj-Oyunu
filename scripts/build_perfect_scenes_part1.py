import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
SCENES_JSON = os.path.join(DATA_DIR, "scenes.json")
SCENES_JS = os.path.join(BASE_DIR, "js", "scenes.js")

# 56 Sahnenin Baştan Sona Kusursuz Doğrulukta Yeniden Yazılmış Verisi
# Her sahne için: (title, description, characters, lines[characterId, startTime, endTime, text])

PERFECT_SCENES = {}

# 1. Oto Pazar
PERFECT_SCENES["meme-artist-ne-arar"] = {
    "title": "Oto Pazar Röportajı - Artist Ne Arar La Pazarda!",
    "description": "Oto pazarı sokak röportajı efsanesi: 'Artist ne arar la pazarda!'",
    "characters": [
        {"id": "muhabir", "name": "Muhabir", "color": "#3b82f6", "avatar": "🎤"},
        {"id": "pazarci", "name": "Pazarcı Dayı", "color": "#ef4444", "avatar": "🧢"}
    ],
    "lines": [
        {"characterId": "muhabir", "startTime": 0.0, "endTime": 3.54, "text": "Hayırlı günler. Hayırlı günler efendim. Otopazarında bir artış var mı?"},
        {"characterId": "pazarci", "startTime": 4.5, "endTime": 8.92, "text": "Artış mı? Ne artışı? Artist ne arar la pazarda? Ben böyle bir şey görmedim."},
        {"characterId": "pazarci", "startTime": 9.06, "endTime": 14.42, "text": "Ben 55 yaşındayım. Bize araba alışverişi için geliyor buraya, artist olarak bize gelmez bu işler."}
    ]
}

# 2. Çıkar Telefonunu
PERFECT_SCENES["meme-cikar-telefonunu"] = {
    "title": "Sokak Röportajı - Ekonomi ve Telefon Kavgası",
    "description": "Sokak röportajı klasiği: Genç ekonomiden şikayet ederken dayının 'Çıkar telefonunu!' çıkışı.",
    "characters": [
        {"id": "muhabir", "name": "Muhabir", "color": "#3b82f6", "avatar": "🎤"},
        {"id": "genc", "name": "Genç", "color": "#10b981", "avatar": "📱"},
        {"id": "dayi", "name": "Dayı", "color": "#ef4444", "avatar": "👴"}
    ],
    "lines": [
        {"characterId": "muhabir", "startTime": 0.0, "endTime": 0.78, "text": "Ekonominiz nasıl?"},
        {"characterId": "genc", "startTime": 1.2, "endTime": 2.88, "text": "Çok kötü ya şu an inanılmaz çok kötü!"},
        {"characterId": "dayi", "startTime": 2.88, "endTime": 4.9, "text": "Çok kötü telefonunu çıkar bakayım!"},
        {"characterId": "genc", "startTime": 4.9, "endTime": 7.0, "text": "Abi ne alakası var telefonla ya?"},
        {"characterId": "dayi", "startTime": 7.0, "endTime": 8.12, "text": "Telefonunu al!"},
        {"characterId": "genc", "startTime": 8.12, "endTime": 10.0, "text": "Al tamam telefonu!"},
        {"characterId": "dayi", "startTime": 14.52, "endTime": 15.78, "text": "Ekonomi kötü diyorsun..."}
    ]
}

# 3. KV Pala / Seyfo Dayı
PERFECT_SCENES["kv-pala-oluler"] = {
    "title": "Kurtlar Vadisi - Seyfo Dayı Hüsrev Ağa'yı Anlatıyor",
    "description": "Kurtlar Vadisi klasik sahne: Seyfo Dayı masada Polat ve ekibine Hüsrev Ağa'ya gelen gizemli adamları anlatıyor.",
    "characters": [
        {"id": "seyfo", "name": "Seyfo Dayı", "color": "#1e3a8a", "avatar": "🧔"},
        {"id": "polat", "name": "Polat Alemdar", "color": "#0284c7", "avatar": "🕶️"}
    ],
    "lines": [
        {"characterId": "seyfo", "startTime": 0.0, "endTime": 3.36, "text": "Hüsrev Ağa'nın yanına bir, bir buçuk ay evvel birileri gelmiş..."},
        {"characterId": "seyfo", "startTime": 3.92, "endTime": 7.84, "text": "Kimisi diyor ki akrabası, kimisi diyor ki akrabasının adamları..."},
        {"characterId": "seyfo", "startTime": 8.44, "endTime": 11.68, "text": "Ama kime sorduysam dedikleri üç kişiymiş bunlar."},
        {"characterId": "polat", "startTime": 12.28, "endTime": 14.2, "text": "İsim, nam bir şey duydun mu dayı?"}
    ]
}

# 4. Sıfır Bir Cio Savaş
PERFECT_SCENES["sifir-bir-cio"] = {
    "title": "Sıfır Bir - Cio & Savaş Alacak Verecek Davası",
    "description": "Sıfır Bir Adana klasiği: Cio ve Savaş'ın araba içindeki alacak verecek tartışması.",
    "characters": [
        {"id": "cio", "name": "Cio Baba", "color": "#ef4444", "avatar": "🔫"},
        {"id": "savas", "name": "Savaş Satış", "color": "#3b82f6", "avatar": "🚗"}
    ],
    "lines": [
        {"characterId": "cio", "startTime": 0.92, "endTime": 2.8, "text": "Bak sen herhalde anlatacağım mevzuyu tam anlamadın he?"},
        {"characterId": "cio", "startTime": 2.96, "endTime": 3.5, "text": "Neydi o?"},
        {"characterId": "savas", "startTime": 5.66, "endTime": 6.86, "text": "Sarsılmaz abi ben ya, dinliyorum."},
        {"characterId": "cio", "startTime": 7.8, "endTime": 11.04, "text": "O gün bir dostuyla bir alacak verecek meselesi için bir yere gitmişler..."},
        {"characterId": "savas", "startTime": 13.38, "endTime": 14.98, "text": "Adamlar aralarında bitirmiş işi abicim."}
    ]
}

# 5. Sıfır Bir Yahya Seyfi
PERFECT_SCENES["sifir-bir-yahya-cezaevi"] = {
    "title": "Sıfır Bir - Yahya & Seyfi Cezaevi Sorgusu",
    "description": "Sıfır Bir Cezaevi sorgu odası: Seyfi'nin 'ıslah-ı nefis oldum' savunması ve Yahya'nın tepkisi.",
    "characters": [
        {"id": "seyfi", "name": "Seyfi", "color": "#10b981", "avatar": "⛓️"},
        {"id": "yahya", "name": "Yahya / Polis", "color": "#ef4444", "avatar": "👮"}
    ],
    "lines": [
        {"characterId": "seyfi", "startTime": 0.0, "endTime": 1.68, "text": "Benim kimseyle işim olmaz."},
        {"characterId": "seyfi", "startTime": 2.44, "endTime": 5.46, "text": "Ben cezaevinden çıktıktan sonra ıslah-ı nefis oldum."},
        {"characterId": "yahya", "startTime": 8.14, "endTime": 9.86, "text": "Çocuk mu kandırıyorsun lan?!"},
        {"characterId": "yahya", "startTime": 11.02, "endTime": 16.48, "text": "Cezaevinden çıktın, kendine bir oluşum yaptın ve intikam için saldırdın!"},
        {"characterId": "seyfi", "startTime": 17.72, "endTime": 20.48, "text": "Bu senin kendi kafanda kurguladığın bir ifade."},
        {"characterId": "seyfi", "startTime": 20.98, "endTime": 23.52, "text": "Eğer varsa elinde bir delilin bana onla gel!"}
    ]
}

# 6. Kolpaçino Saatli Bomba
PERFECT_SCENES["meme-kolpacino-saatli-bomba"] = {
    "title": "Kolpaçino - Saatli Bomba",
    "description": "Kolpaçino Bomba Sahnesi: Sabri Abi'nin üstündeki bombayı Ganyotçu'ya gösterdiği an.",
    "characters": [
        {"id": "ganyotcu", "name": "Ganyotçu Abi", "color": "#3b82f6", "avatar": "🧔"},
        {"id": "sabri", "name": "Sabri Abi", "color": "#ef4444", "avatar": "💣"}
    ],
    "lines": [
        {"characterId": "ganyotcu", "startTime": 0.94, "endTime": 2.44, "text": "Aleykümselam Sabri hoş geldin."},
        {"characterId": "sabri", "startTime": 2.72, "endTime": 4.44, "text": "Ganyotçu abi sıkıntı var sıkıntı!"},
        {"characterId": "ganyotcu", "startTime": 4.92, "endTime": 5.46, "text": "Hayırdır?"},
        {"characterId": "sabri", "startTime": 5.92, "endTime": 7.72, "text": "Sorma abi başıma neler geldi abi!"},
        {"characterId": "sabri", "startTime": 7.8, "endTime": 10.28, "text": "Dayak yedim, paramızı çantaları takmadan çaldılar..."},
        {"characterId": "sabri", "startTime": 10.28, "endTime": 12.22, "text": "Bir de bunu bırakıp gittiler abi!"},
        {"characterId": "ganyotcu", "startTime": 12.98, "endTime": 14.66, "text": "Üstündeki ne lan, bankamatik mi?"},
        {"characterId": "sabri", "startTime": 14.86, "endTime": 16.08, "text": "Yok abi saatli bomba!"},
        {"characterId": "ganyotcu", "startTime": 16.5, "endTime": 18.42, "text": "Nasıl saatli bomba lan? Saati durmuş bunun!"}
    ]
}

# 7. Soruya Soruyla Cevap Verme
PERFECT_SCENES["meme-sonuc-ne-soru-cevap"] = {
    "title": "Röportaj - Soruya Soruyla Cevap Verme!",
    "description": "Efsanevi dükkan diyaloğu: Nargileci Abi ile muhabir gencin kısır döngü tartışması.",
    "characters": [
        {"id": "muhabir", "name": "Muhabir Genç", "color": "#0ea5e9", "avatar": "🎙️"},
        {"id": "dayi", "name": "Nargileci Dayı", "color": "#10b981", "avatar": "🧔"}
    ],
    "lines": [
        {"characterId": "muhabir", "startTime": 0.0, "endTime": 0.76, "text": "Eee?"},
        {"characterId": "dayi", "startTime": 1.1, "endTime": 1.8, "text": "Eee?"},
        {"characterId": "muhabir", "startTime": 1.92, "endTime": 2.32, "text": "Sonuç?"},
        {"characterId": "dayi", "startTime": 2.44, "endTime": 3.06, "text": "Sonuç ne?"},
        {"characterId": "muhabir", "startTime": 3.42, "endTime": 4.1, "text": "Sana soruyorum!"},
        {"characterId": "dayi", "startTime": 4.22, "endTime": 5.14, "text": "Sana ben soruyorum!"},
        {"characterId": "muhabir", "startTime": 5.28, "endTime": 6.22, "text": "Sen bana niye soruyorsun ki?"},
        {"characterId": "dayi", "startTime": 6.54, "endTime": 7.8, "text": "Sen bana niye soruyorsun ki?!"},
        {"characterId": "muhabir", "startTime": 7.8, "endTime": 8.66, "text": "Ben soruyorum soruyu!"},
        {"characterId": "dayi", "startTime": 9.24, "endTime": 10.54, "text": "Soruya soruyla cevap verme!"},
        {"characterId": "muhabir", "startTime": 10.76, "endTime": 12.34, "text": "Nasıl soruya soruyla cevap verme?!"}
    ]
}

# 8. Bear I Love You
PERFECT_SCENES["meme-00e48267f85a643e"] = {
    "title": "Parodi - Bear I Love You So So Much",
    "description": "Viral ilişki ve itiraf parodisi sahnesi.",
    "characters": [
        {"id": "nikki", "name": "Nikki", "color": "#ec4899", "avatar": "👱‍♀️"},
        {"id": "bear", "name": "Bear", "color": "#8b5cf6", "avatar": "🧸"}
    ],
    "lines": [
        {"characterId": "nikki", "startTime": 0.0, "endTime": 3.28, "text": "Bear, I love you so, so much."},
        {"characterId": "nikki", "startTime": 3.89, "endTime": 5.87, "text": "I don't think I could live without you."},
        {"characterId": "bear", "startTime": 10.96, "endTime": 13.16, "text": "You love me more than anyone in the world?"},
        {"characterId": "nikki", "startTime": 18.03, "endTime": 19.59, "text": "Yes, more than anyone."},
        {"characterId": "bear", "startTime": 23.82, "endTime": 24.84, "text": "Nikki?"},
        {"characterId": "nikki", "startTime": 26.28, "endTime": 27.28, "text": "Yeah?"},
        {"characterId": "bear", "startTime": 28.11, "endTime": 29.49, "text": "Does your dad really have cancer?"},
        {"characterId": "nikki", "startTime": 49.02, "endTime": 51.5, "text": "No... no... no..."},
        {"characterId": "bear", "startTime": 52.39, "endTime": 53.39, "text": "What?!"}
    ]
}

# 9. Çığlık Atan Çocuk
PERFECT_SCENES["meme-01bda7b30a7b9e4b"] = {
    "title": "Viral - Çığlık Atan Çocuk",
    "description": "Oyun oynarken birden çılgına dönüp ekran başında bağıran çocuk klasiği.",
    "characters": [
        {"id": "cocuk", "name": "Çığlık Atan Çocuk", "color": "#f97316", "avatar": "👦"}
    ],
    "lines": [
        {"characterId": "cocuk", "startTime": 26.3, "endTime": 28.5, "text": "Okay..."},
        {"characterId": "cocuk", "startTime": 30.0, "endTime": 33.5, "text": "AAAAAA! YETER ARTIK YETER!"},
        {"characterId": "cocuk", "startTime": 34.5, "endTime": 37.0, "text": "İSTEMİYORUM ARTIK!"}
    ]
}

# 10. Sıfır Bir Garip
PERFECT_SCENES["meme-021005e91e320d20"] = {
    "title": "Sıfır Bir - Bu Aslan Parçasının Adı Garip",
    "description": "Sıfır Bir çatı sahnesi: Savaş'ın Garip'i Cio ve ekibe emanet ettiği racon anı.",
    "characters": [
        {"id": "savas", "name": "Savaş Satış", "color": "#3b82f6", "avatar": "🧔"},
        {"id": "cio", "name": "Cio Baba", "color": "#ef4444", "avatar": "🔫"},
        {"id": "garip", "name": "Garip", "color": "#10b981", "avatar": "🧑"}
    ],
    "lines": [
        {"characterId": "savas", "startTime": 0.0, "endTime": 1.66, "text": "Bu aslan parçasının adı Garip."},
        {"characterId": "savas", "startTime": 3.04, "endTime": 4.98, "text": "Artık Garip sizin kardeşinizdir."},
        {"characterId": "cio", "startTime": 5.48, "endTime": 6.14, "text": "Hoş geldiniz abi."},
        {"characterId": "savas", "startTime": 6.64, "endTime": 7.06, "text": "Eyvallah."},
        {"characterId": "cio", "startTime": 7.66, "endTime": 8.76, "text": "Hoş geldin kardeş."},
        {"characterId": "savas", "startTime": 12.14, "endTime": 13.36, "text": "Garip, bu Oltacı'dır."},
        {"characterId": "savas", "startTime": 14.66, "endTime": 15.3, "text": "Garip!"},
        {"characterId": "garip", "startTime": 15.58, "endTime": 15.92, "text": "Buyur abi."},
        {"characterId": "cio", "startTime": 16.74, "endTime": 18.62, "text": "Oğlum artık bunlar senin abilerindir."},
        {"characterId": "garip", "startTime": 18.94, "endTime": 19.26, "text": "Eyvallah."},
        {"characterId": "cio", "startTime": 19.58, "endTime": 21.8, "text": "Sen ölmeden bunlara bir şey olmayacak."},
        {"characterId": "cio", "startTime": 22.62, "endTime": 23.12, "text": "Anladın?"},
        {"characterId": "garip", "startTime": 23.3, "endTime": 24.34, "text": "Başım gözüm üstüne abi."},
        {"characterId": "cio", "startTime": 25.06, "endTime": 25.5, "text": "Heh."},
        {"characterId": "savas", "startTime": 27.14, "endTime": 29.06, "text": "Burada da emanetleriniz var, ver oğlum."},
        {"characterId": "cio", "startTime": 33.0, "endTime": 33.96, "text": "Bize müsaade."}
    ]
}

# 11. Sınıf Başkanı
PERFECT_SCENES["meme-0c8ee1a80532ffce"] = {
    "title": "Viral - Ben Bu Sınıfın Sınıf Başkanıyım!",
    "description": "Okul koridorunda sınıf başkanının diğer öğrenciye otorite kurmaya çalıştığı viral video.",
    "characters": [
        {"id": "baskan", "name": "Sınıf Başkanı", "color": "#ef4444", "avatar": "📢"},
        {"id": "ogrenci", "name": "İsyankar Öğrenci", "color": "#3b82f6", "avatar": "🎒"}
    ],
    "lines": [
        {"characterId": "baskan", "startTime": 0.3, "endTime": 3.0, "text": "Senin böyle konuşmaya ne hakkın var?!"},
        {"characterId": "ogrenci", "startTime": 3.3, "endTime": 5.0, "text": "Sana ne oğlum, sana ne?!"},
        {"characterId": "baskan", "startTime": 5.3, "endTime": 8.5, "text": "Sen öğretmenine de mi böyle konuşuyorsun terbiyesiz?!"},
        {"characterId": "ogrenci", "startTime": 8.6, "endTime": 10.5, "text": "Sana ne lan, sana ne?!"},
        {"characterId": "baskan", "startTime": 11.0, "endTime": 13.5, "text": "Ne demek sana ne? Ya sabır Allah'ım!"},
        {"characterId": "baskan", "startTime": 14.5, "endTime": 16.0, "text": "Evet her şeyi bilirim ben!"},
        {"characterId": "baskan", "startTime": 16.42, "endTime": 19.64, "text": "Ben bu sınıfın sınıf başkanıysam her şeyi bilmek zorundayım!"},
        {"characterId": "ogrenci", "startTime": 21.66, "endTime": 23.5, "text": "Sana ne ya, sana ne?!"},
        {"characterId": "baskan", "startTime": 29.88, "endTime": 32.26, "text": "Herkes üstüme geliyor ya yok böyle bir şey!"}
    ]
}

# 12. Recep İvedik Deve
PERFECT_SCENES["meme-1094542b34c286b1"] = {
    "title": "Recep İvedik - Deveyle Göz Göze Gelme & Turkcell Tarifesi",
    "description": "Recep İvedik Psikolog sahnesi: Deve travması anlatımı ve araya giren telefon tarifesi görüşmesi.",
    "characters": [
        {"id": "recep", "name": "Recep İvedik", "color": "#f97316", "avatar": "🧔"},
        {"id": "operator", "name": "Müşteri Temsilcisi", "color": "#06b6d4", "avatar": "🎧"},
        {"id": "psikolog", "name": "Psikolog", "color": "#64748b", "avatar": "📋"}
    ],
    "lines": [
        {"characterId": "recep", "startTime": 4.08, "endTime": 6.46, "text": "O meymenetsiz hayvanla göz göze gelince..."},
        {"characterId": "recep", "startTime": 6.46, "endTime": 8.54, "text": "Bir de bir gözü büyük bir gözü ufak böyle..."},
        {"characterId": "recep", "startTime": 8.54, "endTime": 11.36, "text": "Böyle iki tane hörgücü var, kakası var böyle kapkara..."},
        {"characterId": "recep", "startTime": 11.36, "endTime": 13.24, "text": "Bütün psikolojim altüst oldu yani."},
        {"characterId": "recep", "startTime": 13.74, "endTime": 15.12, "text": "Kusura bakmayın parazel, affedersiniz. Efendim?"},
        {"characterId": "operator", "startTime": 18.14, "endTime": 20.74, "text": "Recep Bey, ben Turkcell'den arıyorum."},
        {"characterId": "operator", "startTime": 21.54, "endTime": 22.7, "text": "Biz faturalarınızı inceledik."},
        {"characterId": "recep", "startTime": 22.76, "endTime": 23.2, "text": "Neden?"},
        {"characterId": "operator", "startTime": 23.5, "endTime": 25.02, "text": "Çok daha ucuza konuşabilmeniz için."},
        {"characterId": "recep", "startTime": 25.22, "endTime": 25.5, "text": "He."},
        {"characterId": "operator", "startTime": 25.6, "endTime": 28.42, "text": "Şu an avantajlı dakika paketlerimizden birini seçerseniz..."},
        {"characterId": "operator", "startTime": 28.42, "endTime": 30.78, "text": "Aldığınız dakika kadar hediye dakika kazanacaksınız."},
        {"characterId": "recep", "startTime": 31.0, "endTime": 32.32, "text": "Sağ ol ben almayayım."},
        {"characterId": "recep", "startTime": 32.52, "endTime": 35.2, "text": "Benim için böyle bir fedakarlık yapmanıza gerek yok lütfen ben memnunum."},
        {"characterId": "operator", "startTime": 35.34, "endTime": 37.72, "text": "Recep Bey, bu şekilde konuşmalarınızın dakikası..."},
        {"characterId": "recep", "startTime": 37.8, "endTime": 38.3, "text": "Nasıl?"},
        {"characterId": "operator", "startTime": 38.4, "endTime": 39.18, "text": "En fazla sekiz kuruşa gelecek."},
        {"characterId": "recep", "startTime": 39.18, "endTime": 40.76, "text": "Hemen geçelim, hemen geçelim!"},
        {"characterId": "operator", "startTime": 41.02, "endTime": 41.9, "text": "Onaylıyor musunuz?"},
        {"characterId": "recep", "startTime": 42.34, "endTime": 42.86, "text": "Onaylıyorum!"},
        {"characterId": "operator", "startTime": 43.18, "endTime": 45.12, "text": "Çok teşekkür ederim Recep Bey, iyi günler."},
        {"characterId": "recep", "startTime": 45.4, "endTime": 45.92, "text": "Sağ ol bebeğim."},
        {"characterId": "psikolog", "startTime": 48.28, "endTime": 49.0, "text": "Vaktiniz doldu Recep Bey."},
        {"characterId": "recep", "startTime": 49.34, "endTime": 50.02, "text": "Bir saat oldu mu?"},
        {"characterId": "psikolog", "startTime": 50.34, "endTime": 50.82, "text": "Oldu tabii."},
        {"characterId": "recep", "startTime": 51.22, "endTime": 51.78, "text": "Borcumuz ne kadar?"},
        {"characterId": "psikolog", "startTime": 52.02, "endTime": 53.02, "text": "Yüz elli YTL."},
        {"characterId": "recep", "startTime": 53.68, "endTime": 54.5, "text": "Yuh!"},
        {"characterId": "recep", "startTime": 55.02, "endTime": 56.14, "text": "Demin kadın aradı söyledi..."},
        {"characterId": "recep", "startTime": 56.14, "endTime": 59.66, "text": "Ben seni arasam dakikası 8 kuruştan saati 5 YTL bile etmiyor!"},
        {"characterId": "recep", "startTime": 60.18, "endTime": 62.3, "text": "Hadi git! Beni kendimle baş başa bırak!"},
        {"characterId": "recep", "startTime": 62.86, "endTime": 64.18, "text": "Tarifenin keyfini çıkartacağım!"}
    ]
}

# 13. The Mentalist Can Pen
PERFECT_SCENES["meme-27377eac7c1dbc11"] = {
    "title": "The Mentalist - Patrick Jane 'Can Pen' Çince Sorgusu",
    "description": "Patrick Jane beden diliyle Çinli görgü tanığını sorgularken Ajan Cho ve Lisbon izliyor.",
    "characters": [
        {"id": "lisbon", "name": "Ajan Lisbon", "color": "#ef4444", "avatar": "👩‍💼"},
        {"id": "jane", "name": "Patrick Jane", "color": "#3b82f6", "avatar": "🕵️"},
        {"id": "cho", "name": "Ajan Cho", "color": "#64748b", "avatar": "👮‍♂️"},
        {"id": "canpen", "name": "Can Pen (Tanık)", "color": "#10b981", "avatar": "👧"}
    ],
    "lines": [
        {"characterId": "lisbon", "startTime": 0.0, "endTime": 4.16, "text": "Kızın adı Can Pen. Çinli, dilimizi bilmiyor."},
        {"characterId": "jane", "startTime": 5.1, "endTime": 5.52, "text": "Tamam."},
        {"characterId": "jane", "startTime": 6.7, "endTime": 8.76, "text": "Merhaba, benim adım Patrick."},
        {"characterId": "jane", "startTime": 9.06, "endTime": 11.36, "text": "Tamam, hoş geldin."},
        {"characterId": "cho", "startTime": 11.86, "endTime": 14.42, "text": "Bir tercümana ihtiyacımız olacak."},
        {"characterId": "jane", "startTime": 15.8, "endTime": 18.0, "text": "Omuzundaki o iğrenç şey..."},
        {"characterId": "jane", "startTime": 18.64, "endTime": 22.6, "text": "Dilimizi konuşuyor ama biraz utangaç değil mi?"},
        {"characterId": "canpen", "startTime": 24.72, "endTime": 27.74, "text": "Dilinizi konuşmam, erkekler benimle konuşmaz."},
        {"characterId": "jane", "startTime": 28.12, "endTime": 28.98, "text": "Böylesi daha iyi."},
        {"characterId": "jane", "startTime": 28.98, "endTime": 30.88, "text": "Bay Pochette vurulduğunda ne gördün?"},
        {"characterId": "canpen", "startTime": 31.14, "endTime": 31.86, "text": "Hiçbir şey."},
        {"characterId": "canpen", "startTime": 32.28, "endTime": 35.98, "text": "Ödümü koparan korkunç bir silah sesi duydum ve adam öldü."},
        {"characterId": "canpen", "startTime": 36.44, "endTime": 37.46, "text": "Korkmuştum bu kadar."},
        {"characterId": "jane", "startTime": 37.6, "endTime": 38.68, "text": "Vuran kişi nasıl biriydi?"},
        {"characterId": "canpen", "startTime": 38.94, "endTime": 39.28, "text": "Görmedim."},
        {"characterId": "jane", "startTime": 39.62, "endTime": 40.48, "text": "İyi bir yalancısın."},
        {"characterId": "jane", "startTime": 40.84, "endTime": 41.9, "text": "İyi ama çok iyi değil."},
        {"characterId": "jane", "startTime": 42.88, "endTime": 44.18, "text": "Onu yakından görmüş."}
    ]
}

# 14. Akraba Tanıtma Çilesi
PERFECT_SCENES["meme-3e05e9c18616c529"] = {
    "title": "Viral - Akraba Tanıtma Çilesi (Anneanne vs Torun & Kevser)",
    "description": "Anneannenin toruna zorla sülale akrabalarını ezberletmeye çalıştığı, Kevser teyzenin de araya girdiği çile sahnesi.",
    "characters": [
        {"id": "anneanne", "name": "Anneanne", "color": "#ec4899", "avatar": "👵"},
        {"id": "torun", "name": "Torun", "color": "#3b82f6", "avatar": "👦"},
        {"id": "kevser", "name": "Kevser Teyze", "color": "#10b981", "avatar": "👩"}
    ],
    "lines": [
        {"characterId": "anneanne", "startTime": 0.0, "endTime": 2.98, "text": "Bak kim bu? Bu benim en küçük torunum."},
        {"characterId": "torun", "startTime": 3.12, "endTime": 3.84, "text": "Hıooo!"},
        {"characterId": "anneanne", "startTime": 4.22, "endTime": 6.16, "text": "Eee sen tanıdın mı onu, kim o?"},
        {"characterId": "torun", "startTime": 6.44, "endTime": 7.16, "text": "Hatırlamadım."},
        {"characterId": "anneanne", "startTime": 7.68, "endTime": 11.34, "text": "Bak onun dedesiyle benim amcam kardeş!"},
        {"characterId": "anneanne", "startTime": 11.62, "endTime": 14.16, "text": "Ha onun dedesiyle senin ne olacak? Kardeş!"},
        {"characterId": "anneanne", "startTime": 14.48, "endTime": 16.02, "text": "Çocuklarının kayınçosu!"},
        {"characterId": "anneanne", "startTime": 18.14, "endTime": 21.04, "text": "Bunun iç güveysi kimmiş hadi söyle bakayım bana!"},
        {"characterId": "torun", "startTime": 21.2, "endTime": 23.8, "text": "Onun kayınçosu, nasıl amcam?"},
        {"characterId": "anneanne", "startTime": 24.18, "endTime": 25.42, "text": "Öyle değil bak!"},
        {"characterId": "kevser", "startTime": 25.72, "endTime": 26.94, "text": "Abla zorlama çocuğu ya!"},
        {"characterId": "anneanne", "startTime": 27.06, "endTime": 29.0, "text": "Ağlamasın! Öğrensin çocuk!"},
        {"characterId": "anneanne", "startTime": 29.0, "endTime": 29.8, "text": "Kimmiş söyle?!"},
        {"characterId": "torun", "startTime": 31.98, "endTime": 32.98, "text": "Öyle değil!"},
        {"characterId": "anneanne", "startTime": 33.3, "endTime": 34.34, "text": "Düzgün söyle kim?!"},
        {"characterId": "kevser", "startTime": 34.58, "endTime": 36.28, "text": "Allah Allah tamam ağlama oğlum..."},
        {"characterId": "anneanne", "startTime": 36.28, "endTime": 38.14, "text": "Öğrenecek o! Bu iş burada bitmedi!"},
        {"characterId": "anneanne", "startTime": 40.86, "endTime": 42.92, "text": "Sakın bak ses çıkartma gebertirim!"},
        {"characterId": "torun", "startTime": 43.16, "endTime": 43.66, "text": "Hı hı."},
        {"characterId": "anneanne", "startTime": 43.74, "endTime": 45.66, "text": "Heh kim şu hatırladın mı bak bakayım?"},
        {"characterId": "anneanne", "startTime": 47.9, "endTime": 50.78, "text": "Onun amcasıyla benim teyzemin çocukları kardeş!"},
        {"characterId": "anneanne", "startTime": 51.06, "endTime": 51.72, "text": "Kimmiş söyle?!"},
        {"characterId": "kevser", "startTime": 52.24, "endTime": 54.0, "text": "Oğlum teyzeni tanıdın mı sen?"},
        {"characterId": "anneanne", "startTime": 54.32, "endTime": 57.4, "text": "O değil! Onun teyzelerini bileceksin!"}
    ]
}

# 15. Unlost Bloklama
PERFECT_SCENES["meme-414a57bd5b2e7e34"] = {
    "title": "Cantuğ 'Unlost' - CS:GO Dust 2 'Beni Bloklama' Öfkesi",
    "description": "Unlost'un CS:GO maçında takım arkadaşının kapıda bloklaması üzerine çılgına dönmesi.",
    "characters": [
        {"id": "unlost", "name": "Cantuğ (Unlost)", "color": "#ef4444", "avatar": "🎯"},
        {"id": "teammate", "name": "Takım Arkadaşı", "color": "#3b82f6", "avatar": "🛡️"}
    ],
    "lines": [
        {"characterId": "unlost", "startTime": 0.0, "endTime": 0.92, "text": "Beni bloklama!"},
        {"characterId": "unlost", "startTime": 1.8, "endTime": 3.46, "text": "Bloklama ya! Söyledim bir de ya!"},
        {"characterId": "unlost", "startTime": 4.44, "endTime": 5.86, "text": "Evrilmiş, nasıl evrilmiş ya?!"},
        {"characterId": "unlost", "startTime": 11.9, "endTime": 13.74, "text": "İşte buydu abi ya!"},
        {"characterId": "unlost", "startTime": 13.74, "endTime": 16.72, "text": "Yıllardır yapmadığım özel vuruşum buydu beyler!"},
        {"characterId": "unlost", "startTime": 17.22, "endTime": 18.5, "text": "Teşekkürler beyler arkadaşlar."},
        {"characterId": "unlost", "startTime": 21.22, "endTime": 22.5, "text": "Beni bloklamayın artık!"}
    ]
}

# 16. KV Şu Teybi Kapatır Mısın
PERFECT_SCENES["meme-43a4d9b0fddc8d10"] = {
    "title": "Kurtlar Vadisi - Şu Teybi Kapatır Mısın?",
    "description": "Kurtlar Vadisi efsane sahne: Memati Baş'ın takside teybi kapatmayan şoföre patlaması.",
    "characters": [
        {"id": "memati", "name": "Memati Baş", "color": "#0f172a", "avatar": "🔫"},
        {"id": "sofor", "name": "Şoför", "color": "#f59e0b", "avatar": "🚕"}
    ],
    "lines": [
        {"characterId": "memati", "startTime": 1.32, "endTime": 2.04, "text": "Dayıcım!"},
        {"characterId": "memati", "startTime": 2.86, "endTime": 6.32, "text": "Bir şey konuşuyoruz da, şu teybi kapatır mısın?"},
        {"characterId": "memati", "startTime": 12.3, "endTime": 13.02, "text": "Hey!"},
        {"characterId": "memati", "startTime": 14.36, "endTime": 15.08, "text": "Kime diyorum?!"},
        {"characterId": "memati", "startTime": 18.96, "endTime": 19.84, "text": "Şu teybi kapatsana!"},
        {"characterId": "memati", "startTime": 21.92, "endTime": 24.36, "text": "Dayı kapat şu teybi arıza çıkacak bak ha!"},
        {"characterId": "memati", "startTime": 25.36, "endTime": 26.28, "text": "Kapatsana lan!"},
        {"characterId": "memati", "startTime": 30.0, "endTime": 30.64, "text": "Kapatsana!"},
        {"characterId": "memati", "startTime": 33.52, "endTime": 34.74, "text": "Kapatsana şunu deli etme adamı!"}
    ]
}

# 17. Doktor Bey Bu Çocuk Isırıyor
PERFECT_SCENES["meme-48b70fd6e5bc2cd8"] = {
    "title": "Recep İvedik - Doktor Bey Bu Çocuk Isırıyor",
    "description": "Recep İvedik hastane sırasında beklerken dertli annenin saldırgan çocuğuna patlıyor: 'Bu adamın asabını bozma!'",
    "characters": [
        {"id": "recep", "name": "Recep İvedik", "color": "#ef4444", "avatar": "🧔"},
        {"id": "anne", "name": "Dertli Anne", "color": "#ec4899", "avatar": "👩‍👦"},
        {"id": "doktor", "name": "Doktor", "color": "#06b6d4", "avatar": "🩺"}
    ],
    "lines": [
        {"characterId": "doktor", "startTime": 0.0, "endTime": 1.14, "text": "Sizin neyiniz vardı?"},
        {"characterId": "anne", "startTime": 1.62, "endTime": 4.06, "text": "Benim çocuk hasta, oraya buraya saldırıyor!"},
        {"characterId": "anne", "startTime": 4.34, "endTime": 6.3, "text": "Bana saldırıyor, boynumu ısırdı!"},
        {"characterId": "anne", "startTime": 7.0, "endTime": 9.0, "text": "Bu tarafımı ısırdı, kulağımı ısırdı!"},
        {"characterId": "anne", "startTime": 9.36, "endTime": 10.14, "text": "Elimi kaptı!"},
        {"characterId": "doktor", "startTime": 10.3, "endTime": 11.26, "text": "Bunları bu mu yaptı ya?"},
        {"characterId": "anne", "startTime": 11.62, "endTime": 13.54, "text": "Evet böyle saldırganlık hastalığı var."},
        {"characterId": "recep", "startTime": 15.36, "endTime": 16.82, "text": "Oğlum neden annene... Lan!"},
        {"characterId": "recep", "startTime": 20.02, "endTime": 22.42, "text": "Oğlum bu adamın asabını bozma!"},
        {"characterId": "recep", "startTime": 22.56, "endTime": 23.8, "text": "Ağzını burnunu kırarım ha!"},
        {"characterId": "recep", "startTime": 28.34, "endTime": 31.86, "text": "Lan! Sen deliysen ben de deliyim lan!"},
        {"characterId": "recep", "startTime": 34.42, "endTime": 36.6, "text": "Oğlum o iki gözünü çıkartırım burada!"},
        {"characterId": "recep", "startTime": 39.34, "endTime": 40.74, "text": "Bir şey konuşuyoruz dinle lan!"},
        {"characterId": "anne", "startTime": 43.4, "endTime": 44.04, "text": "Yapma oğlum..."},
        {"characterId": "recep", "startTime": 45.16, "endTime": 46.74, "text": "Kafanı vurursun bak buraya!"},
        {"characterId": "recep", "startTime": 51.72, "endTime": 54.38, "text": "Abla şuna bir zincir mincir takın bir şey yapın ya, böyle olmaz!"},
        {"characterId": "doktor", "startTime": 55.36, "endTime": 58.56, "text": "Pitbull bile dolaştırmak yasalara aykırı, bunu dolaştırmayın sokakta!"}
    ]
}

# 18. Ne Dedin Lan
PERFECT_SCENES["meme-493f3ad55c94c4cf"] = {
    "title": "Viral - Ne Dedin Lan! (Kılıçdaroğlu Kazandı)",
    "description": "Oturma odasında gencin 'Kılıçdaroğlu Konya'yı kazandı' şakasına takkeli dedenin hiddetli tepkisi.",
    "characters": [
        {"id": "dede", "name": "Takkeli Dede", "color": "#ef4444", "avatar": "👴"},
        {"id": "genc", "name": "Genç", "color": "#3b82f6", "avatar": "📱"}
    ],
    "lines": [
        {"characterId": "genc", "startTime": 1.54, "endTime": 3.08, "text": "Kılıçdaroğlu Konya'yı kazandı!"},
        {"characterId": "dede", "startTime": 3.86, "endTime": 4.5, "text": "Ne diyorsun lan?!"},
        {"characterId": "genc", "startTime": 4.82, "endTime": 5.2, "text": "Valla!"},
        {"characterId": "genc", "startTime": 6.12, "endTime": 7.1, "text": "Kılıçdaroğlu kazandı."},
        {"characterId": "dede", "startTime": 7.22, "endTime": 7.34, "text": "Ne?!"},
        {"characterId": "dede", "startTime": 7.64, "endTime": 8.4, "text": "Ne diyorsun lan?!"},
        {"characterId": "genc", "startTime": 9.9, "endTime": 10.44, "text": "Ne olacak?"},
        {"characterId": "dede", "startTime": 12.34, "endTime": 13.44, "text": "Ulan ne dedin sen?!"}
    ]
}

# 19. Benim Adım Cafer
PERFECT_SCENES["meme-4b5781e28db674b5"] = {
    "title": "Viral - Benim Adım Cafer (Alayınıza Gider)",
    "description": "Sokak röportajı efsanesi: Cafer'in kendini tanıttığı unutulmaz monolog.",
    "characters": [
        {"id": "cafer", "name": "Cafer", "color": "#ef4444", "avatar": "😎"},
        {"id": "spiker", "name": "Röportajcı Genç", "color": "#3b82f6", "avatar": "🎤"}
    ],
    "lines": [
        {"characterId": "cafer", "startTime": 0.0, "endTime": 2.22, "text": "Benim adım Cafer. Boyum bir on."},
        {"characterId": "cafer", "startTime": 2.88, "endTime": 3.74, "text": "Kilom yirmi beş."},
        {"characterId": "cafer", "startTime": 4.46, "endTime": 5.84, "text": "Gözlerimin rengini bilmiyorum."},
        {"characterId": "cafer", "startTime": 6.56, "endTime": 8.14, "text": "Ciguli'yi dinlemeyi severim."},
        {"characterId": "cafer", "startTime": 8.84, "endTime": 12.48, "text": "En sevdiğim yazar Manapınarından Hacıbeyin Ahmet."},
        {"characterId": "cafer", "startTime": 12.78, "endTime": 16.32, "text": "Sevdiğim futbolcu Yenimahalle'den Abidin'in Mehmet."},
        {"characterId": "cafer", "startTime": 16.74, "endTime": 19.74, "text": "Samsun 216 ve Parliament'i severim."},
        {"characterId": "cafer", "startTime": 20.3, "endTime": 24.04, "text": "Doğunun bir atasözü vardır: Sağlığınız için Yeni Rakı için!"},
        {"characterId": "cafer", "startTime": 24.86, "endTime": 27.5, "text": "Kısa boylu ve mavi gözlü kızları severim."},
        {"characterId": "cafer", "startTime": 27.5, "endTime": 31.18, "text": "Tatilimi Namazgâh Dağları'nda geçiriyorum."},
        {"characterId": "cafer", "startTime": 31.66, "endTime": 34.38, "text": "En sevdiğim araba Murat 131."},
        {"characterId": "cafer", "startTime": 35.22, "endTime": 36.84, "text": "Tekno ve kemençeye bayılırım."},
        {"characterId": "cafer", "startTime": 37.36, "endTime": 39.02, "text": "Mekanım Yenimahalle."},
        {"characterId": "cafer", "startTime": 39.1, "endTime": 41.08, "text": "Lakabım 35'lik Rakı."},
        {"characterId": "cafer", "startTime": 41.9, "endTime": 45.68, "text": "En sevdiğim hocam ilkokulda Kenan hocam."},
        {"characterId": "cafer", "startTime": 45.82, "endTime": 48.92, "text": "En sevdiğim komedyen Yenimahalle'den Michael."},
        {"characterId": "cafer", "startTime": 52.42, "endTime": 55.78, "text": "En uyuz olduğum şey, tek sigaramın istenmesi."},
        {"characterId": "cafer", "startTime": 56.72, "endTime": 58.42, "text": "Kafamda hep pis işler."},
        {"characterId": "cafer", "startTime": 58.62, "endTime": 62.58, "text": "Benim adım Cafer! Alayınıza gider! Korkun benden!"},
        {"characterId": "spiker", "startTime": 63.14, "endTime": 63.96, "text": "Senden mi Cafer?"},
        {"characterId": "cafer", "startTime": 64.16, "endTime": 65.04, "text": "Evet benden!"}
    ]
}

# 20. KV Kahveci Cemal
PERFECT_SCENES["meme-54c6bba12da44d49"] = {
    "title": "Kurtlar Vadisi - Kahveci Cemal Çakır Baskınını Anlatıyor",
    "description": "Kurtlar Vadisi 1. Sezon: Çakır'ın kahveyi basışını Cemal Meral'e anlatıyor.",
    "characters": [
        {"id": "meral", "name": "Meral", "color": "#db2777", "avatar": "👩"},
        {"id": "cemal", "name": "Kahveci Cemal", "color": "#4b5563", "avatar": "☕"}
    ],
    "lines": [
        {"characterId": "cemal", "startTime": 0.0, "endTime": 0.76, "text": "Kahveye geldi..."},
        {"characterId": "meral", "startTime": 1.42, "endTime": 2.68, "text": "Nasıl kahveye geldi?!"},
        {"characterId": "cemal", "startTime": 3.46, "endTime": 4.98, "text": "Geldi lafını söyledi gitti..."},
        {"characterId": "meral", "startTime": 6.0, "endTime": 7.2, "text": "Nasıl gitti Cemal?!"},
        {"characterId": "cemal", "startTime": 8.1, "endTime": 11.02, "text": "Abla geldi bir tufan, gitti bir boran..."},
        {"characterId": "cemal", "startTime": 11.76, "endTime": 15.02, "text": "Gövde üstünde baş, baş üstünde akıl bırakmadı... Esti geçti!"},
        {"characterId": "meral", "startTime": 16.62, "endTime": 17.66, "text": "Kaç kişi bastı?"},
        {"characterId": "cemal", "startTime": 17.98, "endTime": 20.42, "text": "Bir o, bir de ondan kara bir oğlan."},
        {"characterId": "meral", "startTime": 21.02, "endTime": 23.0, "text": "İki kişi fiyakanızı mı kesti Cemal?!"},
        {"characterId": "cemal", "startTime": 23.72, "endTime": 25.66, "text": "Halit Ağa benim aklım bu işlere ermez."},
        {"characterId": "cemal", "startTime": 26.34, "endTime": 30.86, "text": "Ama bu yaşa geldim, bu kadar aslan gördüm, böylesini görmedim!"},
        {"characterId": "cemal", "startTime": 31.42, "endTime": 33.62, "text": "Koca kahveyi cephaneliğe çevirdi, çizdi gitti..."}
    ]
}

print(f"Bölüm 1 hazırlandı: {len(PERFECT_SCENES)} sahne.")
