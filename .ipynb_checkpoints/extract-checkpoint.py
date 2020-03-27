import time
from datetime import datetime
import os  # for path control
import sys

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

# ! These packages to deal with tables and multi-dimensional array
import numpy as np
import pandas as pd


master_job_link = "https://www.indeed.com/jobs?q=Software+Engineer&l=Boston"
master_job_link2 = "https://www.indeed.com/jobs?q=data+scientist&l=Boston"
master_job_link3 = "https://www.indeed.com/jobs?q=web+developer&l=Boston"
link2 = "https://www.indeed.com/jobs?q=Software%20Engineer&l=Boston&vjk=2826852a029ff8f6" #Example of a job's link


def headless_options():
    """
    Sets the configurations for the driver. In our case, we add the headless settings because we want the program
    to crawl in the background

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


def get_all_ids(driver_path, job_link, num_page, ):
    """
    This function gets all the ids found in the master_job_link and returns it as a list

    :return: list of such ids. the WebDriver itself
    """
    ids = []
    driver = webdriver.Chrome(driver_path, options=headless_options())
    for page in range(0, num_page):
        driver.get(job_link + '&start='+str(page*10))
        ids_elements = driver.find_elements_by_xpath('//*[@data-jk]')
        ids.extend([link.get_attribute("data-jk") for link in ids_elements])

    return ids, driver


def write_to_txt(all_ids):
    """
    This function writes all the ids to txt file

    :param all_ids: all the job ids in a list
    :return:
    """

    output = open("data\ids.txt", "w+")
    output.writelines(["%s\n" % item for item in all_ids])
    output.write("%s" % datetime.now(tz=None))
    output.close()


def read_from_txt():
    file = open("data\ids.txt", "r+")
    read_ids = file.read()
    read_ids = read_ids.split("\n")
    crawl_time = read_ids.pop()
    return read_ids, crawl_time


def test(driver, job_link, job_ids):
    pass
    # driver.get(job_link + "&vjk=" + job_ids)
    # company = driver.find_element_by_xpath('//*[@id="vjs-cn"]').text
    # print("Companies' ids:", company, sep="\n", end="\n\n")


def test():
    a = datetime.now(tz=None)
    print(a)
    time.sleep(2)
    b = datetime.now(tz=None)
    print(b)
    print(b-a)


def get_desc(driver, job_link, job_ids):
    """
    This function gets all the listed items in the job descriptions and writes them into pandas table

    :param driver: the WebDriver
    :param job_link: the master job link
    :param job_ids: a list of all ids
    :return: a Pandas DataFrame with each job's information
    """

    # These are the information to be included in the DataFrame
    companies = []
    positions = []
    all_ids = []
    descriptions = []

    # for each job
    for id in job_ids:
        try:
            driver.get(job_link + "&vjk=" + id)

            # wait for element to be visible then get it
            desc_li = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located(
                (By.XPATH, '//div[@id="vjs-desc"]//li')))
            desc_li = [el.text for el in desc_li]  # get the text part in the gotten WebElements
            company = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#vjs-cn'))).text
            position = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#vjs-jobtitle'))).text

            # Append the gotten info
            companies.append(company)
            positions.append(position)
            all_ids.append(id)
            descriptions.append(desc_li)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            companies.append(np.nan)
            positions.append(np.nan)
            all_ids.append(np.nan)
            descriptions.append(np.nan)

    # Writes the info to nparray then format and create pandas DataFrame
    everything = np.array([companies, positions, all_ids, descriptions])
    everything = everything.transpose()
    df = pd.DataFrame(data=everything, columns=["Companies", "Positions", "ID", "Descriptions"])
    return df


def write_to_csv(dframe):
    """
    This function creates a folder data (optional) and export the DataFrame to a .csv file
    :return: No return
    """
    file_name = "\data_test.csv"
    directory = os.path.dirname(os.path.realpath('__file__')) + "\data"
    try:
        # Create target Directory
        os.mkdir(directory)
        print("Directory ", directory, " Created ")
    except FileExistsError:
        print("Directory ", directory, " already exists")

    dframe.to_csv((directory + file_name), index=None, header=True)

# def get_desc_test(driver, job_link)


def main():
    """
    Run everything
    :return: nothing
    """

    driver_path = ChromeDriverManager().install()

    # Next 3 lines is getting the ids
    num_pages = 5
    all_ids, driver = get_all_ids(driver_path, master_job_link2, num_pages)
    write_to_txt(all_ids)

    # This gets the
    deez_ids, time = read_from_txt()
    print("deez ids", deez_ids, "\n", "Time: ", time)
    df = get_desc(driver, master_job_link2, deez_ids)
    write_to_csv(df)

    driver.implicitly_wait(10)
    driver.quit()

    return


if __name__ == "__main__":
    main()
