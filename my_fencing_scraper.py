from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#recibe una tupla, donde esta (atl1_id, a1_id_page) de un atleta, mas una lista de (atl_id, atl_id_page) 
# de los atletas de los que se obtendran los enfrentamientos
#y devuelve una lista de enfrentamientos, los cuales tiene la estructura de clash(atl1_id, atl2_id, winner_id, date)

def GetClashesFromWeb(atl1_id__atl1_idpage, atl_ids__atl_ids_page):
    atl1_id = atl1_id__atl1_idpage[0]
    atl1_id_page = atl1_id__atl1_idpage[1]

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    clashes = []

    for atl_id, atl_id_page in atl_ids__atl_ids_page:
        url = f'https://fie.org/head-to-head?firstAthlete={atl1_id_page}&secondAthlete={atl_id_page}'


        driver.get(url)
        wait = WebDriverWait(driver, 6)

        try:    
            wait.until(EC.visibility_of_element_located((By.XPATH, ".//div[contains(@class, 'HeadToHead-match-lines')]")))
            matches_content = driver.find_element(By.XPATH, ".//div[contains(@class, 'HeadToHead-match-lines')]")

            clashes_group = matches_content.find_elements(By.XPATH, ".//div[contains(@class, 'Grid Grid--alignCenter')]")
            for clash in clashes_group:
                data = clash.text
                atl1_result, atl_result, date = ObtainClashResultAndDate(data)
                winner_id = atl1_id if int(atl1_result) >= int(atl_result) else atl_id

                clashes.append((atl1_id, atl_id, atl1_result+'_'+atl_result, winner_id, date))

                print(clashes[len(clashes)-1])
        except:
            continue

    driver.quit()
    return clashes



def ObtainClashResultAndDate(text:str):
    info = text.split('\n')
    atl1_result = info[0]
    date = info[1]
    atl2_result = info[len(info)-1]

    return (atl1_result, atl2_result, date)