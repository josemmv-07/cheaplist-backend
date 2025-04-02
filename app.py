from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import subprocess

app = Flask(__name__)

# 🛠️ Instalar Google Chrome en tiempo real si no está
def setup_google_chrome():
    chrome_path = "/usr/bin/google-chrome"  # Ruta ajustada a la correcta en tu sistema
    if not os.path.exists(chrome_path):
        print("Instalando Google Chrome en tiempo de ejecución...")
        subprocess.run([
            "wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
        ])
        subprocess.run([
            "dpkg", "-i", "google-chrome-stable_current_amd64.deb"
        ])
        subprocess.run([
            "apt-get", "-fy", "install"
        ])
        subprocess.run(["rm", "-f", "google-chrome-stable_current_amd64.deb"])
    else:
        print(f"Google Chrome ya está instalado en {chrome_path}")

@app.route('/buscar', methods=['GET'])
def buscar_producto():
    nombre_producto = request.args.get('producto')
    if not nombre_producto:
        return jsonify({'error': 'Falta el parámetro "producto"'}), 400

    # 👇 Instala Google Chrome si hace falta
    setup_google_chrome()

    options = Options()
    options.binary_location = "/usr/bin/google-chrome"  # Aseguramos que Chrome esté en esta ruta
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = f"https://tienda.mercadona.es/search-results/?query={nombre_producto}"
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-cell"))
        )

        productos_divs = driver.find_elements(By.CLASS_NAME, "product-cell")
        productos = []

        for div in productos_divs:
            try:
                nombre = div.find_element(By.CLASS_NAME, "product-cell__description-name").text
                precio_texto = div.find_element(By.CLASS_NAME, "product-price__unit-price").text
                precio = float(precio_texto.replace("€", "").replace(",", ".").strip())
                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "supermercado": "Mercadona"
                })
            except Exception:
                continue

        if not productos:
            return jsonify({'mensaje': 'Producto no encontrado'}), 404

        producto_mas_barato = sorted(productos, key=lambda x: x["precio"])[0]
        return jsonify(producto_mas_barato)

    except Exception as e:
        print(f"Error durante el scraping: {str(e)}")
        return jsonify({'error': str(e)}), 500

    finally:
        driver.quit()

@app.route('/')
def index():
    return jsonify({"mensaje": "Bienvenido a la API de CheapList!"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(debug=True, host='0.0.0.0', port=port)
