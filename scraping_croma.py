import pickle
import re
import requests
import random as randi
from bs4 import BeautifulSoup
import unidecode

URL = "https://www.croma.com/tcl-127-cm-50-inch-4k-ultra-hd-led-smart-tv-black-50p8e-/p/220899"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
r = requests.get(URL,headers=headers)

def write_to_file(text, name, set=False):
    if (not set):
        # Writing items which require utf-8 encoding
        f1 = open(name, 'wb')
        text = text.encode("utf-8")
    else:
        # Writing items which do not require utf-8 encoding
        f1 = open(name, 'w')
        text = str(text)

    f1.write(text)
    f1.close()


def write_pairs_to_file(pairs, name):
    features = pairs[0]
    values = pairs[1]
    m = len(features)
    f1 = open(name, 'w')
    for i in range(m):
        cur = [features[i],values[i]]
        size = len(cur)
        s = "Feature: " + "\t" + str(cur[0])  # Size =1
        if size == 2:
            s += ("\n" + "Value: " + "\t" + str(cur[1]))
        s += "\n"
        f1.write(s)

def to_file(text):
    f1 = open("test.txt","w")
    f1.write(text)

def get_feat_val_pairs(soup):
    master_table = soup.findAll('div',class_="info-block")
    # print(master_table[0])
    feature_set = []
    value_set = []
    for headline in master_table:
        attr = headline.find_all(class_='attrib')
        for i in range(len(attr)):
            cur_attr_text = attr[i].text.strip()
            re.sub(r"\s+", " ", cur_attr_text)
            feature_set.append(cur_attr_text)
        attr_val = headline.find_all('span',class_='attribvalue')
        for i in range(len(attr_val)):
            cur_attr_val_text = attr_val[i].text.strip(' \t\n\r')
            # removes tabs and newlines from given string
            cur_attr_val_text = re.sub(r"\s+", " ", cur_attr_val_text)
            value_set.append(cur_attr_val_text)
    return feature_set,value_set
    # print(feature_set,value_set)


def store_data(pairs):
    dbfile = open('croma_model1_bin', 'wb')
    pickle.dump(pairs, dbfile)
    dbfile.close()


if __name__ == '__main__':
    soup = BeautifulSoup(r.content, 'html5lib')
    text = soup.prettify()
    write_to_file(text, "data.txt")
    features,values = get_feat_val_pairs(soup)
    pairs = [features,values]
    store_data(pairs)
    write_pairs_to_file(pairs,"croma_model1")
    store_data(pairs)