import os
import re
import sys
import socket
import hashlib
import platform
import subprocess
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import quote, urlparse
import requests
import ipaddress
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
try:
    import dns.resolver
except ImportError:
    dns = None
try:
    import msvcrt
except ImportError:
    msvcrt = None
import os
import ctypes
def enable_ansi():
    if os.name == "nt":
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(
                kernel32.GetStdHandle(-11),
                7
            )
        except:
            pass
enable_ansi()
def set_console_size():
    if os.name != "nt":
        return
    os.system("mode con: cols=120 lines=38")
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            user32 = ctypes.windll.user32
            width = 1100
            height = 650
            screen_w = user32.GetSystemMetrics(0)
            screen_h = user32.GetSystemMetrics(1)
            x = max(0, (screen_w - width) // 2)
            y = max(0, (screen_h - height) // 2)
            user32.MoveWindow(
                hwnd,
                x,
                y,
                width,
                height,
                True
            )
    except Exception:
        pass
def gradient(text):
    colors = [
        (0, 80, 255),
        (0, 150, 255),
        (0, 220, 255),
        (0, 255, 200),
        (0, 255, 120)
    ]
    result = ""
    visible_chars = [c for c in text if c != "\n"]
    total = max(len(visible_chars), 1)
    position = 0
    for char in text:
        if char == "\n":
            result += "\n"
            continue
        ratio = position / max(total - 1, 1)
        scaled = ratio * (len(colors) - 1)
        index = min(int(scaled), len(colors) - 2)
        local = scaled - index
        r1, g1, b1 = colors[index]
        r2, g2, b2 = colors[index + 1]
        r = int(r1 + (r2 - r1) * local)
        g = int(g1 + (g2 - g1) * local)
        b = int(b1 + (b2 - b1) * local)
        result += f"\033[38;2;{r};{g};{b}m{char}"
        position += 1
    result += "\033[0m"
    return result
def clear():
    os.system("cls" if os.name == "nt" else "clear")
def safe_input(prompt=""):
    try:
        return input(prompt)
    except EOFError:
        return ""
def titre(text):
    line = "=" * 64
    print("\n" + gradient(line))
    print(gradient(f"{text:^64}"))
    print(gradient(line) + "\n")
def print_kv(key, value):
    if value is None or value == "":
        value = "N/A"
    print(f"{str(key):<20}: {value}")
def get_session():
    session = requests.Session()
    session.headers.update(HEADERS)
    return session
def normalize_username(username):
    username = (username or "").strip()
    if username.startswith("@"):
        username = username[1:]
    return username
def couleur_bleue():
    if os.name == "nt":
        os.system("color 09")
APP_NAME = "MULTI TOOLS BY YS"
VERSION = "3.0"
HEADERS = {
    "User-Agent": f"MultiTools-OSINT/{VERSION} (public-information checker)"
}
TIMEOUT = 8
MAX_WORKERS = 8
SITES = {
    "GitHub": "https://github.com/",
    "Reddit": "https://www.reddit.com/user/",
    "TikTok": "https://www.tiktok.com/@",
    "YouTube": "https://www.youtube.com/@",
    "Instagram": "https://www.instagram.com/",
    "X": "https://x.com/",
    "Twitch": "https://www.twitch.tv/",
    "Pinterest": "https://www.pinterest.com/",
    "SoundCloud": "https://soundcloud.com/",
    "DeviantArt": "https://www.deviantart.com/",
    "Steam": "https://steamcommunity.com/id/",
}
OSINT_SITES = [
    ("OSINT Framework", "https://osintframework.com/"),
    ("MultiSearch", "https://multisearch.to/"),
    ("BrixHub", "https://brixhub.to/"),
]
EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
)
def terminal_width():
    try:
        return max(80, shutil.get_terminal_size((100, 30)).columns)
    except Exception:
        return 100
ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
def center_text(text):
    width = terminal_width()
    lines = text.splitlines()
    centered = []
    for line in lines:
        if not line:
            centered.append("")
            continue
        visible = ANSI_RE.sub("", line)
        padding = max((width - len(visible)) // 2, 0)
        centered.append(" " * padding + line)
    return "\n".join(centered)
def banner():
    logo = r"""
███╗   ███╗██╗   ██╗██╗  ████████╗██╗
████╗ ████║██║   ██║██║  ╚══██╔══╝██║
██╔████╔██║██║   ██║██║     ██║   ██║
██║╚██╔╝██║██║   ██║██║     ██║   ██║
██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║
╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝
████████╗ ██████╗  ██████╗ ██╗     ███████╗
╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
   ██║   ██║   ██║██║   ██║██║     ███████╗
   ██║   ██║   ██║██║   ██║██║     ╚════██║
   ██║   ╚██████╔╝╚██████╔╝███████╗███████║
   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                         B Y   Y S
"""
    print(center_text(gradient(logo)))
    sep = "═" * min(76, terminal_width() - 4)
    print(center_text(gradient(sep)))
    print(center_text(gradient("MULTI TOOLS BY YS")))
    print(center_text(gradient("PUBLIC OSINT / NETWORK / SYSTEM TOOLS")))
    print(center_text(gradient(sep)))
    print()
def ip_lookup():
    ip = safe_input("\nEntre une IP : ")
    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        print("[!] Adresse IP invalide.")
        return
    titre("ANALYSE IP")
    print_kv("IP", address)
    print_kv("Version", f"IPv{address.version}")
    if address.is_loopback:
        print_kv("Type", "Loopback / machine locale")
        return
    if address.is_private:
        print_kv("Type", "IP privée")
        print("[i] Une IP privée n'est normalement pas géolocalisable par une API publique.")
        return
    if address.is_reserved:
        print_kv("Type", "IP réservée")
        return
    print_kv("Type", "IP publique")
    print("\n[*] Recherche sur ipwho.is...")
    try:
        response = requests.get(
            f"https://ipwho.is/{address}",
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        if not data.get("success", False):
            print(f"[!] API : {data.get('message', 'information indisponible')}")
            return
        connection = data.get("connection") or {}
        print("\n──────── LOCALISATION ────────")
        for name, value in [
            ("IP", data.get("ip")),
            ("Type", data.get("type")),
            ("Continent", data.get("continent")),
            ("Pays", data.get("country")),
            ("Code pays", data.get("country_code")),
            ("Région", data.get("region")),
            ("Ville", data.get("city")),
            ("Code postal", data.get("postal")),
            ("Latitude", data.get("latitude")),
            ("Longitude", data.get("longitude")),
        ]:
            print_kv(name, value)
        print("\n──────── CONNEXION ───────────")
        for name, value in [
            ("ASN", connection.get("asn")),
            ("Organisation", connection.get("org")),
            ("ISP", connection.get("isp")),
            ("Domaine", connection.get("domain")),
        ]:
            print_kv(name, value)
        print("\n[i] La géolocalisation IP reste approximative.")
    except requests.exceptions.Timeout:
        print("[!] Timeout de l'API.")
    except requests.exceptions.RequestException as exc:
        print(f"[!] Erreur réseau : {exc}")
    except ValueError:
        print("[!] Réponse API invalide.")
def check_username_site(session, name, base_url, username):
    url = base_url + quote(username, safe="")
    try:
        response = session.get(url, timeout=TIMEOUT, allow_redirects=True)
        status = response.status_code
        if status == 200:
            return name, "found", url
        if status == 404:
            return name, "not_found", url
        if status in (401, 403):
            return name, "blocked", url
        if status == 429:
            return name, "rate_limit", url
        return name, f"http_{status}", url
    except requests.exceptions.Timeout:
        return name, "timeout", url
    except requests.exceptions.ConnectionError:
        return name, "connection", url
    except requests.exceptions.RequestException:
        return name, "error", url
def username_checker():
    username = normalize_username(safe_input("\nEntre un pseudo : "))
    if not username:
        print("[!] Pseudo vide.")
        return
    if "/" in username or " " in username:
        print("[!] Entre uniquement le pseudo, sans URL.")
        return
    titre(f"CHECKER PSEUDO : @{username}")
    print("[*] Vérification des plateformes publiques...")
    print("[i] Un résultat 200 ne prouve pas que le compte appartient à la personne recherchée.\n")
    session = get_session()
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(check_username_site, session, name, base, username)
            for name, base in SITES.items()
        ]
        for future in as_completed(futures):
            results.append(future.result())
    order = {name: i for i, name in enumerate(SITES)}
    results.sort(key=lambda item: order[item[0]])
    counts = {"found": 0, "not_found": 0, "blocked": 0, "rate_limit": 0}
    for name, status, url in results:
        if status == "found":
            print(f"[+] {name:<14} → potentiellement trouvé")
            print(f"    {url}")
            counts["found"] += 1
        elif status == "not_found":
            print(f"[-] {name:<14} → non trouvé")
            counts["not_found"] += 1
        elif status == "blocked":
            print(f"[?] {name:<14} → accès bloqué")
            counts["blocked"] += 1
        elif status == "rate_limit":
            print(f"[!] {name:<14} → rate limit")
            counts["rate_limit"] += 1
        else:
            labels = {
                "timeout": "timeout",
                "connection": "connexion impossible",
                "error": "erreur réseau",
            }
            print(f"[?] {name:<14} → {labels.get(status, status)}")
    print("\n──────── RÉSUMÉ ─────────────")
    print(f"Potentiellement trouvés : {counts['found']}")
    print(f"Non trouvés             : {counts['not_found']}")
    print(f"Bloqués                 : {counts['blocked']}")
    print(f"Rate limit              : {counts['rate_limit']}")
def phone_number():
    number = safe_input("\nEntre un numéro de téléphone : ")
    if not number:
        print("[!] Numéro vide.")
        return
    region = None
    if not number.startswith("+"):
        region = safe_input("Code pays ISO (ex: FR, BE, CA, US) : ").upper()
        if not re.fullmatch(r"[A-Z]{2}", region):
            print("[!] Code pays ISO invalide.")
            return
    try:
        parsed = phonenumbers.parse(number, region)
        titre("PHONE NUMBER")
        international = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
        e164 = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.E164
        )
        types = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Ligne fixe",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixe ou mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Numéro gratuit",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PAGER: "Pager",
        }
        print_kv("International", international)
        print_kv("E.164", e164)
        print_kv("Pays/région", geocoder.description_for_number(parsed, "fr"))
        print_kv("Opérateur", carrier.name_for_number(parsed, "fr"))
        print_kv("Fuseau(x)", ", ".join(timezone.time_zones_for_number(parsed)))
        print_kv("Valide", "Oui" if phonenumbers.is_valid_number(parsed) else "Non")
        print_kv("Possible", "Oui" if phonenumbers.is_possible_number(parsed) else "Non")
        print_kv("Type", types.get(phonenumbers.number_type(parsed), "Autre / inconnu"))
    except phonenumbers.NumberParseException as exc:
        print(f"[!] Numéro impossible à analyser : {exc}")
