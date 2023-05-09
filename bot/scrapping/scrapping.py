from selenium import webdriver
import bot.scrapping.constants as const
from bs4 import BeautifulSoup
import requests
import os
import time


class FlipcartBoat(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH, teardown=False, openwindow=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ["PATH"] += self.driver_path
        op = webdriver.ChromeOptions()
        op.add_argument("headless")
        os.environ["PATH"] += self.driver_path
        if openwindow:
            print("inside the if block of init")
            super(FlipcartBoat, self).__init__()
        else:
            super(FlipcartBoat, self).__init__(options=op)

        self.implicitly_wait(40)
        self.maximize_window()

    def __exit__(self, *args) -> None:
        if self.teardown:
            self.quit()

    def land_on_first_page(self):
        self.get(const.FLIPCART_URL)

    def remove_popup(self):
        button = self.find_element_by_css_selector(
            "button[class = '_2KpZ6l _2doB4z']")
        button.click()

    def flipkart_login(self, email, password):
        self.find_element_by_css_selector(
            "#container > div > div._1kfTjk > div._1rH5Jn > div._2Xfa2_ > div.go_DOp._2errNR > div > div > div > a"
        ).click()
        email_input = self.find_element_by_css_selector(
            "body > div._2Sn47c > div > div > div > div > div._36HLxm.col.col-3-5 > div > form > div:nth-child(1) > input"
        )
        email_input.clear()
        email_input.send_keys(email)

        password_input = self.find_element_by_css_selector(
            "body > div._2Sn47c > div > div > div > div > div._36HLxm.col.col-3-5 > div > form > div:nth-child(2) > input"
        )
        password_input.clear()
        password_input.send_keys(password)
        time.sleep(5)
        password_input.send_keys("\ue007")
        time.sleep(5)

    def search_products(self, search_string):
        input_field = self.find_element_by_css_selector(
            "input[placeholder = 'Search for products, brands and more']"
        )
        input_field.send_keys(search_string)
        input_field.send_keys("\ue007")

    def get_product(self, text):
        element = self.find_element_by_partial_link_text(text)
        element.click()
        time.sleep(100)

    def find_all_products(self, new_string):
        product_list = []
        new_string = new_string.replace(" ", "%20")
        URL = f"https://www.flipkart.com/search?q={new_string}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        print("the flipkart url is", URL)
        html_data = requests.get(URL)
        data = html_data.text
        soup = BeautifulSoup(data, "html.parser")

        product_list_data = soup.find_all("div", {"class": "_13oc-S"})
        print(len(product_list_data))

        product_index = 0
        for product in product_list_data:

            product_heading = None
            if product.find("div", {"class": "_4rR01T"}):
                product_heading = product.find(
                    "div", {"class": "_4rR01T"}).text

            product_ratting = None
            if product.find("div", {"class": "_3LWZlK"}):
                product_ratting = product.find(
                    "div", {"class": "_3LWZlK"}).text

            text = None
            if product.find("span", {"class": "_2_R_DZ"}):
                text = ""
                if product.find("span", {"class": "_2_R_DZ"}):
                    product_user_review_text = product.find(
                        "span", {"class": "_2_R_DZ"}
                    )
                    if product_user_review_text.find("span"):
                        for span in product_user_review_text.find("span").find_all(
                            "span"
                        ):
                            text += span.text

            details_list = None
            if product.find("div", {"class": "fMghEO"}):
                product_details = product.find("div", {"class": "fMghEO"}).find_all(
                    "li"
                )
                details_list = []
                for detail_text in product_details:
                    details_list.append(detail_text.text)

            price_of_product = None
            if product.find("div", {"class", "_30jeq3 _1_WHN1"}):
                price_of_product = product.find(
                    "div", {"class", "_30jeq3 _1_WHN1"}
                ).text

            if product.find("div", {"class": "_3I9_wc _27UcVY"}):
                original_price = product.find(
                    "div", {"class": "_3I9_wc _27UcVY"}).text
            else:
                original_price = None

            discount_percentage = None
            if product.find("div", {"class": "_3Ay6Sb"}):
                discount_percentage = product.find(
                    "div", {"class": "_3Ay6Sb"}).text

            product_url = "#"
            if product.find("a", {"class": "_1fQZEK"}):
                product_url = f"https://www.flipkart.com{product.find('a', {'class': '_1fQZEK'}).get('href')}"

            if product_url == "#":
                if product.find("a", {"class": "s1Q9rs"}):
                    product_url = product.find(
                        "a", {"class": "s1Q9rs"}).get("href")
                    product_url = f"https://www.flipkart.com{product_url}"
                    if product_heading == None:
                        product_heading = product.find(
                            "a", {"class": "s1Q9rs"}).text

            product_image = "#"
            if product.find("div", {"class": "CXW8mj"}):
                product_image = (
                    product.find("div", {"class": "CXW8mj"}).find(
                        "img").get("src")
                )

            product_list.append(
                {
                    "product_index": product_index,
                    "product_image": product_image,
                    "product_heading": product_heading,
                    "product_ratting": product_ratting,
                    "user_review_text": text,
                    "price_of_product": price_of_product,
                    "original_price": original_price,
                    "discount_percentage": discount_percentage,
                    "product_description": details_list,
                    "product_url": product_url,
                }
            )
            product_index += 1
        print("done with flipkart")
        return product_list


# AMAZON SCRAPPING


class AmazonBot(webdriver.Chrome):
    def __init__(self, driver_path=const.DRIVER_PATH, teardown=False, openwindow=False):
        self.driver_path = driver_path
        self.teardown = teardown
        self.recursion_count = 1
        os.environ["PATH"] += self.driver_path
        op = webdriver.ChromeOptions()
        op.add_argument("headless")
        if openwindow:
            print("inside the if block of init")
            super(AmazonBot, self).__init__()
        else:
            super(AmazonBot, self).__init__(options=op)

        self.implicitly_wait(40)
        self.maximize_window()

    def land_on_first_page(self):
        self.get(const.AMAZON_URL)

    def set_currency(self, currency):
        currency_button = self.find_element_by_css_selector(
            'span[class="icp-nav-flag icp-nav-flag-us"]'
        )
        currency_button.click()

        currency_dropdown = self.find_element_by_css_selector(
            'span[id="a-autoid-0-announce"]'
        )
        currency_dropdown.click()

        clicking_curr = self.find_element_by_css_selector(
            'a[id="icp-sc-dropdown_2"]')
        clicking_curr.click()
        save_button = self.find_element_by_css_selector(
            'input[aria-labelledby="icp-btn-save-announce"]'
        )
        save_button.click()

    def amazon_login(self, email, password):
        self.find_element_by_css_selector(
            "#nav-link-accountList-nav-line-1").click()
        email_input = self.find_element_by_id("ap_email")
        email_input.clear()
        email_input.send_keys(email)
        email_input.send_keys("\ue007")

        password_input = self.find_element_by_id("ap_password")
        password_input.clear()
        password_input.send_keys(password)
        password_input.send_keys("\ue007")
        time.sleep(4)

    def search_product(self, search_string):
        input_box = self.find_element_by_css_selector("#twotabsearchtextbox")
        input_box.clear()
        input_box.send_keys(search_string)
        input_box.send_keys("\ue007")

    def get_product(self, text):
        element = self.find_element_by_partial_link_text(text)
        element.click()
        time.sleep(1000)

    def find_all_products(self, search_string):

        search_string = search_string.replace(" ", "+")
        URL = f"https://www.amazon.com/s?k={search_string}&crid=2GFL0I0G28G6M&sprefix=redme+mobiles%2Caps%2C487&ref=nb_sb_noss"
        print("the amazon url is", URL)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip",
            "DNT": "1",
            "Connection": "close",
        }

        product_list = []
        data = requests.get(URL, headers=headers, params={"wait": 2})
        text_data = data.text
        soup = BeautifulSoup(text_data, "html.parser")

        product_list_data = soup.find_all(
            "div",
            {
                "class": "s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t2 puis-include-content-margin puis s-latency-cf-section s-card-border"
            },
        )
        # s-card-container s-overflow-hidden aok-relative puis-wide-grid-style puis-wide-grid-style-t2 puis-include-content-margin puis s-latency-cf-section s-card-border
        # s-card-container s-overflow-hidden s-include-content-margin s-latency-cf-section s-card-border
        # s-include-content-margin s-latency-cf-section s-border-bottom s-border-top
        if len(product_list_data) == 0:
            print(len(product_list_data))
            if self.recursion_count == 8:
                return product_list
            self.recursion_count += 1
            return self.find_all_products(search_string)
        else:
            print("The legth of the amazon products is", len(product_list_data))
            product_index = 100
            for product in product_list_data:

                product_image = None
                if product.find(
                    "div", {"class": "a-section aok-relative s-image-fixed-height"}
                ):
                    product_image = (
                        product.find(
                            "div",
                            {"class": "a-section aok-relative s-image-fixed-height"},
                        )
                        .find("img")
                        .get("src")
                    )

                product_link = None
                if product.find(
                    "a", {"class": "a-link-normal s-link-style a-text-normal"}
                ):
                    product_link = product.find(
                        "a", {"class": "a-link-normal s-link-style a-text-normal"}
                    ).get("href")
                    product_link = f"https://www.amazon.com{product_link}"

                product_description = None
                if product.find(
                    "span", {"class": "a-size-medium a-color-base a-text-normal"}
                ):
                    product_description = product.find(
                        "span", {
                            "class": "a-size-medium a-color-base a-text-normal"}
                    ).text
                    product_description = product_description.strip()

                total_review = None
                if product.find("span", {"class": "a-size-base"}):
                    total_review = product.find(
                        "span", {"class": "a-size-base"}).text

                product_price = None
                if product.find("span", {"class": "a-price-whole"}):
                    whole = product.find(
                        "span", {"class": "a-price-whole"}).text
                    product_price = whole
                if product.find("span", {"class": "a-price-fraction"}):
                    fraction = product.find(
                        "span", {"class": "a-price-fraction"}).text
                    product_price = f"{product_price}{fraction}"

                ratting = None
                if product.find(
                    "i",
                    {
                        "class": "a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom"
                    },
                ):
                    ratting = (
                        product.find(
                            "i",
                            {
                                "class": "a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom"
                            },
                        )
                        .find("span")
                        .text
                    )

                product_list.append(
                    {
                        "product_index": product_index,
                        "product_image": product_image,
                        "product_link": product_link,
                        "product_description": product_description,
                        "ratting": ratting,
                        "total_review": total_review,
                        "product_price": product_price,
                    }
                )
                product_index += 1
            return product_list

    def find_all_an(self, search_string):
        search_string = search_string.replace(" ", "+")
        URL = f"https://www.amazon.com/s?k={search_string}&crid=2GFL0I0G28G6M&sprefix=redme+mobiles%2Caps%2C487&ref=nb_sb_noss"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip",
            "DNT": "1",
            "Connection": "close",
        }

        print(URL)

        product_list = []
        data = requests.get(URL, headers=headers, params={"wait": 2})
        text_data = data.text
        soup = BeautifulSoup(text_data, "html.parser")

        product_box = soup.find_all(
            "div",
            {
                "class": "s-expand-height s-include-content-margin s-latency-cf-section s-border-bottom s-border-top"
            },
        )

        if len(product_box) > 0:
            product_index = 100
            for product in product_box:
                product_image = None
                if product.find("img", {"class": "s-image"}):
                    product_image = product.find(
                        "img", {"class": "s-image"}).get("src")
                product_desc = None
                if product.find(
                    "span", {
                        "class", "a-size-base-plus a-color-base a-text-normal"}
                ):
                    product_desc = product.find(
                        "span", {
                            "class", "a-size-base-plus a-color-base a-text-normal"}
                    ).text
                ratting = None
                if product.find(
                    "i",
                    {
                        "class": "a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom"
                    },
                ):
                    ratting = (
                        product.find(
                            "i",
                            {
                                "class": "a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom"
                            },
                        )
                        .find("span")
                        .text
                    )
                product_link = None
                if product.find(
                    "a", {"class": "a-link-normal s-link-style a-text-normal"}
                ):
                    product_link = product.find(
                        "a", {"class": "a-link-normal s-link-style a-text-normal"}
                    ).get("href")
                    product_link = f"https://www.amazon.com{product_link}"
                total_review = None
                if product.find("span", {"class": "a-size-base"}):
                    total_review = product.find(
                        "span", {"class": "a-size-base"}).text
                product_price = None
                if product.find("span", {"class": "a-price-whole"}):
                    whole = product.find(
                        "span", {"class": "a-price-whole"}).text
                    product_price = whole
                if product.find("span", {"class": "a-price-fraction"}):
                    fraction = product.find(
                        "span", {"class": "a-price-fraction"}).text
                    product_price = f"{product_price}{fraction}"

                product_list.append(
                    {
                        "product_index": product_index,
                        "product_image": product_image,
                        "product_link": product_link,
                        "product_description": product_desc,
                        "ratting": ratting,
                        "total_review": total_review,
                        "product_price": product_price,
                    }
                )

                product_index += 1
            return product_list

        else:
            return product_list
