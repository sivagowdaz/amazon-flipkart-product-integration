from bot.scrapping.scrapping import FlipcartBoat, AmazonBot
import time
import concurrent.futures

def flipkart_function(search_string):
    bot = FlipcartBoat()
    products = bot.find_all_products(search_string)
    return products

def amazon_function(search_string):
    bot = AmazonBot()
    products = bot.find_all_products(search_string)
    if len(products) == 0:
        products=bot.find_all_an(search_string)
    return products

def call_thread(search_string):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = executor.submit(amazon_function, search_string)
        t2 = executor.submit(flipkart_function, search_string)

    return t1.result(), t2.result()


def login_to_amazon(email, password, search_string, match_text):
    bot2 = AmazonBot(openwindow=True)
    bot2.land_on_first_page()
    bot2.set_currency('currency')
    bot2.amazon_login(email, password)
    bot2.search_product(search_string)
    bot2.get_product(match_text)

def login_to_flipkart(email, password, search_string, match_text):
    print("the match string is ", match_text)
    bot1 = FlipcartBoat(openwindow=True)
    bot1.land_on_first_page()
    bot1.remove_popup()
    bot1.flipkart_login(email, password)
    bot1.search_products(search_string)
    bot1.get_product(match_text)


