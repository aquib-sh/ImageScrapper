#   IMAGE EXTRACTOR
# A simple tool for searching and downloading images from bing search
# use Python version > 3.7

import os
import random
import time
from string import ascii_letters

import requests
from bs4 import BeautifulSoup

def generate_random_sequence() -> str:
    """Generates a sequence of random letters and numbers,
    to be used in naming images later.

    Returns
    --------
    name: str
        A name made up of 10 letters and 5 numbers randomly.
        example: "RbCsfpoxqM8686241812"

    """
    name = ""
    # Add 10 random letters to the string
    for i in range(0, 10):
        letter = random.choice(ascii_letters)
        name += letter

    # Add 5 random numbers to the string
    for i in range(0, 5):
        number = random.randint(0, 100)
        name += str(number) # str() is used to typecast number to a string

    return name

def write_image_from_link(link, output_folder="Results") -> int:
    """Downloads the image from link and writes it to a JPEG file 
    having random name generated from generate_random_sequence()

    Parameters
    ----------
    link: str
        URL of the image
        example: "https://media.sciencephoto.com/image/e1300006/800wm/E1300006-Avalanche.jpg".

    output_folder: str (DEFAULT="Results")
        output folder where images will be downloaded to
        example: Results

    Returns
    ------
    :int
        0 if the download and write operation is sucessful
        1 if the download and write operation failed

    """
    # if the folder doesn't exists then create it. 
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
        print(f"[+] Creating directory {output_folder}")

    # generate a random name for creating file and add .jpeg to that name
    img_f_name = generate_random_sequence() + ".jpeg"
    img_path = os.path.join(output_folder, img_f_name)

    # get image data by GET request
    response = requests.get(link)

    # exit if the download failed.
    if (response.status_code) != 200:
        print(f"CONNECTION ERROR: Failed to download from {link}")
        return 1

    image_data = response.content

    # open a file pointer and write the binary data to image
    fp = open(img_path, "wb")
    fp.write(image_data)
    return 0

def extract_links_from_soup(soup) -> list:
    """Extracts image links from soup.
    
    Parameters
    -----------
    soup: BeautifulSoup
        BeautifulSoup object from where we will extract links

    Returns
    -------
    links: list
        List of image links.
    """
    links = []
    image_elems = soup.find_all("a", {"class":"iusc"})
    for elem in image_elems:
        image_info = eval(elem["m"]) #convert string json key:value data to python dict
        img_url = image_info["murl"]
        links.append(img_url)
    return links

def intro():
    print("$"*37)
    print("$"*10, "IMAGE EXTRACTOR", "$"*10)
    print("$"*37)
    print("\nAUTHOR: SHAIKH AQUIB\n")

def outro():
    print("Bye :)")

def main():
    """Main routine."""
    # it is necessary to spoof user agent otherwise bing might reject requests
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    request_header = {"user-agent":USER_AGENT}

    img_count = 1

    intro()

    # Start the main process
    while (1):
        print("*** enter q to quit ***")
        term = input("Enter the search term: ")
    
        if term == "q":
            outro()
            break

        img_count = int(input("How many images do you want? (1-35): "))

        response = requests.get(
            url = f"https://www.bing.com/images/search?q={term}&safeSearch=off",
            headers = request_header
            )

        # If the request is not sucessful then skip
        if (response.status_code != 200):
            print(f"[!] Error: request for {term} returned with {response.status_code}")
            continue

        # parse the HTML source
        soup = BeautifulSoup(response.content, "html.parser")
        image_urls = extract_links_from_soup(soup)
        total_images = len(image_urls)

        for i in range(0, img_count):
            # break if total images have been read from list
            if (i >= total_images):
                break

            url = image_urls[i]
            print(f"[+] Extracting image #{i+1}")
            status = write_image_from_link(url)
            if status == 1:
                print("[!] Failed")
            

if __name__ == "__main__":
    main()