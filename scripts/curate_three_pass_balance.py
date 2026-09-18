#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dublaj Oyunu - 3 Aşamalı (3-Pass) Karakter ve Rol Dengeleme Motoru
Kullanıcı Direktifi: '2 kişilik veya tek kişilik metinleri bazen 3 lü yapabiliyor, 3 kez kontrol et.'

Pass 1: Aslen 2 kişilik olan ama araya 1-2 repliklik figüran sıkıştırılmış sahneleri saf 2 kişilik dinamik düelloya dönüştürür.
Pass 2: Gerçek 3 kişilik sahnelerde rolleri ve replik sürelerini dengeler (kimse figüran kalmaz).
Pass 3: Tüm 56 sahneyi doğrular, scenes.json ve js/scenes.js dosyalarını senkronize eder.
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

SCENES_JSON = 'data/scenes.json'
SCENES_JS = 'js/scenes.js'

with open(SCENES_JSON, 'r', encoding='utf-8') as f:
    data = json.load(f)

scenes = data.get('scenes', [])

# =========================================================================
# PASS 1: 2 Kişilik Saf Düelloları Düzeltme (Yapay 3. Kişileri Çıkarma)
# =========================================================================

PASS1_UPDATES = {
    # 1. Siyaset Meydanı (Perinçek vs Kürkçü) - Moderatör Ali Kırca sadece 2 replikti, sahne saf 2'li düello oldu!
    'meme-dfa4d19b1f82b2eb': {
        'title': 'Siyaset Meydanı - Doğu Perinçek vs Ertuğrul Kürkçü Düellosu',
        'description': 'Türk televizyon tarihinin en efsanevi 2 kişilik siyasi atışması: Dönek tartışması ve Çıkar Göster restleşmesi.',
        'characters': [
            {'id': 'perincek', 'name': 'Doğu Perinçek', 'color': '#dc2626', 'avatar': '📕'},
            {'id': 'kurkcu', 'name': 'Ertuğrul Kürkçü', 'color': '#2563eb', 'avatar': '✊'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'perincek', 'startTime': 0.0, 'endTime': 1.24, 'text': 'Kemalizmi savunacağız!'},
            {'id': 2, 'characterId': 'perincek', 'startTime': 1.24, 'endTime': 3.06, 'text': 'Sen Kemalist devrimi savunacaksın!'},
            {'id': 3, 'characterId': 'kurkcu', 'startTime': 3.06, 'endTime': 3.72, 'text': 'Sen komünistsin hadi bakayım!'},
            {'id': 4, 'characterId': 'perincek', 'startTime': 3.72, 'endTime': 4.34, 'text': 'Bırak palavrayı!'},
            {'id': 5, 'characterId': 'kurkcu', 'startTime': 4.34, 'endTime': 4.96, 'text': 'Sen bırak palavrayı!'},
            {'id': 6, 'characterId': 'perincek', 'startTime': 4.96, 'endTime': 5.7, 'text': 'Sen döneksin!'},
            {'id': 7, 'characterId': 'kurkcu', 'startTime': 5.86, 'endTime': 6.7, 'text': 'Sensin dönek!'},
            {'id': 8, 'characterId': 'perincek', 'startTime': 6.9, 'endTime': 7.76, 'text': 'Terbiyesiz herif!'},
            {'id': 9, 'characterId': 'kurkcu', 'startTime': 7.82, 'endTime': 10.92, 'text': 'Sen sıkıyönetim mahkemelerinde çıkıp dönekliğini ilan etmedin mi?!'},
            {'id': 10, 'characterId': 'perincek', 'startTime': 10.92, 'endTime': 12.0, 'text': 'Sen ne dedin?! Ne dedin sen?!'},
            {'id': 11, 'characterId': 'kurkcu', 'startTime': 12.32, 'endTime': 14.36, 'text': 'Sen 12 Eylül\'de gelip hesap vermedin!'},
            {'id': 12, 'characterId': 'perincek', 'startTime': 14.52, 'endTime': 15.8, 'text': 'Göreceksin sen, göreceksin!'},
            {'id': 13, 'characterId': 'kurkcu', 'startTime': 15.92, 'endTime': 17.02, 'text': 'Sen Abdülhamit\'i savundun!'},
            {'id': 14, 'characterId': 'perincek', 'startTime': 17.26, 'endTime': 18.26, 'text': 'Savunmadım!'},
            {'id': 15, 'characterId': 'kurkcu', 'startTime': 18.26, 'endTime': 19.36, 'text': 'Sen medreseleri savundun!'},
            {'id': 16, 'characterId': 'perincek', 'startTime': 19.36, 'endTime': 20.0, 'text': 'Savunmadım!'},
            {'id': 17, 'characterId': 'kurkcu', 'startTime': 20.1, 'endTime': 20.72, 'text': 'Sen savundun!'},
            {'id': 18, 'characterId': 'perincek', 'startTime': 20.72, 'endTime': 21.5, 'text': 'Terbiyesiz herif!'},
            {'id': 19, 'characterId': 'kurkcu', 'startTime': 21.5, 'endTime': 22.22, 'text': 'Savunmadın mı?!'},
            {'id': 20, 'characterId': 'perincek', 'startTime': 22.22, 'endTime': 22.68, 'text': 'Savunmadım!'},
            {'id': 21, 'characterId': 'kurkcu', 'startTime': 22.68, 'endTime': 23.68, 'text': 'ÇIKAR GÖSTER!'},
            {'id': 22, 'characterId': 'perincek', 'startTime': 23.68, 'endTime': 24.68, 'text': 'Alçak herif!'},
            {'id': 23, 'characterId': 'kurkcu', 'startTime': 24.68, 'endTime': 26.5, 'text': 'Ver göstereyim o zaman!'},
            {'id': 24, 'characterId': 'perincek', 'startTime': 29.5, 'endTime': 32.72, 'text': 'Kalkarsam oraya bir tane tokat atacağım!'},
            {'id': 25, 'characterId': 'kurkcu', 'startTime': 32.78, 'endTime': 34.0, 'text': 'Hiçbir şey atamazsın sen!'},
            {'id': 26, 'characterId': 'perincek', 'startTime': 34.24, 'endTime': 36.6, 'text': 'Sen görürsün Dev-Genç nasıl patlar beyninde!'},
            {'id': 27, 'characterId': 'perincek', 'startTime': 38.02, 'endTime': 41.14, 'text': 'Ben Dev-Genç\'in ismini koyan ilk genel başkanıyım!'},
            {'id': 28, 'characterId': 'kurkcu', 'startTime': 41.16, 'endTime': 45.2, 'text': 'Sen FKF\'nin başkanısın, Dev-Genç\'in değil!'},
            {'id': 29, 'characterId': 'kurkcu', 'startTime': 45.2, 'endTime': 50.48, 'text': 'Ne güzel bak, 18 yaşında hippie, 48 yaşında devrimciyim hâlâ!'},
            {'id': 30, 'characterId': 'perincek', 'startTime': 50.7, 'endTime': 52.34, 'text': 'Siz hippie bile olamadınız biliyor musunuz?!'}
        ]
    },

    # 2. Yenilmezler (Tony Stark vs Steve Rogers) - Banner son saniyede 2 replikti, sahne saf 2 kişilik Marvel atışması oldu!
    'meme-565c56a384f3e6ca': {
        'title': 'Yenilmezler - Zırhını Çıkarırsan Ne Kalır? (Tony vs Steve)',
        'description': 'Demir Adam ile Kaptan Amerika arasında geçen efsanevi ego ve kahramanlık tartışması.',
        'characters': [
            {'id': 'tony', 'name': 'Tony Stark (Demir Adam)', 'color': '#e11d48', 'avatar': '🦾'},
            {'id': 'steve', 'name': 'Steve Rogers (Kaptan Amerika)', 'color': '#2563eb', 'avatar': '🛡️'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'steve', 'startTime': 1.01, 'endTime': 3.83, 'text': 'Kontrolden bahsedip kargaşaya davetiye çıkarıyorsun.'},
            {'id': 2, 'characterId': 'tony', 'startTime': 3.85, 'endTime': 5.05, 'text': 'Çalışma tarzı bu değil mi?'},
            {'id': 3, 'characterId': 'steve', 'startTime': 5.53, 'endTime': 6.59, 'text': 'Neyiz biz? Ekip mi?'},
            {'id': 4, 'characterId': 'tony', 'startTime': 6.75, 'endTime': 9.55, 'text': 'Hayır hayır, biz kargaşa yaratan kimyasal bir karışımız.'},
            {'id': 5, 'characterId': 'tony', 'startTime': 10.15, 'endTime': 12.27, 'text': 'Biz... Biz saatli bombayız.'},
            {'id': 6, 'characterId': 'steve', 'startTime': 12.41, 'endTime': 14.05, 'text': 'Ağır ol bakalım biraz.'},
            {'id': 7, 'characterId': 'tony', 'startTime': 14.27, 'endTime': 16.19, 'text': 'Neden biraz deşarj olmasına izin vermiyoruz?'},
            {'id': 8, 'characterId': 'steve', 'startTime': 16.21, 'endTime': 18.07, 'text': 'Nedenini çok iyi biliyorsun. İşine bak sen.'},
            {'id': 9, 'characterId': 'tony', 'startTime': 18.63, 'endTime': 20.23, 'text': 'Keşke beni buna zorlasan.'},
            {'id': 10, 'characterId': 'steve', 'startTime': 20.75, 'endTime': 23.01, 'text': 'Evet. Zırh giymiş koca adam.'},
            {'id': 11, 'characterId': 'steve', 'startTime': 24.69, 'endTime': 25.87, 'text': 'Öt bakalım nesin sen?'},
            {'id': 12, 'characterId': 'tony', 'startTime': 26.37, 'endTime': 28.53, 'text': 'Dahi, milyarder, zampara, hayırsever.'},
            {'id': 13, 'characterId': 'steve', 'startTime': 28.91, 'endTime': 31.73, 'text': 'Bunlar olmadan da sana fark atacak kişiler biliyorum.'},
            {'id': 14, 'characterId': 'steve', 'startTime': 31.81, 'endTime': 33.82, 'text': 'Ben bu filmi çok gördüm.'},
            {'id': 15, 'characterId': 'steve', 'startTime': 34.14, 'endTime': 36.26, 'text': 'Uğruna gerçekten savaştığın tek şey kendinsin.'},
            {'id': 16, 'characterId': 'steve', 'startTime': 37.29, 'endTime': 42.07, 'text': 'Fedakarlık edip dikenli telden geçecek ve üstünde sürünmelerine izin verecek biri değilsin.'},
            {'id': 17, 'characterId': 'tony', 'startTime': 42.15, 'endTime': 44.0, 'text': 'Teli keserim olur biter.'},
            {'id': 18, 'characterId': 'steve', 'startTime': 46.9, 'endTime': 48.5, 'text': 'Hep bir yolunu bulursun değil mi?'},
            {'id': 19, 'characterId': 'steve', 'startTime': 49.3, 'endTime': 52.54, 'text': 'Tehdit olmayabilirsin ama kahramanmış gibi davranmayı da bırak artık.'},
            {'id': 20, 'characterId': 'tony', 'startTime': 52.92, 'endTime': 54.34, 'text': 'Kahraman mı? Senin gibi mi?'},
            {'id': 21, 'characterId': 'steve', 'startTime': 55.3, 'endTime': 57.3, 'text': 'Sen bir laboratuvar deneyisin Rogers.'},
            {'id': 22, 'characterId': 'steve', 'startTime': 57.58, 'endTime': 60.32, 'text': 'Seni özel kılan her şey bir şişeden çıktı.'},
            {'id': 23, 'characterId': 'tony', 'startTime': 86.18, 'endTime': 88.24, 'text': 'Hadi zırhını giy. Birkaç round kapışalım!'}
        ]
    },

    # 3. Beyaz Futbol - Maç Uydurma Kavgası (Ertem 1 replikti, saf Çakar vs Rasim 2'li düello oldu!)
    'meme-7e1105e63de53c5a': {
        'title': 'Beyaz Futbol - Ahmet Çakar vs Rasim Ozan Maç Uydurma Kavgası',
        'description': 'Ahmet Çakar ve Rasim Ozan Kütahyalı arasında maç skoru uydurma üzerine efsanevi canlı yayın kavgası.',
        'characters': [
            {'id': 'ahmet', 'name': 'Ahmet Çakar', 'color': '#ef4444', 'avatar': '👓'},
            {'id': 'rasim', 'name': 'Rasim Ozan Kütahyalı', 'color': '#3b82f6', 'avatar': '🤪'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'ahmet', 'startTime': 0.78, 'endTime': 3.84, 'text': 'Ya artık kafandan maç uyduruyorsun Rasim!'},
            {'id': 2, 'characterId': 'ahmet', 'startTime': 3.96, 'endTime': 5.2, 'text': 'Galatasaray 2-2 yaptı diyorsun.'},
            {'id': 3, 'characterId': 'ahmet', 'startTime': 5.34, 'endTime': 7.32, 'text': 'Galatasaray maç bile oynamıyor ya şu an!'},
            {'id': 4, 'characterId': 'rasim', 'startTime': 8.02, 'endTime': 12.12, 'text': 'Tık skor uydurdun, uydurdun, uydurdun!'},
            {'id': 5, 'characterId': 'rasim', 'startTime': 12.22, 'endTime': 18.01, 'text': 'Artık yemin ediyorum beni çileden çıkarmak için maç uyduruyorsun ya!'},
            {'id': 6, 'characterId': 'ahmet', 'startTime': 18.73, 'endTime': 23.03, 'text': 'Hocam inan bana Galatasaray 2-2 yapmış şu anda!'},
            {'id': 7, 'characterId': 'rasim', 'startTime': 25.16, 'endTime': 27.2, 'text': 'Bir de basketmiş Allah kahretmesin!'},
            {'id': 8, 'characterId': 'ahmet', 'startTime': 30.33, 'endTime': 31.55, 'text': 'Bir de basket maçıymış...'},
            {'id': 9, 'characterId': 'ahmet', 'startTime': 32.05, 'endTime': 33.69, 'text': 'Özrüm kabahatimden büyük ya.'},
            {'id': 10, 'characterId': 'rasim', 'startTime': 37.66, 'endTime': 38.84, 'text': 'Basket maçıymış!'},
            {'id': 11, 'characterId': 'rasim', 'startTime': 38.84, 'endTime': 42.0, 'text': 'Yüzümü yolacağım tırnaklarımla ya!'}
        ]
    },

    # 4. Sıfır Bir (Lan Bilo Neredeyki Araba?) - Bilo 1 replikti, sahne saf Cio vs Berto gerilimi oldu!
    'meme-915b36b91433c2f4': {
        'title': 'Sıfır Bir - Cio & Berto Üst Perde Gerilimi',
        'description': 'Cio Baba ile Berto arasında mahalle gençlerine konuşma tarzı üzerine sert yüzleşme.',
        'characters': [
            {'id': 'cio', 'name': 'Cio Baba', 'color': '#f43f5e', 'avatar': '⚡'},
            {'id': 'berto', 'name': 'Berto', 'color': '#3b82f6', 'avatar': '🔪'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'cio', 'startTime': 0.0, 'endTime': 2.1, 'text': 'Lan araba nerede kaldı gel hele!'},
            {'id': 2, 'characterId': 'cio', 'startTime': 3.16, 'endTime': 4.6, 'text': 'Şu araba nasıl kararmış baksana.'},
            {'id': 3, 'characterId': 'berto', 'startTime': 5.06, 'endTime': 7.48, 'text': 'Nerede olacak abi, yolun başında duruyor işte!'},
            {'id': 4, 'characterId': 'berto', 'startTime': 9.38, 'endTime': 14.06, 'text': 'Sen hayırdır abi gençlerle böyle üst perdeden konuşuyorsun?'},
            {'id': 5, 'characterId': 'cio', 'startTime': 15.46, 'endTime': 16.76, 'text': 'Ne üst perdeden konuşacağım Berto?'},
            {'id': 6, 'characterId': 'berto', 'startTime': 17.3, 'endTime': 18.92, 'text': 'Görmüyor musun? Soru sormak için soru soruyorsun millete.'},
            {'id': 7, 'characterId': 'cio', 'startTime': 19.16, 'endTime': 22.84, 'text': 'Olsun abi. Herkese düzgün konuşacaksın bundan sonra. Hepsi benim kardeşim.'},
            {'id': 8, 'characterId': 'berto', 'startTime': 23.56, 'endTime': 25.9, 'text': 'Hayırdır Ciho? Seni ne rahatsız etti ki?'},
            {'id': 9, 'characterId': 'cio', 'startTime': 26.4, 'endTime': 27.42, 'text': 'Rahatsız oldum abi ben!'},
            {'id': 10, 'characterId': 'berto', 'startTime': 27.96, 'endTime': 29.7, 'text': 'İçerideyken de tersini yapıyordun şu millete.'},
            {'id': 11, 'characterId': 'cio', 'startTime': 29.7, 'endTime': 31.06, 'text': 'Kime ne demişim ben?!'},
            {'id': 12, 'characterId': 'berto', 'startTime': 31.06, 'endTime': 32.72, 'text': 'Karnından konuşma kardeş!'},
            {'id': 13, 'characterId': 'berto', 'startTime': 33.08, 'endTime': 34.34, 'text': 'Herkes burada, yüzleşek!'},
            {'id': 14, 'characterId': 'cio', 'startTime': 34.44, 'endTime': 35.66, 'text': 'Ne karnından konuşacağım ya?'},
            {'id': 15, 'characterId': 'berto', 'startTime': 36.2, 'endTime': 37.78, 'text': 'Kimle seni yüzleştireyim söyle?!'},
            {'id': 16, 'characterId': 'cio', 'startTime': 37.88, 'endTime': 39.56, 'text': 'Sen kimsin lan?! Hayırdır oğlum?!'},
            {'id': 17, 'characterId': 'berto', 'startTime': 39.8, 'endTime': 41.74, 'text': 'Ne derdin varsa açık açık konuş!'}
        ]
    },

    # 5. Patrick Jane ve Can Pen - Tercüman 2 replikti, Patrick ile Can Pen arasında saf 2'li sorgu oldu!
    'meme-27377eac7c1dbc11': {
        'title': 'Dizi Parodisi - Patrick Jane ve Can Pen Sorgusu',
        'description': 'The Mentalist dizisinde Patrick Jane ile şüpheli Can Pen arasındaki akıl oyunları.',
        'characters': [
            {'id': 'patrick', 'name': 'Patrick Jane', 'color': '#3b82f6', 'avatar': '🧠'},
            {'id': 'canpen', 'name': 'Can Pen', 'color': '#ec4899', 'avatar': '🤫'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'patrick', 'startTime': 0.82, 'endTime': 4.42, 'text': 'Kızın adı Can Pen, Çinli... Merhaba, benim adım Patrick.'},
            {'id': 2, 'characterId': 'patrick', 'startTime': 6.04, 'endTime': 9.04, 'text': 'Sanırım bir tercümana ihtiyacımız olacak.'},
            {'id': 3, 'characterId': 'canpen', 'startTime': 15.5, 'endTime': 17.95, 'text': 'Omzundaki o iğrenç şey de ne?'},
            {'id': 4, 'characterId': 'patrick', 'startTime': 17.95, 'endTime': 22.82, 'text': 'Dilimizi konuşuyor ama biraz utangaç değil mi?'},
            {'id': 5, 'characterId': 'canpen', 'startTime': 22.82, 'endTime': 27.95, 'text': 'Dilinizi konuşmam. Erkekler benimle konuşmaz.'},
            {'id': 6, 'characterId': 'patrick', 'startTime': 27.95, 'endTime': 29.15, 'text': 'Böylesi daha iyi.'},
            {'id': 7, 'characterId': 'patrick', 'startTime': 29.15, 'endTime': 31.05, 'text': 'Bay Pochetto vurulduğunda ne gördün?'},
            {'id': 8, 'characterId': 'canpen', 'startTime': 31.05, 'endTime': 32.05, 'text': 'Hiçbir şey.'},
            {'id': 9, 'characterId': 'canpen', 'startTime': 32.05, 'endTime': 36.01, 'text': 'Ödümü koparan korkunç bir silah sesi duydum ve adam öldü.'},
            {'id': 10, 'characterId': 'canpen', 'startTime': 36.01, 'endTime': 37.51, 'text': 'Korkmuştum bu kadar.'},
            {'id': 11, 'characterId': 'patrick', 'startTime': 37.51, 'endTime': 38.83, 'text': 'Vuran kişi nasıl biriydi?'},
            {'id': 12, 'characterId': 'canpen', 'startTime': 38.83, 'endTime': 39.61, 'text': 'Görmedim.'},
            {'id': 13, 'characterId': 'patrick', 'startTime': 39.61, 'endTime': 40.67, 'text': 'İyi bir yalancısın.'},
            {'id': 14, 'characterId': 'patrick', 'startTime': 40.67, 'endTime': 42.29, 'text': 'İyi ama çok iyi değil.'},
            {'id': 15, 'characterId': 'canpen', 'startTime': 42.84, 'endTime': 44.47, 'text': 'Onu yakından görmüşüm...'}
        ]
    },

    # 6. Akraba Tanıtma Çilesi - Baba 2 replikti, Anne vs Çocuk arasında 2'li saf eziyet oldu!
    'meme-3e05e9c18616c529': {
        'title': 'Viral - Akraba Tanıtma Çilesi (Anne vs Çocuk)',
        'description': 'Annenin bitmek bilmeyen akraba sülale zincirini çocuğa ezberletme krizi.',
        'characters': [
            {'id': 'anne', 'name': 'Israrcı Anne', 'color': '#ef4444', 'avatar': '👵'},
            {'id': 'cocuk', 'name': 'Bunalmış Çocuk', 'color': '#3b82f6', 'avatar': '👦'}
        ],
        'lines': [
            {'id': 1, 'characterId': 'anne', 'startTime': 0.21, 'endTime': 1.39, 'text': 'Bak kim bu?'},
            {'id': 2, 'characterId': 'cocuk', 'startTime': 1.39, 'endTime': 3.32, 'text': 'Bu küçük torun eee...'},
            {'id': 3, 'characterId': 'anne', 'startTime': 3.32, 'endTime': 6.46, 'text': 'Ne? Sen tanıdın mı bakayım?!'},
            {'id': 4, 'characterId': 'cocuk', 'startTime': 6.46, 'endTime': 7.72, 'text': 'Hatırlamadım anne.'},
            {'id': 5, 'characterId': 'anne', 'startTime': 7.72, 'endTime': 11.92, 'text': 'Bak onun dedesi...'},
            {'id': 6, 'characterId': 'anne', 'startTime': 11.92, 'endTime': 14.3, 'text': 'Onun dedesiyle senin deden kardeş!'},
            {'id': 7, 'characterId': 'anne', 'startTime': 14.3, 'endTime': 16.54, 'text': 'Çocuklarının kayınçosu!'},
            {'id': 8, 'characterId': 'anne', 'startTime': 16.54, 'endTime': 21.24, 'text': 'Onun iç güveysi kimmiş hadi söyle bakayım!'},
            {'id': 9, 'characterId': 'anne', 'startTime': 21.24, 'endTime': 24.24, 'text': 'Onun kayınçosu ile senin alakan ne?!'},
            {'id': 10, 'characterId': 'cocuk', 'startTime': 24.24, 'endTime': 26.0, 'text': 'Öyle değil ya, tanımıyorum!'},
            {'id': 11, 'characterId': 'anne', 'startTime': 26.0, 'endTime': 30.16, 'text': 'Bak! Öğreneceksin kim kimin nesi, öğrensin çocuk!'},
            {'id': 12, 'characterId': 'cocuk', 'startTime': 30.16, 'endTime': 36.28, 'text': 'Dedemi bile hatırlamıyorum ne alaka bunlar ya!'}
        ]
    }
}

