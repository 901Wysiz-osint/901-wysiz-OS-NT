#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 901 Wysız OSINT Tool
# Termux uyumlu, eğitim amaçlı OSINT aracı

import os
import sys
import time
import requests
import json

# ========================
# RENKLER
# ========================
class Renk:
    KIRMIZI = '\033[91m'
    YESIL = '\033[92m'
    SARI = '\033[93m'
    MAVI = '\033[94m'
    MOR = '\033[95m'
    TURKUAZ = '\033[96m'
    BEYAZ = '\033[97m'
    SIFIRLA = '\033[0m'

# ========================
# BANNER
# ========================
def banner():
    os.system('clear')
    print(Renk.TURKUAZ + """
    █████╗  ██████╗  ██╗    ██╗██╗   ██╗███████╗██╗███████╗
    ██╔══██╗██╔═████╗███║    ██║╚██╗ ██╔╝██╔════╝██║╚══███╔╝
    ███████║██║██╔██║╚██║    ██║ ╚████╔╝ ███████╗██║  ███╔╝ 
    ██╔══██║████╔╝██║ ██║    ██║  ╚██╔╝  ╚════██║██║ ███╔╝  
    ██║  ██║╚██████╔╝ ██║    ██║   ██║   ███████║██║███████╗
    ╚═╝  ╚═╝ ╚═════╝  ╚═╝    ╚═╝   ╚═╝   ╚══════╝╚═╝╚══════╝
    """ + Renk.SIFIRLA)
    print(Renk.YESIL + "              901 Wysız OSINT Tool" + Renk.SIFIRLA)
    print(Renk.SARI + "         [ Termux Uyumlu - Eğitim Amaçlı ]" + Renk.SIFIRLA)
    print(Renk.KIRMIZI + "     ============================================" + Renk.SIFIRLA)
    print()

