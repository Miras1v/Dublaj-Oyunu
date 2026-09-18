#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dublaj Oyunu - 3 Aşamalı Kapsamlı Karakter & Rol Tutarlılık Denetçisi
1. Kontrol: Karakter sayımı ve hiç konuşmayan 'hayali' karakterlerin tespiti.
2. Kontrol: 3 veya daha fazla karakterli sahnelerin incelenmesi (Tek/iki kişilik metinlerin yapay olarak 3'e bölünmesi).
3. Kontrol: Düzeltmelerin uygulanması ve test doğrulaması.
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

SCENES_JSON = 'data/scenes.json'

with open(SCENES_JSON, 'r', encoding='utf-8') as f:
    data = json.load(f)

scenes = data.get('scenes', [])

print("=================================================================")
print("2. AŞAMA (PASS 2): 3 ve Daha Fazla Karakterli Sahnelerin Analizi")
print("=================================================================")

multi_char_scenes = []

for idx, s in enumerate(scenes):
    chars = s.get('characters', [])
    lines = s.get('lines', [])
    
    if len(chars) >= 3:
        speaker_counts = {}
        for l in lines:
            cid = l.get('characterId')
            if cid and cid != 'None':
                speaker_counts[cid] = speaker_counts.get(cid, 0) + 1
        
        multi_char_scenes.append({
            'index': idx + 1,
            'id': s['id'],
            'title': s.get('title'),
            'char_count': len(chars),
            'chars': [(c['id'], c['name']) for c in chars],
            'speaker_counts': speaker_counts,
            'lines_count': len(lines)
        })

print(f"Toplam 3 veya daha fazla karakterli sahne sayısı: {len(multi_char_scenes)}\n")

for item in multi_char_scenes:
    print(f"[{item['index']:02d}] {item['id']} - {item['title']} (Karakter Sayısı: {item['char_count']}, Replik: {item['lines_count']})")
    print(f"    Karakterler ve Replik Sayıları: {item['speaker_counts']}")
    # 1 veya 2 replikli azınlık karakterler var mı?
    low_speakers = [cid for cid, count in item['speaker_counts'].items() if count <= 2]
    if low_speakers:
        print(f"    🔍 DİKKAT: Çok az replik alan karakterler (Yapay 3. kişi olabilir): {low_speakers}")
    print()
