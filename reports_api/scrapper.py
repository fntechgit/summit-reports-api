import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    chrome_options = Options()
    # Commented out headless mode to allow the browser to open
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    s = Service(r'C:\Webdrivers\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    return driver


def scrape_web(url):
    driver = setup_driver()
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # Scroll down the page to ensure lazy-loaded elements are triggered to load
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Wait to load page

    product_tiles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.js-product-tile')))

    products_data = []
    for product in product_tiles:
        name = product.find_element(By.CSS_SELECTOR, 'a.js-product-tile-link').text.strip()
        if not name:
            # If the product name is not found in the usual place, look elsewhere
            name = product.find_element(By.CSS_SELECTOR, '.product-tile .product-tile-content a').text.strip()

        price = product.find_element(By.CSS_SELECTOR, '.sales-price').text.strip()
        link = product.find_element(By.CSS_SELECTOR, 'a.js-product-tile-link').get_attribute('href')

        # Waiting for the image to be loaded
        WebDriverWait(product, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'img'))
        )
        image_element = product.find_element(By.CSS_SELECTOR, 'img')
        image_url = image_element.get_attribute('src')
        if not image_url or "data:image" in image_url:
            image_url = image_element.get_attribute('data-src')

        products_data.append((name, price, link, image_url))

    driver.quit()

    return products_data



def write_csv(web, data) :
    # Write the product data to a CSV file
    with open('products.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product Name', 'Price', 'URL', 'Image URL'])  # Header
        for product in data:
            writer.writerow(product)
            print(f'Product Name: {product[0]}, Price: {product[1]}, URL: {product[2]}, Image URL: {product[3]}')

    print("The CSV file has been saved.")

# Run the scraper
websites = [
'https://www.lacoste.com/ar/lacoste/hombre/indumentaria/remeras/',
'https://www.lacoste.com/ar/lacoste/hombre/indumentaria/remeras/'
]

products = []

for url in websites:
    products = products + scrape_web(url)

write_csv(products)