import csv
from datetime import datetime
import os.path

import requests as r
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
import time


class MainParser:
    def __init__(self, config):
        self.ua = UserAgent()
        self.main_link = config["main_link"]
        self.link = config["link"]
        self.file_name = config["file_name"]
        if config["proxy_pass"]:
            self.proxies = config["proxies"]
        else:
            self.proxies = {}

    def init_parser(self):
        page = 1
        news = 0
        parsed_data = []

        try:
            while True:
                resp = r.get(
                    f"{self.link}{page}",
                    headers={
                        'Connection': 'keep-alive',
                        'User-Agent': self.ua.chrome,
                        'Cache-Control': 'max-age=0, no-cache, no-store',
                        'Pragma': 'no-cache'
                    },
                    proxies=self.proxies,
                )
                print(f"Response status: {resp}")

                resp_content = resp.content

                parsed_html = BS(resp_content, 'html.parser')
                lines = parsed_html.select(".article-list > .no-style")

                if len(lines):
                    for line in lines:
                        parsed_data.append(
                            {
                                "Title": line.span.text,
                                "Add date": line.find('div', attrs={'class': 'article-item-date'}).text,
                                "Pars date": datetime.now().strftime("%H:%M:%S %d-%m-%Y"),
                                "URL": f"{self.main_link}{line.get('href')}"
                            }
                        )
                        news += 1
                    page += 1
                else:
                    break

            print(f"Total pages - {page - 1}")
            print(f"Total news - {news}")
            print("_____________________________________________________\n")

            return self.csv_rw(parsed_data)
        except Exception as error:
            print(f"Error with request: {error}")

    def live_parser(self):
        req_count = 0
        try:
            while True:
                anti_cache = str(time.time())
                resp = r.get(
                    f"{self.link}1&some_stuff={anti_cache}",
                    headers={
                        'Connection': 'keep-alive',
                        'User-Agent': self.ua.chrome,
                        'Cache-Control': 'max-age=0, no-cache, no-store',
                        'Pragma': 'no-cache'
                    },
                    proxies=self.proxies,
                )

                resp_content = resp.content

                parsed_html = BS(resp_content, 'html.parser')
                lines = parsed_html.select(".article-list > .no-style")

                parsed_data = []

                for line in lines:
                    parsed_data.append(
                        {
                            "Title": line.span.text,
                            "Add date": line.find('div', attrs={'class': 'article-item-date'}).text,
                            "Pars date": datetime.now().strftime("%H:%M:%S %d-%m-%Y"),
                            "URL": f"{self.main_link}{line.get('href')}"
                        }
                    )
                req_count += 1
                time.sleep(1)
                print(f"Response status: {resp}. Total requests: {req_count}")
                self.csv_rw(parsed_data)
        except Exception as error:
            print(f"Error with request: {error}")

    def csv_rw(self, parsed_data):
        total_rows_added = 0
        row_names = ["Title", "Add date", "Pars date", "URL"]
        if not os.path.isfile(self.file_name):
            try:
                with open(self.file_name, mode="w", encoding='utf-8') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, delimiter=",", lineterminator="\r", fieldnames=row_names)
                    csv_writer.writeheader()
                    for data in parsed_data:
                        csv_writer.writerow(
                            {
                                "Title": data["Title"],
                                "Add date": data["Add date"],
                                "Pars date": data["Pars date"],
                                "URL": data["URL"]
                            }
                        )
                        total_rows_added += 1
                print(f"File successfully created!")
                print(f"Total rows added in file: {total_rows_added}")
            except Exception as error:
                print(f"Error while creating file: {error}")

        else:
            total_new_news = 0
            csv_news_titles = []
            new_news = []
            try:
                with open(self.file_name, mode="r", encoding='utf-8') as csv_file:
                    csv_reader = csv.DictReader(csv_file, delimiter=",")
                    for row in csv_reader:
                        csv_news_titles.append(row["Title"])
                for data in parsed_data:
                    if not data["Title"] in csv_news_titles:
                        new_news.append(data)
                if len(new_news):
                    with open(self.file_name, mode="a", encoding='utf-8') as csv_file:
                        csv_writer = csv.DictWriter(csv_file, delimiter=",", lineterminator="\r", fieldnames=row_names)
                        for news in new_news:
                            csv_writer.writerow(
                                {
                                    "Title": news["Title"],
                                    "Add date": news["Add date"],
                                    "Pars date": news["Pars date"],
                                    "URL": news["URL"]
                                }
                            )
                            total_new_news += 1
                print(f"Total new news added: {total_new_news}")
            except Exception as error:
                print(f"Error while updating file: {error}")
