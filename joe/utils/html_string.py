import copy
import html2text
from scrapy.selector import Selector
import unicodedata, re, locale
"""
input : selector
extract string from start index until to end index
"""


def normalize_unicode(value, encode_ascii=True):
    if isinstance(value, unicode):
        if encode_ascii:
            return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        else:
            return unicodedata.normalize('NFKD', value)
    else:
        return value


def normalize_space(value, encode_ascii=True):
    if isinstance(value, list):
        result = []
        for i in value:
            v = normalize_space(i, encode_ascii)
            if v:
                result.append(v)
        return result
    else:
        value = ' '.join(normalize_unicode(value, encode_ascii).split()).strip()
        return value if value and len(value) > 0 else None

def substring(selector, re1, r2):
    data = selector.re(re.compile(re1 + '(.*)' + r2, re.S))
    return normalize_space(html2text.html2text(data[0])) if data else None


def html_to_text(data, encode_ascii=True):
    if data:
        result = []
        if isinstance(data, list):
            for i in data:
                try:
                    value = html2text.html2text(normalize_unicode(i, encode_ascii))
                    result.append(value)
                except:
                    log.msg("html_to_text : Ignore  character not in unicode ", level=log.INFO)
                    # try to convert unicode to text before
            result = ' '.join([normalize_space(i) for i in result if normalize_space(i)]).strip()
        else:
            data = normalize_space(html2text.html2text(data))
            result = data.strip() if data else None
        if result and len(result) > 0:
            return result
        return None



def clean_text(text):
    if text:
        text = re.sub("None,|None", '', text).strip()
        return text if text else None
    return None


def object_to_string(value):
    value_copy = copy.copy(value)
    if isinstance(value_copy, dict):
        for i in value_copy.keys():
            value_copy[i] = str(value_copy[i])[:80]
    return value_copy