def resolve_dns(domain):
    try:
        infos = socket.getaddrinfo(domain, 443, type=socket.SOCK_STREAM)
        return sorted({info[4][0] for info in infos})
    except socket.gaierror:
        return []
def email_analysis():
    email = safe_input("\nEntre une adresse email : ")
    if not EMAIL_REGEX.fullmatch(email):
        print("[!] Format email invalide.")
        return
    local_part, domain = email.rsplit("@", 1)
    domain = domain.lower()
    titre("ANALYSE EMAIL")
    print_kv("Email", email)
    print_kv("Utilisateur", local_part)
    print_kv("Domaine", domain)
    print("\n──────── DNS ─────────────────")
    addresses = resolve_dns(domain)
    if addresses:
        print("[+] Domaine résolvable")
        for address in addresses[:10]:
            print(f"    → {address}")
    else:
        print("[!] Aucune adresse DNS trouvée.")
    print("\n──────── MAIL / MX ───────────")
    if dns is None:
        print("[!] dnspython n'est pas installé.")
        return
    try:
        mx_records = dns.resolver.resolve(domain, "MX", lifetime=5)
        servers = sorted(str(record.exchange).rstrip(".") for record in mx_records)
        if servers:
            for server in servers:
                print(f"    → {server}")
        else:
            print("[!] Aucun MX trouvé.")
    except Exception as exc:
        print(f"[!] Impossible de récupérer les MX : {exc}")
    print("\n[i] Cet outil ne vérifie pas si la boîte mail existe réellement.")
