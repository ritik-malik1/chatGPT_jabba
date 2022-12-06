from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fastapi import FastAPI
from dotenv import load_dotenv
from time import sleep
from os import getenv

load_dotenv()

app = FastAPI()

########
email = getenv("EMAIL")
passwd = getenv("PASSWD")
########


def start_selenium():

    # start the driver
    driver = webdriver.Firefox(executable_path="geckodriver")

    driver.get("https://chat.openai.com/auth/login")

    # click on login
    driver.find_element("xpath","/html/body/div/div/div/div[4]/button[1]").click()

    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='username']"))
    )

    # click on email
    driver.find_element("xpath","//*[@id='username']").click()
    # send email
    driver.find_element("xpath","//*[@id='username']").send_keys(email)
    # click on continue
    driver.find_element("xpath","/html/body/main/section/div/div/div/form/div[2]/button").click()
    # wait to load
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='password']"))
    )
    # click on passwd
    driver.find_element("xpath","//*[@id='password']").click()
    # send passwd
    driver.find_element("xpath","//*[@id='password']").send_keys(passwd)
    # click on continue
    driver.find_element("xpath","/html/body/main/section/div/div/div/form/div[2]/button").click()

    # logged in! Now skip 3 *next prompts*
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button"))
    )
    # click on next
    driver.find_element("xpath","/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button").click()
    # click on 2nd next
    driver.find_element("xpath","/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]").click()
    # click on 3rd next
    driver.find_element("xpath","/html/body/div[2]/div/div/div/div[2]/div/div/div[2]/div[4]/button[2]").click()

    return driver

driver = start_selenium()


def check_if_complete(driver):

    sleep(1)
    count = 0

    while True:
        len1 = len(driver.find_element("xpath","/html/body/div/div/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]/div[1]").text)
        sleep(1)
        len2 = len(driver.find_element("xpath","/html/body/div/div/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]/div[1]").text)

        if len1 == len2:
            count+=1
        
        if count > 1:
            break
    

def get_chat_GPT_result(query, driver):

    # type the prompt
    driver.find_element("xpath","/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/textarea").send_keys(query)
    # press ENTER
    driver.find_element("xpath","/html/body/div/div/div[1]/main/div[2]/form/div/div[2]/textarea").send_keys(Keys.RETURN)


    check_if_complete(driver)

    # answer
    result = driver.find_element("xpath","/html/body/div/div/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]/div[1]").text

    # reset the thread
    driver.find_element("xpath","/html/body/div/div/div[2]/div/div/nav/a[1]").click()

    return result





@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/chatGPT/{query}")
async def search_query(query):

    if query == "":
        return {"message": "empty query detected"}


    result = get_chat_GPT_result(query, driver)

    return {"message": result}

