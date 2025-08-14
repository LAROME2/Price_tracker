import requests
from bs4 import BeautifulSoup
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
products_json = os.getenv("PRODUCTS")

try:
    products = json.loads(products_json) if products_json else []
except json.JSONDecodeError:
    print("❌ Error al leer PRODUCTS desde .env. Verifica el formato JSON.")
    products = []

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
}

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ No se encontró TELEGRAM_TOKEN o TELEGRAM_CHAT_ID en .env")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        r = requests.post(url, data=payload, timeout=5)
        if r.status_code == 200:
            print("✅ Mensaje enviado a Telegram")
            return True
        else:
            print(f"⚠️ Error enviando mensaje: {r.text}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Timeout enviando mensaje a Telegram")
        return False
    except Exception as e:
        print(f"❌ Excepción enviando mensaje: {e}")
        return False

def get_price(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        price_tag = soup.find("span", class_="a-offscreen")
        if not price_tag:
            print("⚠️ No se encontró el precio en la página")
            return None

        price_text = price_tag.get_text().strip().replace("$", "").replace(",", "")
        return float(price_text)
    except requests.exceptions.Timeout:
        print("❌ Timeout obteniendo precio")
        return None
    except Exception as e:
        print(f"Error obteniendo precio: {e}")
        return None

def main():
    for product in products:
        url = product.get("url")
        target = product.get("target_price")
        if not url or not target:
            print("⚠️ Producto con datos incompletos, se omite.")
            continue

        print(f"\nConsultando producto: {url}")
        price = get_price(url)
        if price is None:
            print("No se pudo obtener el precio.")
        else:
            print(f"Precio actual: ${price}")
            print(f"Precio objetivo: ${target}")
            if price <= target:
                mensaje = f"📉 🧨🧨🧨 ¡Precio bajo para {url}!\nPrecio actual: ${price}"
                send_telegram_message(mensaje)
            else:
                print("Precio aún alto, sin alertas.")
        
        print("Esperando 15 segundos para siguiente producto...")
        time.sleep(15)

if __name__ == "__main__":
    main()