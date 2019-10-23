from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import pickle

def store_data(model_links):
    dbfile = open('model_links', 'wb')
    pickle.dump(model_links, dbfile)
    dbfile.close()


def get_pg_links():
    pg_links = []
    for i in range(1,15):
        link = base_pg_link+str(i)
        pg_links.append(link)
    return pg_links

def get_model_links(pg_links):
    model_links = []
    for pg_link in pg_links:
        resp = requests.get(pg_link)
        # https://www.flipkart.com/search?count=40&otracker=CLP_filters&otracker=nmenu_sub_TVs+and+Appliances_0_Smart+and+Ultra+HD&otracker=nmenu_sub_TVs+%26+Appliances_0_Smart+%26+Ultra+HD&p%5B%5D=facets.smart_tv%255B%255D%3DYes&p%5B%5D=facets.resolution%255B%255D%3DUltra%2BHD%2B%25284K%2529&sid=ckf%2Fczl&page=1
        # https://www.flipkart.com/search?count=40&otracker=CLP_filters&p%5B%5D=facets.smart_tv%255B%255D%3DYes&p%5B%5D=facets.resolution%255B%255D%3DUltra%2BHD%2B%25284K%2529&sid=ckf%2Fczl&otracker=nmenu_sub_TVs+and+Appliances_0_Smart+and+Ultra+HD&otracker=nmenu_sub_TVs+%26+Appliances_0_Smart+%26+Ultra+HD&page=2
        http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
        html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
        encoding = html_encoding or http_encoding
        soup = BeautifulSoup(resp.content, from_encoding=encoding)
        cnt_models = 0
        for link in soup.find_all('a', href=True):
            l = link['href']
            if("-tv" in l):
                cnt_models+=1
                model = "https://www.flipkart.com"+l
                model_links.append(model)
                print(l)
        print(cnt_models)
    print("len_mdl",len(model_links))
    return model_links
# import httplib2
# from bs4 import BeautifulSoup, SoupStrainer
#
# http = httplib2.Http()
# status, response = http.request('http://www.nytimes.com')
#
# for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
#     if link.has_attr('href'):
#         print(link['href'])

if __name__ == '__main__':
    base_pg_link = "https://www.flipkart.com/search?count=40&otracker=CLP_filters&otracker=nmenu_sub_TVs+and+Appliances_0_Smart+and+Ultra+HD&otracker=nmenu_sub_TVs+%26+Appliances_0_Smart+%26+Ultra+HD&p%5B%5D=facets.smart_tv%255B%255D%3DYes&p%5B%5D=facets.resolution%255B%255D%3DUltra%2BHD%2B%25284K%2529&sid=ckf%2Fczl&page="
    pg_links = get_pg_links()
    model_links = get_model_links(pg_links)
    # store_data(model_links)