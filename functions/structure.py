import requests
from bs4 import BeautifulSoup
import tools

def structure_sprider(quire):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    path = f"https://m.chemsrc.com/mip/s/{quire}/"
    res = requests.post(path, headers=headers)
    bs = BeautifulSoup(res.text, 'html.parser')
    compounds = bs.find_all('li', class_='gb-block')

    reply_list = []
    for item in compounds:
        link = item.find('a')
        compound_name = link.get('data-title')
        compound_number = link.get('href').split('/')[-1]
        compound_link = 'https://www.chemsrc.com/cas/' + compound_number
        reply = compound_name + '\n' + compound_link
        reply_list.append(reply)

    ret = reply_list
    return ret

def structure_quire(text):
    quire_text = text.split(' ')
    if len(quire_text) == 1:
        compound = structure_sprider(text)
        reply = compound[0]
        return reply
    else:
        quire = quire_text[0]
        num = int(quire_text[-1])
        if num > 10:
            return '查询消息过多, 请少一点哦~'
        else:

            compounds = structure_sprider(quire)[:num]
            reply = '\n'.join(compounds)
            return reply



    

