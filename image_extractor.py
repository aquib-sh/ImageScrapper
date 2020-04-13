import requests
from bs4 import BeautifulSoup
import os
import random
import time
#from urllib.parse import urljoin



def generateRandomSequence():
    seq = ""
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
               "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
                ]
    for i in range(0,5):
        seq = seq + random.choice(letters) + str(random.randrange(1,1000))
    
    return seq


def scrape():
    while True:
        print("*** enter q to quit ***")
        term = input("Enter the search term: ")
    
        if term == "q":
            break
        
        url = "https://bing.com"
    

        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"

        r = requests.get(url + "/images/search", params={"q":term,"safeSearch":"off"},headers = {"user-agent": USER_AGENT})

        soup = BeautifulSoup(r.content,"html.parser")

        li = soup.find_all("a",class_="iusc")
        links = [eval(l['m'])['murl'] for l in li]
        len(links)


        print("{0} results found with the search term: {1}".format(len(links), term))
        choice = input("Do You Want To Extract The Images? Y or N ")
    
        if choice == "y" or choice == "Y":
            write_images(links)

        r.close()
    
    #if(int(limit) > 35):
        #scrape(term, limit - 35, offset)

def write_images(links):
    
    dir_name = "Result"
    if os.path.isdir(dir_name) == False:
        print("[+] Creating Directory Named '{0}'".format(dir_name))
        os.mkdir(dir_name)
   
    n = 1
    for i in links:
        req = requests.get(i)
        print("[+] Extracting Image #",n)
        with open(("{0}/" + generateRandomSequence() + ".jpg").format(dir_name),"wb") as img:
            img.write(req.content)
        n += 1
        req.close()




start = """
$$$$$$$       $$$     $$$       $$$$$$           $$$$$$$$   $$       $$   $$$$$$$$$$
  $$         $$ $$   $$ $$      $$               $$           $$    $$        $$
  $$        $$  $$  $$   $$     $$  $$$$         $$$$$$$$       $$$$          $$
  $$       $$    $ $$     $$    $$  $$ $         $$           $$    $$        $$
$$$$$$$   $$               $$   $$$$$$ $         $$$$$$$$   $$       $$       $$


COPYRIGHT(C) 2020 SHAIKH AQUIB             

                     """
print(start)
print("[+] Starting...")
print("")
time.sleep(2)

scrape()

   
    


      




        





