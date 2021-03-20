from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import csv
import re


def create_file(file_name):
    """
    Checks if a file with the provided filename already exists. If not it creates it.
    :param file_name: str
    :return: None
    """
    try:
        f = open(file_name)
        f.close()
    except IOError:
        csv_columns = ['date', 'author', 'title', 'tags', 'link', 'text']
        with open(file_name, 'w', encoding='UTF-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter='|')
            writer.writeheader()
            csvfile.close()


def save_article(article, csv_file):
    """
    Takes a DataFrame with the articles information and appends it to the prev. created csv file
    :param article: DataFrame
    :param csv_file: str
    :return: None
    """
    csv_columns = ['date', 'author', 'title', 'tags', 'link', 'text']
    with open(csv_file, 'a', encoding='UTF-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter='|')
        # writer.writeheader()
        writer.writerow(article)
        csvfile.close()


def get_articles(page_url, csv_file):
    """
    Calls get_links and iterates through list of url and extracts article metadata and full text.
    :param page_url: list of urls
    :param csv_file: str
    """
    data = requests.get(page_url)  # url of article page
    soup = BeautifulSoup(data.content, 'html.parser')
    articles = soup.findAll('div', {'class': "container news-archive"})[0].contents[3].contents
    article_urls = []
    for j in range(1, len(articles) - 1, 2):
        article_urls.append(articles[j].contents[1].attrs['href'])
    df = pd.read_csv(csv_file, sep='|')
    for url in article_urls:
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')
        date = re.findall(r'[\d{4}]+', url)
        try:
            title = " ".join(soup.findAll('title')[0].text.split())
        except IndexError:
            title = 'No title'
        x = df.index[df.title == title]
        if len(x) == 0:
            print(title)
            full_text = soup.findAll('div', {'class': "col-md-6 blog-mobile"})
            try:
                author = full_text[0].contents[4].contents[2].contents[0]
            except IndexError:
                author = 'Unknown'
            paras = full_text[0].contents[1].contents
            text = ''
            for para in paras:
                try:
                    snippet = para.text + ' '
                    text += re.sub('\n', ' ', snippet)
                except AttributeError:
                    pass
            try:
                tags = full_text[0].contents[7].contents
                tag_list = ''
                for i in range(2, len(tags)):
                    try:
                        tag_list += tags[i].text
                        if i < len(tags) - 1:
                            tag_list += ', '
                    except AttributeError:
                        pass
            except IndexError:
                tag_list = 'No Tags'
            article = {'date': str(date[2] + '-' + date[1] + '-' + date[0]),
                       'author': author,
                       'tags': tag_list,
                       'link': url,
                       'title': title,
                       'text': text}
            save_article(article, csv_file)
        else:
            print('Duplicate: ' + title)
            pass
        time.sleep(0.2)


def scrape(csv_name):
    """
    Looks for the first article and iterates through all older articles by getting the links through the buttonthreefold process. First through years, second through months and lastly through days.
    "previous article". Extracts all articles.
    """
    # initial scraping of latest article
    url = 'https://aback-blog.iwi.unisg.ch/'
    data = requests.get(url)
    soup = BeautifulSoup(data.content, 'html.parser')
    categories = soup.findAll('div', {'class': "kategorien"})[0].contents
    for i in range(1, len(categories)-1, 2):
        url = categories[i].attrs['href']
        print(url)
        get_articles(url, csv_name)
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')
        navigation = soup.findAll('div', {'class': "navigation"})
        if len(navigation) > 0:
            k = 2
            while True:
                url_nav = url + 'page/' + str(k)
                print(url_nav)
                k += 1
                data = requests.get(url_nav)
                if data.status_code == 404:
                    break
                else:
                    get_articles(url_nav, csv_name)
    return 'Scraping done'


def main():
    # set working directory
    #os.chdir('/Users/alex/PycharmProjects/data')

    # user input at the beginning
    file_name = input('File name:\n')
    if len(file_name.split('.')) == 1:
        file_name += '.csv'

    # create file and run scraper
    create_file(file_name)
    scrape(file_name)


if __name__ == '__main__':
    main()
