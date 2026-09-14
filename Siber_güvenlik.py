#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 901|Wysiz Siber Güvenlik Araç Seti
# Eğitim amaçlıdır. Sadece kendi sistemlerinizde kullanın.

import os
import sys
import time
import hashlib
import socket
import json
import base64
import random
import string
import subprocess

class Renk:
    KIRMIZI = '\033[91m'
    YESIL = '\033[92m'
    SARI = '\033[93m'
    MAVI = '\033[94m'
    MOR = '\033[95m'
    TURKUAZ = '\033[96m'
    BEYAZ = '\033[97m'
    SIFIRLA = '\033[0m'

def banner():
    os.system('clear')
    print(Renk.TURKUAZ + """
    ╔══════════════════════════════════════════════════╗
    ║     901|Wysiz SİBER GÜVENLİK ARAÇ SETİ          ║
    ║        [ Eğitim Amaçlı - Kendi Sisteminizde ]    ║
    ╚══════════════════════════════════════════════════╝
    """ + Renk.SIFIRLA)
    print(Renk.SARI + "  Yapımcı: 901|Wysiz" + Renk.SIFIRLA)
    print()

def menu():
    print(Renk.BEYAZ + "  [1]  Port Tarayıcı (Kendi IP'nde)" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [2]  Şifre Güç Testi" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [3]  Dosya Hash Hesaplayıcı" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [4]  Rastgele Şifre Üretici" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [5]  Metin Şifreleyici (Base64)" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [6]  Metin Şifre Çözücü (Base64)" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [7]  Site Güvenlik Tarayıcısı" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [8]  IP Adresi Sorgulayıcı" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [9]  Log Analiz Aracı" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [10] Güvenlik Kontrol Listesi" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [11] Çıkış" + Renk.SIFIRLA)
    print()
    return input(Renk.YESIL + "  Seçiminiz (1-11): " + Renk.SIFIRLA)

# ========================
# 1. PORT TARAYICI
# ========================
def port_tarayici():
    print(Renk.SARI + "\n  [!] Port Tarayıcı - Sadece kendi IP'nizde kullanın!" + Renk.SIFIRLA)
    hedef = input(Renk.YESIL + "  Hedef IP (boş = kendi IP'n): " + Renk.SIFIRLA)
    if not hedef:
        hedef = "127.0.0.1"
    
    try:
        baslangic = int(input(Renk.SARI + "  Başlangıç portu (1): " + Renk.SIFIRLA) or "1")
        bitis = int(input(Renk.SARI + "  Bitiş portu (1024): " + Renk.SIFIRLA) or "1024")
    except:
        baslangic, bitis = 1, 1024
    
    print(Renk.MAVI + f"\n  [*] {hedef} taranıyor ({baslangic}-{bitis})..." + Renk.SIFIRLA)
    acik = []
    
    for port in range(baslangic, bitis + 1):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            if s.connect_ex((hedef, port)) == 0:
                acik.append(port)
                print(Renk.YESIL + f"  [+] Port {port} AÇIK" + Renk.SIFIRLA)
            s.close()
        except:
            pass
    
    if not acik:
        print(Renk.KIRMIZI + "  [-] Açık port bulunamadı." + Renk.SIFIRLA)
    else:
        print(Renk.YESIL + f"\n  [+] Toplam {len(acik)} açık port bulundu: {acik}" + Renk.SIFIRLA)

# ========================
# 2. ŞİFRE GÜÇ TESTİ
# ========================
def sifre_testi():
    print(Renk.SARI + "\n  [!] Şifre Güç Testi" + Renk.SIFIRLA)
    sifre = input(Renk.YESIL + "  Test edilecek şifre: " + Renk.SIFIRLA)
    
    if not sifre:
        print(Renk.KIRMIZI + "  [X] Şifre boş olamaz!" + Renk.SIFIRLA)
        return
    
    import re
    import math
    
    uzunluk = len(sifre)
    kucuk = len(re.findall(r'[a-z]', sifre))
    buyuk = len(re.findall(r'[A-Z]', sifre))
    rakam = len(re.findall(r'[0-9]', sifre))
    ozel = len(re.findall(r'[^a-zA-Z0-9]', sifre))
    
    havuz = 0
    if kucuk: havuz += 26
    if buyuk: havuz += 26
    if rakam: havuz += 10
    if ozel: havuz += 33
    
    entropi = uzunluk * math.log2(havuz) if havuz > 0 else 0
    
    puan = min(uzunluk * 4, 40) + min(kucuk, 10) + min(buyuk * 2, 15) + min(rakam * 2, 15) + min(ozel * 3, 20)
    puan = min(puan, 100)
    
    if puan < 30:
        seviye = Renk.KIRMIZI + "ÇOK ZAYIF" + Renk.SIFIRLA
    elif puan < 50:
        seviye = Renk.SARI + "ZAYIF" + Renk.SIFIRLA
    elif puan < 70:
        seviye = Renk.MAVI + "ORTA" + Renk.SIFIRLA
    elif puan < 90:
        seviye = Renk.YESIL + "GÜÇLÜ" + Renk.SIFIRLA
    else:
        seviye = Renk.MOR + "ÇOK GÜÇLÜ" + Renk.SIFIRLA
    
    print(f"\n  Uzunluk: {uzunluk}")
    print(f"  Küçük harf: {kucuk}, Büyük harf: {buyuk}, Rakam: {rakam}, Özel: {ozel}")
    print(f"  Entropi: {entropi:.1f} bit")
    bar = "█" * int(puan / 5) + "░" * (20 - int(puan / 5))
    print(f"  Güç: [{bar}] %{puan}")
    print(f"  Seviye: {seviye}")

