from newspaper import Article
from bs4 import BeautifulSoup
import requests

vnexpress_category = {
    'Thời sự': 'https://vnexpress.net/thoi-su',
    'Góc nhìn': 'https://vnexpress.net/goc-nhin',
    'Thế giới': 'https://vnexpress.net/the-gioi',
    'Kinh doanh': 'https://vnexpress.net/kinh-doanh',
    'Giải trí': 'https://vnexpress.net/giai-tri',
    'Thể thao': 'https://vnexpress.net/the-thao', 
    'Pháp luật': 'https://vnexpress.net/phap-luat', 
    'Giáo dục': 'https://vnexpress.net/giao-duc', 
    'Sức khỏe': 'https://vnexpress.net/suc-khoe',
    'Đời sống': 'https://vnexpress.net/doi-song', 
    'Du lịch': 'https://vnexpress.net/du-lich',
    'Khoa học': 'https://vnexpress.net/khoa-hoc',
    'Số hóa': 'https://vnexpress.net/so-hoa',
    'Xe': 'https://vnexpress.net/oto-xe-may',
    'Ý kiến': 'https://vnexpress.net/y-kien',
    'Tâm sự': 'https://vnexpress.net/tam-su' 
}

def get_article_url(category):
    start_url = vnexpress_category[category]
    r = requests.get(start_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    article_url = soup.select_one('article div a')['href']
    return article_url

def get_article(category):
    article_url = get_article_url(category)
    print(article_url)
    # get_article = {
    #     'title': '',
    #     'content': '',
    #     'url': ''
    # }
    # article = Article(article_url)
    # article.download()
    # article.html
    # article.parse()
    # get_article['title'] = article.title 
    # get_article['content'] = article.text
    # get_article['url'] = article_url
    # return get_article

    article_data_dict = {
        'url': '',
        'title': '', 
        'content': ''
    }
    r = requests.get(article_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    article_data_dict['url'] = article_url

    titles = soup.find_all('h1', class_='title_news_detail')
    contents = soup.find_all('p', class_='Normal')

    title_data = ''
    for title in titles:
        title_data = title_data + title.text.replace('\n', '').replace('\t', '')
    article_data_dict['title'] = title_data
        
    content_data = ''
    for content in contents:
        content_data = content_data + content.text.replace('\xa0', ' ').replace('\t', '') + ' '
    content_data = content_data.translate({ord(c): ' ' for c in "!@#$%^&*()[]{};:,<>?\|`~-=_+"})
    article_data_dict['content'] = content_data
    print(article_data_dict)
    return article_data_dict


