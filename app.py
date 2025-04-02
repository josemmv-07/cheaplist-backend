from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os

app = Flask(__name__)

@app.route('/buscar', methods=['GET'])
def buscar_producto():
    nombre_producto = request.args.get('producto')
    if not nombre_producto:
        return jsonify({'error': 'Falta el parámetro "producto"'}), 400

    print("🔧 Preparando Selenium...")
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")

    try:
        service = Service("/usr/bin/chromedriver")
        print("🚀 Lanzando navegador...")
        driver = webdriver.Chrome(service=service, options=options)

        url = f"https://tienda.mercadona.es/search-results/?query={nombre_producto}"
        print(f"🌐 Abriendo URL: {url}")
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-cell"))
        )
        print("✅ Página cargada correctamente")

        productos_divs = driver.find_elements(By.CLASS_NAME, "product-cell")
        productos = []

        for div in productos_divs:
            try:
                nombre = div.find_element(By.CLASS_NAME, "product-cell__description-name").text
                precio_texto = div.find_element(By.CLASS_NAME, "product-price__unit-price").text
                precio = float(precio_texto.replace("€", "").replace(",", ".").strip())
                print(f"🛒 Producto encontrado: {nombre} - {precio}€")
                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "supermercado": "Mercadona"
                })
            except Exception as e:
                print(f"❌ Error en un producto: {e}")
                continue

        if not productos:
            print("⚠️ No se encontraron productos.")
            return jsonify({'mensaje': 'Producto no encontrado'}), 404

        producto_mas_barato = sorted(productos, key=lambda x: x["precio"])[0]
        print(f"💸 Producto más barato: {producto_mas_barato}")
        return jsonify(producto_mas_barato)

    except Exception as e:
        print(f"🔥 Error durante el scraping: {str(e)}")
        return jsonify({'error': str(e)}), 500

    finally:
        print("🧹 Cerrando navegador...")
        try:
            driver.quit()
        except:
            pass

@app.route('/')
def index():
    return jsonify({"mensaje": "Bienvenido a la API de CheapList!"})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))
    app.run(debug=True, host='0.0.0.0', port=port)
