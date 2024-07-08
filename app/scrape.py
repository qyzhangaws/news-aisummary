from cgitb import html
import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from datetime import date

class  ScrapeBitCoin:
    def __init__(self, base_url):
        self.base_url = base_url

    # extract links from category sublink
    def extract_links(self, category_name, category_sublink):
        html_body = None
        category_url = f"{self.base_url}{category_sublink}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--disable-gpu", "--single-process"])
            page = browser.new_page()
            page.set_default_timeout(120000)

            print("beginning to scrape: " + str(datetime.datetime.now()))
            page.goto(category_url)
            page.wait_for_load_state("networkidle")
            print("end to waiting for scrape: " + str(datetime.datetime.now()))
        
            html_body = page.inner_html("body")
            browser.close()

        if not html_body:
            return None
        
        # Parse the HTML content
        soup = BeautifulSoup(html_body, "html.parser")

        # Extract all links under 
        articles_links = []
        div_elements = soup.find_all("div", class_="sc-iUsXpp kcpyVT")   
        for div in div_elements:
            article_element = div.find("a", class_="sc-curcqj eBZSow")
            article_attrs = div.find("p", "sc-iMUcOm icqriC").get_text(strip=True)
            article_attr_publish = article_attrs.split("|")[-1].strip()
            article_attr_publish_pattern = r'(\d+)\s*hours?\s*ago'
            article_attr_publish_withinday = re.search(article_attr_publish_pattern, article_attr_publish)
            if not article_attr_publish_withinday: 
                break
     
            link = self.base_url + article_element.get("href")
            publish_date = date.today().isoformat()
            articles_links.append(
                {
                    "link": link,
                    "publish_date": publish_date
                }
            )
            
        return articles_links

    def scrape_article(self, link):
        html_content = self._scrape_html_body(link["link"])
        return self._extract_content_text(html_content, link["publish_date"])
        
    def _scrape_html_body(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--disable-gpu", "--single-process"])
            page = browser.new_page()
            page.set_default_timeout(120000)

            print("beginning to scrape: " + str(datetime.datetime.now()))
            page.goto(url,)
            page.wait_for_load_state("networkidle")
            print("end to waiting for scrape: " + str(datetime.datetime.now()))
        
            html_body = page.inner_html("body")
            browser.close()
            return html_body

    def _extract_content_text(self, html_content, publish_date):
        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Extract the article title
        title = soup.find("h1", class_="sc-jhwbPl iDuNAH").text.strip()

        # Extract the article body
        article_body = soup.find("div", class_="article__body")
        article_text = article_body.get_text(strip=True, separator="\n")

        # Extract the author name
        author_name = soup.find("h5", class_="sc-gsqrwE sc-irCEUn hocceF hoVGXL").text.strip()

        return {
            "title": title,
            "content": article_text,
            "author": author_name,
            "date": publish_date,
        }



