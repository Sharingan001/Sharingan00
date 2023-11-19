import sys
import requests
from bs4 import BeautifulSoup
import os
import time
import random
from headers.agents import Headers
from tkinter import *
from tkinter import scrolledtext
from banner.banner import Banner

class Colors:
    # Console colors
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple
    C = '\033[36m'  # cyan
    GR = '\033[37m'  # gray
    BOLD = '\033[1m'
    END = '\033[0m'

class Configuration:
    DARKDUMP_ERROR_CODE_STANDARD = -1
    DARKDUMP_SUCCESS_CODE_STANDARD = 0

    DARKDUMP_MIN_DATA_RETRIEVE_LENGTH = 1
    DARKDUMP_RUNNING = False
    DARKDUMP_OS_UNIX_LINUX = False
    DARKDUMP_OS_WIN32_64 = False
    DARKDUMP_OS_DARWIN = False

    DARKDUMP_REQUESTS_SUCCESS_CODE = 200
    DARKDUMP_PROXY = False

    descriptions = []
    urls = []

    __darkdump_api__ = "https://ahmia.fi/search/?q="
    __proxy_api__ = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite"

class Proxies(object):
    def __init__(self):
        self.proxy = {}

    def assign_proxy(self):
        req = requests.get(Configuration.__proxy_api__)
        if req.status_code == Configuration.DARKDUMP_REQUESTS_SUCCESS_CODE:
            for line in req.text.splitlines():
                if line:
                    proxy = line.split(':')
                    self.proxy["http"] = "http://" + proxy[0] + ':' + proxy[1]
        else:
            pass
    
    def get_proxy(self):
        return self.proxy["http"]

    def get_proxy_dict(self):
        return self.proxy

class Darkdump(object):
    def crawl(self, query, amount, verbose=False):
        clr = Colors()
        prox = Proxies()

        headers = random.choice(Headers().useragent)
        if Configuration.DARKDUMP_PROXY:
            prox.assign_proxy()
            proxy = prox.get_proxy()
            if verbose:
                print(clr.BOLD + clr.P + "~:~ Using Proxy: " + clr.C + proxy + clr.END + '\n')
            page = requests.get(Configuration.__darkdump_api__ + query, proxies=prox.get_proxy_dict())
        else:
            page = requests.get(Configuration.__darkdump_api__ + query)
        page.headers = headers

        if verbose:
            print(clr.BOLD + clr.G + f"Request URL: {page.url}\n" +
                  f"Response Status Code: {page.status_code}\n" +
                  f"Response Headers: {page.headers}\n" +
                  f"Response Content: {page.text}\n" +
                  clr.END)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='ahmiaResultsPage')
        second_results = results.find_all('li', class_='result')
        res_length = len(second_results)

        Configuration.descriptions = []
        Configuration.urls = []

        for iterator in range(res_length):
            Configuration.descriptions.append(second_results[iterator].find('p').text)
            Configuration.urls.append(second_results[iterator].find('cite').text)
        # Remove duplicates
        Configuration.descriptions = list(dict.fromkeys(Configuration.descriptions))
        Configuration.urls = list(dict.fromkeys(Configuration.urls))
        try:
            if len(Configuration.descriptions) >= Configuration.DARKDUMP_MIN_DATA_RETRIEVE_LENGTH:
                for iterator in range(amount):
                    site_url = Configuration.urls[iterator]
                    site_description = Configuration.descriptions[iterator]
                    print(clr.BOLD + clr.G + f"[+] Website: {site_description}\n\t> Onion Link: {clr.R}{site_url}\n" +
                          clr.END)
            else:
                print(clr.BOLD + clr.R + "[!] No results found." + clr.END)
        except IndexError as ie:
            print(clr.BOLD + clr.O + f"[~] No more results to be shown ({ie}): " + clr.END)

class DarkdumpGUI:
    def __init__(self, master):
        self.master = master
        master.title("Darkdump GUI")

        self.query_label = Label(master, text="Enter Query:")
        self.query_label.pack()

        self.query_entry = Entry(master)
        self.query_entry.pack()

        self.amount_label = Label(master, text="Enter Amount of searches:")
        self.amount_label.pack()

        self.amount_entry = Entry(master)
        self.amount_entry.pack()

        self.verbose_var = IntVar()
        self.verbose_checkbox = Checkbutton(master, text="Verbose Mode", variable=self.verbose_var)
        self.verbose_checkbox.pack()

        self.search_button = Button(master, text="Search", command=self.search)
        self.search_button.pack()

        self.result_text = scrolledtext.ScrolledText(master, width=80, height=20, wrap=WORD)
        self.result_text.pack()

    def search(self):
        query = self.query_entry.get()
        amount = int(self.amount_entry.get())
        verbose = bool(self.verbose_var.get())

        darkdump = Darkdump()
        darkdump.crawl(query, amount, verbose)
        
        # Append the results to the GUI text area
        for description, url in zip(Configuration.descriptions, Configuration.urls):
            result = f"Website: {description}\nOnion Link: {url}\n\n"
            self.result_text.insert(INSERT, result)

if __name__ == "__main__":
    root = Tk()
    gui = DarkdumpGUI(root)
    root.mainloop()
