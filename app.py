from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/buscar', methods=['GET'])
def buscar_producto():
    nombre_producto = request.args.get('producto')
    if not nombre_producto:
        return jsonify({'error': 'Falta el parámetro "producto"'}), 400

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        url = f"https://tienda.mercadona.es/search-results/?query={nombre_producto}"
        driver.get(url)

        # Espera hasta que se carguen los productos (máximo 10s)
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

        driver.quit()

        if not productos:
            return jsonify({'mensaje': 'Producto no encontrado'}), 404

        producto_mas_barato = sorted(productos, key=lambda x: x["precio"])[0]
        return jsonify(producto_mas_barato)

    except Exception as e:
        driver.quit()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
