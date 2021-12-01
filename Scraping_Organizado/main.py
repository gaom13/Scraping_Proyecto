from selenium import webdriver
from pyvirtualdisplay import Display
import time

class Item():
    def cont_item(selfs):
        display = Display(visible=0, size=[800, 600])
        display.start()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--incognito')
        chrome_options.add_argument('--headless')
        selfs.driver = webdriver.Chrome(executable_path='/home/wolfphyton/Scraping_Organizado/chromedriver',options=chrome_options)
        selfs.driver.get('https://www.google.com')
        selfs.driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys("Facebook")
        time.sleep(5)
        selfs.driver.quit()
        print("YES")


def go():
    inst_item = Item()
    inst_item.cont_item()
