__author__ = 'bangnguyen'
import json
import time
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import xlsxwriter
SIZE = 1000
AGO = 48
MAIL_TO = ["bang.nguyenviet@nttdata.com","jtman95@gmail.com"]


"""
MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = '587'
MAIL_FROM = 'bang2606@gmail.com'
MAIL_PASS = 'xyz'
"""
MAIL_HOST = 'mail.ifisolution.com'
MAIL_PORT = '587'
MAIL_FROM = 'nguyenvb@ifisolution.com'
MAIL_PASS = 'Abcd@1234'

def get_mailer():
    mailer = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
    mailer.ehlo()
    if 'gmail' in MAIL_HOST:
        mailer.starttls()
    mailer.ehlo()
    mailer.login(MAIL_FROM, MAIL_PASS)
    return mailer


def hightlight_to_text(data):
    result = ""
    for d in data:
        result += "%s \n" % (d)
    return result


def clean_text(text):
    return text.strip().lower()


def hit_to_comment(hit):
    source = hit['_source']
    date_string = datetime.datetime.fromtimestamp(source['date_time']).strftime('%H:%M:%S %d/%m/%Y')
    highlight = hightlight_to_text(hit['highlight']['content'])
    link = source['link']
    website = source['website']
    source['date_string'] = date_string
    source['highlight'] = highlight
    source['link'] = link
    source['website'] = website
    return source


def unique_list(hits):
    unique = {}
    for hit in hits:
        comment = hit_to_comment(hit)
        hlk = comment['highlight']
        if hlk in unique.keys():
            if comment['date_time'] > unique[hlk]['date_time']:
                unique[hlk] = comment
        else:
            unique[hlk] = comment
    data = unique.values()
    data.sort(key=lambda x: x['date_time'], reverse=True)
    return data


def write_to_csv(comments):
    file_name = 'output.xlsx'
    workbook = xlsxwriter.Workbook('output.xlsx')
    worksheet = workbook.add_worksheet()
    for id, cl in enumerate(['Highlight', 'Date', 'Original Link', 'Website']):
        worksheet.write(0, id, cl)
    row = 1
    for comment in comments:
        worksheet.write(row, 0, comment['highlight'])
        worksheet.write(row, 1, comment['date_string'])
        worksheet.write(row, 2, comment['link'])
        worksheet.write(row, 3, comment['website'])
        row += 1
    workbook.close()
    return file_name


def send(msg, mail_to):
    mailer = get_mailer()
    mailer.sendmail(MAIL_FROM, [mail_to], msg.as_string())
    mailer.quit()


def send_email(comments, mail_to):
    today = datetime.date.today()
    msg = MIMEMultipart()
    msg['From'] = MAIL_FROM
    msg['To'] = mail_to
    msg['Subject'] = "Result crawled data for %s" % (today.strftime('%d/%m/%Y'))
    html = "<style>em {color:red}; tr { line-height: 24px; }</style>"
    html += "<table>"
    for id, comment in enumerate(comments):
        html += "<tr> <td style='vertical-align: top'><b>%s</b></td>   <td style='width:800px'>%s</td> <td>%s</td> <td><a href='%s'>Click here</a></td>  <td>%s</td></tr>" % (
            id + 1,
            comment['highlight'], comment['date_string'], comment['link'], comment['website'])
    html += "</table>"
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    send(msg, mail_to)


def send_email_current_status():
    print "send_current_status"
    msg = MIMEMultipart()
    msg['From'] = MAIL_FROM
    msg['To'] = MAIL_TO
    msg['Subject'] = 'Skilledup Scraper : Current Status of scraper '

    send(msg)




def start_job():
    url = 'http://127.0.0.1:9200/joe/comments/_search'
    # url = 'http://localhost:9200/joe/comments/_search'
    #url = 'http://keywordstool.co:9200/joe/comments/_search'
    one_days_ago = int(time.time()) - AGO * 3600
    date = "16/10/2014"
    parameters = [
        "Lupanzula",
        "Medikemos",
        "brussels",
        "bhatti",
        "darling buds",
        "cooley",
        "charlotte",
        "north carolina",
        "dr. k",
        "karadeniz",
        "turkey",
        "tillman",
        "joe",
        "joe tillman",
        "jotronic",
        "joetronic",
        "mentor"
    ]

    final_params = []
    for para in parameters:
        final_params.append({"match_phrase": {"content": para.strip()}})
    query = {
        "sort": [
            {"date_time": {"order": "desc"}}
        ],
        "query": {
            "bool": {
                "should": final_params
            }
        },
        "filter": {
            "range": {"date_time": {
                "gte": one_days_ago}
                      }
        },
        "highlight": {
            "fields": {
                "content": {}
            }
        },
        "size": SIZE
    }
    resp = requests.post(url, data=json.dumps(query))
    data = resp.json()
    print "len before %s " % (len(data['hits']['hits']))
    comments = unique_list(data['hits']['hits'])
    print "len after  %s " % (len(comments))
    for e in MAIL_TO:
        send_email(comments, e)


