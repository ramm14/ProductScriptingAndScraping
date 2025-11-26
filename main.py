from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

# This works for scraping electronics only
def search_buffer():
    time.sleep(3)


def write_into_file(product):
    if os.path.exists("products.json") and os.path.getsize("products.json") > 0:
        with open("products.json", "r") as j_file:
            data = json.load(j_file)
    else:
        data = []

    data.append(product)
    with open("products.json","w") as f:
        json.dump(data, f, indent=4)


def find_image_url(product_name):
    name_of_product = product_name
    driver.get(f"https://www.gettyimages.com/search/2/image-film?phrase={name_of_product}")
    search_buffer()
    source_tag = driver.find_element(By.TAG_NAME , value="source")
    return str(source_tag.get_attribute("srcset"))


def scrape_product(product_name):
    try:
        driver.get("https://www.amazon.com/")
        search_buffer()
        continue_button = driver.find_element(By.CLASS_NAME, value="a-button-text")
        if continue_button:
            continue_button.click()
        else:
            pass
        searchbar = driver.find_element(By.ID, value="twotabsearchtextbox")
        print("found")
        searchbar.click()
        searchbar.send_keys(product_name)
        search_buffer()
        search_submit_btn = driver.find_element(By.ID, value="nav-search-submit-button")
        search_submit_btn.click()
        search_buffer()
        first_product = driver.find_elements(By.CLASS_NAME, value="a-link-normal")[1]
        first_product.click()
        search_buffer()
        product_title = driver.find_element(By.ID, value="productTitle")
        product_price = driver.find_element(By.CLASS_NAME, value="a-price-whole")
        product_description = driver.find_elements(By.CSS_SELECTOR, value="#feature-bullets span")[1]
        print(product_title.text, "X", product_price.text, "X", product_description.text)
        return {"title": product_title.text, "price": int(product_price.text), "description": product_description.text ,"image_url" : find_image_url(product_name)}
    except:
        print("Something went wrong....")


def main():
    chosen_product = input("Enter an electronic product: ")
    product = scrape_product(chosen_product)
    write_into_file(product)
    print("Complete !")


if __name__ == '__main__':
    main()