def dns_lookup():
    domain = safe_input("\nDomaine ou nom d'hôte : ").strip().lower()
    if not domain:
        print("[!] Domaine vide.")
        return
    titre("DNS LOOKUP")
    records = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]
    if dns is None:
        print("[!] Installe dnspython avec : python -m pip install dnspython")
        return
    resolver = dns.resolver.Resolver()
    for record_type in records:
        print(f"\n── {record_type} ──")
        try:
            answers = resolver.resolve(domain, record_type, lifetime=5)
            for answer in answers:
                print(f"  {answer}")
        except Exception:
            print("  N/A")
def normalize_url(url):
    if not re.match(r"^https?://", url, re.I):
        return "https://" + url
    return url
def url_inspector():
    raw = safe_input("\nURL à analyser : ")
    url = normalize_url(raw)
    try:
        parsed = urlparse(url)
        if not parsed.hostname:
            print("[!] URL invalide.")
            return
    except ValueError:
        print("[!] URL invalide.")
        return
    titre("URL INSPECTOR")
    print_kv("Schéma", parsed.scheme)
    print_kv("Domaine", parsed.hostname)
    print_kv("Port", parsed.port or ("443" if parsed.scheme == "https" else "80"))
    print_kv("Chemin", parsed.path or "/")
    print_kv("Paramètres", parsed.query or "Aucun")
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        print("\n──────── HTTP ────────────────")
        print_kv("Status", response.status_code)
        print_kv("Final URL", response.url)
        print_kv("Serveur", response.headers.get("Server"))
        print_kv("Content-Type", response.headers.get("Content-Type"))
        print_kv("Taille", response.headers.get("Content-Length", "inconnue"))
        print_kv("Temps", f"{response.elapsed.total_seconds():.2f}s")
        print("\n──────── SÉCURITÉ ────────────")
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Referrer-Policy",
        ]
        for header in security_headers:
            print_kv(header, "présent" if header in response.headers else "absent")
    except requests.exceptions.RequestException as exc:
        print(f"[!] Requête impossible : {exc}")
