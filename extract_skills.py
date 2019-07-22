# scrape indeed job listings to rank given skills in order of most needed
# takes about 1 minute per 10 job listings or 2 minutes per page
# @author: Osamah Mandawi
# @email: oamandawi@brandeis.edu 

"""This is an explanation of the structure of indeed.com
"""
# This is an example of what the first job listings page for software
# engineering in MA looks like: https://www.indeed.com/jobs?q=software+engineer&l=MA&sort=date
# Now, if we look at a single job: https://www.indeed.com/jobs?q=software+engineer&l=MA&sort=date&vjk=3916106ade6d80b3
# Note that this is the same URL as the one before, with only vjk=3916106ade6d80b3, the unique job id, added to it.
# Overall, this means we can replace the text after q= to get results for a different job (with spaces converted to +),
# and replace text after l= with state abbreviation

# ? Must have the following: 
# 1. Have pip ready: https://stackoverflow.com/questions/4750806/how-do-i-install-pip-on-windows?rq=1
# * Note, you may already have pip, so check by going to cmd, typing python, and then import pip and you should get no errors, if you have it
# 2. Have selenium ready: https://pypi.org/project/selenium/
# * use: 'pip install selenium' without quotes in cmd

# ? Nice to have the following to get visual results:
# 1. Have easygui ready: https://pypi.org/project/easygui/
# * use: 'pip install easygui' without quotes in cmd
# 2. Have matplotlib ready (this is quite heavy): https://pypi.org/project/matplotlib/
# * use: 'pip install matplotlib' without quotes in cmd



# ! Get the packages to count time program took to run
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


