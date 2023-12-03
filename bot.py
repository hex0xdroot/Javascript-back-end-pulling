import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import requests
from bs4 import BeautifulSoup
import jsbeautifier

def access_js_files():
    url = entry_url.get()
    
    js_files = get_js_files(url)
    
    if js_files:
        text_output.delete(1.0, tk.END)  # Mevcut içeriği temizle
        for index, (js_file, content) in enumerate(js_files.items(), start=1):
            formatted_js = format_js(content)  # JavaScript kodunu düzenle
            text_output.insert(tk.END, f"JavaScript Dosyası {index}:\n")
            text_output.insert(tk.END, f"{formatted_js}\n\n")

def format_js(js_code):
    # JavaScript kodunu düzenle
    return jsbeautifier.beautify(js_code)

def get_js_files(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return {f'Erişim başarısız: {response.status_code} {response.reason}': ''}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        js_files = {}
        for script in soup.find_all('script', src=True):
            js_url = script['src']
            if not js_url.startswith(('http://', 'https://')):
                # URL, http veya https ile başlamıyorsa, başına web sitesinin URL'sini ekleyin
                js_url = url + js_url
            js_response = requests.get(js_url)
            if js_response.status_code == 200:
                js_content = js_response.text
                js_files[js_url] = js_content
        
        return js_files
    
    except requests.exceptions.RequestException as e:
        return {f'Hata: {e}': ''}

def create_gui():
    # Ana pencereyi oluştur
    root = tk.Tk()
    root.title("JavaScript Dosyalarının İçeriğine Erişim")

    # Pencere boyutunu ayarla
    root.geometry("800x600")  # Boyutu daha büyük yap

    # Etiket
    label_url = ttk.Label(root, text="Web sitesinin URL'sini girin:")
    label_url.pack(pady=10)

    # URL giriş kutusu
    global entry_url
    entry_url = ttk.Entry(root, width=60)
    entry_url.pack(pady=5)

    # Buton
    button_access = ttk.Button(root, text="JavaScript Dosyalarının İçeriğine Eriş", command=access_js_files)
    button_access.pack(pady=10)

    # Metin çıktı alanı
    global text_output
    text_output = scrolledtext.ScrolledText(root, height=20, width=80)  # Kaydırma çubuğu eklenmiş metin çıktısı
    text_output.pack()

    # Ana döngüyü başlat
    root.mainloop()

if __name__ == "__main__":
    create_gui()
