from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from probando_regresion import GetDateMonthYear
from datetime import date

def GetAthletesClashes(urls):

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    clashes = []
    
    for url in urls:
    
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        wait.until(EC.visibility_of_element_located((By.XPATH, ".//p[contains(@class, 'card-meta-value')]")))
        personal_data = driver.find_elements(By.XPATH, ".//p[contains(@class, 'card-meta-value')]")
        #age = personal_data[1].text
        #style = personal_data[3].text
        style = 'gr'
        category = '67 Kg'


        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "tab-anchor")))
        buttons = driver.find_elements(By.CLASS_NAME, value='tab-anchor')

        
        for button in buttons:
            try:
                span = button.find_element(By.XPATH, ".//span[text()='Results']")
                button.click()
                break
            except:
                continue
                
        tab_cont = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='tab-item tab-item-result']")))
        tab_cont_groups = tab_cont.find_elements(By.XPATH, ".//div[@class='tabs-container-group']")
        tabs_cont_content = EliminateTabDuplicates(tab_cont_groups)

        for tab in tabs_cont_content:
            event_data = tab.find_elements(By.XPATH, ".//span[@class='meta']")
            games_tokio_date = date(2021, 7, 1)
            Date = event_data[1].text
            Date_ = GetDateMonthYear(Date)
            
            buttons = tab.find_elements(By.XPATH, ".//button[@class='btn-link']")

            for button in buttons:

                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(0.5)
                driver.execute_script("window.scrollBy(0, -150);")
                time.sleep(0.5)

                button.click()

                panel = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='waf-accordion-panel']")))
                #category = panel.find_element(By.XPATH, ".//div[contains(@class, 'content-item')]//div[contains(@class, 'content-wrapper')]//div[contains(@class, 'card-meta')]//span[contains(@class, 'meta')]").text
                contents_items = panel.find_elements(By.XPATH, ".//div[contains(@class, 'content-item')]")
                cards_info = panel.find_elements(By.CLASS_NAME, value='card-label')
                cards_number =  panel.find_elements(By.CLASS_NAME, value='card-number')
                statuses = panel.find_elements(By.XPATH, ".//span[contains(@class, 'text status')]")

                for i in range(len(contents_items)):
                    atl_1_name = cards_info[i*2].text
                    atl_2_name = cards_info[i*2 + 1].text
                    atl_1_points = cards_number[i*2].text
                    atl_2_points = cards_number[i*2 + 1].text
                    winning_form = statuses[i].text
                    clash = (style, category, atl_1_name, atl_2_name, (atl_1_points, atl_2_points), atl_1_name, winning_form, Date)
                    clashes.append(clash)

                    print(f'{clash},')



            #for content_item in contents_items:
            #    time.sleep(1)
            #    category = content_item.find_element(By.CLASS_NAME, value='meta').text
            #    card_won = content_item.find_element(By.XPATH, "//*[@class='card-item card-a won']")
            #    atl_1_name = card_won.find_element(By.CLASS_NAME, 'card-info').text
            #    atl_1_points = card_won.find_element(By.CLASS_NAME, 'card-number').text
            #    card_loss = content_item.find_element(By.XPATH, "//*[@class='card-item card-b']")
            #    atl_2_name = card_loss.find_element(By.CLASS_NAME, 'card-info').text
            #    atl_2_points = card_loss.find_element(By.CLASS_NAME, 'card-number').text
            #    winning_form = content_item.find_element(By.XPATH, "//*[@class='text status']").text

            #    clash = (atl_1_name, atl_2_name, (atl_1_points, atl_2_points), atl_1_name, winning_form)
            #    clashes.append(clash)
            #    print(clash)
        
        
    driver.quit()
    return clashes

def EliminateTabDuplicates(tabs_cont_groups):
    notGlobalDuplicatedTabs = []

    for tab_cont_group in tabs_cont_groups:
        tabs_cont_content = tab_cont_group.find_elements(By.XPATH, ".//div[@class='tabs-container-content']")

        notDuplicatedTexts = []
        notDuplicatedTabs = []

        for tab in tabs_cont_content:
            card = tab.find_element(By.XPATH, ".//div[@class='card-info']")
            span = card.find_element(By.XPATH, ".//span[@class='text']")
            text = span.text
            if text not in notDuplicatedTexts:
                notDuplicatedTexts.append(text)
                notDuplicatedTabs.append(tab)
        
        notGlobalDuplicatedTabs.extend(notDuplicatedTabs)

    return notGlobalDuplicatedTabs
