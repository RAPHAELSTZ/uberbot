from Params import Params
from selenium import webdriver
import time
from datetime import date, datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options as OptionsChrome
from selenium.webdriver.support.ui import WebDriverWait
import os
from pathlib import Path
import requests
import wget
import locale


class browser_methods:

    def wait_for_element(self, method, argument, timeout=10, condition="visible"):
        try:
            if condition == "clickable":
                cond = ec.element_to_be_clickable((getattr(By, method), argument))
            elif condition == "invisible":
                cond = ec.invisibility_of_element_located((getattr(By, method), argument))
            else:
                print(getattr(By, method), argument)
                cond = ec.presence_of_element_located((getattr(By, method), argument))
            WebDriverWait(self.driver, timeout).until(cond)
        except TimeoutException as e:
            raise e
        else:          
            if condition != "invisible":
                return self.driver.find_element(getattr(By, method), argument)
            else:
                return


    def __init__(self, choix, reports="normal"):
        self.chosen_bot = ""
        if(choix == "1"):
            self.chosen_bot = "uber"
            locale.setlocale(locale.LC_ALL, "en")

        elif(choix == "2"):
            self.chosen_bot = "uber_eat"
            locale.setlocale(locale.LC_ALL, "fr")

        else:
            print("Erreur de robot")

        # If page == -1 robot is done
        self.page_uber= 0
        self.page_uber_eat = 0

        # Table with all receipts
        self.list_of_receipt_uber = []
        self.list_of_receipt_uber_eat = []
        self.config = Params()
        self.url_uber = self.config.robot["url_uber"]
        self.url_uber_eat = self.config.robot["url_uber_eat"]

        self.day = date.today()
        self.day_folder = self.day.strftime("%d-%m-%Y")

        self.end_day = "2019-09-16"

        # self.chosen_bot = "uber_eat"
        # self.chosen_bot = "uber"


        # Start of Uber receipt robot
        if(self.chosen_bot == "uber"):
            # connect:
            dirpath = os.getcwd()
            chrome_options = OptionsChrome()
            # chrome_options.add_argument(executable_path=r'C:/Program Files (x86)/Google/Chrome/Application/Driver/ChromeDriver.exe')
            chrome_options.add_argument("user-data-dir=selenium")
            self.my_dir_path = dirpath+"\\my_receipts\\RECEIPT_"+self.day_folder

            prefs = {
            "download.default_directory": self.my_dir_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
            }
            chrome_options.add_experimental_option('prefs', prefs)


            self.driver = webdriver.Chrome(executable_path=r'C:/Program Files (x86)/Google/Chrome/Application/Driver/ChromeDriver.exe', chrome_options=chrome_options ) 
        

            self.driver.get(self.url_uber)
            print("Bienvenue dans le robot extracteur de recu uber")
            self.end_day = input("Veuillez entrer la date du recu le plus ancien que vous voulez recevoir impérativement au format AAAA-MM-JJ (2019-09-16) ")
            print("Le robot travaille sur la page : "+self.driver.current_url)


            print("Veuillez vous connecter à uber puis REVENIR et appuyez sur ENTRER")
            input("APPUYEZ SUR ENTRER SSI VOUS ETES CONNECTé!")
            
            while self.page_uber != -1:
                self.find_element_uber()
            print("Le robot télécharge tous les élements dans le repertoire "+ self.my_dir_path +", veuillez patienter")
                
            for obj in self.list_of_receipt_uber:
                title = obj.date.replace(":","-")
                download_url = "https://riders.uber.com/trips/"+ obj.id +"/pdf-receipt/"
                self.driver.get(download_url)
            
            # PAUSE IMPORTANTE SINON BUG
            time.sleep(2)


            for filename in os.listdir(self.my_dir_path): 
                filename_ = ""
                if(filename.endswith(".tmp")):
                    filename_ = self.deleteEndOfWord(filename, 4)
                
                if(filename.endswith(")")):
                    filename_ = self.deleteEndOfWord(filename, 8)
                
                if(filename.endswith(".crdown")):
                    filename_ = self.deleteEndOfWord(filename, 7)

                filename_ = filename
                work_file_name = self.deleteEndOfWord(filename_[8:], 4)
                
                for receipt in self.list_of_receipt_uber:
                    if (receipt.id == work_file_name):
                        try:
                            os.rename(self.my_dir_path+"/"+filename, self.my_dir_path+"/"+receipt.date.replace(":","-")+". at "+ receipt.price +".pdf")  
                        except:
                            print("Un des receipt n'a pas été téléchargé!")  
                    else:
                        print()

        if(self.chosen_bot == "uber_eat"):

            # connect:
            dirpath = os.getcwd()
            chrome_options = OptionsChrome()
            # chrome_options.add_argument(executable_path=r'C:/Program Files (x86)/Google/Chrome/Application/Driver/ChromeDriver.exe')
            chrome_options.add_argument("user-data-dir=selenium")
            self.my_dir_path = dirpath+"\\my_receipts\\RECEIPT_"+self.day_folder+"\\uber_eat"

            prefs = {
            "download.default_directory": self.my_dir_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
            }
            chrome_options.add_experimental_option('prefs', prefs)


            self.driver = webdriver.Chrome(executable_path=r'C:/Program Files (x86)/Google/Chrome/Application/Driver/ChromeDriver.exe', chrome_options=chrome_options ) 
        


            self.driver.get(self.url_uber_eat)
            print("Bienvenue dans le robot extracteur de recu uber")
            self.end_day = input("Veuillez entrer la date du recu le plus ancien que vous voulez recevoir impérativement au format AAAA-MM-JJ (2019-09-16) ")
            print("Le robot travaille sur la page : "+self.driver.current_url)


            print("Veuillez vous connecter à uber EAT puis REVENIR et appuyez sur ENTRER")
            input("APPUYEZ SUR ENTRER SSI VOUS ETES CONNECTé!")
            
            while self.page_uber_eat != -1:
                self.find_element_uber_eat()
            print("Le robot télécharge tous les élements dans le repertoire "+ self.my_dir_path +", veuillez patienter")
                
            for obj in self.list_of_receipt_uber_eat:
                # title = obj.date.replace(":","-")
                download_page_url = obj.page_url
                self.driver.get(download_page_url)
                self.downloadUberEatReceipt()
                print("Fin dl recu.")

            # PAUSE IMPORTANTE SINON BUG
            time.sleep(2)
            print(self.my_dir_path)
            for filename in os.listdir(self.my_dir_path): 
                filename_ = ""
                print("file name :")
                print(filename)
                if(filename.endswith(".tmp")):
                    filename_ = self.deleteEndOfWord(filename, 4)
                
                if(filename.endswith(")")):
                    filename_ = self.deleteEndOfWord(filename, 8)
                
                if(filename.endswith(".crdown")):
                    filename_ = self.deleteEndOfWord(filename, 7)

                filename_ = filename
                work_file_name = self.deleteEndOfWord(filename_[18:], 4)

                for receipt in self.list_of_receipt_uber_eat:
                    if (receipt.page_id == work_file_name):
                        try:
                            os.rename(self.my_dir_path+"/"+filename, self.my_dir_path+"/"+receipt.date.replace(":","-")+".pdf")  
                        except:
                            print("Un des receipt n'a pas été téléchargé!")  
                    else:
                        print("fin")



    def wait(self, t):
        time.sleep(t)

    def find_fill(self, name, content):
        # elt_param = self.config.robot["champ_"+name]
        element = self.driver.find_element_by_name(name) 
        element.send_keys(content)
        # element.send_keys(Keys.TAB)
    
    def find_element_uber(self):
        WebDriverWait(self.driver, 10).until(
           ec.presence_of_element_located((By.ID, "root"))
        )
        elements = self.driver.find_elements_by_css_selector("div[data-identity='trip-container']")

        if(elements is not None):
            for index, element in enumerate(elements):
                receipt_id = element.get_attribute("data-trip-id")
              
                ride_date_element = element.find_element_by_css_selector("div.b1 > div:nth-child(1)")
                ride_date = ride_date_element.get_attribute("innerText")

                receipt_price_element = element.find_element_by_css_selector("div.b1 > div:nth-child(2)")
                receipt_price = receipt_price_element.get_attribute("innerText")

                date_object =  self.getDateObjetFromString(ride_date).strftime('%Y-%m-%d')

                if(date_object > self.end_day):
                    # Inclusion de la date dans l'array d'objet
                    self.list_of_receipt_uber.append(MyUberReceipt(receipt_id, ride_date, receipt_price))
                    print("Travail en cours sur element n°"+str(index))
                    if(index == len(elements)-1):
                        print("Fin non sur première page")
                        self.page_uber += 10
                        self.driver.get("https://riders.uber.com/trips?offset="+str(self.page_uber))
                        # data-identity="pagination-next"
                else:
                    # renommage des fichiers
                    self.page_uber = -1

                # 18 September 2019, 5:30pm
        else:
            print("Element not found")


    def find_element_uber_eat(self):    
        WebDriverWait(self.driver, 10).until(
           ec.presence_of_element_located((By.ID, "root"))
        )
        # wrapper > div.bd.be.bf.aq.bg > div:nth-child(2)
        # Change TO DO
        elements = self.driver.find_elements_by_css_selector("#wrapper > div:nth-child(2) > div:nth-of-type(even)")
        # elements = self.driver.find_element_by_css_selector("div:first-child")
        

        if(elements is not None):
            for index, element in enumerate(elements):
                # receipt_id = element.get_attribute("href")
              
                ride_date_element = element.find_element_by_css_selector("div:nth-child(3) > div:first-child > div:nth-child(2) > div")
                page_url_element = ride_date_element.find_element_by_css_selector("a")
                # ride_date = ride_date_element.get_attribute("innerText")
                ride_date = element.get_attribute("innerText")
                page_url = page_url_element.get_attribute("href")
                page_id = page_url.split("=")[2].split("&")[0]


                date_scrape = ride_date.split("•")
                print("only _date variable is :")
                print(date_scrape[1])
                only_date = date_scrape[1]
                # date_object =  self.getDateObjetFromString(ride_date).strftime('%Y-%m-%d')
                if(index < len(elements)):
                    date_object = self.getUberEatDateObjetFromString(only_date).strftime('%Y-%m-%d %H:%M')
                    # date_object = self.getUberEatDateObjetFromString(only_date).strftime('%Y-%m-%d %H:%M')

                   

                    if(date_object > self.end_day):
                        # Inclusion de la date dans l'array d'objet
                        self.list_of_receipt_uber_eat.append(MyUberEatReceipt( page_id, date_object, page_url ))
                        print("Travail en cours sur element n°"+str(index))
                        if(index == len(elements)-1):
                            print("Fin non sur première page")
                            load_more = self.driver.find_element_by_css_selector("#wrapper > div:nth-child(2) > button")
                            load_more.click()
                            # data-identity="pagination-next"
                    else:
                        # renommage des fichiers
                        for index, obj in enumerate( self.list_of_receipt_uber_eat ):
                            print(str(index)+" : "+str(obj.date)+ "/ url: "+obj.page_url)
                        self.page_uber_eat = -1

                # 18 September 2019, 5:30pm
        else:
            print("Element not found")
            self.page_uber_eat = -1
  
    # Insérer à partir de la fin d'une string
    def insert_str(self,string, str_to_insert, index):
        index_ = len(string) - index
        return string[:index_] + str_to_insert + string[index_:]

    def deleteEndOfWord(self, string, index):
        index_ = len(string) - index
        return string[:index_]

