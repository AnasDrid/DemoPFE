from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver= webdriver.Chrome()

driver.get("https://www.google.com/")
driver.implicitly_wait(2)
element=driver.find_element(by=By.XPATH,value='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
element.send_keys("esi dz")
element=driver.find_element(by=By.XPATH,value='/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]')
element.click()