# ========================
# 3. DOSYA HASH
# ========================
def dosya_hash():
    print(Renk.SARI + "\n  [!] Dosya Hash Hesaplayıcı" + Renk.SIFIRLA)
    dosya = input(Renk.YESIL + "  Dosya yolu: " + Renk.SIFIRLA)
    
    if not os.path.exists(dosya):
        print(Renk.KIRMIZI + "  [X] Dosya bulunamadı!" + Renk.SIFIRLA)
        return
    
    with open(dosya, 'rb') as f:
        data = f.read()
    
    print(Renk.YESIL + f"\n  MD5:    {hashlib.md5(data).hexdigest()}" + Renk.SIFIRLA)
    print(Renk.YESIL + f"  SHA1:   {hashlib.sha1(data).hexdigest()}" + Renk.SIFIRLA)
    print(Renk.YESIL + f"  SHA256: {hashlib.sha256(data).hexdigest()}" + Renk.SIFIRLA)

# ========================
# 4. RASTGELE ŞİFRE
# ========================
def sifre_uret():
    print(Renk.SARI + "\n  [!] Rastgele Şifre Üretici" + Renk.SIFIRLA)
    try:
        uzunluk = int(input(Renk.YESIL + "  Şifre uzunluğu (16): " + Renk.SIFIRLA) or "16")
    except:
        uzunluk = 16
    
    karakterler = string.ascii_letters + string.digits + "!@#$%^&*"
    sifre = ''.join(random.choice(karakterler) for _ in range(uzunluk))
    print(Renk.YESIL + f"\n  [+] Üretilen şifre: {sifre}" + Renk.SIFIRLA)

# ========================
# 5. METİN ŞİFRELE (Base64)
# ========================
def metin_sifrele():
    print(Renk.SARI + "\n  [!] Metin Şifreleyici (Base64)" + Renk.SIFIRLA)
    metin = input(Renk.YESIL + "  Şifrelenecek metin: " + Renk.SIFIRLA)
    sifreli = base64.b64encode(metin.encode()).decode()
    print(Renk.YESIL + f"\n  [+] Şifrelenmiş: {sifreli}" + Renk.SIFIRLA)

# ========================
# 6. METİN ÇÖZ (Base64)
# ========================
def metin_coz():
    print(Renk.SARI + "\n  [!] Metin Şifre Çözücü (Base64)" + Renk.SIFIRLA)
    sifreli = input(Renk.YESIL + "  Çözülecek metin: " + Renk.SIFIRLA)
    try:
        cozulmus = base64.b64decode(sifreli.encode()).decode()
        print(Renk.YESIL + f"\n  [+] Çözülmüş: {cozulmus}" + Renk.SIFIRLA)
    except:
        print(Renk.KIRMIZI + "  [X] Geçersiz Base64!" + Renk.SIFIRLA)

# ========================
# 7. SİTE GÜVENLİK TARAYICI
# ========================
def site_tara():
    print(Renk.SARI + "\n  [!] Site Güvenlik Tarayıcısı" + Renk.SIFIRLA)
    site = input(Renk.YESIL + "  Site URL (https://...): " + Renk.SIFIRLA)
    
    try:
        import requests
        r = requests.get(site, timeout=10)
        print(Renk.YESIL + f"\n  [+] Durum Kodu: {r.status_code}" + Renk.SIFIRLA)
        
        guvenlik_basliklari = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy"
        ]
        
        print(Renk.MAVI + "\n  [*] Güvenlik Başlıkları:" + Renk.SIFIRLA)
        for baslik in guvenlik_basliklari:
            if baslik in r.headers:
                print(Renk.YESIL + f"  [+] {baslik}: VAR" + Renk.SIFIRLA)
            else:
                print(Renk.KIRMIZI + f"  [-] {baslik}: YOK" + Renk.SIFIRLA)
    except Exception as e:
        print(Renk.KIRMIZI + f"  [X] Hata: {e}" + Renk.SIFIRLA)

