import os
import sys

PERFECT_SCENES_5 = {}

# 51. Tut Lan Aşağı Atlıyorum
PERFECT_SCENES_5["meme-ec13d57c1425f814"] = {
    "title": "Viral Video - 'Tut Lan Ben De Aşağı Atlıyorum!'",
    "description": "Balkondan aşağı atlayan gençlerin viral videosu.",
    "characters": [
        {"id": "atlayan", "name": "Atlayan Genç", "color": "#ef4444", "avatar": "🤸"}
    ],
    "lines": [
        {"characterId": "atlayan", "startTime": 8.6, "endTime": 13.5, "text": "Tut lan beni! Ben de aşağı atlıyorum, abone olmayı unutmayın!"}
    ]
}

# 52. KV Laz Ziya vs Testere Necmi
PERFECT_SCENES_5["meme-f0a445c3a2b4afaa"] = {
    "title": "Kurtlar Vadisi - Laz Ziya vs Testere Necmi Konsey Çatışması",
    "description": "Kurtlar Vadisi Konsey Sahnesi: Laz Ziya'nın resti ve Testere Necmi'nin öfke patlaması.",
    "characters": [
        {"id": "laz_ziya", "name": "Laz Ziya", "color": "#1e3a8a", "avatar": "👴"},
        {"id": "testere_necmi", "name": "Testere Necmi", "color": "#dc2626", "avatar": "🪚"}
    ],
    "lines": [
        {"characterId": "laz_ziya", "startTime": 0.0, "endTime": 6.14, "text": "O zaman Ziya Bey benden özür dileyip bu düşmanlığa bir son verecek!"},
        {"characterId": "laz_ziya", "startTime": 6.68, "endTime": 11.06, "text": "Çünkü ben onlara kardeşlikten başka hiçbir şey yapmadım."},
        {"characterId": "testere_necmi", "startTime": 11.74, "endTime": 12.7, "text": "Ulan!"},
        {"characterId": "testere_necmi", "startTime": 14.34, "endTime": 16.06, "text": "Senin yuların mıyım?!"},
        {"characterId": "testere_necmi", "startTime": 17.2, "endTime": 19.68, "text": "Üstünde çağdan mıyım ki?"},
        {"characterId": "testere_necmi", "startTime": 20.96, "endTime": 23.74, "text": "Gözümün içine bakarak beni tehdit edeceksin..."},
        {"characterId": "testere_necmi", "startTime": 24.74, "endTime": 25.86, "text": "Güzel!"},
        {"characterId": "testere_necmi", "startTime": 27.72, "endTime": 30.56, "text": "Utanmadan benden özür bekleyeceksin öyle mi?!"}
    ]
}

# 53. Ahmet Şık Hükümet İstifa
PERFECT_SCENES_5["meme-f337b03a431b512d"] = {
    "title": "Röportaj - Ahmet Şık Hükümet İstifa Dediniz Mi?",
    "description": "Adliye çıkışında muhabirin 'Hükümet istifa dediniz mi?' sorusuna Ahmet Şık'ın yanıtı.",
    "characters": [
        {"id": "muhabir", "name": "Muhabir", "color": "#3b82f6", "avatar": "🎤"},
        {"id": "ahmet", "name": "Ahmet Şık", "color": "#10b981", "avatar": "👓"}
    ],
    "lines": [
        {"characterId": "muhabir", "startTime": 0.68, "endTime": 3.22, "text": "Megafonu elinize alıp 'hükümet istifa' dediniz mi?"},
        {"characterId": "ahmet", "startTime": 3.94, "endTime": 4.12, "text": "Kim?"},
        {"characterId": "muhabir", "startTime": 4.44, "endTime": 4.6, "text": "Siz."},
        {"characterId": "ahmet", "startTime": 6.12, "endTime": 6.88, "text": "Yok."},
        {"characterId": "muhabir", "startTime": 10.0, "endTime": 12.82, "text": "'Hükümet istifa' dediğiniz şeklinde haberleri ben okudum..."}
    ]
}

