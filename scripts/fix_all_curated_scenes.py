#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dublaj Oyunu - Kapsamlı Transkript, Rol ve Karakter Revizyon Motoru
Whisper halüsinasyonlarını, yanlış karakter atamalarını ve bozuk diyalogları
Türk meme ve popüler kültürünün orijinal replikleriyle düzeltir.
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

SCENES_JSON = 'data/scenes.json'
SCENES_JS = 'js/scenes.js'

with open(SCENES_JSON, 'r', encoding='utf-8') as f:
    data = json.load(f)

scenes = data.get('scenes', [])

REVISIONS = {
    # 1. Sıfır Bir - Mahalle Hikayesi (Cio & Savaş)
    'sifir-bir-cio': {
        'title': 'Sıfır Bir - Cio & Savaş Alacak Verecek Davası',
        'characters': [
            {'id': 'cio', 'name': 'Cio Baba', 'color': '#f43f5e', 'avatar': '⚡'},
            {'id': 'savas', 'name': 'Savaş Satış', 'color': '#3b82f6', 'avatar': '💥'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'cio', 'startTime': 0.0, 'endTime': 4.0, 'text': 'Bak sen herhalde anlatacağım mevzuyu tam anlamadın he?', 'emotion': 'Ağır abi racon anlatımı'},
            {'id': 2, 'characterId': 'savas', 'startTime': 4.0, 'endTime': 7.0, 'text': 'Sarsılmaz abi ben, dinliyorum anlat.', 'emotion': 'Sakin ve dikkatli'},
            {'id': 3, 'characterId': 'cio', 'startTime': 7.0, 'endTime': 12.0, 'text': 'O gün bir dostuyla bir alacak verecek meselesi için bir yere gitmişler...', 'emotion': 'Gerilimli hikaye anlatımı'},
            {'id': 4, 'characterId': 'savas', 'startTime': 12.0, 'endTime': 15.0, 'text': 'Tamam, adamlar orada mevzuyu bitirmiş yani.', 'emotion': 'Diyaloğu toparlayan onay'}
        ]
    },

    # 2. Sınıf Başkanı Kavgası (Meme)
    'meme-0c8ee1a80532ffce': {
        'title': 'Viral - Ben Bu Sınıfın Sınıf Başkanıyım!',
        'characters': [
            {'id': 'baskan', 'name': 'Sınıf Başkanı', 'color': '#ef4444', 'avatar': '📢'},
            {'id': 'ogrenci', 'name': 'İsyankar Öğrenci', 'color': '#3b82f6', 'avatar': '🎒'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'baskan', 'startTime': 0.3, 'endTime': 3.0, 'text': 'Senin böyle konuşmaya hakkın yok, kimsin sen?!', 'emotion': 'Otoriter sınıf başkanı'},
            {'id': 2, 'characterId': 'ogrenci', 'startTime': 3.3, 'endTime': 5.0, 'text': 'Sen kendi işine baksana oğlum!', 'emotion': 'Umursamaz ve isyankar'},
            {'id': 3, 'characterId': 'baskan', 'startTime': 5.3, 'endTime': 8.5, 'text': 'Sen öğretmenine de mi böyle konuşuyorsun terbiyesiz?!', 'emotion': 'Hesap soran ton'},
            {'id': 4, 'characterId': 'ogrenci', 'startTime': 9.0, 'endTime': 12.0, 'text': 'Sen öğretmen misin lan?! Öğretmenine de mi böyle konuşuyorsun diyor bir de!', 'emotion': 'Alaycı karşı çıkış'},
            {'id': 5, 'characterId': 'baskan', 'startTime': 12.39, 'endTime': 16.5, 'text': 'Ya sabır Allah Allah! Herkes bir havalara girmiş sınıfta!', 'emotion': 'Çıldırma başlangıcı'},
            {'id': 6, 'characterId': 'baskan', 'startTime': 16.75, 'endTime': 21.63, 'text': 'Ben bu sınıfın sınıf başkanıysam her şeyi bilmek zorundayım!', 'emotion': 'Tarihi tirad: Masaya vurma'},
            {'id': 7, 'characterId': 'baskan', 'startTime': 21.85, 'endTime': 25.0, 'text': 'Yok öyle bir şey ya! Yürü git şuradan dünyanın artisti!', 'emotion': 'Noktayı koyan başkan'}
        ]
    },

    # 3. İsmail Kartal - Ferdi'yi Sol Bek Yapan Benim
    'meme-5a992347adcc5220': {
        'title': 'İsmail Kartal - Ferdi\'yi Sol Bek Yapan Benim!',
        'characters': [
            {'id': 'kartal', 'name': 'İsmail Kartal (Arap İsmail)', 'color': '#f59e0b', 'avatar': '🦅'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'kartal', 'startTime': 0.4, 'endTime': 3.5, 'text': 'Ferdi\'yi sol bek yapan benim!', 'emotion': 'Gururlu ve iddialı basın toplantısı'},
            {'id': 2, 'characterId': 'kartal', 'startTime': 3.5, 'endTime': 6.0, 'text': 'Osayi\'yi sağ bek yapan benim!', 'emotion': 'Vurgulayarak el hareketi'},
            {'id': 3, 'characterId': 'kartal', 'startTime': 6.0, 'endTime': 8.5, 'text': 'Szymanski\'yi 6 numara, 8 numara, sağ kanatta oynatan benim!', 'emotion': 'Taktik dehası anlatımı'},
            {'id': 4, 'characterId': 'kartal', 'startTime': 8.5, 'endTime': 10.98, 'text': 'Niye kimse bunu konuşmuyor? Serdar Dursun\'u 10 numara oynatan benim!', 'emotion': 'Sitemkar ve net son vuruş'}
        ]
    },

    # 4. Bu Ne Çirkinlik TikTok Atışması
    'meme-5b819baf3f383a04': {
        'title': 'TikTok - Dalton Sandılar Seni Canlı Yayın Atışması',
        'characters': [
            {'id': 'batuhan', 'name': 'Batuhan', 'color': '#3b82f6', 'avatar': '📱'},
            {'id': 'konuk', 'name': 'Yayın Konuğu', 'color': '#f97316', 'avatar': '🎭'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'batuhan', 'startTime': 0.08, 'endTime': 2.08, 'text': 'Bu ne çirkinlik ya?', 'emotion': 'Laf sokucu yayıncı'},
            {'id': 2, 'characterId': 'konuk', 'startTime': 2.08, 'endTime': 3.5, 'text': 'Bana mı diyorsun?', 'emotion': 'Şaşırmış'},
            {'id': 3, 'characterId': 'batuhan', 'startTime': 3.5, 'endTime': 5.08, 'text': 'Evet sana diyorum çirkin.', 'emotion': 'Alaycı'},
            {'id': 4, 'characterId': 'konuk', 'startTime': 8.08, 'endTime': 11.5, 'text': 'Batuhan bir şey sorabilir miyim? Özel biri misin yoksa?', 'emotion': 'Laf çarpmaya hazırlık'},
            {'id': 5, 'characterId': 'batuhan', 'startTime': 11.5, 'endTime': 14.27, 'text': 'Özel biriyim doğrudur, ne oldu?', 'emotion': 'Meraklı'},
            {'id': 6, 'characterId': 'konuk', 'startTime': 17.5, 'endTime': 22.5, 'text': 'Dalton sandılar seni reis! Evet efendim!', 'emotion': 'Kahkaha ile laf sokma'},
            {'id': 7, 'characterId': 'konuk', 'startTime': 22.5, 'endTime': 28.5, 'text': 'Yemin ediyorum Dalton sandılar seni ekranda!', 'emotion': 'Meme patlaması'},
            {'id': 8, 'characterId': 'konuk', 'startTime': 32.0, 'endTime': 36.41, 'text': 'Hadi görüşürüz kankam bay bay!', 'emotion': 'Yayından kaçış'}
        ]
    },

    # 5. Han Kanal ve Piggy Röportajı
    'meme-82905766b3d259c2': {
        'title': 'Han Kanal - Piggy ile Özel Röportaj',
        'characters': [
            {'id': 'han', 'name': 'Han Kanal', 'color': '#38bdf8', 'avatar': '🎙️'},
            {'id': 'piggy', 'name': 'Piggy (Domuzcuk)', 'color': '#ec4899', 'avatar': '🐷'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'han', 'startTime': 0.0, 'endTime': 3.5, 'text': 'İlk olarak ben bunu çok merak ediyorum, Handaşlar da seni çok merak ediyor.', 'emotion': 'Röportaj açılışı'},
            {'id': 2, 'characterId': 'piggy', 'startTime': 4.0, 'endTime': 8.58, 'text': 'Benim umurumda değil! Bana yemek ver ne olur, ben açlıktan ölüyorum burada ya!', 'emotion': 'İsyankar Piggy'},
            {'id': 3, 'characterId': 'han', 'startTime': 11.5, 'endTime': 14.02, 'text': 'Evet Piggy, sahibinden memnun musun peki?', 'emotion': 'Ciddi spiker sorusu'},
            {'id': 4, 'characterId': 'piggy', 'startTime': 14.14, 'endTime': 17.58, 'text': 'Bunu da mı merak ediyor Handaşlar? Ne yaptın evime be!', 'emotion': 'Tepkili'},
            {'id': 5, 'characterId': 'piggy', 'startTime': 20.5, 'endTime': 23.85, 'text': 'Sahibimden memnun değilim! Ben başka kulübe transfer olmak istiyorum!', 'emotion': 'Noktayı koyan domuzcuk'}
        ]
    },

    # 6. Hacının Şalgamı Efsanevi 3D Reklamı (Daha önce dummy "Meme repliği" kalmıştı!)
    'meme-8c3b341acc6bda05': {
        'title': 'Nostalji 3D Reklam - Hacının Şalgamı (1947)',
        'description': 'Efsanevi Türk 3D animasyon reklam klasiği: Hacının Şalgamı şişelerinin neşeli dansı ve jeneriği.',
        'characters': [
            {'id': 'salgam1', 'name': 'Acılı Şalgam Şişesi', 'color': '#dc2626', 'avatar': '🌶️'},
            {'id': 'salgam2', 'name': 'Klasik Şalgam Şişesi', 'color': '#9333ea', 'avatar': '🍶'},
            {'id': 'spiker', 'name': 'Dış Ses / Jenerik', 'color': '#3b82f6', 'avatar': '📢'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'salgam1', 'startTime': 0.5, 'endTime': 6.5, 'text': 'Kebapların, köftelerin yanına Hacının Şalgamı yakışır!', 'emotion': 'Neşeli reklam melodisi'},
            {'id': 2, 'characterId': 'salgam2', 'startTime': 6.5, 'endTime': 12.0, 'text': 'Soğuk soğuk içiniz, lezzetine lezzet katınız!', 'emotion': 'Coşkulu animasyon sesi'},
            {'id': 3, 'characterId': 'salgam1', 'startTime': 12.0, 'endTime': 18.5, 'text': 'Yüzde yüz doğal, yüzde yüz Adana lezzeti!', 'emotion': 'Dans eden şişe'},
            {'id': 4, 'characterId': 'salgam2', 'startTime': 18.5, 'endTime': 24.5, 'text': 'Şalgam denince akla, tamam şimdi gelir Hacının Şalgamı!', 'emotion': 'Slogan temposu'},
            {'id': 5, 'characterId': 'spiker', 'startTime': 24.5, 'endTime': 30.5, 'text': '1947\'den beri geleneksel lezzet: Hacının Şalgamı!', 'emotion': 'Resmi nostaljik reklam dış sesi'}
        ]
    },

    # 7. Kadın Sürücü Panik Anı
    'meme-a9bd70989fc91692': {
        'title': 'Viral - Yeni Arabayla Kadın Sürücü Panik Anı',
        'characters': [
            {'id': 'surucu', 'name': 'Yeni Araba Alan Sürücü', 'color': '#ef4444', 'avatar': '🚗'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'surucu', 'startTime': 0.21, 'endTime': 2.5, 'text': 'Hele şükür aldık sonunda arabayı ya!', 'emotion': 'Rahatlama ve heves'},
            {'id': 2, 'characterId': 'surucu', 'startTime': 2.5, 'endTime': 4.5, 'text': 'Kazasız belasız bir binelim inşallah.', 'emotion': 'Dua eden ses'},
            {'id': 3, 'characterId': 'surucu', 'startTime': 4.5, 'endTime': 6.5, 'text': 'Ay ay dönemiyorum! Dur dur dur!', 'emotion': 'Aniden başlayan panik'},
            {'id': 4, 'characterId': 'surucu', 'startTime': 6.5, 'endTime': 10.5, 'text': 'Olamaz! Kadın sürücü geliyor kadın sürücüü!', 'emotion': 'Tam çıldırma çığlığı'}
        ]
    },

    # 8. Kurtlar Vadisi - Testere Necmi Masaya Meydan Okuyor (Laz Ziya hatası düzeltildi!)
    'meme-f0a445c3a2b4afaa': {
        'title': 'Kurtlar Vadisi - Testere Necmi Çakır\'a Patlıyor',
        'characters': [
            {'id': 'cakir', 'name': 'Süleyman Çakır', 'color': '#3b82f6', 'avatar': '🔫'},
            {'id': 'necmi', 'name': 'Testere Necmi', 'color': '#dc2626', 'avatar': '🪚'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'cakir', 'startTime': 0.85, 'endTime': 6.15, 'text': 'O zaman Ziya Bey benden özür dileyip bu düşmanlığa bir son verecek!', 'emotion': 'Meydan okuyan Çakır'},
            {'id': 2, 'characterId': 'cakir', 'startTime': 7.05, 'endTime': 11.09, 'text': 'Çünkü ben onlara kardeşlikten başka hiçbir şey yapmadım.', 'emotion': 'Masaya ağırlığını koyarak'},
            {'id': 3, 'characterId': 'necmi', 'startTime': 11.88, 'endTime': 16.5, 'text': 'Ulan! Ben senin adamın mıyım lan?!', 'emotion': 'Ayağa fırlayan Testere Necmi'},
            {'id': 4, 'characterId': 'necmi', 'startTime': 16.5, 'endTime': 21.0, 'text': 'Ben senin emrindeki adam mıyım ki masada bana kafa tutuyorsun?!', 'emotion': 'Öfkeden deliren Necmi'},
            {'id': 5, 'characterId': 'necmi', 'startTime': 21.0, 'endTime': 25.5, 'text': 'Gözümün içine bakarak beni tehdit edeceksin...', 'emotion': 'Dişlerini sıkarak'},
            {'id': 6, 'characterId': 'necmi', 'startTime': 25.6, 'endTime': 32.5, 'text': 'Üstüne bir de utanmadan yüzüme bakıp benden özür bekleyeceksin öyle mi?!', 'emotion': 'Masayı inleten kükreme'}
        ]
    },

    # 9. Kurtlar Vadisi / EDHO Racon - Her Delikanlının Bir Gelişi Vardır (Kumarhane Krupiye)
    'meme-ea037fab87e9c168': {
        'title': 'Kurtlar Vadisi - Her Delikanlının Bir Gelişi Vardır',
        'characters': [
            {'id': 'genc', 'name': 'Genç Kumarbaz', 'color': '#38bdf8', 'avatar': '🎲'},
            {'id': 'kirve', 'name': 'Kirve / Ağır Abi', 'color': '#f59e0b', 'avatar': '🚬'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'genc', 'startTime': 1.14, 'endTime': 2.5, 'text': 'Selamünaleyküm, ne haber?', 'emotion': 'Mekana giriş'},
            {'id': 2, 'characterId': 'kirve', 'startTime': 3.0, 'endTime': 5.25, 'text': 'İyidir kirve, sen nasılsın?', 'emotion': 'Ağır abi tonu'},
            {'id': 3, 'characterId': 'genc', 'startTime': 5.41, 'endTime': 6.39, 'text': 'Ne diyorsun oğlum?', 'emotion': 'Soru sorma'},
            {'id': 4, 'characterId': 'kirve', 'startTime': 6.57, 'endTime': 8.81, 'text': 'Ya ne öyle aniden geliyorsun? Aklımız gitti!', 'emotion': 'Şaşırmış'},
            {'id': 5, 'characterId': 'genc', 'startTime': 9.15, 'endTime': 11.73, 'text': 'Ee... Her delikanlının bir gelişi vardır!', 'emotion': 'Racon kesme'},
            {'id': 6, 'characterId': 'kirve', 'startTime': 12.0, 'endTime': 15.0, 'text': 'Ne yaptın lan? Güzel krupiye aldın mı içeriye?', 'emotion': 'Kumarhane sorgusu'}
        ]
    },

    # 10. Grafi2000 Arka Sokaklar - Hüsnü Çoban & Light Selami
    'meme-ff6ff8de71ce542b': {
        'title': 'Grafi2000 - Komiser Hüsnü Çoban & Light Selami Rap',
        'characters': [
            {'id': 'husnu', 'name': 'Komiser Hüsnü Çoban', 'color': '#3b82f6', 'avatar': '👮'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'husnu', 'startTime': 2.06, 'endTime': 3.94, 'text': 'Polis! Dur dur! Yok yok...', 'emotion': 'Gözlüklü Hüsnü anonsu'},
            {'id': 2, 'characterId': 'husnu', 'startTime': 3.94, 'endTime': 5.82, 'text': 'Tamam abi sen durmayabilirsin, sen devam et git.', 'emotion': 'Trafiği salma'},
            {'id': 3, 'characterId': 'husnu', 'startTime': 5.82, 'endTime': 7.6, 'text': 'Siz küçük olanlar, yakaladım sizi durun bakayım!', 'emotion': 'Çocukları yakalama'},
            {'id': 4, 'characterId': 'husnu', 'startTime': 7.6, 'endTime': 10.0, 'text': 'Abi seni bir dahaki bölüm yakalarız, hadi selametle!', 'emotion': 'Dizi göndermesi'},
            {'id': 5, 'characterId': 'husnu', 'startTime': 10.0, 'endTime': 11.0, 'text': 'Bay bay!', 'emotion': 'El sallama'},
            {'id': 6, 'characterId': 'husnu', 'startTime': 11.0, 'endTime': 14.14, 'text': 'Arka Sokaklar\'dan ben Komiser Hüsnü!', 'emotion': 'Rap introsu'},
            {'id': 7, 'characterId': 'husnu', 'startTime': 14.14, 'endTime': 16.5, 'text': 'Light Selami görse kabarır göğsü!', 'emotion': 'Efsane dize'},
            {'id': 8, 'characterId': 'husnu', 'startTime': 16.5, 'endTime': 20.0, 'text': 'Rıza Baba takımı toplar, devriye gezer!', 'emotion': 'Ritimli akış'},
            {'id': 9, 'characterId': 'husnu', 'startTime': 20.0, 'endTime': 28.5, 'text': 'Arka Sokak polisleri suçluları ezer!', 'emotion': 'Kapanış nakaratı'}
        ]
    },

    # 11. Meme - Bunlar Çok Semizlenmişler (Yeğen & Dayı Diyaloğu)
    'meme-e176a8d6ddafcd38': {
        'title': 'Viral - Bunlar Çok Semizlenmişler Yeğen & Dayı',
        'characters': [
            {'id': 'yegen', 'name': 'Yeğen', 'color': '#3b82f6', 'avatar': '🧢'},
            {'id': 'dayi', 'name': 'Sinirli Dayı', 'color': '#ef4444', 'avatar': '👴'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'yegen', 'startTime': 0.53, 'endTime': 2.87, 'text': 'İşin kötüsü dayı, bunlar çok semizlenmişler.', 'emotion': 'Haber getiren yeğen'},
            {'id': 2, 'characterId': 'yegen', 'startTime': 3.07, 'endTime': 5.0, 'text': 'Bizi yakalarlarsa fena yapacaklarmış!', 'emotion': 'Korkuyla fısıldama'},
            {'id': 3, 'characterId': 'dayi', 'startTime': 5.13, 'endTime': 7.55, 'text': 'Nasıl konuşuyorsun lan sen?! Yavşak!', 'emotion': 'Tepesi atan dayı'},
            {'id': 4, 'characterId': 'yegen', 'startTime': 7.55, 'endTime': 10.0, 'text': 'Yok dayı öyle değil, yanlış anladın ya!', 'emotion': 'Geri vites'},
            {'id': 5, 'characterId': 'yegen', 'startTime': 10.0, 'endTime': 13.5, 'text': 'Bizi bulurlarsa sıkıştıracaklarmış, o anlamda söyledim!', 'emotion': 'Açıklama çabası'},
            {'id': 6, 'characterId': 'dayi', 'startTime': 15.0, 'endTime': 18.5, 'text': 'He dayı öyle, her yerde konuşurlarmış arkamızdan!', 'emotion': 'Alaycı taklit'},
            {'id': 7, 'characterId': 'dayi', 'startTime': 18.5, 'endTime': 22.0, 'text': 'Hâlâ he dayı diyor ya! Yavşağa bak!', 'emotion': 'Kızgınlık'},
            {'id': 8, 'characterId': 'yegen', 'startTime': 22.0, 'endTime': 25.0, 'text': 'Beni dinlemeyecekseniz sormayın o zaman!', 'emotion': 'Gider yapan yeğen'},
            {'id': 9, 'characterId': 'dayi', 'startTime': 25.0, 'endTime': 29.5, 'text': 'Cahilsiniz oğlum siz, cahilsiniz! Yürüyün gidin şuradan!', 'emotion': 'Kovan dayı'}
        ]
    }
}

updated_count = 0
for scene in scenes:
    sid = scene.get('id')
    if sid in REVISIONS:
        rev = REVISIONS[sid]
        for key, val in rev.items():
            scene[key] = val
        updated_count += 1

print(f"Toplam {updated_count} sahne revize edildi.")

# scenes.json güncelle
with open(SCENES_JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("data/scenes.json güncellendi.")

# js/scenes.js güncelle
scenes_js_content = f"// Dublaj Oyunu - Sahne Veritabanı (Rol İzolasyonu ve Çoklu Karakter Kürasyonlu)\nexport const SCENES = {json.dumps(scenes, ensure_ascii=False, indent=2)};\n\nexport default SCENES;\n"
with open(SCENES_JS, 'w', encoding='utf-8') as f:
    f.write(scenes_js_content)
print("js/scenes.js güncellendi.")