def http_headers():
    raw = safe_input("\nURL : ")
    url = normalize_url(raw)
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True,
        )
        titre("HTTP HEADERS")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
    except requests.exceptions.RequestException as exc:
        print(f"[!] Erreur : {exc}")
def local_network_info():
    titre("RÉSEAU LOCAL")
    hostname = socket.gethostname()
    print_kv("Hostname", hostname)
    try:
        local_ip = socket.gethostbyname(hostname)
        print_kv("IPv4 locale", local_ip)
    except socket.gaierror:
        print_kv("IPv4 locale", "N/A")
    print_kv("Système", platform.system())
    print_kv("Version", platform.version())
    print_kv("Machine", platform.machine())
    print("\n[i] Cet outil affiche uniquement des informations locales basiques.")
def hash_file():
    path = safe_input("\nChemin du fichier : ").strip().strip('"')
    if not os.path.isfile(path):
        print("[!] Fichier introuvable.")
        return
    titre("FILE HASH")
    algorithms = {
        "MD5": hashlib.md5(),
        "SHA1": hashlib.sha1(),
        "SHA256": hashlib.sha256(),
        "SHA512": hashlib.sha512(),
    }
    try:
        with open(path, "rb") as file:
            while True:
                chunk = file.read(1024 * 1024)
                if not chunk:
                    break
                for algorithm in algorithms.values():
                    algorithm.update(chunk)
        print_kv("Fichier", os.path.basename(path))
        print_kv("Taille", f"{os.path.getsize(path):,} octets")
        for name, algorithm in algorithms.items():
            print(f"{name:<18}: {algorithm.hexdigest()}")
    except OSError as exc:
        print(f"[!] Impossible de lire le fichier : {exc}")
def ping_host():
    host = safe_input("\nHôte ou IP à tester : ")
    if not host:
        print("[!] Hôte vide.")
        return
    titre("PING")
    command = ["ping", "-n", "4", host] if os.name == "nt" else ["ping", "-c", "4", host]
    try:
        subprocess.run(command, check=False)
    except OSError as exc:
        print(f"[!] Impossible de lancer ping : {exc}")