# 54. Ezel Kerpeten Ali Sanayi
PERFECT_SCENES_5["meme-fbb565592abea053"] = {
    "title": "Ezel - Kerpeten Ali Sanayide Racon Kesiyor",
    "description": "Ezel 1. Sezon: Kerpeten Ali'nin sanayide çırağa ve ustaya fırça atıp racon kestiği unutulmaz sahne.",
    "characters": [
        {"id": "ali", "name": "Kerpeten Ali", "color": "#dc2626", "avatar": "🔧"},
        {"id": "hoca", "name": "Tamirci Hoca", "color": "#3b82f6", "avatar": "👨‍🔧"},
        {"id": "cirak", "name": "Çırak", "color": "#10b981", "avatar": "👦"}
    ],
    "lines": [
        {"characterId": "ali", "startTime": 1.5, "endTime": 2.76, "text": "Kolay gelsin."},
        {"characterId": "hoca", "startTime": 2.88, "endTime": 4.74, "text": "Hoş geldin Ali, eyvallah."},
        {"characterId": "ali", "startTime": 7.6, "endTime": 10.0, "text": "Kardeş sen geç benim arabanın yanından çekil!"},
        {"characterId": "ali", "startTime": 10.82, "endTime": 13.06, "text": "Ulan elin dursa ayağın durmaz be oğlum!"},
        {"characterId": "ali", "startTime": 16.08, "endTime": 18.3, "text": "Ne gülüyorsun lan? Komik bir şey mi var?!"},
        {"characterId": "cirak", "startTime": 18.74, "endTime": 20.2, "text": "Yok ondan değil abi..."},
        {"characterId": "ali", "startTime": 20.92, "endTime": 24.78, "text": "Yenisin herhalde burada. Sen kimsin benim suratıma güleceksin lan?!"},
        {"characterId": "cirak", "startTime": 25.32, "endTime": 26.32, "text": "Yok yanlış anladın abi."},
        {"characterId": "ali", "startTime": 26.4, "endTime": 30.98, "text": "Kaldır şunu lan! Sen git arabaya bak dolan!"},
        {"characterId": "ali", "startTime": 31.4, "endTime": 34.32, "text": "Dağdan geldiniz İstanbul'da kendinize benzettiniz burayı da..."},
        {"characterId": "ali", "startTime": 35.12, "endTime": 37.62, "text": "Hayır hoca senin oğlan yeni galiba."},
        {"characterId": "hoca", "startTime": 39.22, "endTime": 41.4, "text": "Haa... Senin araba canavar yine maşallah."},
        {"characterId": "ali", "startTime": 41.9, "endTime": 46.44, "text": "Oğlum sen beni caddede göreceksin! Bütün kızları peşime takıyorum Allah seni inandırsın!"},
        {"characterId": "hoca", "startTime": 47.34, "endTime": 48.18, "text": "Doğrudur."},
        {"characterId": "ali", "startTime": 55.0, "endTime": 57.74, "text": "Aaa bak fena çizilmiş lan burası!"},
        {"characterId": "hoca", "startTime": 57.74, "endTime": 59.52, "text": "Yapma lan neresi?"},
        {"characterId": "ali", "startTime": 60.12, "endTime": 61.3, "text": "Bak burası!"},
        {"characterId": "hoca", "startTime": 62.38, "endTime": 65.22, "text": "Ne yapıyorsun lan?! Lan ne yapıyorsun?!"},
        {"characterId": "cirak", "startTime": 66.76, "endTime": 67.16, "text": "Ali abi!"},
        {"characterId": "ali", "startTime": 67.7, "endTime": 69.92, "text": "Senin takımları da bir elden geçirelim mi hoca?"},
        {"characterId": "ali", "startTime": 70.5, "endTime": 75.74, "text": "Bir daha bir edepsizlik görürsem sana öyle bir takarım ki buradan pati çeker kalkarsın!"},
        {"characterId": "ali", "startTime": 76.68, "endTime": 79.58, "text": "Anladın mı hoca? Anladıysan salla silecekleri!"},
        {"characterId": "ali", "startTime": 84.06, "endTime": 86.18, "text": "Sen öldün lan! Öldün lan sen!"},
        {"characterId": "ali", "startTime": 86.9, "endTime": 90.56, "text": "Seni burada tanıyorlarmış ya... Beni de tanırlar lan!"},
        {"characterId": "ali", "startTime": 92.14, "endTime": 93.52, "text": "Beni kim biliyor musun?"},
        {"characterId": "ali", "startTime": 98.76, "endTime": 99.72, "text": "KERPETEN ALİ!"},
        {"characterId": "ali", "startTime": 100.54, "endTime": 101.76, "text": "Çaktırma!"}
    ]
}

