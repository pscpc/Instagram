from selenium import webdriver
# To wait for side load
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

# Allows us to use keyboard keys
from selenium.webdriver.common.keys import Keys
import time
import json
import os

with open('usernames.txt', 'r') as f:
    usernames = [line.strip() for line in f]

f = open('accounts.json',)
accounts = json.load(f)
numoftimes = "1"             # Enter in the number of times you would like to send the message to the recipient
count=40   #to how many account

count_message=0 

# removing the accs who sent from file
def delete_file_line():
        with open("infos/usernames.txt") as f:
            mylist = f.read().splitlines()
        newlist = usernames[:count]
        os.remove("infos/usernames.txt")
        thefile = open('infos/usernames.txt', 'w')
        del mylist[:count]
        for item in mylist:
            thefile.write("%s\n" % item)
    # replace 'user:pass@ip:port' with your information
options = {
    'proxy': {
        'http': 'http://username:password@ip:port',
        'https': 'https://username:password@ip:port',
        'no_proxy': 'localhost,127.0.0.1'
    }
}
PATH = "chromedriver.exe"                   # Step 4 of the installations instructions
driver = webdriver.Chrome(PATH, seleniumwire_options=options)
url = "https://www.instagram.com/"
post='https://www.instagram.com/p/xxxxxxxxx/'

for i in range(len(accounts)):
    driver = webdriver.Chrome(PATH, seleniumwire_options=options)
    print(i)

    if not usernames:
        print('Finished usernames')
        break
    if len(usernames) < count:
        count = len(usernames)

    try:
        # 1) Login işlemleri
        try:
            # replace 'your_absolute_path' with your chrome binary's aboslute path
            print(accounts[i]["username"])
            driver.get(url)
            time.sleep(5)
            cookies = driver.get_cookies()
            print(len(cookies))
            print(cookies)
            time.sleep(3)
            # Waits for the login box to appear on the webpage
            usernamebox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
            # Login to Instagram
            usernamebox.send_keys(accounts[i]["username"])
            passwordbox = driver.find_element_by_name('password')
            passwordbox.send_keys(accounts[i]["password"])
            time.sleep(1)
            loginbutton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')))
            loginbutton.click()
            time.sleep(8)
            print("Logging in")


        except:
            print("Could not login!")
            driver.manage().deleteAllCookies();     
            driver.quit();
            driver = webdriver.Chrome(PATH, seleniumwire_options=options)
            continue

        # 2) post buton
        try: 
            driver.get(post)
            time.sleep(3)
            postbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._5e4p')))
            postbtn.click()
        except:
            print ("Could not find or click the direct message button")
            driver.manage().deleteAllCookies();     
            driver.quit();
            driver = webdriver.Chrome(PATH, seleniumwire_options=options)
            continue
            
        # 3) notification control
        # try:
        #     notificationsnotnow = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.HoLwm')))
        #     notificationsnotnow.click()
        #     print("notification")
        # except:
        #     print ("Could not click not now on the notifications pop up!")
        #     driver.manage().deleteAllCookies();     
        #     driver.quit();
        #     driver = webdriver.Chrome(PATH, seleniumwire_options=options)
        #     continue
            

        # 4) user seçme
        for j in range(count):
            # 4.1) typing usernames
            try:
                print("searchuserbox tıklandı")
                print(usernames[j])
                searchuserbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.j_2Hd')))
                searchuserbox.send_keys(usernames[j])
               

            except:
                print ("Could not find the enter username box!")
                driver.manage().deleteAllCookies();     
                driver.quit();
                driver = webdriver.Chrome(PATH, seleniumwire_options=options)
                continue
            # 4.2) select users
            try:
                print("firstuser tıklandı")
                firstuser = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div[2]/div[2]/div[1]/div/div[3]/button')))
                firstuser.click()
                            
            except:
                print("Could not click on the first user!")
                driver.manage().deleteAllCookies();     
                driver.quit();
                driver = webdriver.Chrome(PATH, seleniumwire_options=options)
                continue
        

        try:
            # Sends the message
            messagebox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div[2]/div[3]/input')))
            messagebox.click()
            message = "message text"
            messagebox.send_keys(message)
            sendbtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div[2]/div[4]/button')))
            sendbtn.click()
            time.sleep(2)
            count_message +=1
                      
        except:
            print("Error sending the message!")
        try:
            print("exit butonu")
            time.sleep(3)
            exitbutton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/span')))
            exitbutton.click()  
            exitbutton2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/div[2]')))
            exitbutton2.click()
        except:
            print("Error exit button")

    except:
        print("An error has occurred")
        driver.quit()
        continue

        
    del usernames[0:count]
    driver.quit()
    delete_file_line()

print(count_message+" instagram dm sent in total")