def osint_sites():
    titre("SITES OSINT PUBLICS")
    for index, (name, url) in enumerate(OSINT_SITES, 1):
        print(f"{index}. {name}")
        print(f"   {url}")
    print("\n[i] Ouvre uniquement les services et ressources que tu connais.")
def email_test():
    titre("EMAIL TEST")
    recipient = safe_input("Adresse de test : ").strip()
    if not EMAIL_REGEX.match(recipient):
        print("[!] Adresse email invalide.")
        return
    subject = safe_input("Sujet : ").strip() or "Test Multi Tools BY YS"
    message = safe_input("Message : ").strip() or "Ceci est un test local."
    print("\n──────── APERÇU ────────")
    print_kv("À", recipient)
    print_kv("Sujet", subject)
    print_kv("Message", message)
    print("\n[i] Aucun email n'a été envoyé. Ce module sert uniquement à tester la saisie et l'aperçu.")
MENUS = [
    {
        "title": "OSINT",
        "items": [
            ("1", "IP Lookup", ip_lookup),
            ("2", "Pseudo Checker", username_checker),
            ("3", "Téléphone", phone_number),
            ("4", "Email / DNS / MX", email_analysis),
            ("5", "Sites OSINT", osint_sites),
            ("6", "Email Test (aperçu local)", email_test),
        ],
    },
    {
        "title": "NETWORK / WEB",
        "items": [
            ("1", "DNS Lookup", dns_lookup),
            ("2", "URL Inspector", url_inspector),
            ("3", "HTTP Headers", http_headers),
            ("4", "Ping Host", ping_host),
            ("5", "Réseau local", local_network_info),
        ],
    },
    {
        "title": "FILES / SYSTEM",
        "items": [
            ("1", "Hash File (MD5/SHA1/SHA256/SHA512)", hash_file),
            ("2", "Informations système", local_network_info),
        ],
    },
]
def show_menu(index):
    clear()
    banner()
    menu = MENUS[index]
    width = min(76, terminal_width() - 4)
    top = "╔" + "═" * width + "╗"
    mid = "╠" + "═" * width + "╣"
    bottom = "╚" + "═" * width + "╝"
    print(center_text(gradient(top)))
    print(center_text(gradient("║" + menu["title"].center(width) + "║")))
    print(center_text(gradient(mid)))
    for key, name, _ in menu["items"]:
        line = f"║  {key}. {name}"
        line += " " * max(0, width - len(line) - 1)
        line += "║"
        print(center_text(gradient(line)))
    print(center_text(gradient(mid)))
    controls = "║  N = menu suivant   B = menu précédent   Q = quitter"
    controls += " " * max(0, width - len(controls) - 1) + "║"
    print(center_text(gradient(controls)))
    print(center_text(gradient(bottom)))
    print(center_text(gradient(f"[ Menu {index + 1}/{len(MENUS)} ]")))
def wait_for_return():
    print("\n==============================================")
    print("[1] Retour au menu")
    print("[2] Quitter")
    print("==============================================")
    while True:
        choice = input("\nChoisis : ").strip().lower()
        if choice == "1":
            return "enter"
        elif choice == "2":
            return "quit"
        else:
            print("[!] Choix invalide.")
def menu():
    index = 0
    while True:
        show_menu(index)
        choice = input("\nChoisis : ").strip().lower()
        if choice == "n":
            index = (index + 1) % len(MENUS)
            continue
        if choice == "b":
            index = (index - 1) % len(MENUS)
            continue
        if choice == "q":
            break
        selected = None
        for key, name, action in MENUS[index]["items"]:
            if choice == key:
                selected = (name, action)
                break
        if selected is None:
            print("\n[!] Touche invalide.")
            input("Appuie sur Entrée...")
            continue
        name, action = selected
        clear()
        banner()
        titre(name)
        try:
            action()
        except KeyboardInterrupt:
            print("\n[!] Opération interrompue.")
        except Exception as exc:
            print(f"\n[!] Erreur inattendue : {exc}")
        result = wait_for_return()
        if result == "quit":
            break
    clear()
    print(f"\n[+] {APP_NAME} {VERSION} fermé.")
    print(
        f"[i] Session terminée : "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
if __name__ == "__main__":
    couleur_bleue()
    set_console_size()
    menu()
