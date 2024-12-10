import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.text import Text
from pathlib import Path
import time

console = Console()

# تحديد مسارات ملفات البروكسيات
proxies_file = Path("adi1.txt")  # ملف حفظ البروكسيات
working_proxies_file = Path("NASR-PAPERO.txt")  # ملف حفظ البروكسيات القوية جداً

# قائمة لتخزين البروكسيات مع نوعها
proxies = []

def fetch_proxies_from_url(url, proxy_type):
    """
    وظيفة لجلب البروكسيات من URL وإضافة نوع البروكسي.
    """
    try:
        response = requests.get(url)
        return [(proxy, proxy_type) for proxy in response.text.splitlines()]
    except Exception as e:
        console.print(f"⚠️ خطأ في جلب البروكسيات من {url}: {e}", style="red")
        return []

def check_proxy(proxy, proxy_type):
    """
    دالة لفحص البروكسي وحفظه مباشرة إذا كان سريعًا وقويًا جدًا.
    """
    try:
        start_time = time.time()  # تسجيل وقت البدء
        response = requests.get("http://httpbin.org/ip", proxies={proxy_type: proxy}, timeout=3)
        response_time = time.time() - start_time  # حساب زمن الاستجابة

        if response.status_code == 200 and response_time < 1:  # معيار السرعة والقوة العالية
            # إذا كان البروكسي قوي جدًا وسريع، نحفظه مباشرة في ملف البروكسيات القوية
            with working_proxies_file.open('a') as f:
                f.write(f"{proxy}\n")  # حفظ البروكسي بدون تعليقات
            console.print(Text(f"✅ {proxy} يعمل - نوع: {proxy_type} - قوة: قوي جدًا - السرعة: {response_time:.2f} ثانية", style="green"))
            return proxy, "قوي جدًا", proxy_type
    except Exception:
        return proxy, "ضعيف", proxy_type
    return proxy, "غير صالح", proxy_type

def main():
    global proxies
    urls = [
        ("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", "http"),
        ("https://raw.githubusercontent.com/prxchk/proxy-list/main/http.txt", "http"),
        ("https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/http_proxies.txt", "http"),
        ("https://raw.githubusercontent.com/Anonym0usWork1221/Free-Proxies/main/proxy_files/https_proxies.txt", "https"),
        ("https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt", "https"),
        ("https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/https/https.txt", "https"),
        ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks4.txt", "socks4"),
        ("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt", "socks4"),
        ("https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/socks5.txt", "socks5"),
        ("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt", "socks5"),
        ("https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt", "socks5"),
        ("https://raw.githubusercontent.com/zevtyardt/proxy-list/main/socks5.txt", "socks5"),
        ("https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt", "socks5"),
    ]

    # سحب البروكسيات
    for url, proxy_type in urls:
        fetched_proxies = fetch_proxies_from_url(url, proxy_type)
        proxies.extend(fetched_proxies)

    console.print(f"[bold cyan]🌐 عدد البروكسيات التي تم سحبها: {len(proxies)}[/bold cyan]")

    # إزالة التكرارات
    proxies = list(set(proxies))
    console.print(f"[bold cyan]🔄 عدد البروكسيات بعد إزالة التكرارات: {len(proxies)}[/bold cyan]")
    
    if not proxies:
        console.print("⚠️ [bold red]لم يتم العثور على بروكسيات.[/bold red]", style="red")
        return

    # حفظ البروكسيات في ملف adi1.txt
    with proxies_file.open('w') as f:
        for proxy, proxy_type in proxies:
            f.write(f"{proxy} ({proxy_type})\n")
    
    console.print(f"[bold blue]📂 تم حفظ البروكسيات في ملف {proxies_file}[/bold blue]")

    console.print("[bold green]🔍 سيتم فحص البروكسيات الآن وحفظ النتائج في ملف adi2.txt...[/bold green]")
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_proxy, proxy, proxy_type): (proxy, proxy_type) for proxy, proxy_type in proxies}
        
        for future in as_completed(futures):
            proxy, proxy_type = futures[future]
            try:
                proxy, strength, proxy_type = future.result()
                if strength != "قوي جدًا":
                    continue  # تجاهل البروكسيات الضعيفة أو غير الصالحة
            except Exception as e:
                console.print(Text(f"⚠️ خطأ في الفحص: {proxy}", style="yellow"))

    console.print(f"[bold blue]📂 تم حفظ جميع البروكسيات القوية والسريعة جدًا في ملف {working_proxies_file}[/bold blue]")

main()
