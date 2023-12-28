import undetected_chromedriver as uc
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from config import api_key

driver = uc.Chrome(headless=False,use_subprocess=True,version_main=116)
driver.get("https://squiz.gg")

press_enter_auto = False

import openai
openai.api_key = api_key

#openai to use gpt-3
def get_response(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": "Tu es un assistant de quiz. Tu répondras à la question de utilisateur. Tu donnera uniquement la réponse et ne détaillera pas, tu répondras par simplement un mot, ou strictement le nécaissaire. Exemple: Quel est la capitale de la France: Paris."},
            {"role": "user", "content": question}
        ])
    res = response["choices"][0]["message"]["content"]


    return res

def send_rep(rep, driver: uc.Chrome):
    ActionChains(driver).send_keys(rep).perform()
    if press_enter_auto:
        ActionChains(driver).send_keys(Keys.ENTER).perform()

#getting the quedtion
question = None
while True:
    try:
        question_txt = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]').text
        if question_txt != question:
            question = question_txt
            rep = get_response(question)
            send_rep(rep, driver)
        sleep(1)
    except KeyboardInterrupt:
        print("Script interrupted manually.")
        break
    except Exception as e:
        continue

driver.close()