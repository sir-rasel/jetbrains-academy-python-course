import sys
import os
import requests
import re
from bs4 import BeautifulSoup
from colorama import Fore

saved_pages = set()
history_stack = list()
dir_name = None
previous_page = None

def remove_last_if_current(url):
    if history_stack[-1] is url:
        history_stack.pop()

def append_in_stack(url):
    if len(history_stack) != 0:
        remove_last_if_current(url)
    history_stack.append(url)

def make_directory():
    global dir_name
    dir_name= sys.argv[1] # Collect the command line argument data
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def read_file(file_name):
    with open('{}/{}'.format(dir_name, file_name + '.txt'), 'r') as file:
        print(Fore.BLUE + file.read())

def write_file(file_name, content):
    with open('{}/{}'.format(dir_name, file_name + '.txt'), 'w') as file:
        file.write(content)

def get_absolute_url(url):
    url = url.strip()
    if url.startswith('https://') == False:
        return 'https://' + url

def get_site_name(url):
    return str(re.findall('^https://(.+)[.]...', url)[0])

def parsing(html):
    soup = BeautifulSoup(html, 'html.parser')
    tag_data = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
    data = ""
    for x in tag_data:
        data += x.get_text().strip()
    return data

def main():
    make_directory()

    while True:
        url = input('')
        if url == 'exit': break
        elif url in saved_pages:
            read_file(url)
            append_in_stack(url)
            previous_page = url
        elif url == "back":
            if len(history_stack) != 0:
                remove_last_if_current(previous_page)
            if len(history_stack) != 0:
                read_file(history_stack.pop())
        else:
            url = get_absolute_url(url)
            try :
                responce = requests.get(url)
                parse_data = parsing(responce.text)

                print(Fore.BLUE + parse_data)

                site_name = get_site_name(url)
                saved_pages.add(site_name)
                write_file(site_name, parse_data)

                append_in_stack(site_name)
                previous_page = site_name
            except:
                print("error: Invalid url")

if __name__ == '__main__':
    main()