# 55. Technopat UEFI Windows
PERFECT_SCENES_5["meme-fdd89b3a7015c460"] = {
    "title": "Technopat - Recep Baltaş & Ali Güngör UEFI Windows Parodisi",
    "description": "Technopat YouTube klasiği: Recep Baltaş ile Ali Güngör'ün robotik onaylaşma parodisi.",
    "characters": [
        {"id": "recep", "name": "Recep Baltaş", "color": "#0ea5e9", "avatar": "💻"},
        {"id": "ali", "name": "Ali Güngör", "color": "#10b981", "avatar": "🖥️"}
    ],
    "lines": [
        {"characterId": "recep", "startTime": 0.0, "endTime": 4.14, "text": "Ben Recep, ben Ali. Bugün sizlerle UEFI Windows toplayacağız. Değil mi Ali?"},
        {"characterId": "ali", "startTime": 4.68, "endTime": 7.92, "text": "Evet Recep, bugün gerçekten de UEFI bir Windows toplayacağız."},
        {"characterId": "recep", "startTime": 8.5, "endTime": 11.14, "text": "Bu anakartımız yanında aparatlarıyla geliyor. Değil mi Recep?"},
        {"characterId": "ali", "startTime": 11.72, "endTime": 14.92, "text": "Evet Ali, sahiden de bu anakartımız yanında aparatlarıyla geliyor."},
        {"characterId": "recep", "startTime": 15.14, "endTime": 17.26, "text": "Dilersen şimdi sistem testlerine geçelim Recep."},
        {"characterId": "ali", "startTime": 17.76, "endTime": 18.66, "text": "Geçelim bakalım Ali."},
        {"characterId": "recep", "startTime": 19.02, "endTime": 22.26, "text": "Shadow of War oynuyoruz, burada bir ork var gördüğün gibi. Öyle değil mi Ali?"},
        {"characterId": "ali", "startTime": 22.62, "endTime": 24.74, "text": "Evet Recep, orada gerçekten de bir ork var."},
        {"characterId": "recep", "startTime": 25.04, "endTime": 27.46, "text": "Şimdi vuruyorum onu Ali, vurdum onu değil mi Ali?"},
        {"characterId": "ali", "startTime": 27.9, "endTime": 29.6, "text": "Evet Recep, gerçekten de vurdun onu."},
        {"characterId": "recep", "startTime": 29.6, "endTime": 32.66, "text": "Bu yeni topladığımız sistem hakkında ne düşünüyorsun Ali?"},
        {"characterId": "ali", "startTime": 33.06, "endTime": 34.42, "text": "Evet Recep gerçekten de öyle."},
        {"characterId": "ali", "startTime": 34.78, "endTime": 35.48, "text": "Öyle değil mi Recep?"},
        {"characterId": "recep", "startTime": 35.96, "endTime": 37.28, "text": "Evet Ali, gerçekten de öyle."},
        {"characterId": "recep", "startTime": 37.68, "endTime": 38.28, "text": "Öyle değil mi Ali?"},
        {"characterId": "ali", "startTime": 38.76, "endTime": 40.44, "text": "Evet Recep, gerçekten de öyle."}
    ]
}

# 56. Hüsnü Çoban Rap
PERFECT_SCENES_5["meme-ff6ff8de71ce542b"] = {
    "title": "Grafi2000 - Komiser Hüsnü Çoban 'Light Selami' Rap Şarkısı",
    "description": "Grafi2000 Arka Sokaklar animasyonu: Komiser Hüsnü Çoban'ın efsanevi rap şarkısı.",
    "characters": [
        {"id": "husnu", "name": "Komiser Hüsnü Çoban", "color": "#2563eb", "avatar": "👮"}
    ],
    "lines": [
        {"characterId": "husnu", "startTime": 1.44, "endTime": 2.68, "text": "Durun polis dur!"},
        {"characterId": "husnu", "startTime": 3.74, "endTime": 7.56, "text": "Tamam abi sen durmayabilirsin sen git, siz küçük olanlar yakaladım sizi durun bakayım!"},
        {"characterId": "husnu", "startTime": 7.76, "endTime": 10.38, "text": "Abi seni bir dahaki bölüm yakalarız, hadi selametle bay bay!"},
        {"characterId": "husnu", "startTime": 10.66, "endTime": 14.12, "text": "Arka Sokaklar'dan ben Komiser Hüsnü!"},
        {"characterId": "husnu", "startTime": 14.26, "endTime": 17.8, "text": "Light Selami görse kabarır göğsü!"},
        {"characterId": "husnu", "startTime": 17.94, "endTime": 21.26, "text": "Arka Sokaklar'dan ben Komiser Hüsnü!"},
        {"characterId": "husnu", "startTime": 21.58, "endTime": 24.9, "text": "Light Selami görse kabarır göğsü!"},
        {"characterId": "husnu", "startTime": 25.22, "endTime": 28.64, "text": "Dürüstlük benim içime işlemiş!"},
        {"characterId": "husnu", "startTime": 28.64, "endTime": 30.98, "text": "Polis Hüsnü derler benim namıma!"},
        {"characterId": "husnu", "startTime": 31.6, "endTime": 34.64, "text": "Vay vay vay vay Hüsnü!"},
        {"characterId": "husnu", "startTime": 35.58, "endTime": 39.26, "text": "Millet Hüsnü'den razı! Millet Hüsnü'den razı!"},
        {"characterId": "husnu", "startTime": 39.46, "endTime": 40.64, "text": "Vay anam Hüsnü diyorlar!"},
        {"characterId": "husnu", "startTime": 41.36, "endTime": 42.98, "text": "Suçlular titriyorlar!"},
        {"characterId": "husnu", "startTime": 43.16, "endTime": 46.36, "text": "Karakolun gururu neşesisin diyorlar!"},
        {"characterId": "husnu", "startTime": 46.6, "endTime": 50.08, "text": "Arka Sokaklar benden soruluyor hakikaten!"},
        {"characterId": "husnu", "startTime": 50.38, "endTime": 53.2, "text": "Kanun namına seyret çok seversin gerçekten!"},
        {"characterId": "husnu", "startTime": 54.2, "endTime": 60.34, "text": "Ama aşık hali de var Arka Sokaklar'da..."},
        {"characterId": "husnu", "startTime": 60.74, "endTime": 69.7, "text": "Çok sevindiniz, ailemizin gülüşüyüz, çok teşekkür ederiz!"}
    ]
}

print(f"Bölüm 5 hazırlandı: {len(PERFECT_SCENES_5)} sahne.")
