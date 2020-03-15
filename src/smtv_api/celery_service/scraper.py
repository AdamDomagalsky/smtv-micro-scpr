import requests
from bs4 import BeautifulSoup as BS

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
ROOT_FS = '/fstorage'


class Scraper:
    def __init__(self, scrape_id, scrape_text = True, scrape_images = False):
        self.scrape_text = scrape_text
        self.scrape_images = scrape_images
        self.scrape_id = scrape_id
        self.visited = set()
        self.session = requests.Session()
        self.session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}

        requests.packages.urllib3.disable_warnings()  # turn off SSL warnings

    def visit_url(self, url, level):
        print(url)
        if url in self.visited:
            return

        self.visited.add(url)

        content = self.session.get(url, verify=False).content
        soup = BS(content)
        # soup = BS(content, "lxml")

        if self.scrape_images:
            for img in soup.select("img[src]"):
                image_url = img["src"]
                if not image_url.startswith(("data:image", "javascript")):
                    self.download_image(urljoin(url, image_url))

            if level > 0:
                for link in soup.select("a[href]"):
                    self.visit_url(urljoin(url, link["href"]), level - 1)

        if self.scrape_text:
            self.download_text(soup)

        # saving all urls visited to file
        with open(f'{ROOT_FS}/{self.scrape_id}.urls_visited','w+') as f_urls:
            urls = '\n'.join(self.visited)
            f_urls.write(urls)


    def download_image(self, image_url):
        local_filename = image_url.split('/')[-1].split("?")[0]

        r = self.session.get(image_url, stream=True, verify=False)
        with open(f'{ROOT_FS}/{local_filename}', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)


    def download_text(self, soup):
        with open(f'{ROOT_FS}/{self.scrape_id}.txt','w+') as f_txt:

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            f_txt.write(text)