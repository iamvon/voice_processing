import ast
from flask import Flask, request, render_template, Response
import jsonpickle
from crawler import crawl_vnexpress  
from processing import processing_content 
from record import voice_record

app = Flask(__name__)

@app.route('/', methods=['GET'])    
def home():
    return render_template('index.html')

@app.route('/api/article', methods=['GET', 'POST'])
def get_article_sentences():
    article = {
        'title': '',
        'url': '',
        'sentences': [],
        'total_sentences': ''
    }
    print(request.get_json())
    request_category = request.get_json()['category']
    # print(request_category)
    get_article = crawl_vnexpress.get_article(request_category)
    print(get_article)
    # print(article_content)
    article_sentences = processing_content.get_sentences(get_article['content'])
    article['title'] = get_article['title']
    article['url'] = get_article['url']
    article['sentences'] = article_sentences 
    article['total_sentences'] = len(article_sentences)
    print(article)

    response_pickled = jsonpickle.encode(article)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/record', methods=['GET', 'POST'])
def record_sentence():
    request_category = request.get_json()['category']
    request_url = request.get_json()['url']
    request_sentence = request.get_json()['sentence']
    request_number = request.get_json()['number']
    request_total = request.get_json()['total']
    record_status = voice_record.record(request_category, request_url, request_sentence, request_number, request_total)
    print(record_status)
    return record_status

if __name__ == "__main__":
    app.run(debug=True)
