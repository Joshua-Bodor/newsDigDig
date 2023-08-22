import argparse
import os
import requests
from datetime import date
from bs4 import BeautifulSoup

# Base URL of the website
base_url = "https://newsdig.tbs.co.jp/"


# Function to fetch and parse the content of a URL
def get_parsed_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        return None


# Function to scrape and save article text
def scrape_and_save_article(article_url, save_path):
    article_soup = get_parsed_page(article_url)
    if article_soup:
        paragraphs = article_soup.find("main").find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs if p.get_text().strip())
        if text:
            article_number = article_url.split("/")[-1].split("?")[0]
            with open(os.path.join(save_path, f"{article_number}.txt"), 'w', encoding='utf8') as file:
                file.write(text)


# Main scraping function
def scrape(download_path):
    menu_url = base_url
    menu_page = get_parsed_page(menu_url)

    if menu_page:
        menu_bar = menu_page.find("div", {"class": "g-menu-wrap"}).find("ul")
        menu_items = menu_bar.find_all("li", {"class": "g-menu-main"})

        for item in menu_items:
            href = item.find("a")["href"]
            genre = href.split('/')[-1]
            genre_url = base_url + href
            genre_page = get_parsed_page(genre_url)

            if genre_page:
                articles = genre_page.find_all("article")
                for article in articles:
                    article_url = base_url + article.find("a")["href"]
                    save_folder = os.path.join(download_path, genre, date.today().strftime("%Y_%m_%d"))
                    os.makedirs(save_folder, exist_ok=True)
                    scrape_and_save_article(article_url, save_folder)
                    print(f"Saved article from {article_url} to {save_folder}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--download_directory", help='Path to save scraped data in.')
    args = parser.parse_args()

    scrape(args.download_directory)


if __name__ == "__main__":
    main()
