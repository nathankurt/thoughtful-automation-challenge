import pandas as pd
import os
from selenium import webdriver

browser_lib = Selenium()

def open_the_website(url):
    return None



def main():
    path = os.path.abspath("chromedriver.exe")
    driver = webdriver.chrome(path)
    try:
        open_the_website("https://itdashboard.gov/")  
    finally:
        return None

if __name__ == "__main__":
    main()