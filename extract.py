import time
import datetime

# ! Get the package to create dialog boxes
import easygui

# ! Get the package to visually print results
import matplotlib.pyplot as plt

# ! Get the package to control the web
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

master_job_link = "https://www.indeed.com/jobs?q=Software+Engineer&l=Boston"
link2 = "https://www.indeed.com/jobs?q=Software%20Engineer&l=Boston&vjk=2826852a029ff8f6" #Example of a job's link


def headless_options():
    """
    Sets the configurations for the driver. In our case, we add the headless settings because we want the program to crawl in the background

    Returns:
        options -- the options configurations to be used in the Google Chrome driver
    """
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("--window-size=1920,1080")
    options.add_argument("--window-size=1366,768")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    return options


def get_all_ids(driver_path, job_link, num_page):
    ids = []
    driver = webdriver.Chrome(driver_path, options=headless_options())
    for page in range(0, num_page):
        driver.get(job_link + '&start='+str(page*10))
        ids_elements = driver.find_elements_by_xpath('//*[@data-jk]')
        ids.extend([link.get_attribute("data-jk") for link in ids_elements])
    return ids, driver


def get_desc(driver, job_link, job_ids):
    descriptions = []
    print(job_ids)

    # for each job
    for id in job_ids:
        driver.get(job_link + "&vjk=" + id)
        elements = driver.find_elements_by_xpath('//div[@id="vjs-desc"]//li')
        company = driver.find_element_by_id("vjs-cn").text
        # print(id, elements, sep="\t")
        elements = [el.text for el in elements]
        descriptions.append(elements)

    print(descriptions)


# def get_desc_test(driver, job_link)

def main():
    """
    Run everything
    :return: nothing
    """
    driver_path = ChromeDriverManager().install()

    all_ids, driver = get_all_ids(driver_path, master_job_link, 1)
    get_desc(driver, master_job_link, all_ids)

    return
    # text = driver.find_element_by_css_selector("#vjs-desc div div")
    # print(text)

    driver.get(link2)

    # elements1 = [el.text for el in elements]
    # elements = map(lambda el: el.text(), elements)
    print("AAAAAAA")
    print(elements1)
    print(len(elements1))

    # text = driver.find_element_by_css_selector("#vjs-desc div div div ul")
    # print(text.text)

    # ids1 = map(lambda id: id.get_attributes("data-jk"), ids)
    # print("BBBBBBB", ids1, sep="\n")

    driver.quit()


if __name__ == "__main__":
    main()