def headless_options():
    """Sets the configurations for the driver. In our case, we add the headless settings because we want the program to crawl in the background

    Returns:
        options -- the options configurations to be used in the Google Chrome driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    return options


def set_driver_path():
    """Sometimes your driver path is not installed. Other times, you don't know where it is. This installs it, if it's not there, and returns 
    where it is, when it's there.

    Returns:
        driver_path -- path of Chrome driver
    """
    driver_path = ChromeDriverManager().install()
    return driver_path


def set_driver(driver_path):
    """Sets the Chrome driver with the driver path and the headless options 
    Arguments:
        driver_path {string address} -- path of Chrome driver
    Returns:
        driver -- the Chrome driver to be used for web crawling
    """
    driver = webdriver.Chrome(driver_path, options=headless_options())
    return driver


def start_gui():
    """Introduce user to the program, and get some information: which field, which state, how many pages of indeed, and which skills.
    
    Returns:
        field -- string with what field user wants to look at job listings for
        state -- which U.S. state to find job listings in
        page_range -- how many pages of indeed job listings to search through
        skills -- which skills to look for
        counter_dict -- the skills dictionary with how many jobs each skill appears in
        search_url_master -- a generated url with the field and state chosen by the user sorted by date to reduce duplicates
    """
    easygui.msgbox("Welcome to Extract_Skills V.0.1\nWe will be using indeed.com to extract our data.\nNote that we will only be looking at job listings within the U.S.\n")
    field = easygui.enterbox(
        "What kind of job do you want data on?\n(e.g. software engineering)")
    field = field.replace(" ", "+")
    state = easygui.enterbox(
        "What state in the U.S. are you looking at?\n(e.g. CA)")
    pages_range = int(easygui.enterbox(
        "How many pages of indeed.com to scrape?"))
    skills = easygui.enterbox(
        "Enter skills, such as programming languages, to look for, seperated by /\n(e.g. python/sas/sql/java/php/master's degree/bachelor's degree)")
    skills = skills.split("/")
    skills = list(map(str.lower,skills))
    counter_dict = {i: 0 for i in skills}
    #! create the search url using the job type and location
    search_url_master = 'https://www.indeed.com/jobs?q='+field+'&l='+state+'&sort=date'
    print("Skills looking for:", skills)
    return field, state, pages_range, skills, counter_dict, search_url_master


def gather_job_listings(pages_range, search_url_master, driver_path):
    """This program gathers all the job listings on as many pages as requested by the user. 
    
    Arguments:
        pages_range {integer} -- how many pages of indeed job listings to search through
        search_url_master {string} -- a generated url with the field and state chosen by the user sorted by date to reduce duplicates
        driver_path {string address} -- path of Chrome driver
    
    Returns:
        start_time -- time in seconds of when the searching process started
        sites -- the urls of all the job listings in a list
    """
    start_time = time.time()
    print("SEARCH STARTS")
    sites = []
    for i in range(0, pages_range):
        driver = set_driver(driver_path)
        #! crawl to the first page of the search
        driver.get(
            search_url_master+'&start='+str(i*10))
        #! get the ids of all the job listings
        ids = driver.find_elements_by_xpath('//*[@data-jk]')
        jdks = []
        for ii in ids:
            # print ii.tag_name
            jdks.append((ii.get_attribute('data-jk')))
        #! combine the ids with the url and save them in a list so then we can go over them job by job
        sites.extend(
            [search_url_master+'&vjk='+jdk for jdk in jdks])
        driver.quit()
    #! remove duplicates
    sites = list(dict.fromkeys(sites))
    print("Amount of job postings found:", len(sites))
    return start_time, sites


def count_keywords(txt, counter_dict):
    """Count how many times each skill appears in the text; update counter_dict

    Arguments:
        txt {string} -- the text description of the job
        counter_dict {dictionary} -- the dictionary of skills and how often they appeared in different jobs

    Returns:
        counter_dict -- the update skills dictionary with how many jobs each skill appears in
    """
    txt = txt.split()
    for skill in counter_dict:
        #! Note that this only counts a skill once even if it appears multiply times in the SAME job description
        if txt.count(skill) > 0:
            counter_dict[skill] += 1
    return counter_dict


def print_results(counter_dict):
    """Print the dictionary of keywords and one how many job listings they have appeared

    Arguments:
        counter_dict {dictionary} -- the dictionary of skills and how often they appeared in different jobs
    """
    for i in counter_dict:
        print(i, counter_dict[i])


def skill_count(sites, counter_dict, driver_path):
    """Go listing by listing using the urls of the listings and count in how many listings the skills appear
    
    Arguments:
        sites {list} -- sites -- the urls of all the job listings in a list
        counter_dict {dictionary} -- the dictionary of skills and how often they appeared in different jobs
        driver_path {string address} -- path of Chrome driver
    
    Returns:
        counter_dict -- fully updated skills dictionary
        end_time -- time in seconds of when all the processes finished
    """
    count_sites = 1
    for site in sites:
        driver = set_driver(driver_path)
        driver.get(site)
        print("url of curr page", site)
        print("job number", count_sites)
        element = driver.find_elements_by_id("vjs-desc")
        if len(element) > 0:
            element = element[0].text.lower()
            element=element.replace("\n", " ")
            # print(element) if you want to see what the descriptions says
            counter_dict = count_keywords(element, counter_dict)
        print_results(counter_dict)
        driver.quit()
        count_sites += 1
    end_time = time.time()
    return counter_dict, end_time


def end_gui(start_time, end_time, counter_dict, sites):
    """Print findings after the program finishes
    """
    print("Time program took to run:  "+str(datetime.timedelta(seconds=(end_time-start_time))))
    result = ""
    for k in sorted(counter_dict, key=counter_dict.get, reverse=True):
        result += (k.capitalize()+" ("+str(counter_dict[k])+")\n")
    easygui.msgbox("Our final list of skills across "+str(len(sites)) +
                   " jobs, sorted from most needed to least:\n"+result+"\nFinished in "+str(datetime.timedelta(seconds=(end_time-start_time))))

def bar_print(field,state,sites,counter_dict):
    """Prints in a nice graph then saves it
    
    Arguments:
        field {string} 
        state {string} 
        sites {list} 
        counter_dict {dictionary}
    """
    plt.bar(*zip(*counter_dict.items()))
    plt.ylabel("Amount of job listing mentions")
    plt.xlabel("Skill")
    plt.suptitle("For {} {} jobs in {}, U.S.".format(str(len(sites)),field.replace("+"," "),state))
    plt.savefig(str(len(sites))+field+state+".png")
    plt.show()


def main():
    """Run everything
    """
    driver_path = set_driver_path()
    field, state, pages_range, skills, counter_dict, search_url_master = start_gui()
    start_time, sites = gather_job_listings(
        pages_range, search_url_master, driver_path)
    counter_dict, end_time = skill_count(sites, counter_dict, driver_path)
    end_gui(start_time, end_time, counter_dict, sites)
    bar_print(field,state,sites,counter_dict)


if __name__ == "__main__":
    main()

# ? Example result from 257 job listings of software engineering in CA
# job number 257
# Java 20
# Python 18
# Perl 0
# C++ 15
# C# 13
# Rust 2
# Ruby 3
# VB 0
# MATLAB 3
# PHP 0
# Scala 1
# HTML 5
# CSS 6
