import requests
from bs4 import BeautifulSoup
import os
import random
import time


#generating random sequence to name the extracted images
def generateRandomSequence():
    seq = ""
    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
               "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
                ]
    for i in range(0,5):
        seq = seq + random.choice(letters) + str(random.randrange(1,1000))
    
    return seq


#writing imagees to the result folder present in the file directory
def write_images(links):

    print("")
    choice = int(input("How many images do you want to extract ? : "))
    print("")

    #creating the Result directory if it already doesn't exits
    dir_name = "Result"
    if os.path.isdir(dir_name) == False:
        print("[+] Creating Directory Named '{0}'".format(dir_name))
        os.mkdir(dir_name)
        
   
    n = 1               #maintinging the counter for user set limit
    for i in links:
        try:
            req = requests.get(i)
            if(n > choice):         #break if the desired limit has reached
                break
            print("[+] Extracting Image #",n)
            with open(("{0}/" + generateRandomSequence() + ".jpg").format(dir_name),"wb") as img:
                img.write(req.content)
            n += 1
            req.close()
        except:
            print("[-] Skipping Current Image Due To Connection Problems")
            continue

#main scrape function
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

        #getting the links from the scrapped html code
        li = soup.find_all("a",class_="iusc")
        links = [eval(l['m'])['murl'] for l in li]
        len(links)

        
        print("{0} results found with the search term: {1}".format(len(links), term))
        choice = input("Do You Want To Extract The Images? Y or N ")
        
        if choice == "y" or choice == "Y":
            write_images(links) #writing images using the previously defined function

        r.close()
    




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

   
    


      




        





