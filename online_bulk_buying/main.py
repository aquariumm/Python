from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

ITEMS = ["Xbox One S 1TB Console", "more stuff"] # need to follow how items are called on the website
SHOPPING_CART = "//span[@class='label']"
REMOVE_PANEL = "//div[@class='cart-items']"
REMOVE_BUTTON = "//div/a[contains(text(), 'Remove')]"
SEARCH_BAR = "//input[contains(@class, 'text')]"
ADD_TO_CART = "//span[contains(text(), 'Add to Cart')]"
CONT_CHECKOUT = "//section[contains(@class, 'basket-aside')]//div[contains(@class,'checkout')]" +\
                "/a/span/span[contains(text(), 'Continue to Checkout')]"
GUEST_XPATH = "//span[contains(text(),'Continue')]"
ITEMS_XPATH = dict(zip(ITEMS, [f"//*[text()[contains(., '{item}')]]" for item in ITEMS]))


def click_xpath(driver, xpath):
    """ Routine click work helper function.

    This function does two things:
        1. locate the element by given xpath
        2. click the located element
    
    Params:
        driver (str): selenium webdriver 
        xpath (str): xpath to locate the required element
    Return:
        bool: weather click() works
    """
    try:
        driver.find_element_by_xpath(xpath).click()
        time.sleep(5)
    except:
        raise 


def clear_cart(driver, xpath1, xpath2):
    """Clear existing items in shopping cart
    
    Params:
        driver (str): selenium webdriver
        xpath1 (str): xpath to the cart panel which holds all items
        xpath2 (str): xpath to individual item 
    """
    try:
        items_exist = driver.find_elements_by_xpath(xpath1)
    except:
        items_exist = False
    
    while items_exist:
        # click delete button to remove items in the cart one at a time
        click_xpath(driver, xpath2)
        try:
            items_exist = driver.find_elements_by_xpath(xpath1)
        except:
            items_exist = False


def add_item(driver, xpath, item):
    """
    Params:
        driver (str): selenium webdriver
        xpath (str): xpath to the search bar
        item (str): item to search in the search bar
    """
    search_box = driver.find_element_by_xpath(xpath)
    search_box.send_keys(item)
    search_box.submit()
    

if __name__ == "__main__":   
    with Chrome(executable_path='./chromedriver_win32/chromedriver.exe') as driver:
        driver.get("https://www.bestbuy.ca/en-ca")
        driver.implicitly_wait(100)
        driver.maximize_window()
        
        # go to shopping cart to clear existing items if any
        click_xpath(driver, SHOPPING_CART)
        clear_cart(driver, REMOVE_PANEL, REMOVE_BUTTON)
        
        # add all items to cart, one item at a time
        for item in ITEMS_XPATH:
            current_url = driver.current_url
            ### search for xbox
            add_item(driver, SEARCH_BAR, item)
            WebDriverWait(driver, 15).until(EC.url_changes(current_url))
            ### select item
            click_xpath(driver, ITEMS_XPATH[item])
            ### add to cart
            click_xpath(driver, ADD_TO_CART)

        # check out shopping cart
        ### click shopping cart icon
        click_xpath(driver, SHOPPING_CART)  
        ### click `Continue to Checkout`
        click_xpath(driver, CONT_CHECKOUT)
        ### checkout as GUEST
        click_xpath(driver, GUEST_XPATH)