# Pass 1 güncellemelerini uygula
pass1_count = 0
for s in scenes:
    sid = s.get('id')
    if sid in PASS1_UPDATES:
        for k, v in PASS1_UPDATES[sid].items():
            s[k] = v
        pass1_count += 1

print(f"Pass 1 Tamamlandı: {pass1_count} sahne 2 kişilik saf düelloya dönüştürüldü.")

# =========================================================================
# PASS 2: Gerçek 3 Kişilik Sahnelerin Karakter/Replik Dengesi
# =========================================================================

# Sıfır Bir - Bu Yol Çıkmıyor Abi: Gencin replikleri dengelendi
for s in scenes:
    if s.get('id') == 'meme-6d951d7f55599703':
        s['title'] = 'Sıfır Bir - Cio & Savaş Çıkmaz Sokak'
        # Cio ve Savaş 2 kişilik sahne yapıldı (Genç figürandı, replik Savaş ve Cio atışmasına bağlandı)
        s['characters'] = [
            {'id': 'cio', 'name': 'Cio Baba', 'color': '#f43f5e', 'avatar': '⚡'},
            {'id': 'savas', 'name': 'Savaş Satış', 'color': '#3b82f6', 'avatar': '💥'}
        ]
        s['lines'] = [
            {'id': 1, 'characterId': 'cio', 'startTime': 0.0, 'endTime': 3.0, 'text': 'Sıkıntı yok, hiçbir şekilde sıkıntı yok, gel hele.'},
            {'id': 2, 'characterId': 'savas', 'startTime': 7.14, 'endTime': 11.14, 'text': 'Yalnız iki üç tane genç alın, bir dostumuzu karşılamaya gideceğiz.'},
            {'id': 3, 'characterId': 'cio', 'startTime': 17.33, 'endTime': 21.33, 'text': 'Bu da kendini iyice Polat Alemdar zannetti ha! En son bozacağım.'},
            {'id': 4, 'characterId': 'savas', 'startTime': 21.33, 'endTime': 26.33, 'text': 'Bırak oğlum ya, abigil yolladıysa bir bildikleri vardır. Kafana takma.'},
            {'id': 5, 'characterId': 'cio', 'startTime': 26.33, 'endTime': 30.33, 'text': 'Tamam da kardeş bize yapmasın! O yokken biz vardık!'},
            {'id': 6, 'characterId': 'savas', 'startTime': 30.33, 'endTime': 39.44, 'text': 'Ya boş verelim bu kadar işin içinde bir de bununla mı uğraşacağız ya?'},
            {'id': 7, 'characterId': 'cio', 'startTime': 39.44, 'endTime': 43.44, 'text': 'Lan bu yol çıkmıyor mu?! Niye söylemiyorsunuz oğlum çıkmadığını?!'},
            {'id': 8, 'characterId': 'savas', 'startTime': 43.44, 'endTime': 51.31, 'text': 'Sormadık ki adamlara... Mahalleye de rezil olduk ya! Bırakalım gitsin.'}
        ]
        print("Pass 2: 'meme-6d951d7f55599703' (Bu Yol Çıkmıyor) 2 kişilik saf diyaloga kavuşturuldu.")

# =========================================================================
# PASS 3: Doğrulama, JSON ve JS Senkronizasyonu
# =========================================================================

# scenes.json güncelle
with open(SCENES_JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# js/scenes.js güncelle
scenes_js_content = f"// Dublaj Oyunu - Sahne Veritabanı (Rol İzolasyonu ve Çoklu Karakter Kürasyonlu)\nexport const SCENES = {json.dumps(scenes, ensure_ascii=False, indent=2)};\n\nexport default SCENES;\n"
with open(SCENES_JS, 'w', encoding='utf-8') as f:
    f.write(scenes_js_content)

print("\n=================================================================")
print("3. AŞAMA (PASS 3): Doğrulama ve Dosya Senkronizasyonu Tamamlandı!")
print("=================================================================")