# ========================
# 8. IP SORGULA
# ========================
def ip_sorgula():
    print(Renk.SARI + "\n  [!] IP Adresi Sorgulayıcı" + Renk.SIFIRLA)
    ip = input(Renk.YESIL + "  IP adresi (boş = kendi IP'n): " + Renk.SIFIRLA)
    
    try:
        import requests
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = r.json()
        
        if data.get("status") == "success":
            print(Renk.YESIL + f"\n  [+] IP: {data.get('query')}" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] Ülke: {data.get('country')}" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] Şehir: {data.get('city')}" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] ISP: {data.get('isp')}" + Renk.SIFIRLA)
        else:
            print(Renk.KIRMIZI + "  [X] Sorgulanamadı!" + Renk.SIFIRLA)
    except Exception as e:
        print(Renk.KIRMIZI + f"  [X] Hata: {e}" + Renk.SIFIRLA)

# ========================
# 9. LOG ANALİZ
# ========================
def log_analiz():
    print(Renk.SARI + "\n  [!] Log Analiz Aracı" + Renk.SIFIRLA)
    dosya = input(Renk.YESIL + "  Log dosyası yolu: " + Renk.SIFIRLA)
    
    if not os.path.exists(dosya):
        print(Renk.KIRMIZI + "  [X] Dosya bulunamadı!" + Renk.SIFIRLA)
        return
    
    with open(dosya, 'r', errors='ignore') as f:
        satirlar = f.readlines()
    
    hatalar = [s for s in satirlar if "error" in s.lower() or "fail" in s.lower()]
    uyarilar = [s for s in satirlar if "warn" in s.lower()]
    
    print(Renk.YESIL + f"\n  [+] Toplam satır: {len(satirlar)}" + Renk.SIFIRLA)
    print(Renk.KIRMIZI + f"  [-] Hata satırı: {len(hatalar)}" + Renk.SIFIRLA)
    print(Renk.SARI + f"  [!] Uyarı satırı: {len(uyarilar)}" + Renk.SIFIRLA)
    
    if hatalar:
        print(Renk.KIRMIZI + "\n  [X] Son 5 hata:" + Renk.SIFIRLA)
        for h in hatalar[-5:]:
            print(f"    {h.strip()[:100]}")

# ========================
# 10. GÜVENLİK KONTROL LİSTESİ
# ========================
def kontrol_listesi():
    print(Renk.SARI + "\n  [!] Güvenlik Kontrol Listesi" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  Aşağıdaki maddeleri kontrol et:\n" + Renk.SIFIRLA)
    
    maddeler = [
        "Güçlü ve benzersiz şifreler kullanıyorum",
        "İki faktörlü kimlik doğrulama (2FA) açık",
        "İşletim sistemim güncel",
        "Antivirüs yazılımım var",
        "Şüpheli e-postalara tıklamıyorum",
        "Genel WiFi'de VPN kullanıyorum",
        "Önemli verilerimi yedekliyorum",
        "Gizlilik ayarlarımı kontrol ettim"
    ]
    
    puan = 0
    for i, madde in enumerate(maddeler, 1):
        cevap = input(Renk.YESIL + f"  {i}. {madde} (e/h): " + Renk.SIFIRLA)
        if cevap.lower() == 'e':
            puan += 1
    
    yuzde = (puan / len(maddeler)) * 100
    print(Renk.MAVI + f"\n  [*] Güvenlik Puanın: %{yuzde:.0f}" + Renk.SIFIRLA)
    
    if yuzde < 50:
        print(Renk.KIRMIZI + "  [!] Güvenlik seviyen düşük. Önlem almalısın!" + Renk.SIFIRLA)
    elif yuzde < 80:
        print(Renk.SARI + "  [!] Fena değil ama daha iyi olabilir." + Renk.SIFIRLA)
    else:
        print(Renk.YESIL + "  [+] Güvenlik seviyen yüksek. Tebrikler!" + Renk.SIFIRLA)

# ========================
# ANA DÖNGÜ
# ========================
def main():
    while True:
        banner()
        secim = menu()
        
        if secim == '1':
            port_tarayici()
        elif secim == '2':
            sifre_testi()
        elif secim == '3':
            dosya_hash()
        elif secim == '4':
            sifre_uret()
        elif secim == '5':
            metin_sifrele()
        elif secim == '6':
            metin_coz()
        elif secim == '7':
            site_tara()
        elif secim == '8':
            ip_sorgula()
        elif secim == '9':
            log_analiz()
        elif secim == '10':
            kontrol_listesi()
        elif secim == '11':
            print(Renk.YESIL + "\n  [i] Çıkış yapılıyor... Görüşürüz!" + Renk.SIFIRLA)
            sys.exit()
        else:
            print(Renk.KIRMIZI + "\n  [X] Geçersiz seçim!" + Renk.SIFIRLA)
        
        input(Renk.SARI + "\n  [i] Devam etmek için Enter'a bas..." + Renk.SIFIRLA)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Renk.KIRMIZI + "\n\n  [X] Program sonlandırıldı." + Renk.SIFIRLA)
        sys.exit()
