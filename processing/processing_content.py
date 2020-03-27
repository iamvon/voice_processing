import re 

def get_sentences(content):
    split_sentences_regex = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
    list_sentences = []
    list_sentences = re.split(split_sentences_regex, content)
    sentences = [sentence.replace('\n', ' ').strip().replace('  ', ' ') for sentence in list_sentences]
    get_sentences = list(filter(None, sentences)) 
    return get_sentences 