# 17 September 2019, 5:18pm => Sep 15 2018 00:00:00
    def getDateObjetFromString(self, date):
        date = date.split(",")
        s_= self.insert_str(date[0], ",", 5)
        d = datetime.strptime(s_, '%d %B, %Y')
        return d

    # Conversion date uber eat to date de: • 01 oct. à 20:20 • ==> Oct 01 2019
    def getUberEatDateObjetFromString(self, date):
        if " à" in date:
            date = date.split(" à")
        if ". à" in date:
            date = date.split(". à")

        # s_= self.insert_str(date[0], ",", 0)
        print("DATE TO CONVERT IS")

        this_year = datetime.today().year
        print("Affichage split date :")
        print(date[0])
        print(date[1])
        date[0] = date[0].replace(u'\xa0', u' ').strip()
        date[1] = date[1].replace(u'\xa0', u' ').strip()
        time_data = self.adjustMonth(date[0])+" "+str(this_year)+" "+date[1]

        # time_data = date[0]+" "+date[1]
        d = datetime.strptime(time_data, '%d %b %Y %H:%M')
        return d


    def quit(self):
        self.driver.quit()
    
    def adjustMonth(self, ma_date):
        work_bit = ma_date.split(" ")

        # if( len(work_bit[1]) > 3 and work_bit[1] != "août" ):
        #     work_bit[1] = work_bit[1][:3]

        work_bit = work_bit[0] + " " + work_bit[1].capitalize()
        return work_bit

    def downloadUberEatReceipt(self):
        # xpath_selector = '//*[@id="wrapper"]/div[4]/div/div[2]/div[2]/div/div/a'
        # dl_link_element = WebDriverWait(self.driver, 10).until(
        #    ec.presence_of_element_located((By.XPATH, xpath_selector))
        # )
        # dl_link_element.click()
        time.sleep(1.7)
        css_selector ="div > div > div > div > div > a"
        bouton_telechargement = self.driver.execute_script("""
            selection = document.querySelectorAll(arguments[0])
            for (elt of selection){
                if(elt.innerText == "Télécharger le PDF"){
                    elt.click()
                    }
                }
            """, css_selector)
        print("BOUTON TROUVé : ")
        print(bouton_telechargement)
        # bouton_telechargement.click()

            





class MyUberReceipt():
    def __init__(self, id, date, price):
        self.id = id
        self.date = date
        self.price = price

class MyUberEatReceipt():
    def __init__(self, page_id, date, page_url):
        self.page_id = page_id
        self.page_url = page_url
        self.date = date
        # self.price = price

    # my_objects = []

    # for i in range(100):
    #     my_objects.append(MyClass(i))

    # # later

    # for obj in my_objects:
    #     print obj.number