#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Dublaj Oyunu - Tüm Sahneler İçin Karakter, Rol İzolasyonu ve Cut Ayrıştırma Motoru
56 sahnenin tamamını gerçek karakter isimleri, renkleri, avatarları ve doğru diyalog kesimleri ile donatır.
3 ve 4 kişilik sahneleri tam olarak ayrıştırır; birleşen replikleri böler.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\mirac\Desktop\Code\Dublaj-Oyunu"
SCENES_JSON_PATH = os.path.join(BASE_DIR, "data", "scenes.json")
SCENES_JS_PATH = os.path.join(BASE_DIR, "js", "scenes.js")

with open(SCENES_JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

scenes = data["scenes"]

# 56 sahnenin tam küratörlük haritası
CURATED_DATA = {
    # 01. Oto Pazar
    "meme-artist-ne-arar": {
        "title": "Oto Pazar Röportajı - Artist Ne Arar La Pazarda!",
        "characters": [
            {"id": "muhabir", "name": "Muhabir", "color": "#38bdf8", "avatar": "🎤"},
            {"id": "pazarci", "name": "Pazarcı Dayı", "color": "#4ade80", "avatar": "🚗"}
        ]
    },
    # 02. Çıkar Telefonunu (3 Karakter)
    "meme-cikar-telefonunu": {
        "title": "Sokak Röportajı - Ekonomi ve Telefon Kavgası",
        "characters": [
            {"id": "muhabir", "name": "Muhabir", "color": "#60a5fa", "avatar": "🎤"},
            {"id": "genc", "name": "Genç", "color": "#34d399", "avatar": "🎒"},
            {"id": "dayi", "name": "Dayı", "color": "#f59e0b", "avatar": "👴"}
        ]
    },
    # 03. Kurtlar Vadisi - Pala
    "kv-pala-oluler": {
        "title": "Kurtlar Vadisi - Sadece Ölüler Görür",
        "characters": [
            {"id": "pala", "name": "Pala", "color": "#a855f7", "avatar": "🕶️"},
            {"id": "bedir", "name": "Bedir", "color": "#38bdf8", "avatar": "🔫"}
        ],
        "lines": [
            {"id": 1, "characterId": "bedir", "startTime": 0.0, "endTime": 3.5, "text": "Hüsrev Ağa'nın yanına bir bir buçuk ay evvel birileri gelmiş."},
            {"id": 2, "characterId": "pala", "startTime": 3.52, "endTime": 5.5, "text": "Kimisi diyor ki akrabası."},
            {"id": 3, "characterId": "bedir", "startTime": 5.52, "endTime": 8.0, "text": "Kimisi diyor ki akrabasının adamları."},
            {"id": 4, "characterId": "pala", "startTime": 8.02, "endTime": 11.64, "text": "Ama kime sorduysam dedikleri üç kişiymiş... Sadece ölüler görür."},
            {"id": 5, "characterId": "pala", "type": "music", "startTime": 11.64, "endTime": 15.0, "text": "🎵 [Kurtlar Vadisi Gerilim Müziği — Kayıt Kilitli]"}
        ]
    },
    # 04. Sıfır Bir Mahalle
    "sifir-bir-cio": {
        "title": "Sıfır Bir - Mahalle Hikayesi Anlatımı",
        "characters": [
            {"id": "cio", "name": "Cio Baba", "color": "#f43f5e", "avatar": "⚡"},
            {"id": "savas", "name": "Savaş", "color": "#e11d48", "avatar": "💥"}
        ],
        "lines": [
            {"id": 1, "characterId": "cio", "startTime": 0.0, "endTime": 4.0, "text": "Bak sen herhalde anlatacağım ayakkabı... Neydi ya?"},
            {"id": 2, "characterId": "savas", "startTime": 4.0, "endTime": 7.0, "text": "Sarsılmaz abi ben ya."},
            {"id": 3, "characterId": "cio", "startTime": 7.0, "endTime": 12.0, "text": "O gün bir dostuyla bir alacak verecek meselesi için bir yere gitmişler."},
            {"id": 4, "characterId": "savas", "startTime": 12.0, "endTime": 15.0, "text": "Tamam adamlar aralarına biterdi şimacım."}
        ]
    },
    # 05. Sıfır Bir - Yahya & Seyfi Cezaevi
    "sifir-bir-yahya-cezaevi": {
        "title": "Sıfır Bir - Yahya & Seyfi Cezaevi Sorgusu",
        "characters": [
            {"id": "seyfi", "name": "Seyfi", "color": "#f97316", "avatar": "🧔"},
            {"id": "yahya", "name": "Yahya / Polis", "color": "#3b82f6", "avatar": "👮"}
        ],
        "lines": [
            {"id": 1, "characterId": "seyfi", "startTime": 0.0, "endTime": 7.0, "text": "Benim kimseyle işim olmaz, ben cezaevinden çıktıktan sonra ıslah-ı nefis oldum."},
            {"id": 2, "characterId": "yahya", "startTime": 7.5, "endTime": 17.8, "text": "Çocuk mu kandırıyorsun lan? Cezaevinden çıktın kendine bir oluşum yaptın ve intikam için saldırdın!"},
            {"id": 3, "characterId": "seyfi", "startTime": 18.0, "endTime": 24.8, "text": "Bu senin kendi kafanda kurguladığın bir ifade. Eğer varsa bir delilin bana onla gel!"},
            {"id": 4, "characterId": "seyfi", "type": "music", "startTime": 25.0, "endTime": 40.29, "text": "🎵 [Fon Müziği / Edit — Mikrofon Kilitli]"}
        ]
    },
    # 06. Kolpaçino Saatli Bomba
    "meme-kolpacino-saatli-bomba": {
        "title": "Kolpaçino - Saatli Bomba",
        "characters": [
            {"id": "ganyotcu", "name": "Ganyotçu Abi", "color": "#38bdf8", "avatar": "👔"},
            {"id": "sabri", "name": "Sabri Abi", "color": "#fbbf24", "avatar": "😰"}
        ]
    },
    # 07. Soruya Soruyla Cevap Verme
    "meme-sonuc-ne-soru-cevap": {
        "title": "Röportaj - Soruya Soruyla Cevap Verme!",
        "characters": [
            {"id": "muhabir", "name": "Takım Elbiseli Adam", "color": "#38bdf8", "avatar": "🎤"},
            {"id": "roportajci", "name": "Soru Soran Genç", "color": "#fbbf24", "avatar": "🧢"}
        ]
    },
    # 08. Bear I Love You So So
    "meme-00e48267f85a643e": {
        "title": "Parodi - Bear I Love You So So Much",
        "characters": [
            {"id": "nikki", "name": "Nikki", "color": "#f472b6", "avatar": "👧"},
            {"id": "bear", "name": "Bear", "color": "#fbbf24", "avatar": "🧸"}
        ],
        "char_map": {"karakter_1": "nikki", "karakter_2": "bear"}
    },
    # 09. Bakın Kılın / Çığlık
    "meme-01bda7b30a7b9e4b": {
        "title": "Viral - Çığlık Atan Çocuk",
        "characters": [
            {"id": "cocuk", "name": "Çığlık Atan Çocuk", "color": "#ef4444", "avatar": "😱"}
        ],
        "char_map": {"karakter_1": "cocuk"}
    },
    # 10. Sıfır Bir - Bu Aslan Parçasının Adı Garip
    "meme-021005e91e320d20": {
        "title": "Sıfır Bir - Bu Aslan Parçasının Adı Garip",
        "characters": [
            {"id": "savas", "name": "Savaş Satış", "color": "#e11d48", "avatar": "🦁"},
            {"id": "garip", "name": "Garip", "color": "#f59e0b", "avatar": "👤"},
            {"id": "mahkumlar", "name": "Koğuştakiler", "color": "#38bdf8", "avatar": "👥"}
        ],
        "lines": [
            {"id": 1, "characterId": "savas", "startTime": 0.0, "endTime": 2.0, "text": "Bu aslan parçasının adı Garip."},
            {"id": 2, "characterId": "savas", "startTime": 2.0, "endTime": 4.77, "text": "Artık Garip sizin kardeşinizdir."},
            {"id": 3, "characterId": "mahkumlar", "startTime": 4.77, "endTime": 6.77, "text": "Hoş geldin abi."},
            {"id": 4, "characterId": "garip", "startTime": 6.77, "endTime": 7.83, "text": "Eyvallah."},
            {"id": 5, "characterId": "mahkumlar", "startTime": 7.83, "endTime": 10.28, "text": "Hoş geldin kardeş."},
            {"id": 6, "characterId": "mahkumlar", "startTime": 10.28, "endTime": 11.28, "text": "Hoş geldin kardeş."},
            {"id": 7, "characterId": "savas", "startTime": 11.28, "endTime": 13.73, "text": "Garip voltadır."},
            {"id": 8, "characterId": "savas", "startTime": 13.73, "endTime": 15.53, "text": "Garip..."},
            {"id": 9, "characterId": "garip", "startTime": 15.53, "endTime": 16.53, "text": "Buyur abi."},
            {"id": 10, "characterId": "savas", "startTime": 16.53, "endTime": 18.53, "text": "Oğlum artık bunlar senin abilerindir."},
            {"id": 11, "characterId": "garip", "startTime": 18.53, "endTime": 19.53, "text": "Eyvallah."},
            {"id": 12, "characterId": "savas", "startTime": 19.53, "endTime": 22.53, "text": "Sen ölmeden bunlara bir şey olmayacak."},
            {"id": 13, "characterId": "mahkumlar", "startTime": 22.53, "endTime": 23.53, "text": "Anladın mı?"},
            {"id": 14, "characterId": "garip", "startTime": 23.53, "endTime": 24.53, "text": "Başım gözüm üstüne abi."},
            {"id": 15, "characterId": "savas", "startTime": 24.53, "endTime": 25.53, "text": "He."},
            {"id": 16, "characterId": "savas", "startTime": 25.53, "endTime": 33.42, "text": "Burada da emanetleriniz var. Ver oğlum."},
            {"id": 17, "characterId": "savas", "startTime": 33.42, "endTime": 34.17, "text": "Bize müsaade."}
        ]
    },
    # 11. Sınıf Başkanı Kavgası
    "meme-0c8ee1a80532ffce": {
        "title": "Meme - Sınıf Başkanı Kavgası",
        "characters": [
            {"id": "baskan", "name": "Sınıf Başkanı", "color": "#38bdf8", "avatar": "🤓"},
            {"id": "ogrenci", "name": "İsyankar Öğrenci", "color": "#f87171", "avatar": "😤"}
        ],
        "char_map": {"karakter_1": "baskan", "karakter_2": "ogrenci"}
    },
    # 12. Recep İvedik - Psikologda Turkcell (3 Karakter!)
    "meme-1094542b34c286b1": {
        "title": "Recep İvedik - Psikologda Turkcell Kampanyası",
        "characters": [
            {"id": "recep", "name": "Recep İvedik", "color": "#f59e0b", "avatar": "🦍"},
            {"id": "psikolog", "name": "Psikolog", "color": "#38bdf8", "avatar": "👓"},
            {"id": "pinar", "name": "Pınar (Turkcell)", "color": "#3b82f6", "avatar": "📱"}
        ],
        "lines": [
            {"id": 1, "characterId": "recep", "startTime": 2.38, "endTime": 13.32, "text": "He böyle o kertenkele hayvanla göz göze gelince, bir gözü büyük bir gözü ufak... Bütün piskolojik dengem altüst oldu yani."},
            {"id": 2, "characterId": "recep", "startTime": 13.8, "endTime": 15.18, "text": "Kusura bakmayın pardon, affedersin."},
            {"id": 3, "characterId": "recep", "startTime": 17.48, "endTime": 18.48, "text": "Efendim?"},
            {"id": 4, "characterId": "pinar", "startTime": 18.48, "endTime": 19.3, "text": "Recep Bey?"},
            {"id": 5, "characterId": "recep", "startTime": 19.3, "endTime": 20.0, "text": "Efendim!"},
            {"id": 6, "characterId": "pinar", "startTime": 20.0, "endTime": 21.0, "text": "Ben Turkcell'den Pınar."},
            {"id": 7, "characterId": "recep", "startTime": 21.0, "endTime": 21.8, "text": "Söyle bebişim."},
            {"id": 8, "characterId": "pinar", "startTime": 21.8, "endTime": 23.0, "text": "Biz faturalarınızı inceledik."},
            {"id": 9, "characterId": "recep", "startTime": 23.0, "endTime": 24.0, "text": "Neden?"},
            {"id": 10, "characterId": "pinar", "startTime": 24.0, "endTime": 26.0, "text": "Çok daha ucuza konuşabilmeniz için."},
            {"id": 11, "characterId": "recep", "startTime": 26.0, "endTime": 26.8, "text": "He..."},
            {"id": 12, "characterId": "pinar", "startTime": 26.8, "endTime": 31.0, "text": "Şu an darlık dakika paketlerimizden birini seçerseniz aldığınız dakika kadar hediye kazanacaksınız."},
            {"id": 13, "characterId": "recep", "startTime": 31.0, "endTime": 35.5, "text": "Sağ ol, ben almayayım. Benim için fedakarlık yapmanıza gerek yok, ben memnunum."},
            {"id": 14, "characterId": "pinar", "startTime": 35.5, "endTime": 39.2, "text": "Recep Bey bu şekilde dakikası en fazla sekiz kuruşa gelecek."},
            {"id": 15, "characterId": "recep", "startTime": 39.2, "endTime": 41.0, "text": "Hemen geçelim! Hemen geçelim!"},
            {"id": 16, "characterId": "pinar", "startTime": 41.04, "endTime": 42.0, "text": "Onaylıyor musunuz?"},
            {"id": 17, "characterId": "recep", "startTime": 42.0, "endTime": 43.1, "text": "Onaylıyorum!"},
            {"id": 18, "characterId": "pinar", "startTime": 43.16, "endTime": 44.5, "text": "Çok teşekkür ederim Recep Bey."},
            {"id": 19, "characterId": "pinar", "startTime": 44.58, "endTime": 45.3, "text": "İyi günler."},
            {"id": 20, "characterId": "recep", "startTime": 45.4, "endTime": 46.5, "text": "Sağ ol bebeğim."},
            {"id": 21, "characterId": "psikolog", "startTime": 47.26, "endTime": 48.5, "text": "Ondan sonra... Vaktiniz doldu."},
            {"id": 22, "characterId": "recep", "startTime": 48.8, "endTime": 50.1, "text": "Bir saat oldu mu?"},
            {"id": 23, "characterId": "psikolog", "startTime": 50.1, "endTime": 51.5, "text": "Oldu tabii."},
            {"id": 24, "characterId": "recep", "startTime": 51.5, "endTime": 52.2, "text": "Borcumuz ne kadar?"},
            {"id": 25, "characterId": "psikolog", "startTime": 52.2, "endTime": 53.5, "text": "Yüz elli YTL."},
            {"id": 26, "characterId": "recep", "startTime": 53.74, "endTime": 54.8, "text": "Yuh!"},
            {"id": 27, "characterId": "recep", "startTime": 55.04, "endTime": 59.7, "text": "Demin kadın aradı söyledi, ben seni arasam dakikası sekiz kuruştan saati beş YTL bile etmiyor!"},
            {"id": 28, "characterId": "recep", "startTime": 59.7, "endTime": 61.0, "text": "Hadi git!"},
            {"id": 29, "characterId": "recep", "startTime": 61.04, "endTime": 62.5, "text": "Beni kendimle baş başa bırak."},
            {"id": 30, "characterId": "recep", "startTime": 62.96, "endTime": 64.22, "text": "Tarifenin keyfini çıkartacağım!"}
        ]
    },
    # 13. Dedektif Patrick & Can Pen (3 Karakter)
    "meme-27377eac7c1dbc11": {
        "title": "Dizi Parodisi - Patrick Jane ve Can Pen",
        "characters": [
            {"id": "patrick", "name": "Patrick Jane", "color": "#38bdf8", "avatar": "🕵️"},
            {"id": "canpen", "name": "Can Pen", "color": "#ec4899", "avatar": "👧"},
            {"id": "tercuman", "name": "Polis / Tercüman", "color": "#fbbf24", "avatar": "👮"}
        ],
        "lines": [
            {"id": 1, "characterId": "tercuman", "startTime": 0.82, "endTime": 4.42, "text": "Kızın adı Can Pen, Çinli. Dilimizi bilmiyor."},
            {"id": 2, "characterId": "patrick", "startTime": 4.42, "endTime": 6.04, "text": "Tamam."},
            {"id": 3, "characterId": "patrick", "startTime": 6.04, "endTime": 9.04, "text": "Merhaba, benim adım Patrick."},
            {"id": 4, "characterId": "tercuman", "startTime": 12.91, "endTime": 15.5, "text": "Bir tercümana ihtiyacımız olacak."},
            {"id": 5, "characterId": "canpen", "startTime": 15.5, "endTime": 17.95, "text": "Omzundaki o iğrenç şey de ne?"},
            {"id": 6, "characterId": "patrick", "startTime": 17.95, "endTime": 22.82, "text": "Dilimizi konuşuyor ama biraz utangaç değil mi?"},
            {"id": 7, "characterId": "canpen", "startTime": 22.82, "endTime": 27.95, "text": "Dilinizi konuşmam. Erkekler benimle konuşmaz."},
            {"id": 8, "characterId": "patrick", "startTime": 27.95, "endTime": 29.15, "text": "Böylesi daha iyi."},
            {"id": 9, "characterId": "patrick", "startTime": 29.15, "endTime": 31.05, "text": "Bay Pochetto vurulduğunda ne gördün?"},
            {"id": 10, "characterId": "canpen", "startTime": 31.05, "endTime": 32.05, "text": "Hiçbir şey."},
            {"id": 11, "characterId": "canpen", "startTime": 32.05, "endTime": 36.01, "text": "Ödümü koparan korkunç bir silah sesi duydum ve adam öldü."},
            {"id": 12, "characterId": "canpen", "startTime": 36.01, "endTime": 37.51, "text": "Korkmuştum bu kadar."},
            {"id": 13, "characterId": "patrick", "startTime": 37.51, "endTime": 38.83, "text": "Vuran kişi nasıl biriydi?"},
            {"id": 14, "characterId": "canpen", "startTime": 38.83, "endTime": 39.61, "text": "Görmedim."},
            {"id": 15, "characterId": "patrick", "startTime": 39.61, "endTime": 40.67, "text": "İyi bir yalancısın."},
            {"id": 16, "characterId": "patrick", "startTime": 40.67, "endTime": 42.29, "text": "İyi ama çok iyi değil."},
            {"id": 17, "characterId": "canpen", "startTime": 42.84, "endTime": 44.34, "text": "Onu yakından görmüşüm."}
        ]
    },
    # 14. Akraba Tanıtma (3 Karakter)
    "meme-3e05e9c18616c529": {
        "title": "Meme - Akraba Tanıtma Çilesi",
        "characters": [
            {"id": "anne", "name": "Anne / Teyze", "color": "#ec4899", "avatar": "👵"},
            {"id": "cocuk", "name": "Şaşkın Çocuk", "color": "#38bdf8", "avatar": "🧒"},
            {"id": "baba", "name": "Baba / Abi", "color": "#fbbf24", "avatar": "🧔"}
        ],
        "lines": [
            {"id": 1, "characterId": "anne", "startTime": 0.21, "endTime": 1.39, "text": "Bak kimsin?"},
            {"id": 2, "characterId": "cocuk", "startTime": 1.39, "endTime": 3.32, "text": "Bu küçük torun eee..."},
            {"id": 3, "characterId": "anne", "startTime": 3.32, "endTime": 4.61, "text": "Ne?"},
            {"id": 4, "characterId": "anne", "startTime": 4.61, "endTime": 6.46, "text": "Sen tanıdın mı?"},
            {"id": 5, "characterId": "cocuk", "startTime": 6.46, "endTime": 7.72, "text": "Hatırlamadım."},
            {"id": 6, "characterId": "anne", "startTime": 7.72, "endTime": 11.92, "text": "Bak onun dedesi..."},
            {"id": 7, "characterId": "anne", "startTime": 11.92, "endTime": 14.3, "text": "Onun dedesiyle senin deden kardeş."},
            {"id": 8, "characterId": "anne", "startTime": 14.3, "endTime": 16.54, "text": "Çocuklarının kayınçosu."},
            {"id": 9, "characterId": "anne", "startTime": 16.54, "endTime": 18.42, "text": "Çocuklarının kayınçosu..."},
            {"id": 10, "characterId": "anne", "startTime": 18.42, "endTime": 21.24, "text": "Onun iç güveysi kimmiş hadi söyle bakayım!"},
            {"id": 11, "characterId": "anne", "startTime": 21.24, "endTime": 24.24, "text": "Onun kayınçosu ile senin alakan ne?"},
            {"id": 12, "characterId": "cocuk", "startTime": 24.24, "endTime": 25.4, "text": "Öyle değil."},
            {"id": 13, "characterId": "anne", "startTime": 25.4, "endTime": 26.0, "text": "Bak!"},
            {"id": 14, "characterId": "baba", "startTime": 26.0, "endTime": 27.2, "text": "Anne zorlama çocuğu!"},
            {"id": 15, "characterId": "anne", "startTime": 27.2, "endTime": 28.1, "text": "Karışma sen!"},
            {"id": 16, "characterId": "anne", "startTime": 28.1, "endTime": 30.16, "text": "Öğrensin çocuk kimmiş öyle!"},
            {"id": 17, "characterId": "cocuk", "startTime": 30.16, "endTime": 34.28, "text": "Dedemi alamıyorum..."},
            {"id": 18, "characterId": "baba", "startTime": 34.28, "endTime": 36.28, "text": "Allah Allah tamam oğlum, sakin ol."}
        ]
    },
    # 15. Beni Bloklama (1 Karakter)
    "meme-414a57bd5b2e7e34": {
        "title": "Viral - Beni Bloklama Rage",
        "characters": [
            {"id": "gamer", "name": "Öfkeli Oyuncu", "color": "#ef4444", "avatar": "🤬"}
        ],
        "char_map": {"karakter_1": "gamer"}
    },
    # 16. Kurtlar Vadisi - Şu Teybi Kapatır Mısın
    "meme-43a4d9b0fddc8d10": {
        "title": "Kurtlar Vadisi - Şu Teybi Kapatır Mısın?",
        "characters": [
            {"id": "memati", "name": "Memati Baş", "color": "#1e293b", "avatar": "🕶️"},
            {"id": "sofor", "name": "Şoför", "color": "#f59e0b", "avatar": "🚗"}
        ],
        "lines": [
            {"id": 1, "characterId": "memati", "startTime": 3.12, "endTime": 6.6, "text": "Bir şey konuşuyoruz da, şu teybi kapatır mısın?"},
            {"id": 2, "characterId": "sofor", "startTime": 6.6, "endTime": 12.0, "text": "Kapatıyorum, uyuttun abi."},
            {"id": 3, "characterId": "memati", "type": "music", "startTime": 12.0, "endTime": 35.34, "text": "🎵 [Gerilim Müziği — Kayıt Kilitli]"}
        ]
    },
    # 17. Sizin Ne Vardı (Doktor & Anne & Çocuk) (3 Karakter)
    "meme-48b70fd6e5bc2cd8": {
        "title": "Meme - Doktor Bey Bu Çocuk Isırıyor",
        "characters": [
            {"id": "doktor", "name": "Doktor", "color": "#38bdf8", "avatar": "👨‍⚕️"},
            {"id": "anne", "name": "Dertli Anne", "color": "#ec4899", "avatar": "👩"},
            {"id": "adam", "name": "Isırılan Adam", "color": "#f87171", "avatar": "🤕"}
        ],
        "lines": [
            {"id": 1, "characterId": "doktor", "startTime": 0.0, "endTime": 1.3, "text": "Sizin neyiniz vardı?"},
            {"id": 2, "characterId": "anne", "startTime": 1.34, "endTime": 6.24, "text": "Benim çocuk hasta, oraya buraya saldırıyor, bana saldırıyor, boynumu ısırdı..."},
            {"id": 3, "characterId": "anne", "startTime": 6.28, "endTime": 9.92, "text": "...bu tarafımı ısırdı, kulağımı ısırdı, elimi kaptı!"},
            {"id": 4, "characterId": "doktor", "startTime": 9.96, "endTime": 11.24, "text": "Bunları bu mu yaptı ya?"},
            {"id": 5, "characterId": "anne", "startTime": 11.28, "endTime": 13.72, "text": "Evet, böyle bir saldırganlık hastalığı var."},
            {"id": 6, "characterId": "adam", "startTime": 13.76, "endTime": 16.26, "text": "Oğlum neden annene..."},
            {"id": 7, "characterId": "adam", "startTime": 16.3, "endTime": 17.3, "text": "Lan!"},
            {"id": 8, "characterId": "adam", "startTime": 17.34, "endTime": 23.82, "text": "Oğlum bu adamın asabını bozma, senin kaşını gözünü kırarım ha!"},
            {"id": 9, "characterId": "adam", "startTime": 23.86, "endTime": 31.83, "text": "Sen deliysen ben de deliyim lan!"},
            {"id": 10, "characterId": "adam", "startTime": 31.87, "endTime": 36.83, "text": "Allah'ıma bütün dişlerini dökerim buradan ha!"},
            {"id": 11, "characterId": "adam", "startTime": 36.87, "endTime": 40.78, "text": "Bir şey konuşuyorum dinle lan!"},
            {"id": 12, "characterId": "adam", "startTime": 40.82, "endTime": 41.82, "text": "Lan!"},
            {"id": 13, "characterId": "anne", "startTime": 41.82, "endTime": 43.91, "text": "Yapma oğlum."},
            {"id": 14, "characterId": "adam", "startTime": 43.91, "endTime": 46.91, "text": "Oğlum bak kafanı vururum senin oraya!"},
            {"id": 15, "characterId": "adam", "startTime": 46.91, "endTime": 49.51, "text": "Hah!"},
            {"id": 16, "characterId": "adam", "startTime": 49.51, "endTime": 54.37, "text": "Abla şuna bir zincir mincir takın, bir şey yapın ya. Böyle olmaz."},
            {"id": 17, "characterId": "doktor", "startTime": 54.37, "endTime": 58.56, "text": "Pitbull bile dolaştırmak yasalara aykırı ya. Bunu dolaştırmayın sokakta!"}
        ]
    },
    # 18. Ne Dedin Lan
    "meme-493f3ad55c94c4cf": {
        "title": "Meme - Ne Dedin Lan!",
        "characters": [
            {"id": "abi1", "name": "Öfkeli Abi", "color": "#ef4444", "avatar": "😡"},
            {"id": "abi2", "name": "Karşı Taraf", "color": "#f59e0b", "avatar": "😤"}
        ],
        "char_map": {"karakter_1": "abi1", "karakter_2": "abi2"}
    },
    # 19. Benim Adım Cafer (Alayınıza Gider)
    "meme-4b5781e28db674b5": {
        "title": "Viral - Benim Adım Cafer (Alayınıza Gider)",
        "characters": [
            {"id": "cafer", "name": "Cafer", "color": "#f59e0b", "avatar": "🥊"},
            {"id": "spiker", "name": "Röportajcı Genç", "color": "#38bdf8", "avatar": "🎤"}
        ],
        "lines": [
            {"id": 1, "characterId": "cafer", "startTime": 0.0, "endTime": 2.26, "text": "Benim adım Cafer, boyum bir on."},
            {"id": 2, "characterId": "cafer", "startTime": 2.26, "endTime": 4.0, "text": "Kilom yirmi beş."},
            {"id": 3, "characterId": "cafer", "startTime": 4.0, "endTime": 6.04, "text": "Gözlerimin rengini bilmiyorum."},
            {"id": 4, "characterId": "cafer", "startTime": 6.04, "endTime": 8.38, "text": "Ciguli'yi dinlemeyi severim."},
            {"id": 5, "characterId": "cafer", "startTime": 8.38, "endTime": 10.4, "text": "En sevdiğim yazar..."},
            {"id": 6, "characterId": "cafer", "startTime": 10.4, "endTime": 12.5, "text": "Manapınarından Hacıbeyin Ahmet."},
            {"id": 7, "characterId": "cafer", "startTime": 12.5, "endTime": 14.18, "text": "En sevdiğim futbolcu..."},
            {"id": 8, "characterId": "cafer", "startTime": 14.18, "endTime": 16.44, "text": "Yenimahalle'den Abidin'in Mehmet."},
            {"id": 9, "characterId": "cafer", "startTime": 16.44, "endTime": 18.22, "text": "Samsun iki yüz on altı ve..."},
            {"id": 10, "characterId": "cafer", "startTime": 18.22, "endTime": 20.06, "text": "Parliament'i severim."},
            {"id": 11, "characterId": "cafer", "startTime": 20.06, "endTime": 21.62, "text": "Doğunun bir atasözü vardır:"},
            {"id": 12, "characterId": "cafer", "startTime": 21.62, "endTime": 24.1, "text": "Sağlığınız için, Yeni Rakı için!"},
            {"id": 13, "characterId": "cafer", "startTime": 24.1, "endTime": 28.26, "text": "Kısa boylu ve mavi gözlü kızları severim."},
            {"id": 14, "characterId": "cafer", "startTime": 28.26, "endTime": 31.34, "text": "Tatilimi Namazgâh Dağları'nda geçiriyorum."},
            {"id": 15, "characterId": "cafer", "startTime": 32.06, "endTime": 34.62, "text": "En sevdiğim araba Murat 131."},
            {"id": 16, "characterId": "cafer", "startTime": 35.24, "endTime": 36.86, "text": "Tekno ve kemençeye bayılırım."},
            {"id": 17, "characterId": "cafer", "startTime": 37.44, "endTime": 39.0, "text": "Müdavim mekanım Yenimahalle."},
            {"id": 18, "characterId": "cafer", "startTime": 39.14, "endTime": 41.14, "text": "Lakabım 35'lik Rakı."},
            {"id": 19, "characterId": "cafer", "startTime": 42.0, "endTime": 45.1, "text": "En sevdiğim hocam ilkokulda Kenan hocam."},
            {"id": 20, "characterId": "cafer", "startTime": 45.96, "endTime": 48.98, "text": "En sevdiğim komedyen Yenimahalle'den Michael."},
            {"id": 21, "characterId": "cafer", "startTime": 50.27, "endTime": 51.71, "text": "Dallama gibi işleri severim."},
            {"id": 22, "characterId": "cafer", "startTime": 52.88, "endTime": 55.88, "text": "En ünlü olduğum şey tek sigaramın istenmesi."},
            {"id": 23, "characterId": "cafer", "startTime": 55.88, "endTime": 58.42, "text": "Kafamda hep pis işler."},
            {"id": 24, "characterId": "cafer", "startTime": 59.06, "endTime": 62.82, "text": "Benim adım Cafer! Alayınıza gider! Korkun benden!"},
            {"id": 25, "characterId": "spiker", "startTime": 63.24, "endTime": 64.24, "text": "Senden mi Cafer?"},
            {"id": 26, "characterId": "cafer", "startTime": 64.24, "endTime": 65.24, "text": "Evet benden!"}
        ]
    },
    # 20. Kurtlar Vadisi - Kahve Baskını (3 Karakter!)
    "meme-54c6bba12da44d49": {
        "title": "Kurtlar Vadisi - Çakır'ın Kahve Baskını",
        "characters": [
            {"id": "cemal", "name": "Cemal (Kahveci)", "color": "#f59e0b", "avatar": "☕"},
            {"id": "meral", "name": "Meral (Abla)", "color": "#ec4899", "avatar": "💃"},
            {"id": "halit", "name": "Halit Ağa", "color": "#ef4444", "avatar": "🦁"}
        ],
        "lines": [
            {"id": 1, "characterId": "cemal", "startTime": 0.0, "endTime": 1.2, "text": "Kahveye geldi."},
            {"id": 2, "characterId": "meral", "startTime": 1.69, "endTime": 2.73, "text": "Nasıl kahveye geldi?"},
            {"id": 3, "characterId": "cemal", "startTime": 3.51, "endTime": 5.17, "text": "Geldi, lafını söyledi, gitti."},
            {"id": 4, "characterId": "meral", "startTime": 6.14, "endTime": 7.24, "text": "Nasıl gitti Cemal?"},
            {"id": 5, "characterId": "cemal", "startTime": 8.14, "endTime": 11.04, "text": "Abla, geldi bir tufan, gitti bir boran!"},
            {"id": 6, "characterId": "cemal", "startTime": 12.06, "endTime": 15.08, "text": "Gövde üstünde baş, baş üstünde akıl bırakmadı."},
            {"id": 7, "characterId": "cemal", "startTime": 15.56, "endTime": 16.28, "text": "Esti geçti."},
            {"id": 8, "characterId": "halit", "startTime": 16.64, "endTime": 17.7, "text": "Kaç kişi bastı?"},
            {"id": 9, "characterId": "cemal", "startTime": 17.96, "endTime": 20.46, "text": "Bir o, bir de ondan kara bir oğlan."},
            {"id": 10, "characterId": "halit", "startTime": 21.06, "endTime": 23.04, "text": "İki kişi faturanızı mı kesti Cemal?!"},
            {"id": 11, "characterId": "cemal", "startTime": 23.74, "endTime": 25.72, "text": "Halit Ağa, benim aklım bu işlere ermez."},
            {"id": 12, "characterId": "cemal", "startTime": 26.82, "endTime": 29.5, "text": "Ama bu yaşa geldim, bu kadar hasım gördüm..."},
            {"id": 13, "characterId": "cemal", "startTime": 29.5, "endTime": 30.92, "text": "Böylesini görmedim!"},
            {"id": 14, "characterId": "cemal", "startTime": 30.92, "endTime": 33.72, "text": "Koca kahveyi kestane yaptı, çizdi gitti!"}
        ]
    },
    # 21. Yenilmezler: Zırhını Çıkarırsan Ne Kalır? (3 Karakter!)
    "meme-565c56a384f3e6ca": {
        "title": "Yenilmezler - Zırhını Çıkarırsan Ne Kalır?",
        "characters": [
            {"id": "tony", "name": "Tony Stark (Demir Adam)", "color": "#ef4444", "avatar": "🦾"},
            {"id": "steve", "name": "Steve Rogers (Kaptan Amerika)", "color": "#3b82f6", "avatar": "🛡️"},
            {"id": "banner", "name": "Bruce Banner (Hulk)", "color": "#22c55e", "avatar": "🧪"}
        ],
        "lines": [
            {"id": 1, "characterId": "steve", "startTime": 1.01, "endTime": 3.83, "text": "Kontrolden bahsedip kargaşaya davetiye çıkarıyorsun."},
            {"id": 2, "characterId": "tony", "startTime": 3.85, "endTime": 5.05, "text": "Çalışma tarzı bu değil mi?"},
            {"id": 3, "characterId": "steve", "startTime": 5.53, "endTime": 6.59, "text": "Neyiz biz? Ekip mi?"},
            {"id": 4, "characterId": "tony", "startTime": 6.75, "endTime": 9.55, "text": "Hayır hayır, biz kargaşa yaratan kimyasal bir karışımız."},
            {"id": 5, "characterId": "tony", "startTime": 10.15, "endTime": 12.27, "text": "Biz... Biz saatli bombayız."},
            {"id": 6, "characterId": "steve", "startTime": 12.41, "endTime": 14.05, "text": "Ağır ol bakalım biraz."},
            {"id": 7, "characterId": "tony", "startTime": 14.27, "endTime": 16.19, "text": "Neden biraz deşarj olmasına izin vermiyoruz?"},
            {"id": 8, "characterId": "steve", "startTime": 16.21, "endTime": 18.07, "text": "Nedenini çok iyi biliyorsun. İşine bak sen."},
            {"id": 9, "characterId": "tony", "startTime": 18.63, "endTime": 20.23, "text": "Keşke beni buna zorlasan."},
            {"id": 10, "characterId": "steve", "startTime": 20.75, "endTime": 23.01, "text": "Evet. Zırh giymiş koca adam."},
            {"id": 11, "characterId": "steve", "startTime": 24.69, "endTime": 25.87, "text": "Öt bakalım nesin sen?"},
            {"id": 12, "characterId": "tony", "startTime": 26.37, "endTime": 28.53, "text": "Dahi, milyarder, zampara, hayırsever."},
            {"id": 13, "characterId": "steve", "startTime": 28.91, "endTime": 31.73, "text": "Bunlar olmadan da sana fark atacak kişiler biliyorum."},
            {"id": 14, "characterId": "steve", "startTime": 31.81, "endTime": 33.82, "text": "Ben bu filmi çok gördüm."},
            {"id": 15, "characterId": "steve", "startTime": 34.14, "endTime": 36.26, "text": "Uğruna gerçekten savaştığın tek şey kendinsin."},
            {"id": 16, "characterId": "steve", "startTime": 37.29, "endTime": 42.07, "text": "Fedakarlık edip dikenli telden geçecek ve üstünde sürünmelerine izin verecek biri değilsin."},
            {"id": 17, "characterId": "tony", "startTime": 42.15, "endTime": 43.41, "text": "Teli keserim olur biter."},
            {"id": 18, "characterId": "steve", "startTime": 46.9, "endTime": 47.86, "text": "Hep bir yolunu bulursun."},
            {"id": 19, "characterId": "steve", "startTime": 49.3, "endTime": 52.54, "text": "Tehdit olmayabilirsin ama kahramanmış gibi davranmayı da bırak artık."},
            {"id": 20, "characterId": "tony", "startTime": 52.92, "endTime": 54.34, "text": "Kahraman mı? Senin gibi mi?"},
            {"id": 21, "characterId": "steve", "startTime": 55.3, "endTime": 57.3, "text": "Sen bir laboratuvar deneyisin Rogers."},
            {"id": 22, "characterId": "steve", "startTime": 57.58, "endTime": 60.32, "text": "Seni özel kılan her şey bir şişeden çıktı."},
            {"id": 23, "characterId": "tony", "startTime": 86.18, "endTime": 88.24, "text": "Hadi zırhını giy. Birkaç round kapışalım!"},
            {"id": 24, "characterId": "banner", "startTime": 124.44, "endTime": 126.4, "text": "Sırrımı bilmek ister misiniz Ajan Romanoff?"},
            {"id": 25, "characterId": "banner", "startTime": 126.56, "endTime": 128.08, "text": "Nasıl sakin kaldığımı söyleyeyim mi?"},
            {"id": 26, "characterId": "steve", "startTime": 131.19, "endTime": 135.16, "text": "Doktor Banner, o asayı yavaşça bırakın."}
        ]
    },
    # 22. İsmail Kartal Parodisi (1 Karakter)
    "meme-5a992347adcc5220": {
        "title": "Meme - Ferdi'yi Sol Bek Yapan Benim!",
        "characters": [
            {"id": "hoca", "name": "İsmail Kartal Parodisi", "color": "#fbbf24", "avatar": "📋"}
        ],
        "char_map": {"karakter_1": "hoca"}
    },
    # 23. Bu Ne Çirkinlik
    "meme-5b819baf3f383a04": {
        "title": "Viral - Bu Ne Çirkinlik TikTok Atışması",
        "characters": [
            {"id": "yayinci1", "name": "Batuhan", "color": "#38bdf8", "avatar": "📱"},
            {"id": "yayinci2", "name": "Konuk", "color": "#f472b6", "avatar": "🤡"}
        ],
        "char_map": {"karakter_1": "yayinci1", "karakter_2": "yayinci2"}
    },
    # 24. Gamer Rage
    "meme-638a5e3314df054c": {
        "title": "Viral - Duvara Vuran Komşu ve Gamer Rage",
        "characters": [
            {"id": "komsu", "name": "Alt Komşu", "color": "#94a3b8", "avatar": "🔨"},
            {"id": "gamer", "name": "Çıldıran Oyuncu", "color": "#ef4444", "avatar": "🎧"}
        ],
        "char_map": {"karakter_1": "komsu", "karakter_2": "gamer"}
    },
    # 25. Sıfır Bir - Bu Yol Çıkmıyor Abi (3 Karakter)
    "meme-6d951d7f55599703": {
        "title": "Sıfır Bir - Bu Yol Çıkmıyor Abi",
        "characters": [
            {"id": "cio", "name": "Cio Baba", "color": "#f43f5e", "avatar": "⚡"},
            {"id": "savas", "name": "Savaş", "color": "#e11d48", "avatar": "💥"},
            {"id": "genc", "name": "Mahallenin Genci", "color": "#38bdf8", "avatar": "🚗"}
        ],
        "lines": [
            {"id": 1, "characterId": "cio", "startTime": 0.0, "endTime": 2.0, "text": "Sıkıntı yok. Hiçbir şekilde sıkıntı yok."},
            {"id": 2, "characterId": "cio", "startTime": 2.0, "endTime": 3.0, "text": "Gel hele."},
            {"id": 3, "characterId": "savas", "startTime": 7.14, "endTime": 9.14, "text": "Yalnız iki üç tane genç alın."},
            {"id": 4, "characterId": "savas", "startTime": 9.14, "endTime": 11.14, "text": "Bir dostumuzu karşılamaya gideceğiz."},
            {"id": 5, "characterId": "savas", "startTime": 11.14, "endTime": 17.33, "text": "Bak hele lan."},
            {"id": 6, "characterId": "cio", "startTime": 17.33, "endTime": 19.33, "text": "Bu da kendini iyice Polat Alemdar zannetti ha."},
            {"id": 7, "characterId": "cio", "startTime": 19.33, "endTime": 21.33, "text": "En son bozacağım."},
            {"id": 8, "characterId": "savas", "startTime": 21.33, "endTime": 22.33, "text": "Bırak oğlum ya."},
            {"id": 9, "characterId": "savas", "startTime": 22.33, "endTime": 25.33, "text": "Abigil yolladıysa mahalleye bir bildikleri vardır."},
            {"id": 10, "characterId": "savas", "startTime": 25.33, "endTime": 26.33, "text": "Kafana takma böyle şeyleri."},
            {"id": 11, "characterId": "cio", "startTime": 26.33, "endTime": 28.33, "text": "Tamam da kardeş bize yapmasın."},
            {"id": 12, "characterId": "cio", "startTime": 28.33, "endTime": 30.33, "text": "O yokken biz vardık."},
            {"id": 13, "characterId": "savas", "startTime": 30.33, "endTime": 39.44, "text": "Ya boş verelim bu kadar işin içinde bir de bununla mı uğraşacağız ya?"},
            {"id": 14, "characterId": "cio", "startTime": 39.44, "endTime": 40.44, "text": "Lan bu yol çıkmıyor mu?"},
            {"id": 15, "characterId": "genc", "startTime": 40.44, "endTime": 41.44, "text": "Bu yol çıkmıyor abi."},
            {"id": 16, "characterId": "cio", "startTime": 41.44, "endTime": 43.44, "text": "Niye söylemiyorsunuz oğlum?!"},
            {"id": 17, "characterId": "genc", "startTime": 43.44, "endTime": 44.44, "text": "Sormadın ki abi..."},
            {"id": 18, "characterId": "savas", "startTime": 44.44, "endTime": 50.31, "text": "Mahalleye de rezil olduk."},
            {"id": 19, "characterId": "cio", "startTime": 50.31, "endTime": 51.31, "text": "Bırakalım ya."}
        ]
    },
    # 26. Kolpaçino: Orman ve Çoluk Çocuk (3 Karakter!)
    "meme-701778ed8f454ba0": {
        "title": "Kolpaçino - Orman ve Çoluk Çocuk",
        "characters": [
            {"id": "sabri", "name": "Sabri Abi", "color": "#ef4444", "avatar": "🥊"},
            {"id": "tayfun", "name": "Tayfun", "color": "#38bdf8", "avatar": "🕶️"},
            {"id": "ozgur", "name": "Özgür", "color": "#fbbf24", "avatar": "😰"}
        ],
        "lines": [
            {"id": 1, "characterId": "tayfun", "startTime": 0.21, "endTime": 1.47, "text": "Bu ne iş ya?"},
            {"id": 2, "characterId": "sabri", "startTime": 1.87, "endTime": 3.27, "text": "Birine telefon gelir dur..."},
            {"id": 3, "characterId": "sabri", "startTime": 3.47, "endTime": 5.49, "text": "Biri kolonyayla kendini yakmak ister dur..."},
            {"id": 4, "characterId": "sabri", "startTime": 5.65, "endTime": 6.75, "text": "Biri ormana dalar..."},
            {"id": 5, "characterId": "sabri", "startTime": 7.01, "endTime": 8.79, "text": "Çoluk çocuğun elinde oyuncak olduk Tayfun!"},
            {"id": 6, "characterId": "tayfun", "startTime": 9.59, "endTime": 11.15, "text": "Abi ormandan sonrası deniz."},
            {"id": 7, "characterId": "tayfun", "startTime": 11.29, "endTime": 12.51, "text": "İstersen atıp kurtulalım."},
            {"id": 8, "characterId": "sabri", "startTime": 12.73, "endTime": 13.61, "text": "Ne yaparsan yap lan!"},
            {"id": 9, "characterId": "ozgur", "startTime": 14.03, "endTime": 15.03, "text": "Sabri Bey..."},
            {"id": 10, "characterId": "ozgur", "startTime": 15.25, "endTime": 17.53, "text": "Kız arkadaşım aradı durmak zorundaydım yani."},
            {"id": 11, "characterId": "ozgur", "startTime": 17.65, "endTime": 18.37, "text": "Kusura bakmayın."},
            {"id": 12, "characterId": "ozgur", "startTime": 19.01, "endTime": 22.65, "text": "Ayriyeten içinde bulunduğumuz durumdan da ben pek memnun değilim yani."},
            {"id": 13, "characterId": "sabri", "startTime": 22.83, "endTime": 23.85, "text": "Sen ne diyorsun ya?!"},
            {"id": 14, "characterId": "ozgur", "startTime": 23.85, "endTime": 29.61, "text": "Yani diyorum ki gece gece iki ceset, altı adama ait bir yerdeyiz yani..."},
            {"id": 15, "characterId": "sabri", "startTime": 29.61, "endTime": 33.0, "text": "Ne gülüyorsun lan?!"},
            {"id": 16, "characterId": "ozgur", "startTime": 33.0, "endTime": 34.5, "text": "Gülmüyorum abi."},
            {"id": 17, "characterId": "sabri", "startTime": 34.5, "endTime": 36.87, "text": "Yavrum sen kaç yaşındasın?"},
            {"id": 18, "characterId": "ozgur", "startTime": 36.87, "endTime": 39.0, "text": "34 yaşındayım, ne oldu ki?"},
            {"id": 19, "characterId": "sabri", "startTime": 39.0, "endTime": 45.5, "text": "Bak kardeşim sen güzel bir kardeşe benziyorsun. Benim yaşım 50. Bak donuma..."},
            {"id": 20, "characterId": "sabri", "startTime": 45.5, "endTime": 54.81, "text": "İyi bak! Donum görünüyor! Donum olmasa bizzat popomun kendisi görünecek!"}
        ]
    },
    # 27. Kolpaçino: Cezaevi Çıkışı (3 Karakter)
    "meme-71af9284d4ab8edf": {
        "title": "Kolpaçino - Cezaevi Çıkışı ve Manitalar",
        "characters": [
            {"id": "sabri", "name": "Sabri Abi", "color": "#ef4444", "avatar": "😎"},
            {"id": "ozgur", "name": "Özgür", "color": "#fbbf24", "avatar": "🤩"},
            {"id": "sahin", "name": "Şahin", "color": "#38bdf8", "avatar": "🚗"}
        ],
        "lines": [
            {"id": 1, "characterId": "ozgur", "startTime": 0.0, "endTime": 2.0, "text": "Oğlum nasıl özlemişim lan dışarıyı?"},
            {"id": 2, "characterId": "sahin", "startTime": 2.0, "endTime": 4.0, "text": "Bakarsın bugün kavuşuruz Özgür!"},
            {"id": 3, "characterId": "sabri", "startTime": 4.0, "endTime": 6.13, "text": "Özgür manitalara bak lan!"},
            {"id": 4, "characterId": "sabri", "startTime": 6.13, "endTime": 8.13, "text": "Oğlum memlekete yaz gelmiş lan!"},
            {"id": 5, "characterId": "ozgur", "startTime": 8.13, "endTime": 10.13, "text": "Başına vurdu valla abi buyur."},
            {"id": 6, "characterId": "ozgur", "startTime": 10.13, "endTime": 12.13, "text": "Sana özgürlükten bahsediyorum sen manita diyorsun."},
            {"id": 7, "characterId": "sabri", "startTime": 12.13, "endTime": 15.13, "text": "Oğlum neyin kafasını yaşıyorsun baksana kızlara!"},
            {"id": 8, "characterId": "sahin", "startTime": 15.13, "endTime": 18.7, "text": "Harbi yandık abi ya."},
            {"id": 9, "characterId": "sabri", "startTime": 18.7, "endTime": 20.7, "text": "Harbi klimayı açın yandık be!"},
            {"id": 10, "characterId": "ozgur", "startTime": 20.7, "endTime": 24.56, "text": "Kimin yandığı belli oluyor abi."}
        ]
    },
    # 28. Neden Terörist Oldunuz (Flash TV)
    "meme-74ca08745cf708a8": {
        "title": "Flash TV - Neden Dağa Çıktınız Röportajı",
        "characters": [
            {"id": "muhabir", "name": "Muhabir", "color": "#38bdf8", "avatar": "🎤"},
            {"id": "koylu", "name": "Köylü Dayı", "color": "#4ade80", "avatar": "👴"}
        ],
        "char_map": {"karakter_1": "muhabir", "karakter_2": "koylu"}
    },
    # 29. Beyaz Futbol - Artık Götünden Maç Uyduruyorsun (3 Karakter!)
    "meme-7e1105e63de53c5a": {
        "title": "Beyaz Futbol - Maç Uydurma Kavgası",
        "characters": [
            {"id": "ahmet", "name": "Ahmet Çakar", "color": "#ef4444", "avatar": "👴"},
            {"id": "rasim", "name": "Rasim Ozan Kütahyalı", "color": "#fbbf24", "avatar": "🤪"},
            {"id": "ertem", "name": "Ertem Şener", "color": "#38bdf8", "avatar": "🎙️"}
        ],
        "lines": [
            {"id": 1, "characterId": "ahmet", "startTime": 0.78, "endTime": 3.84, "text": "Ya Ertem artık kafandan maç uyduruyorsun!"},
            {"id": 2, "characterId": "ahmet", "startTime": 3.96, "endTime": 5.2, "text": "GS 2-2 yaptı diyorsun."},
            {"id": 3, "characterId": "ahmet", "startTime": 5.34, "endTime": 7.32, "text": "Galatasaray maç bile oynamıyor ya şu an!"},
            {"id": 4, "characterId": "rasim", "startTime": 8.02, "endTime": 12.12, "text": "Tık skor uydurdun, uydurdun, uydurdun!"},
            {"id": 5, "characterId": "rasim", "startTime": 12.22, "endTime": 18.01, "text": "Artık yemin ediyorum beni çileden çıkarmak için maç uyduruyorsun ya!"},
            {"id": 6, "characterId": "ertem", "startTime": 18.73, "endTime": 23.03, "text": "Hocam inan bana Galatasaray 2-2 yapmış şu anda!"},
            {"id": 7, "characterId": "rasim", "startTime": 25.16, "endTime": 27.2, "text": "Bir de basketmiş Allah kahretmesin!"},
            {"id": 8, "characterId": "ahmet", "startTime": 30.33, "endTime": 31.55, "text": "Bir de basketmiş..."},
            {"id": 9, "characterId": "ahmet", "startTime": 32.05, "endTime": 33.69, "text": "Özrüm kabahatimden büyük ya."},
            {"id": 10, "characterId": "rasim", "startTime": 37.66, "endTime": 38.84, "text": "Basket maçıymış!"},
            {"id": 11, "characterId": "rasim", "startTime": 38.84, "endTime": 40.84, "text": "Yüzümü yolacağım tırnaklarımla ya!"}
        ]
    },
    # 30. Han Kanal & Piggy
    "meme-82905766b3d259c2": {
        "title": "Meme - Han Kanal ve Piggy Röportajı",
        "characters": [
            {"id": "han", "name": "Han Kanal", "color": "#38bdf8", "avatar": "🎮"},
            {"id": "piggy", "name": "Piggy (Domuzcuk)", "color": "#f472b6", "avatar": "🐷"}
        ],
        "char_map": {"karakter_1": "han", "karakter_2": "piggy"}
    },
    # 31. Keloğlan: Huysuz ve Uzun İksir Peşinde (3 Karakter!)
    "meme-82adcb0c41c171e1": {
        "title": "Keloğlan - Huysuz ve Uzun İksir Peşinde",
        "characters": [
            {"id": "huysuz", "name": "Huysuz", "color": "#f59e0b", "avatar": "🧌"},
            {"id": "uzun", "name": "Uzun", "color": "#34d399", "avatar": "🦒"},
            {"id": "cadi", "name": "Cadı / Keloğlan", "color": "#a855f7", "avatar": "🧙"}
        ],
        "lines": [
            {"id": 1, "characterId": "huysuz", "startTime": 0.42, "endTime": 4.42, "text": "Geliyorlar! Herkes konuştuğumuz gibi yerlerine geçsin ve kıpırdamasın."},
            {"id": 2, "characterId": "uzun", "startTime": 8.78, "endTime": 12.9, "text": "İyi de sen böyle bir suratla karşımda durursan ben gülerim."},
            {"id": 3, "characterId": "huysuz", "startTime": 13.24, "endTime": 15.2, "text": "He de bir gül de vezir de bizi mahvetsin!"},
            {"id": 4, "characterId": "uzun", "startTime": 19.75, "endTime": 22.21, "text": "Huysuz, hız tozunun etkisi geçmemiş miydi?"},
            {"id": 5, "characterId": "huysuz", "startTime": 22.45, "endTime": 23.37, "text": "Dur bakalım Uzun."},
            {"id": 6, "characterId": "cadi", "startTime": 25.58, "endTime": 29.76, "text": "Sizi akıllılar sizi! Biz yokken çaldıklarımızı çalacaktınız he?"},
            {"id": 7, "characterId": "uzun", "startTime": 30.28, "endTime": 37.04, "text": "Bu Huysuz bir şey icat etti."},
            {"id": 8, "characterId": "huysuz", "startTime": 37.91, "endTime": 38.83, "text": "Tozun neydi o?"},
            {"id": 9, "characterId": "cadi", "startTime": 42.58, "endTime": 46.96, "text": "Sizi uyanıklar!"}
        ]
    },
    # 32. Gülme Krizi (1 Karakter)
    "meme-840ad8a37e2bb450": {
        "title": "Viral - Gülme Krizine Giren Spiker",
        "characters": [
            {"id": "spiker", "name": "Gülme Krizindeki Spiker", "color": "#fbbf24", "avatar": "😂"}
        ],
        "char_map": {"karakter_1": "spiker"}
    },
    # 33. Laf Yarışı
    "meme-88139b3306f24519": {
        "title": "Meme - Cem Yılmaz'ın Yandan Yemişi",
        "characters": [
            {"id": "dayi1", "name": "Laf Sokucu Dayı", "color": "#f87171", "avatar": "👴"},
            {"id": "dayi2", "name": "Cem Yılmaz Çakması", "color": "#38bdf8", "avatar": "🤡"}
        ],
        "char_map": {"karakter_1": "dayi1", "karakter_2": "dayi2"}
    },
    # 34. Otel Fotoğrafçısı
    "meme-885102943a735982": {
        "title": "Parodi - Israrcı Otel Fotoğrafçısı",
        "characters": [
            {"id": "fotografci", "name": "Otel Fotoğrafçısı", "color": "#38bdf8", "avatar": "📸"},
            {"id": "turist", "name": "Tatilci Dayı", "color": "#fbbf24", "avatar": "🏖️"}
        ],
        "lines": [
            {"id": 1, "characterId": "fotografci", "startTime": 11.38, "endTime": 14.18, "text": "Beyefendi stop stop stop! Bir tane fotoğrafınızı çekeceğim."},
            {"id": 2, "characterId": "turist", "startTime": 14.18, "endTime": 16.7, "text": "İstemiyorum ben fotoğraf falan arkadaşım lütfen."},
            {"id": 3, "characterId": "fotografci", "startTime": 16.7, "endTime": 19.42, "text": "Beyefendi sadece bir tane hatıra için fotoğraf çekeceğiz."},
            {"id": 4, "characterId": "turist", "startTime": 19.42, "endTime": 21.98, "text": "Ben fotoğraf falan istemiyorum arkadaşım lütfen beni rahat bırak."},
            {"id": 5, "characterId": "fotografci", "startTime": 21.98, "endTime": 23.5, "text": "Çok güzel olacak inanın bana."},
            {"id": 6, "characterId": "fotografci", "startTime": 23.5, "endTime": 24.18, "text": "Şöyle hafif..."},
            {"id": 7, "characterId": "turist", "startTime": 39.07, "endTime": 41.43, "text": "Oğlum istemiyorum diyorum ben fotoğraf falan! Lütfen bırak beni."},
            {"id": 8, "characterId": "fotografci", "startTime": 41.43, "endTime": 44.27, "text": "Beyefendi çekinmenize gerek yok, ben otelin fotoğrafçısıyım lütfen."},
            {"id": 9, "characterId": "fotografci", "startTime": 44.27, "endTime": 47.14, "text": "Sadece bir tane güzel bir manzara fotoğrafı."},
            {"id": 10, "characterId": "turist", "startTime": 47.14, "endTime": 48.22, "text": "Evet?"},
            {"id": 11, "characterId": "turist", "startTime": 48.22, "endTime": 49.22, "text": "Havuz çıkıyor mu?"},
            {"id": 12, "characterId": "fotografci", "startTime": 49.22, "endTime": 51.22, "text": "Evet, çok güzel bir manzara fotoğrafı olacak."},
            {"id": 13, "characterId": "turist", "startTime": 51.72, "endTime": 52.92, "text": "Dur o zaman, poz vereceğim."},
            {"id": 14, "characterId": "fotografci", "startTime": 54.1, "endTime": 55.1, "text": "Evet, çok iyi."},
            {"id": 15, "characterId": "turist", "startTime": 55.3, "endTime": 56.8, "text": "Üçten geriye say ama lütfen."},
            {"id": 16, "characterId": "fotografci", "startTime": 57.0, "endTime": 58.0, "text": "Tamam."},
            {"id": 17, "characterId": "fotografci", "startTime": 58.0, "endTime": 59.6, "text": "Üç, iki, bir..."},
            {"id": 18, "characterId": "turist", "startTime": 61.96, "endTime": 63.16, "text": "Ama efendim bu olmadı ki!"},
            {"id": 19, "characterId": "fotografci", "startTime": 63.46, "endTime": 64.16, "text": "Ne lan?!"},
            {"id": 20, "characterId": "turist", "startTime": 64.66, "endTime": 65.66, "text": "Ayy!"}
        ]
    },
    # 35. TRT Dizi Betimlemesi
    "meme-8c3b341acc6bda05": {
        "title": "TRT - Sesli Betimleme Parodisi",
        "characters": [
            {"id": "spiker", "name": "Betimleme Spikeri", "color": "#38bdf8", "avatar": "🎙️"}
        ],
        "char_map": {"karakter_1": "spiker"}
    },
    # 36. Yemek Hazır
    "meme-909c5d25fce176ea": {
        "title": "Meme - Yemek Hazır / Ben Yemeyeceğim",
        "characters": [
            {"id": "anne", "name": "Anne", "color": "#ec4899", "avatar": "🍲"},
            {"id": "ogul", "name": "İsyankar Çocuk", "color": "#38bdf8", "avatar": "👦"}
        ],
        "lines": [
            {"id": 1, "characterId": "anne", "startTime": 0.4, "endTime": 1.54, "text": "Yemek hazır!"},
            {"id": 2, "characterId": "ogul", "startTime": 2.06, "endTime": 2.8, "text": "Ben yemeyeceğim."},
            {"id": 3, "characterId": "anne", "startTime": 5.46, "endTime": 6.32, "text": "Aç değil misin?"},
            {"id": 4, "characterId": "ogul", "startTime": 6.82, "endTime": 7.82, "text": "Buyurun..."}
        ]
    },
    # 37. Sıfır Bir - Lan Bilo! (3 Karakter!)
    "meme-915b36b91433c2f4": {
        "title": "Sıfır Bir - Lan Bilo Neredeyki Araba?",
        "characters": [
            {"id": "cio", "name": "Cio Baba", "color": "#f43f5e", "avatar": "⚡"},
            {"id": "berto", "name": "Berto", "color": "#fbbf24", "avatar": "🧢"},
            {"id": "bilo", "name": "Bilo", "color": "#38bdf8", "avatar": "🚗"}
        ],
        "lines": [
            {"id": 1, "characterId": "cio", "startTime": 0.0, "endTime": 0.6, "text": "...olur zaten."},
            {"id": 2, "characterId": "cio", "startTime": 1.34, "endTime": 2.1, "text": "Lan Bilo!"},
            {"id": 3, "characterId": "cio", "startTime": 3.16, "endTime": 4.6, "text": "Şu araba nasıl kararmış gel hele."},
            {"id": 4, "characterId": "bilo", "startTime": 5.06, "endTime": 6.1, "text": "Neredeyki abi araba?"},
            {"id": 5, "characterId": "cio", "startTime": 6.7, "endTime": 7.48, "text": "Anamın damında!"},
            {"id": 6, "characterId": "berto", "startTime": 9.38, "endTime": 10.58, "text": "Nerede oğlum yolun başında!"},
            {"id": 7, "characterId": "berto", "startTime": 11.96, "endTime": 14.06, "text": "Sen hayırdır abi gençlerle üst perdeden konuşuyorsun?"},
            {"id": 8, "characterId": "cio", "startTime": 15.46, "endTime": 16.76, "text": "Ne üst perdeden konuşacağım Ciho?"},
            {"id": 9, "characterId": "berto", "startTime": 17.3, "endTime": 18.92, "text": "Görmüyor musun? Soru sormak için soruyor."},
            {"id": 10, "characterId": "cio", "startTime": 19.16, "endTime": 21.78, "text": "Olsun abi. Herkese düzgün konuşacaksın bundan sonra."},
            {"id": 11, "characterId": "cio", "startTime": 22.1, "endTime": 22.84, "text": "Hepsi benim kardeşim."},
            {"id": 12, "characterId": "berto", "startTime": 23.56, "endTime": 24.24, "text": "Hayırdır Ciho?"},
            {"id": 13, "characterId": "cio", "startTime": 24.7, "endTime": 25.9, "text": "Seni ne rahatsız etti ki?"},
            {"id": 14, "characterId": "berto", "startTime": 26.4, "endTime": 27.42, "text": "Rahatsız oldum abi ben."},
            {"id": 15, "characterId": "berto", "startTime": 27.96, "endTime": 29.7, "text": "İçerideyken de tersini yapıyordun şu millete."},
            {"id": 16, "characterId": "cio", "startTime": 29.7, "endTime": 31.06, "text": "Kime ne demişim ben?"},
            {"id": 17, "characterId": "berto", "startTime": 31.06, "endTime": 32.72, "text": "Karnından konuşma kardeş."},
            {"id": 18, "characterId": "berto", "startTime": 33.08, "endTime": 34.34, "text": "Herkes burada, yüzleşek."},
            {"id": 19, "characterId": "cio", "startTime": 34.44, "endTime": 35.66, "text": "Ne karnından konuşacağım ya?"},
            {"id": 20, "characterId": "berto", "startTime": 36.2, "endTime": 37.78, "text": "Kimle seni yüzleştireyim?"},
            {"id": 21, "characterId": "cio", "startTime": 37.88, "endTime": 39.56, "text": "Sen kimsin lan? Hayırdır oğlum?!"},
            {"id": 22, "characterId": "berto", "startTime": 39.8, "endTime": 41.3, "text": "Ne derdin varsa açık açık konuş!"}
        ]
    },
    # 38. Sıfır Bir - Cihat, Cabbar Halletsin (3 Karakter!)
    "meme-93cba130dd88ebfa": {
        "title": "Sıfır Bir - Cihat & Cabbar Halletsin",
        "characters": [
            {"id": "cihat", "name": "Cihat", "color": "#f97316", "avatar": "🔫"},
            {"id": "savas", "name": "Savaş", "color": "#e11d48", "avatar": "💥"},
            {"id": "cabbar", "name": "Cabbar", "color": "#38bdf8", "avatar": "💣"}
        ],
        "lines": [
            {"id": 1, "characterId": "cihat", "startTime": 0.0, "endTime": 4.15, "text": "Abi sen dur, bu kadar işin içinde bir de Özcan'la uğraşma."},
            {"id": 2, "characterId": "cabbar", "startTime": 6.23, "endTime": 7.63, "text": "Cabbar'lar halleder."},
            {"id": 3, "characterId": "cihat", "startTime": 8.94, "endTime": 10.02, "text": "Hallederik abi."},
            {"id": 4, "characterId": "savas", "startTime": 10.94, "endTime": 16.72, "text": "Peki sen öyle diyorsan Cihat, Cabbar halletsin."},
            {"id": 5, "characterId": "savas", "startTime": 17.13, "endTime": 19.25, "text": "Bir şeye ihtiyacınız olursa söyleyin kardeş."},
            {"id": 6, "characterId": "cabbar", "startTime": 19.72, "endTime": 23.9, "text": "Tamam abi, Özcan elimizde. Siz kafanızı yormayın."},
            {"id": 7, "characterId": "cihat", "startTime": 24.1, "endTime": 36.5, "text": "Cabbar halledecekmiş... Kendi başını halleder anca."},
            {"id": 8, "characterId": "cihat", "startTime": 37.52, "endTime": 41.58, "text": "Ayık olun siz de oğlum, biz hallederiz falan desenize!"},
            {"id": 9, "characterId": "cabbar", "startTime": 41.86, "endTime": 44.22, "text": "İlla lafa ben mi gireceğim amına koyayım ya?"}
        ]
    },
    # 39. JoJo: Za Warudo (3 Karakter!)
    "meme-9db0b71d01ec8690": {
        "title": "JoJo - Za Warudo! Zamanı Durdurma",
        "characters": [
            {"id": "dio", "name": "Dio Brando", "color": "#fbbf24", "avatar": "🧛"},
            {"id": "jotaro", "name": "Jotaro Kujo", "color": "#38bdf8", "avatar": "⭐"},
            {"id": "anlatici", "name": "Anlatıcı", "color": "#a855f7", "avatar": "📖"}
        ],
        "lines": [
            {"id": 1, "characterId": "dio", "startTime": 0.0, "endTime": 3.64, "text": "DURDURAK BİLMEYEN SON SALDIRIMI YAPACAĞIM!"},
            {"id": 2, "characterId": "dio", "startTime": 3.64, "endTime": 6.8, "text": "VE SON BİR KEZ ZAMANI DURDURACAĞIM!"},
            {"id": 3, "characterId": "dio", "startTime": 6.8, "endTime": 12.27, "text": "ZAMANI DURDURDUĞUM 9 SANİYE İÇİNDE BUNU BİTİRECEĞİM!"},
            {"id": 4, "characterId": "dio", "startTime": 12.27, "endTime": 14.19, "text": "ZA WARUDO! ZAMAN DURSUN!"},
            {"id": 5, "characterId": "dio", "startTime": 23.12, "endTime": 28.73, "text": "Bir saniye geçti..."},
            {"id": 6, "characterId": "dio", "startTime": 28.73, "endTime": 31.31, "text": "İki saniye geçti..."},
            {"id": 7, "characterId": "dio", "startTime": 31.31, "endTime": 33.41, "text": "Üç saniye geçti..."},
            {"id": 8, "characterId": "anlatici", "startTime": 33.41, "endTime": 37.91, "text": "Bir nedenden dolayı zaman durmuşken Dio ortalıktan kayboldu."},
            {"id": 9, "characterId": "dio", "startTime": 37.91, "endTime": 40.89, "text": "Dört saniye geçti..."},
            {"id": 10, "characterId": "anlatici", "startTime": 40.89, "endTime": 43.93, "text": "Fakat Jotaro kafa yormayı bıraktı."},
            {"id": 11, "characterId": "anlatici", "startTime": 43.93, "endTime": 46.65, "text": "Dio'nun nasıl bir planı olsa da..."},
            {"id": 12, "characterId": "anlatici", "startTime": 46.65, "endTime": 50.53, "text": "Zaman durmuşken sadece 2 saniye hareket edebilen Jotaro'ya..."},
            {"id": 13, "characterId": "anlatici", "startTime": 50.53, "endTime": 53.09, "text": "Nasıl saldırsa da..."},
            {"id": 14, "characterId": "anlatici", "startTime": 53.09, "endTime": 58.51, "text": "Tek yapması gereken o 2 saniyede Star Platinum'un yumruklarını indirmek!"},
            {"id": 15, "characterId": "dio", "startTime": 58.51, "endTime": 60.59, "text": "Beş saniye geçti..."},
            {"id": 16, "characterId": "jotaro", "startTime": 60.59, "endTime": 63.17, "text": "Bildiğim tek şey var Dio..."},
            {"id": 17, "characterId": "jotaro", "startTime": 63.17, "endTime": 68.6, "text": "Bir daha görürsem ağzını burnunu kıracağım!"},
            {"id": 18, "characterId": "dio", "startTime": 68.6, "endTime": 72.56, "text": "Altı saniye geçti..."},
            {"id": 19, "characterId": "jotaro", "startTime": 72.56, "endTime": 73.26, "text": "Yolla hadi!"},
            {"id": 20, "characterId": "dio", "startTime": 73.26, "endTime": 78.28, "text": "Yedi saniye geçti..."},
            {"id": 21, "characterId": "dio", "startTime": 78.28, "endTime": 85.0, "text": "Dokuz saniye geçti! ORA ORA ORA!"}
        ]
    },
    # 40. Arabayı Yeni Alan Adam (1 Karakter)
    "meme-a9bd70989fc91692": {
        "title": "Viral - Arabayı Yeni Alan Adamın Panik Anı",
        "characters": [
            {"id": "adam", "name": "Yeni Araba Alan Adam", "color": "#f59e0b", "avatar": "🚗"}
        ],
        "char_map": {"karakter_1": "adam"}
    },
    # 41. Kurtlar Vadisi - Al Mahmut Bunlar Misafirin (3 Karakter!)
    "meme-ac037f6b8ed128c4": {
        "title": "Kurtlar Vadisi - Pala & Bedir & Mahmut",
        "characters": [
            {"id": "pala", "name": "Pala", "color": "#1e293b", "avatar": "🕶️"},
            {"id": "bedir", "name": "Bedir", "color": "#38bdf8", "avatar": "🔫"},
            {"id": "mahmut", "name": "Mahmut", "color": "#ef4444", "avatar": "😤"}
        ],
        "lines": [
            {"id": 1, "characterId": "pala", "startTime": 0.85, "endTime": 3.47, "text": "Al Mahmut, bunlar bir süre misafirin olacak."},
            {"id": 2, "characterId": "bedir", "startTime": 5.28, "endTime": 6.28, "text": "Geç."},
            {"id": 3, "characterId": "pala", "startTime": 6.1, "endTime": 7.1, "text": "Bak hele."},
            {"id": 4, "characterId": "bedir", "startTime": 6.88, "endTime": 7.88, "text": "Geç geç."},
            {"id": 5, "characterId": "mahmut", "startTime": 7.42, "endTime": 10.18, "text": "Biz gelmezsek bunların eti senin kemiği yiğitlerin olsun ya."},
            {"id": 6, "characterId": "pala", "startTime": 10.46, "endTime": 12.6, "text": "Siz kafanızı yormayın kardeş."},
            {"id": 7, "characterId": "pala", "startTime": 13.88, "endTime": 15.58, "text": "Sağ salim gidin."},
            {"id": 8, "characterId": "bedir", "startTime": 15.72, "endTime": 16.52, "text": "Gelin inşallah."},
            {"id": 9, "characterId": "mahmut", "startTime": 16.96, "endTime": 17.74, "text": "İnşallah abi."},
            {"id": 10, "characterId": "mahmut", "startTime": 18.14, "endTime": 19.14, "text": "İnşallah."},
            {"id": 11, "characterId": "pala", "startTime": 19.06, "endTime": 26.31, "text": "Hainler sizi..."},
            {"id": 12, "characterId": "mahmut", "startTime": 27.11, "endTime": 29.31, "text": "Öyle feda etmek değil oğlum."},
            {"id": 13, "characterId": "bedir", "startTime": 32.77, "endTime": 33.51, "text": "Sakin ol Mahmut."},
            {"id": 14, "characterId": "bedir", "startTime": 33.91, "endTime": 34.77, "text": "Bizim seninle bir işimiz yok."},
            {"id": 15, "characterId": "mahmut", "startTime": 37.96, "endTime": 39.78, "text": "Senin benimle işin yok da..."},
            {"id": 16, "characterId": "pala", "startTime": 41.26, "endTime": 42.64, "text": "Benim seninle işim var!"},
            {"id": 17, "characterId": "pala", "startTime": 42.64, "endTime": 43.64, "text": "Kahpe!"},
            {"id": 18, "characterId": "pala", "startTime": 43.64, "endTime": 48.43, "text": "Gittiniz kime uşaklık yapıyordunuz oğlum?!"}
        ]
    },
    # 42. Sıfır Bir - Filozof Okuyacaksın Lan (3 Karakter!)
    "meme-b65ba8effc3ba1fb": {
        "title": "Sıfır Bir - Filozof Sen Okuyacaksın Lan!",
        "characters": [
            {"id": "ozgur", "name": "Özgür", "color": "#f43f5e", "avatar": "⭐"},
            {"id": "filozof", "name": "Filozof (Çocuk)", "color": "#38bdf8", "avatar": "🎓"},
            {"id": "berto", "name": "Berto", "color": "#fbbf24", "avatar": "🧢"}
        ],
        "lines": [
            {"id": 1, "characterId": "ozgur", "startTime": 0.0, "endTime": 1.0, "text": "Ne yapıyorsun lan Filozof?"},
            {"id": 2, "characterId": "filozof", "startTime": 1.0, "endTime": 4.0, "text": "Ne yapayım vallahi Özgür abi, sizi gördüm bir selam vereyim dedim."},
            {"id": 3, "characterId": "ozgur", "startTime": 4.0, "endTime": 6.0, "text": "Adam ya, büyümüş de küçülmüş fırıldak seni."},
            {"id": 4, "characterId": "ozgur", "startTime": 6.0, "endTime": 7.0, "text": "Okul nasıl gidiyor?"},
            {"id": 5, "characterId": "filozof", "startTime": 7.0, "endTime": 9.0, "text": "Bu seneden sonra Özgür abi bırakacağım."},
            {"id": 6, "characterId": "ozgur", "startTime": 9.0, "endTime": 13.1, "text": "Niye oğlum? Mahalleyi sen kurtaracaksın oğlum, okusana!"},
            {"id": 7, "characterId": "filozof", "startTime": 13.1, "endTime": 16.1, "text": "Anamın durumu yok, o da artık bırak çalış diyor."},
            {"id": 8, "characterId": "ozgur", "startTime": 16.1, "endTime": 19.7, "text": "Olur mu öyle oğlum? Konuşak lan bunun anasıyla!"},
            {"id": 9, "characterId": "berto", "startTime": 19.7, "endTime": 23.06, "text": "Senin gibi zeki bir çocuk okuldan mı alınır lan?"},
            {"id": 10, "characterId": "ozgur", "startTime": 23.06, "endTime": 26.54, "text": "Bak biz okumadık ne olduk, bari siz okuyun lan!"},
            {"id": 11, "characterId": "ozgur", "startTime": 26.54, "endTime": 31.57, "text": "Berto kardeş, konuşun anasıyla. Okul masraflarını biz karşılarız."},
            {"id": 12, "characterId": "ozgur", "startTime": 31.57, "endTime": 35.57, "text": "Kendilerinin de bir ihtiyacı olursa hallederiz, kafasını yormasın."},
            {"id": 13, "characterId": "berto", "startTime": 35.57, "endTime": 39.57, "text": "Tamam kardeş, ben yarın gider konuşurum. Filozof'u da okulsuz bırakmayız aslanım."},
            {"id": 14, "characterId": "ozgur", "startTime": 39.57, "endTime": 46.98, "text": "Oğlum Filozof! Sen okuyacaksın lan! Doktor olacaksın, mühendis olacaksın, savcı olacaksın, hakim olacaksın!"},
            {"id": 15, "characterId": "berto", "startTime": 46.98, "endTime": 50.98, "text": "Bizim mahallemizden de böyle insanlar çıkabileceğini göstereceksin, tamam mı aslanım?"},
            {"id": 16, "characterId": "filozof", "startTime": 50.98, "endTime": 55.14, "text": "Tamam diyorum abi, Allah'ını severim lan senin. Hadi gidelim."}
        ]
    },
    # 43. Nazif ÖSS'yi Kaçırdın (3 Karakter!)
    "meme-c0ba8b38a59eb9ef": {
        "title": "Meme - Nazif ÖSS'yi Kaçırdın!",
        "characters": [
            {"id": "anne", "name": "Anne", "color": "#ec4899", "avatar": "🧕"},
            {"id": "baba", "name": "Baba", "color": "#f59e0b", "avatar": "👴"},
            {"id": "nazif", "name": "Nazif", "color": "#38bdf8", "avatar": "🤦‍♂️"}
        ],
        "lines": [
            {"id": 1, "characterId": "anne", "startTime": 0.5, "endTime": 7.46, "text": "Nazif, ÖSS'yi kaçırdın! ÖSS'yi kaçırdın Nazif!"},
            {"id": 2, "characterId": "nazif", "startTime": 8.75, "endTime": 10.41, "text": "Ya anasını satayım ya..."},
            {"id": 3, "characterId": "anne", "startTime": 12.34, "endTime": 14.54, "text": "Okuyup büyük adam olamayacaksın Nazif!"},
            {"id": 4, "characterId": "baba", "startTime": 19.75, "endTime": 21.45, "text": "Nasıl kaçırdın ÖSS'yi Nazif?"},
            {"id": 5, "characterId": "baba", "startTime": 23.28, "endTime": 24.74, "text": "Kaçta başlıyordu sınav?"},
            {"id": 6, "characterId": "nazif", "startTime": 25.12, "endTime": 25.7, "text": "10."},
            {"id": 7, "characterId": "baba", "startTime": 25.72, "endTime": 26.72, "text": "Saat kaç?"},
            {"id": 8, "characterId": "nazif", "startTime": 26.72, "endTime": 27.58, "text": "1."},
            {"id": 9, "characterId": "anne", "startTime": 30.89, "endTime": 32.21, "text": "Çalışmış mıydın o sınava?"},
            {"id": 10, "characterId": "nazif", "startTime": 34.49, "endTime": 37.41, "text": "Çok yoğun bir tempoyla çalıştım yaklaşık 4 ay."},
            {"id": 11, "characterId": "baba", "startTime": 39.13, "endTime": 40.37, "text": "Gece gündüz ders çalıştın..."}
        ]
    },
    # 44. Sıfır Bir - Koğuş Girişi ve Mesul (3 Karakter!)
    "meme-d7c49cb4311f4bf7": {
        "title": "Sıfır Bir - Cezaevi Koğuş Girişi ve Mesul",
        "characters": [
            {"id": "savas", "name": "Savaş Satış", "color": "#e11d48", "avatar": "🦁"},
            {"id": "mesul", "name": "Koğuş Mesulü", "color": "#f59e0b", "avatar": "🧔"},
            {"id": "soner", "name": "Soner", "color": "#38bdf8", "avatar": "👤"}
        ],
        "lines": [
            {"id": 1, "characterId": "soner", "startTime": 0.5, "endTime": 1.62, "text": "Selamünaleyküm."},
            {"id": 2, "characterId": "mesul", "startTime": 1.7, "endTime": 2.98, "text": "Aleykümselam baba."},
            {"id": 3, "characterId": "soner", "startTime": 3.06, "endTime": 5.46, "text": "Abi biz arkadaşlarla kendi aramızda da konuştuk..."},
            {"id": 4, "characterId": "soner", "startTime": 5.54, "endTime": 8.98, "text": "Şu köşede bir yer yapsak biz orada kalsak kendimize."},
            {"id": 5, "characterId": "mesul", "startTime": 9.73, "endTime": 11.45, "text": "Gereksiz başı sonra yatın."},
            {"id": 6, "characterId": "mesul", "startTime": 11.53, "endTime": 13.63, "text": "Bir de yer mi beğendireceğiz size?"},
            {"id": 7, "characterId": "savas", "startTime": 13.71, "endTime": 14.75, "text": "Mesul sensin değil mi?"},
            {"id": 8, "characterId": "mesul", "startTime": 14.83, "endTime": 15.95, "text": "Mesul benim baba."},
            {"id": 9, "characterId": "savas", "startTime": 16.03, "endTime": 17.31, "text": "Bu kardeş niye konuşuyor?"},
            {"id": 10, "characterId": "mesul", "startTime": 17.39, "endTime": 19.07, "text": "Bu kardeş bir daha konuşamaz."},
            {"id": 11, "characterId": "mesul", "startTime": 19.15, "endTime": 20.83, "text": "Sen konuşma Soner!"},
            {"id": 12, "characterId": "mesul", "startTime": 20.91, "endTime": 24.59, "text": "Baba istediğiniz yerde yatabilirsiniz kafanıza göre."},
            {"id": 13, "characterId": "savas", "startTime": 24.67, "endTime": 26.22, "text": "Eyvallah."},
            {"id": 14, "characterId": "savas", "startTime": 26.3, "endTime": 29.5, "text": "Sen sen ol, abilerin konuşurken lafa girme tamam mı?"}
        ]
    },
    # 45. Doğu Perinçek vs Ertuğrul Kürkçü (3 Karakter!)
    "meme-dfa4d19b1f82b2eb": {
        "title": "Siyaset Meydanı - Doğu Perinçek vs Ertuğrul Kürkçü",
        "characters": [
            {"id": "perincek", "name": "Doğu Perinçek", "color": "#ef4444", "avatar": "👉"},
            {"id": "kurkcu", "name": "Ertuğrul Kürkçü", "color": "#3b82f6", "avatar": "📑"},
            {"id": "moderatör", "name": "Ali Kırca (Moderatör)", "color": "#fbbf24", "avatar": "🎙️"}
        ],
        "lines": [
            {"id": 1, "characterId": "perincek", "startTime": 0.0, "endTime": 1.24, "text": "Kemalizmi savunacağız!"},
            {"id": 2, "characterId": "perincek", "startTime": 1.24, "endTime": 3.06, "text": "Sen Kemalist devrimi savunacaksın!"},
            {"id": 3, "characterId": "kurkcu", "startTime": 3.06, "endTime": 3.72, "text": "Sen komünistsin hadi bakayım!"},
            {"id": 4, "characterId": "perincek", "startTime": 3.72, "endTime": 4.34, "text": "Bırak palavrayı!"},
            {"id": 5, "characterId": "kurkcu", "startTime": 4.34, "endTime": 4.96, "text": "Sen bırak palavrayı!"},
            {"id": 6, "characterId": "perincek", "startTime": 4.96, "endTime": 5.7, "text": "Sen döneksin!"},
            {"id": 7, "characterId": "kurkcu", "startTime": 5.86, "endTime": 6.7, "text": "Sensin dönek!"},
            {"id": 8, "characterId": "perincek", "startTime": 6.9, "endTime": 7.76, "text": "Terbiyesiz herif!"},
            {"id": 9, "characterId": "kurkcu", "startTime": 7.82, "endTime": 10.92, "text": "Sen sıkıyönetim mahkemelerinde çıkıp dönekliğini ilan etmedin mi?!"},
            {"id": 10, "characterId": "perincek", "startTime": 10.92, "endTime": 11.86, "text": "Sen ne dedin?!"},
            {"id": 11, "characterId": "kurkcu", "startTime": 12.32, "endTime": 13.3, "text": "Sen 12 Eylül'de..."},
            {"id": 12, "characterId": "kurkcu", "startTime": 13.3, "endTime": 14.36, "text": "12 Eylül'de gelmiyorsun!"},
            {"id": 13, "characterId": "perincek", "startTime": 14.52, "endTime": 15.52, "text": "Göreceksin!"},
            {"id": 14, "characterId": "perincek", "startTime": 15.34, "endTime": 16.34, "text": "Göreceksin!"},
            {"id": 15, "characterId": "kurkcu", "startTime": 15.92, "endTime": 17.02, "text": "Sen Abdülhamit'i savundun!"},
            {"id": 16, "characterId": "perincek", "startTime": 17.26, "endTime": 18.26, "text": "Savunmadım!"},
            {"id": 17, "characterId": "kurkcu", "startTime": 17.84, "endTime": 18.8, "text": "Sen medreseleri savundun!"},
            {"id": 18, "characterId": "perincek", "startTime": 18.8, "endTime": 19.8, "text": "Savunmadım!"},
            {"id": 19, "characterId": "kurkcu", "startTime": 19.36, "endTime": 20.0, "text": "Sen savundun!"},
            {"id": 20, "characterId": "perincek", "startTime": 20.1, "endTime": 20.72, "text": "Terbiyesiz herif!"},
            {"id": 21, "characterId": "kurkcu", "startTime": 20.72, "endTime": 21.5, "text": "Savunmadın mı?"},
            {"id": 22, "characterId": "perincek", "startTime": 21.5, "endTime": 22.22, "text": "Savunmadım!"},
            {"id": 23, "characterId": "kurkcu", "startTime": 22.68, "endTime": 23.68, "text": "ÇIKAR GÖSTER!"},
            {"id": 24, "characterId": "perincek", "startTime": 23.68, "endTime": 24.68, "text": "Alçak herif!"},
            {"id": 25, "characterId": "kurkcu", "startTime": 24.68, "endTime": 25.56, "text": "Ver göstereyim!"},
            {"id": 26, "characterId": "moderatör", "startTime": 25.56, "endTime": 27.5, "text": "Sakin olun beyler lütfen..."},
            {"id": 27, "characterId": "perincek", "startTime": 30.0, "endTime": 32.72, "text": "Bir tane tokat atacağım!"},
            {"id": 28, "characterId": "kurkcu", "startTime": 32.78, "endTime": 33.98, "text": "Hiçbir şey atamazsın!"},
            {"id": 29, "characterId": "perincek", "startTime": 34.24, "endTime": 36.6, "text": "Sen görürsün Dev-Genç nasıl patlar beyninde!"},
            {"id": 30, "characterId": "moderatör", "startTime": 36.96, "endTime": 37.96, "text": "Lütfen..."},
            {"id": 31, "characterId": "perincek", "startTime": 38.02, "endTime": 41.14, "text": "Ben Dev-Genç'in ismini koyan ilk genel başkanıyım!"},
            {"id": 32, "characterId": "kurkcu", "startTime": 41.16, "endTime": 42.64, "text": "Sen FKF'nin başkanısın."},
            {"id": 33, "characterId": "kurkcu", "startTime": 42.64, "endTime": 45.2, "text": "Sen Dev-Genç'in başkanıydın."},
            {"id": 34, "characterId": "kurkcu", "startTime": 45.2, "endTime": 50.48, "text": "Ne güzel 18 yaşında hippie, 48 yaşında devrimciyim hala!"},
            {"id": 35, "characterId": "perincek", "startTime": 50.7, "endTime": 52.16, "text": "Siz hippie bile olamadınız biliyor musunuz?!"}
        ]
    },
    # 46. İşin Kötüsü Bunlar Çok Semizlenmişler
    "meme-e176a8d6ddafcd38": {
        "title": "Meme - Bunlar Çok Semizlenmişler",
        "characters": [
            {"id": "yegen", "name": "Yeğen", "color": "#38bdf8", "avatar": "🧢"},
            {"id": "dayi", "name": "Sinirli Dayı", "color": "#ef4444", "avatar": "👴"}
        ],
        "char_map": {"karakter_1": "yegen", "karakter_2": "dayi"}
    },
    # 47. Toteme Çorba Yazmışlar (1 Karakter)
    "meme-e826a1eb54f96a91": {
        "title": "Viral - Toteme Çorba Yazmışlar Rant",
        "characters": [
            {"id": "sofor", "name": "Aç Kalan Sürücü", "color": "#f97316", "avatar": "🥣"}
        ],
        "char_map": {"karakter_1": "sofor"}
    },
    # 48. Buzdolabı Işığı ve Şabat İcadı
    "meme-e8c99d3f73f2c634": {
        "title": "Meme - Buzdolabı Işığı ve Şabat İcadı",
        "characters": [
            {"id": "anlatan", "name": "Buluşu Anlatan Adam", "color": "#38bdf8", "avatar": "💡"},
            {"id": "dinleyen", "name": "Şüpheci Arkadaş", "color": "#fbbf24", "avatar": "🤨"}
        ],
        "char_map": {"karakter_1": "anlatan", "karakter_2": "dinleyen"}
    },
    # 49. Ümit Usta: Kuru Fasulye Kalmadı (Cuts & Split!)
    "meme-e93c45e8d6f4a3d8": {
        "title": "Meme - Kuru Fasulyeci Ümit Usta Parodisi",
        "characters": [
            {"id": "umit", "name": "Ümit Usta", "color": "#f59e0b", "avatar": "👨‍🍳"},
            {"id": "musteri", "name": "Aç Müşteri", "color": "#38bdf8", "avatar": "🍲"}
        ],
        "lines": [
            {"id": 1, "characterId": "musteri", "startTime": 0.0, "endTime": 6.76, "text": "Çorba falan yapma öyle, kendi evinin altında 11 gibi açıyor 2 gibi kapatıyor zaten kalmıyor, olana kadar efsane bir tat yapacağız."},
            {"id": 2, "characterId": "musteri", "startTime": 6.76, "endTime": 8.64, "text": "Ümit Usta 2 kuru versene bize be."},
            {"id": 3, "characterId": "umit", "startTime": 8.64, "endTime": 10.24, "text": "Kuru kalmadı oğlumuz."},
            {"id": 4, "characterId": "musteri", "startTime": 10.24, "endTime": 11.36, "text": "Yapma be abi."},
            {"id": 5, "characterId": "musteri", "startTime": 11.36, "endTime": 12.72, "text": "İyi yarın geliriz biz o zaman."},
            {"id": 6, "characterId": "umit", "startTime": 12.72, "endTime": 14.16, "text": "Ne yarın açmam."},
            {"id": 7, "characterId": "musteri", "startTime": 14.16, "endTime": 14.88, "text": "Hadi ya."},
            {"id": 8, "characterId": "musteri", "startTime": 14.88, "endTime": 16.24, "text": "İyi tamam Cuma geliriz ya."},
            {"id": 9, "characterId": "umit", "startTime": 16.24, "endTime": 17.6, "text": "Cuma da açmam."},
            {"id": 10, "characterId": "musteri", "startTime": 17.6, "endTime": 20.24, "text": "Haa Cuma gelemeyiz zaten toplantı var."},
            {"id": 11, "characterId": "umit", "startTime": 20.24, "endTime": 22.0, "text": "Ne ha Cuma açarım o zaman."},
            {"id": 12, "characterId": "musteri", "startTime": 22.0, "endTime": 23.84, "text": "Ümit Usta 2 kuru ver bize be."},
            {"id": 13, "characterId": "umit", "startTime": 23.84, "endTime": 25.52, "text": "Kalmadı oğlumuz yav."},
            {"id": 14, "characterId": "musteri", "startTime": 25.52, "endTime": 28.24, "text": "Saat 11'de açmadın mı sen? 11'i 10 geçiyor ne ara bitti?!"},
            {"id": 15, "characterId": "umit", "startTime": 28.24, "endTime": 31.08, "text": "Ben bir kase yaptım, kendime kadar yedim onu ya."},
            {"id": 16, "characterId": "musteri", "startTime": 31.08, "endTime": 32.02, "text": "Yarın kaçta açacaksın?"},
            {"id": 17, "characterId": "umit", "startTime": 32.34, "endTime": 34.12, "text": "Sabahın en 4.30'unda açarım."},
            {"id": 18, "characterId": "musteri", "startTime": 34.92, "endTime": 36.9, "text": "Öğlen bize iki kuru verirsin abi."},
            {"id": 19, "characterId": "umit", "startTime": 36.92, "endTime": 38.5, "text": "Oğlumuz ne konuşacağım sabah sabah?"},
            {"id": 20, "characterId": "musteri", "startTime": 38.84, "endTime": 40.88, "text": "Abi sen deli misin sabah 4.30'da açacaksın?"},
            {"id": 21, "characterId": "umit", "startTime": 41.14, "endTime": 43.78, "text": "Açtım da kapatacağım ya camiye gideceğim."},
            {"id": 22, "characterId": "umit", "startTime": 43.96, "endTime": 46.64, "text": "Sular soğuk orada burada sıcağına abdest aldım gideceğim şimdi."},
            {"id": 23, "characterId": "umit", "startTime": 47.02, "endTime": 48.0, "text": "11 gibi gelin."},
            {"id": 24, "characterId": "musteri", "startTime": 48.04, "endTime": 49.04, "text": "Bu ne?"},
            {"id": 25, "characterId": "umit", "startTime": 49.85, "endTime": 53.25, "text": "Narsist kişiliğime yenik düştüm ve zirvede bırakıyorum."},
            {"id": 26, "characterId": "umit", "startTime": 53.39, "endTime": 55.89, "text": "Siz bunu okuduğunuzda ben çoktan emekli olacağım."},
            {"id": 27, "characterId": "umit", "startTime": 56.53, "endTime": 58.33, "text": "Kurucu üye Ümit Usta."}
        ]
    },
    # 50. Kurtlar Vadisi - Her Delikanlının Bir Gelişi Vardır
    "meme-ea037fab87e9c168": {
        "title": "Kurtlar Vadisi - Her Delikanlının Bir Gelişi Vardır",
        "characters": [
            {"id": "raconcu", "name": "Ağır Abi", "color": "#1e293b", "avatar": "🕶️"},
            {"id": "genc", "name": "Genç", "color": "#fbbf24", "avatar": "😨"}
        ],
        "char_map": {"karakter_1": "genc", "karakter_2": "raconcu"}
    },
    # 51. Tut Lan Ben De Aşağı Atlıyorum
    "meme-ec13d57c1425f814": {
        "title": "Viral - Tut Lan Ben De Aşağı Atlıyorum",
        "characters": [
            {"id": "kanka1", "name": "Aşağıdaki Kanka", "color": "#38bdf8", "avatar": "😱"},
            {"id": "kanka2", "name": "Atlayan Kanka", "color": "#ef4444", "avatar": "🤸"}
        ],
        "char_map": {"karakter_1": "kanka1", "karakter_2": "kanka2"}
    },
    # 52. Kurtlar Vadisi - Ziya Bey Özür Dileyip (3 Karakter!)
    "meme-f0a445c3a2b4afaa": {
        "title": "Kurtlar Vadisi - Çakır Masaya Meydan Okuyor",
        "characters": [
            {"id": "cakir", "name": "Süleyman Çakır", "color": "#ef4444", "avatar": "🔥"},
            {"id": "necmi", "name": "Testere Necmi", "color": "#38bdf8", "avatar": "🪓"},
            {"id": "lazziya", "name": "Laz Ziya", "color": "#f59e0b", "avatar": "🗡️"}
        ],
        "lines": [
            {"id": 1, "characterId": "cakir", "startTime": 0.85, "endTime": 6.15, "text": "O zaman Ziya Bey benden özür dileyip bu düşmanlığa bir son verecek!"},
            {"id": 2, "characterId": "cakir", "startTime": 7.05, "endTime": 11.09, "text": "Çünkü ben onlara kardeşlikten başka hiçbir şey yapmadım."},
            {"id": 3, "characterId": "necmi", "startTime": 11.88, "endTime": 16.12, "text": "Ulan! Ben senin adamın mıyım?!"},
            {"id": 4, "characterId": "lazziya", "startTime": 17.42, "endTime": 19.74, "text": "Üstündeki adam mıyım ki?"},
            {"id": 5, "characterId": "necmi", "startTime": 20.97, "endTime": 23.95, "text": "Gözümün içine bakarak beni tehdit edeceksin..."},
            {"id": 6, "characterId": "lazziya", "startTime": 25.6, "endTime": 30.66, "text": "Yüzüme utanmadan özür bekleyeceksin!"}
        ]
    },
    # 53. Ahmet Şık - Megafonu Elinize Alıp
    "meme-f337b03a431b512d": {
        "title": "Röportaj - Ahmet Şık Hükümet İstifa Dediniz Mi?",
        "characters": [
            {"id": "muhabir", "name": "Muhabir", "color": "#38bdf8", "avatar": "🎤"},
            {"id": "ahmet", "name": "Ahmet Şık", "color": "#f59e0b", "avatar": "📣"}
        ],
        "lines": [
            {"id": 1, "characterId": "muhabir", "startTime": 0.4, "endTime": 3.22, "text": "Megafonu elinize alıp hükümet istifa dediniz mi?"},
            {"id": 2, "characterId": "ahmet", "startTime": 3.92, "endTime": 4.4, "text": "Kim?"},
            {"id": 3, "characterId": "muhabir", "startTime": 4.44, "endTime": 5.44, "text": "Siz."},
            {"id": 4, "characterId": "ahmet", "startTime": 6.63, "endTime": 7.63, "text": "Yo."},
            {"id": 5, "characterId": "muhabir", "startTime": 10.34, "endTime": 12.84, "text": "Hükümet istifa dediğiniz şeklinde haberleri ben okudum."}
        ]
    },
    # 54. Ezel - Kerpeten Ali Sanayide (3 Karakter!)
    "meme-fbb565592abea053": {
        "title": "Ezel - Kerpeten Ali Sanayide Racon",
        "characters": [
            {"id": "ali", "name": "Kerpeten Ali", "color": "#ef4444", "avatar": "🔧"},
            {"id": "cirak", "name": "Çırak", "color": "#38bdf8", "avatar": "👦"},
            {"id": "hoca", "name": "Hoca (Usta)", "color": "#f59e0b", "avatar": "👨‍🔧"}
        ],
        "lines": [
            {"id": 1, "characterId": "cirak", "startTime": 1.55, "endTime": 2.55, "text": "Kolay gelsin."},
            {"id": 2, "characterId": "ali", "startTime": 2.91, "endTime": 3.79, "text": "Vay koçum."},
            {"id": 3, "characterId": "ali", "startTime": 4.15, "endTime": 4.77, "text": "Hoca ne haber?"},
            {"id": 4, "characterId": "hoca", "startTime": 6.51, "endTime": 7.11, "text": "Eyvallah."},
            {"id": 5, "characterId": "ali", "startTime": 7.65, "endTime": 10.01, "text": "Kardeş, sen geç benim arabanın yanına da bir bak."},
            {"id": 6, "characterId": "cirak", "startTime": 10.81, "endTime": 13.15, "text": "Lan elin dursa ayağın durmaz be oğlum."},
            {"id": 7, "characterId": "ali", "startTime": 14.35, "endTime": 18.32, "text": "Ne gülüyorsun lan? Komik bir şey mi var?"},
            {"id": 8, "characterId": "cirak", "startTime": 18.78, "endTime": 20.24, "text": "Yok ondan değil abi."},
            {"id": 9, "characterId": "ali", "startTime": 21.1, "endTime": 22.1, "text": "Yenisin herhalde burada."},
            {"id": 10, "characterId": "ali", "startTime": 23.06, "endTime": 24.84, "text": "Sen kimsin benim suratıma güleceksin lan?!"},
            {"id": 11, "characterId": "cirak", "startTime": 25.34, "endTime": 26.36, "text": "Yok yanlış anladın abi."},
            {"id": 12, "characterId": "ali", "startTime": 26.42, "endTime": 27.42, "text": "Konuşma lan!"},
            {"id": 13, "characterId": "ali", "startTime": 27.52, "endTime": 28.3, "text": "Sen git arabaya bak."},
            {"id": 14, "characterId": "hoca", "startTime": 30.7, "endTime": 31.7, "text": "Dur lan."},
            {"id": 15, "characterId": "hoca", "startTime": 31.56, "endTime": 34.48, "text": "Dağdan geldiniz, İstanbul'u kendinize benzettiniz anasını satayım."},
            {"id": 16, "characterId": "ali", "startTime": 34.48, "endTime": 38.04, "text": "Hayır hoca, senin oğlan yeni galiba?"},
            {"id": 17, "characterId": "hoca", "startTime": 38.04, "endTime": 41.78, "text": "He, canavar yeni."},
            {"id": 18, "characterId": "ali", "startTime": 41.78, "endTime": 44.28, "text": "Oğlum, sen beni caddede göreceksin."},
            {"id": 19, "characterId": "ali", "startTime": 44.28, "endTime": 46.91, "text": "Bütün arabaları peşime takıyorum Allah seni inandırsın."},
            {"id": 20, "characterId": "cirak", "startTime": 46.91, "endTime": 48.36, "text": "Doğrudur."},
            {"id": 21, "characterId": "cirak", "startTime": 48.36, "endTime": 58.08, "text": "Aaa bak fena çizilmiş burası."},
            {"id": 22, "characterId": "ali", "startTime": 58.08, "endTime": 60.34, "text": "Yapma lan, neresi?"},
            {"id": 23, "characterId": "cirak", "startTime": 60.34, "endTime": 61.34, "text": "Bak burası."},
            {"id": 24, "characterId": "ali", "startTime": 61.34, "endTime": 64.49, "text": "Ne yapıyorsun lan?!"},
            {"id": 25, "characterId": "hoca", "startTime": 64.49, "endTime": 65.49, "text": "Lan ne yapıyorsun?"},
            {"id": 26, "characterId": "cirak", "startTime": 65.49, "endTime": 67.0, "text": "Ali abi..."},
            {"id": 27, "characterId": "ali", "startTime": 67.0, "endTime": 70.0, "text": "Senin takımlarını da bir elden geçirelim mi hoca?"},
            {"id": 28, "characterId": "ali", "startTime": 70.0, "endTime": 74.0, "text": "He, bir daha bir edepsizliğini görürsem sana bir 100 beygir daha takarım!"},
            {"id": 29, "characterId": "ali", "startTime": 74.0, "endTime": 76.0, "text": "Buradan pati yapar kalkarsın!"},
            {"id": 30, "characterId": "ali", "startTime": 76.0, "endTime": 78.0, "text": "Anladın mı hoca?"},
            {"id": 31, "characterId": "ali", "startTime": 78.0, "endTime": 80.0, "text": "Anladıysan salla silecekleri!"},
            {"id": 32, "characterId": "ali", "startTime": 80.0, "endTime": 86.32, "text": "Sen öldün lan, öldün lan sen!"},
            {"id": 33, "characterId": "ali", "startTime": 86.32, "endTime": 88.32, "text": "Öldün lan sen!"},
            {"id": 34, "characterId": "ali", "startTime": 88.32, "endTime": 90.61, "text": "Seni burada tanıyorlarmış ya..."},
            {"id": 35, "characterId": "ali", "startTime": 90.61, "endTime": 101.18, "text": "Beni de tanırlar!"},
            {"id": 36, "characterId": "hoca", "startTime": 101.18, "endTime": 103.18, "text": "Biliyor musun? Çaktın mı?"}
        ]
    },
    # 55. Technopat: Sistem Toplama Parodisi (Cut Split & Real Names!)
    "meme-fdd89b3a7015c460": {
        "title": "Technopat - Sistem Toplama Parodisi",
        "characters": [
            {"id": "recep", "name": "Recep Baltaş", "color": "#0ea5e9", "avatar": "💻"},
            {"id": "ali", "name": "Ali Güngör", "color": "#f59e0b", "avatar": "🖥️"}
        ],
        "lines": [
            {"id": 1, "characterId": "recep", "startTime": 0.0, "endTime": 0.70, "text": "Ben Recep."},
            {"id": 2, "characterId": "ali", "startTime": 0.85, "endTime": 1.40, "text": "Ben Ali."},
            {"id": 3, "characterId": "recep", "startTime": 1.60, "endTime": 4.16, "text": "Bugün sizlerle UEFI Windows toplayacağız, değil mi Ali?"},
            {"id": 4, "characterId": "ali", "startTime": 4.68, "endTime": 8.02, "text": "Evet Recep, bugün gerçekten de UEFI bir Windows toplayacağız."},
            {"id": 5, "characterId": "ali", "startTime": 8.46, "endTime": 11.14, "text": "Bu anakartımız yanında aparatlarıyla geliyor, değil mi Recep?"},
            {"id": 6, "characterId": "recep", "startTime": 11.72, "endTime": 14.92, "text": "Evet Ali, sahiden de bu anakartımız yanında aparatlarıyla geliyor."},
            {"id": 7, "characterId": "ali", "startTime": 15.1, "endTime": 17.26, "text": "Dilersen şimdi sistem testlerine geçelim Recep."},
            {"id": 8, "characterId": "recep", "startTime": 17.76, "endTime": 18.68, "text": "Geçelim bakalım Ali."},
            {"id": 9, "characterId": "recep", "startTime": 18.98, "endTime": 22.3, "text": "Shadow of War oynuyoruz, burada bir ork var gördüğün gibi, öyle değil mi Ali?"},
            {"id": 10, "characterId": "ali", "startTime": 22.6, "endTime": 24.76, "text": "Evet Recep, orada gerçekten de bir ork var."},
            {"id": 11, "characterId": "recep", "startTime": 25.08, "endTime": 27.48, "text": "Şimdi vuruyorum onu Ali. Vurdum onu, değil mi Ali?"},
            {"id": 12, "characterId": "ali", "startTime": 27.48, "endTime": 29.68, "text": "Evet Recep, gerçekten de vurdun onu."},
            {"id": 13, "characterId": "recep", "startTime": 30.0, "endTime": 32.68, "text": "Bu yeni topladığımız sistem hakkında ne düşünüyorsun Ali?"},
            {"id": 14, "characterId": "ali", "startTime": 33.0, "endTime": 34.48, "text": "Evet Recep, gerçekten de öyle."},
            {"id": 15, "characterId": "ali", "startTime": 34.84, "endTime": 35.56, "text": "Öyle değil mi Recep?"},
            {"id": 16, "characterId": "recep", "startTime": 36.0, "endTime": 37.32, "text": "Evet Ali, gerçekten de öyle."},
            {"id": 17, "characterId": "recep", "startTime": 37.74, "endTime": 38.32, "text": "Öyle değil mi Ali?"},
            {"id": 18, "characterId": "ali", "startTime": 38.76, "endTime": 40.46, "text": "Evet Recep, gerçekten de öyle."}
        ]
    },
    # 56. Arka Sokaklar: Komiser Hüsnü Çoban
    "meme-ff6ff8de71ce542b": {
        "title": "Arka Sokaklar - Komiser Hüsnü Çoban Parodisi",
        "characters": [
            {"id": "husnu", "name": "Komiser Hüsnü", "color": "#38bdf8", "avatar": "👮"}
        ],
        "char_map": {"karakter_1": "husnu"}
    }
}

print(f"Toplam sahne sayısı: {len(scenes)}")
updated_count = 0

for scene in scenes:
    s_id = scene.get("id")
    if s_id not in CURATED_DATA:
        continue
    
    curation = CURATED_DATA[s_id]
    
    # 1. Başlık güncelleme
    if "title" in curation:
        scene["title"] = curation["title"]
        
    # 2. Karakterler güncelleme
    if "characters" in curation:
        scene["characters"] = curation["characters"]
        
    # 3. Replikler güncelleme veya karakter eşleştirme
    if "lines" in curation:
        scene["lines"] = curation["lines"]
    elif "char_map" in curation:
        cmap = curation["char_map"]
        for line in scene.get("lines", []):
            cid = line.get("characterId")
            if cid in cmap:
                line["characterId"] = cmap[cid]
                
    # 4. Süre güvenlik kontrolü
    max_line_end = max([l.get("endTime", 0) for l in scene.get("lines", [])] + [0])
    if max_line_end > scene.get("duration", 0):
        scene["duration"] = round(max_line_end + 0.5, 2)
        
    updated_count += 1
    print(f"✅ Güncellendi: [{s_id}] -> {scene['title']} ({len(scene.get('characters', []))} karakter, {len(scene.get('lines', []))} replik)")

# Kaydet
payload = {
    "version": "2.5.0",
    "totalScenes": len(scenes),
    "scenes": scenes
}

with open(SCENES_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

js_content = f"// Dublaj Oyunu - Sahne Veritabanı (Rol İzolasyonu ve Çoklu Karakter Kürasyonlu)\nexport const SCENES = {json.dumps(scenes, ensure_ascii=False, indent=2)};\n"
with open(SCENES_JS_PATH, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"\n🎉 İşlem tamamlandı! Toplam {updated_count} sahne baştan sona kürate edildi ve kaydedildi.")