# ========================
# MENÜ
# ========================
def menu():
    print(Renk.BEYAZ + "  [1] Telefon Numarası Sorgula" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [2] Kullanıcı Adı Sorgula" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [3] E-posta Adresi Sorgula" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [4] IP Adresi Sorgula" + Renk.SIFIRLA)
    print(Renk.BEYAZ + "  [5] Çıkış" + Renk.SIFIRLA)
    print()
    secim = input(Renk.YESIL + "  Seçiminiz (1-5): " + Renk.SIFIRLA)
    return secim

# ========================
# 1. TELEFON NUMARASI SORGULA
# ========================
def telefon_sorgula():
    print(Renk.SARI + "\n  [!] Telefon numarası sorgulama (uluslararası format: +905551112233)" + Renk.SIFIRLA)
    numara = input(Renk.YESIL + "  Numara: " + Renk.SIFIRLA)
    print(Renk.MAVI + f"\n  [*] {numara} sorgulanıyor..." + Renk.SIFIRLA)
    
    # Numara doğrulama
    if not numara.startswith('+'):
        print(Renk.KIRMIZI + "  [X] Numara + ile başlamalıdır!" + Renk.SIFIRLA)
        return
    
    # Basit format kontrolü
    temiz = numara.replace('+', '').replace(' ', '').replace('-', '')
    if not temiz.isdigit():
        print(Renk.KIRMIZI + "  [X] Geçersiz numara formatı!" + Renk.SIFIRLA)
        return
    
    print(Renk.YESIL + f"  [+] Numara formatı geçerli: {numara}" + Renk.SIFIRLA)
    print(Renk.SARI + "  [i] Detaylı sorgulama için harici API gerekir." + Renk.SIFIRLA)
    print(Renk.BEYAZ + f"  [i] Numara: {numara}" + Renk.SIFIRLA)
    print(Renk.BEYAZ + f"  [i] Ülke kodu: +{temiz[:2]}" + Renk.SIFIRLA)
    print(Renk.BEYAZ + f"  [i] Numara: {temiz[2:]}" + Renk.SIFIRLA)

# ========================
# 2. KULLANICI ADI SORGULA
# ========================
def kullanici_adi_sorgula():
    print(Renk.SARI + "\n  [!] Kullanıcı adı sorgulama (Telegram, TikTok, Instagram vb.)" + Renk.SIFIRLA)
    kullanici = input(Renk.YESIL + "  Kullanıcı adı (@ olmadan): " + Renk.SIFIRLA)
    kullanici = kullanici.replace('@', '')
    
    print(Renk.MAVI + f"\n  [*] {kullanici} sorgulanıyor..." + Renk.SIFIRLA)
    
    platformlar = [
        {"isim": "Telegram", "url": f"https://t.me/{kullanici}"},
        {"isim": "TikTok", "url": f"https://www.tiktok.com/@{kullanici}"},
        {"isim": "Instagram", "url": f"https://www.instagram.com/{kullanici}"},
        {"isim": "Twitter/X", "url": f"https://x.com/{kullanici}"},
        {"isim": "GitHub", "url": f"https://github.com/{kullanici}"},
        {"isim": "Reddit", "url": f"https://www.reddit.com/user/{kullanici}"},
    ]
    
    for p in platformlar:
        try:
            r = requests.get(p["url"], timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                print(Renk.YESIL + f"  [+] {p['isim']}: BULUNDU → {p['url']}" + Renk.SIFIRLA)
            else:
                print(Renk.KIRMIZI + f"  [-] {p['isim']}: Bulunamadı ({r.status_code})" + Renk.SIFIRLA)
        except:
            print(Renk.KIRMIZI + f"  [-] {p['isim']}: Bağlantı hatası" + Renk.SIFIRLA)
        time.sleep(0.5)

# ========================
# 3. E-POSTA SORGULA
# ========================
def eposta_sorgula():
    print(Renk.SARI + "\n  [!] E-posta adresi sorgulama" + Renk.SIFIRLA)
    eposta = input(Renk.YESIL + "  E-posta: " + Renk.SIFIRLA)
    
    if '@' not in eposta:
        print(Renk.KIRMIZI + "  [X] Geçersiz e-posta formatı!" + Renk.SIFIRLA)
        return
    
    print(Renk.MAVI + f"\n  [*] {eposta} sorgulanıyor..." + Renk.SIFIRLA)
    
    # Basit format kontrolü
    kullanici, domain = eposta.split('@')
    print(Renk.YESIL + f"  [+] Kullanıcı adı: {kullanici}" + Renk.SIFIRLA)
    print(Renk.YESIL + f"  [+] Domain: {domain}" + Renk.SIFIRLA)
    print(Renk.SARI + "  [i] Veri ihlali kontrolü için haveibeenpwned.com kullanın." + Renk.SIFIRLA)
    print(Renk.BEYAZ + f"  [i] Kontrol linki: https://haveibeenpwned.com/account/{eposta}" + Renk.SIFIRLA)

# ========================
# 4. IP ADRESİ SORGULA
# ========================
def ip_sorgula():
    print(Renk.SARI + "\n  [!] IP adresi sorgulama" + Renk.SIFIRLA)
    ip = input(Renk.YESIL + "  IP adresi (boş bırakırsan kendi IP'n): " + Renk.SIFIRLA)
    
    if not ip:
        ip = ""
        print(Renk.MAVI + "\n  [*] Kendi IP adresin sorgulanıyor..." + Renk.SIFIRLA)
    else:
        print(Renk.MAVI + f"\n  [*] {ip} sorgulanıyor..." + Renk.SIFIRLA)
    
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = r.json()
        
        if data.get("status") == "success":
            print(Renk.YESIL + f"  [+] IP: {data.get('query')}" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] Ülke: {data.get('country')} ({data.get('countryCode')})" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] Bölge: {data.get('regionName')}" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] Şehir: {data.get('city')}" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] ISP: {data.get('isp')}" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] Organizasyon: {data.get('org')}" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] Konum: {data.get('lat')}, {data.get('lon')}" + Renk.SIFIRLA)
            print(Renk.YESIL + f"  [+] Zaman Dilimi: {data.get('timezone')}" + Renk.SIFIRLA)
        else:
            print(Renk.KIRMIZI + "  [X] IP sorgulanamadı!" + Renk.SIFIRLA)
    except Exception as e:
        print(Renk.KIRMIZI + f"  [X] Hata: {e}" + Renk.SIFIRLA)

# ========================
# ANA DÖNGÜ
# ========================
def main():
    while True:
        banner()
        secim = menu()
        
        if secim == '1':
            telefon_sorgula()
        elif secim == '2':
            kullanici_adi_sorgula()
        elif secim == '3':
            eposta_sorgula()
        elif secim == '4':
            ip_sorgula()
        elif secim == '5':
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