import sys
import requests
from bs4 import BeautifulSoup
import os
import time
import random
from headers.agents import Headers
from tkinter import *
from tkinter import scrolledtext
from banner.banner import Banner

class Colors:
    # Console colors
    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple
    C = '\033[36m'  # cyan
    GR = '\033[37m'  # gray
    BOLD = '\033[1m'
    END = '\033[0m'

class Configuration:
    DARKDUMP_ERROR_CODE_STANDARD = -1
    DARKDUMP_SUCCESS_CODE_STANDARD = 0

    DARKDUMP_MIN_DATA_RETRIEVE_LENGTH = 1
    DARKDUMP_RUNNING = False
    DARKDUMP_OS_UNIX_LINUX = False
    DARKDUMP_OS_WIN32_64 = False
    DARKDUMP_OS_DARWIN = False

    DARKDUMP_REQUESTS_SUCCESS_CODE = 200
    DARKDUMP_PROXY = False

    descriptions = []
    urls = []

    __darkdump_api__ = "https://ahmia.fi/search/?q="
    __proxy_api__ = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=elite"

class Proxies(object):
    def __init__(self):
        self.proxy = {}

    def assign_proxy(self):
        req = requests.get(Configuration.__proxy_api__)
        if req.status_code == Configuration.DARKDUMP_REQUESTS_SUCCESS_CODE:
            for line in req.text.splitlines():
                if line:
                    proxy = line.split(':')
                    self.proxy["http"] = "http://" + proxy[0] + ':' + proxy[1]
        else:
            pass
    
    def get_proxy(self):
        return self.proxy["http"]

    def get_proxy_dict(self):
        return self.proxy

class Darkdump(object):
    def crawl(self, query, amount, verbose=False):
        clr = Colors()
        prox = Proxies()

        headers = random.choice(Headers().useragent)
        if Configuration.DARKDUMP_PROXY:
            prox.assign_proxy()
            proxy = prox.get_proxy()
            if verbose:
                print(clr.BOLD + clr.P + "~:~ Using Proxy: " + clr.C + proxy + clr.END + '\n')
            page = requests.get(Configuration.__darkdump_api__ + query, proxies=prox.get_proxy_dict())
        else:
            page = requests.get(Configuration.__darkdump_api__ + query)
        page.headers = headers

        if verbose:
            print(clr.BOLD + clr.G + f"Request URL: {page.url}\n" +
                  f"Response Status Code: {page.status_code}\n" +
                  f"Response Headers: {page.headers}\n" +
                  f"Response Content: {page.text}\n" +
                  clr.END)

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='ahmiaResultsPage')
        second_results = results.find_all('li', class_='result')
        res_length = len(second_results)

        Configuration.descriptions = []
        Configuration.urls = []

        for iterator in range(res_length):
            Configuration.descriptions.append(second_results[iterator].find('p').text)
            Configuration.urls.append(second_results[iterator].find('cite').text)
        # Remove duplicates
        Configuration.descriptions = list(dict.fromkeys(Configuration.descriptions))
        Configuration.urls = list(dict.fromkeys(Configuration.urls))
        try:
            if len(Configuration.descriptions) >= Configuration.DARKDUMP_MIN_DATA_RETRIEVE_LENGTH:
                for iterator in range(amount):
                    site_url = Configuration.urls[iterator]
                    site_description = Configuration.descriptions[iterator]
                    print(clr.BOLD + clr.G + f"[+] Website: {site_description}\n\t> Onion Link: {clr.R}{site_url}\n" +
                          clr.END)
            else:
                print(clr.BOLD + clr.R + "[!] No results found." + clr.END)
        except IndexError as ie:
            print(clr.BOLD + clr.O + f"[~] No more results to be shown ({ie}): " + clr.END)

class DarkdumpGUI:
    def __init__(self, master):
        self.master = master
        master.title("Darkdump GUI")

        self.query_label = Label(master, text="Enter Query:")
        self.query_label.pack()

        self.query_entry = Entry(master)
        self.query_entry.pack()

        self.amount_label = Label(master, text="Enter Amount:")
        self.amount_label.pack()

        self.amount_entry = Entry(master)
        self.amount_entry.pack()

        self.verbose_var = IntVar()
        self.verbose_checkbox = Checkbutton(master, text="Verbose Mode", variable=self.verbose_var)
        self.verbose_checkbox.pack()

        self.search_button = Button(master, text="Search", command=self.search)
        self.search_button.pack()

        self.result_text = scrolledtext.ScrolledText(master, width=1200, height=700, wrap=WORD)
        self.result_text.pack()

    def search(self):
        query = self.query_entry.get()
        amount = int(self.amount_entry.get())
        verbose = bool(self.verbose_var.get())

        darkdump = Darkdump()
        darkdump.crawl(query, amount, verbose)
        
        # Append the results to the GUI text area
        for description, url in zip(Configuration.descriptions, Configuration.urls):
            result = f"Website: {description}\nOnion Link: {url}\n\n"
            self.result_text.insert(INSERT, result)

if __name__ == "__main__":
    root = Tk()
    gui = DarkdumpGUI(root)
    root.mainloop()

