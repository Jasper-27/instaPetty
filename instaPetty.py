import time
import os
import datetime
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium import webdriver

import getpass

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException



print("     ____           __        ____       __  __            ")
print("    /  _/___  _____/ /_____ _/ __ \___  / /_/ /___  __     ")
print("     / // __ \/ ___/ __/ __ `/ /_/ / _ \/ __/ __/ / / /    ")
print("   _/ // / / (__  ) /_/ /_/ / ____/  __/ /_/ /_/ /_/ /     ")
print("  /___/_/ /_/____/\__/\__,_/_/    \___/\__/\__/\__, /      ")
print("                                              /____/       ")
print("                                             by Jasper-27  ")
print("                                                           ")



account = input("Target account: ")
print("")
print("Login to instagram")
yourusername = input("Your username: ")
yourpassword = getpass.getpass("Your password: ")


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(ChromeDriverManager().install())


driver.get('https://www.instagram.com/accounts/login/')
sleep(2)
WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Accept')]"))).click()
sleep(1)
username_input = driver.find_element_by_css_selector("input[name='username']")
password_input = driver.find_element_by_css_selector("input[name='password']")
username_input.send_keys(yourusername)
password_input.send_keys(yourpassword)
login_button = driver.find_element_by_xpath("//button[@type='submit']")
login_button.click()
WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Not Now')]"))).click()
sleep(2)
          


def getPeople(page):
  driver.get('https://www.instagram.com/%s' % account)
  sleep(2) 

  driver.find_element_by_xpath('//a[contains(@href, "%s")]' % page).click()
  scr2 = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
  sleep(5)
  count_text = scr2.text

  count_text = count_text.split(" ")[0]

  count_text = count_text.replace(',', '') # Removes comma if there is one 

  count = int(count_text)

  dirname = os.path.dirname(os.path.abspath(__file__))
  csvfilename = os.path.join(dirname, account + "-" + page + ".txt")
  file_exists = os.path.isfile(csvfilename) # dunno what this does
  f = open(csvfilename,'w')

  people = []

  for i in range(1, count + 1):   # -3 because there are some weird extra bits added 
    try:
      scr1 = driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[%s]' % i)

      driver.execute_script("arguments[0].scrollIntoView();", scr1)
      text = scr1.text.split()[0] # Gets the username from the text 

      f.write(text + "\n")
      people.append(text)

      sleep(0.2)  # the speed it scrolls through accounts. higher = more stable, lower = faster
      

    except:
      print("Error / end of list")
      break
      

  f.close()


  try:
    return people
  except: 
    print("error")
    return 1


followers = getPeople("followers")

following = getPeople("following")

  
driver.quit() # Exits the the web driver

print("Followers: ", len(followers))
print("Following: ", len(following))


csvfilename = os.path.join(account + " doesn't follow back.txt")
file_exists = os.path.isfile(csvfilename) # dunno what this does
f = open(csvfilename,'w')

not_following = []
for i in followers: 
  if i not in following:
    not_following.append(i)
    f.write(i + "\n")

f.close()


csvfilename = os.path.join(account + " is not follwed back.txt")
file_exists = os.path.isfile(csvfilename) # dunno what this does
f = open(csvfilename,'w')

not_followers = []
for i in following: 
  if i not in followers:
    not_followers.append(i)
    f.write(i + "\n")

f.close()


print("These people don't follow you back")
print(not_followers)
print("")

print("You don't follow these people back")
print(not_following)
print("")