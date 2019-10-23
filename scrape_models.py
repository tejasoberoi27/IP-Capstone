import pickle

import requests
import random as randi
from bs4 import BeautifulSoup
import importlib

# import link_find



# URL = "https://www.flipkart.com/lg-108cm-43-inch-ultra-hd-4k-led-smart-tv/p/itma1038b75c4b3f?pid=TVSFJY52G4XYG7TA&srno=b_1_4&otracker=browse&lid=LSTTVSFJY52G4XYG7TA13WKXK&fm=organic&iid=4b979445-3b1b-4f1d-a451-67c3ca4cf7c6.TVSFJY52G4XYG7TA.SEARCH&ssid=986ztb6erk0000001569949096511https://www.flipkart.com/lg-108cm-43-inch-ultra-hd-4k-led-smart-tv/p/itma1038b75c4b3f?pid=TVSFJY52G4XYG7TA&srno=b_1_4&otracker=browse&lid=LSTTVSFJY52G4XYG7TA13WKXK&fm=organic&iid=4b979445-3b1b-4f1d-a451-67c3ca4cf7c6.TVSFJY52G4XYG7TA.SEARCH&ssid=986ztb6erk0000001569949096511"
# URL = "https://www.flipkart.com/lg-108cm-43-inch-ultra-hd-4k-led-smart-tv/p/itmf7yraubnjgyzg?pid=TVSF7YRA5MZ96AC3&lid=LSTTVSF7YRA5MZ96AC3UYD2BL&marketplace=FLIPKART&fm=productRecommendation%2Fsimilar&iid=R%3As%3Bp%3ATVSFJY52G4XYG7TA%3Bl%3ALSTTVSFJY52G4XYG7TA13WKXK%3Bpt%3App%3Buid%3Aa86e00de-3972-6caa-4ee9-0b4d2c5bc04b%3B.TVSF7YRA5MZ96AC3.LSTTVSF7YRA5MZ96AC3UYD2BL&ppt=pp&ppn=pp&ssid=986ztb6erk0000001569949096511&otracker=pp_reco_Similar%2BProducts_2_32.productCard.PMU_HORIZONTAL_LG%2B108cm%2B%252843%2Binch%2529%2BUltra%2BHD%2B%25284K%2529%2BLED%2BSmart%2BTV_TVSF7YRA5MZ96AC3.LSTTVSF7YRA5MZ96AC3UYD2BL_productRecommendation%2Fsimilar_1&otracker1=pp_reco_PINNED_productRecommendation%2Fsimilar_Similar%2BProducts_GRID_productCard_cc_2_NA_view-all&cid=TVSF7YRA5MZ96AC3.LSTTVSF7YRA5MZ96AC3UYD2BL"
URL = "https://www.flipkart.com/lg-108cm-43-inch-ultra-hd-4k-led-smart-tv/p/itma1038b75c4b3f?pid=TVSFJY52G4XYG7TA&srno=b_1_22&otracker=CLP_filters&lid=LSTTVSFJY52G4XYG7TAB9CDET&fm=organic&iid=bb3d3af7-ea4c-4952-b0ef-61fc303b7bfe.TVSFJY52G4XYG7TA.SEARCH&ssid=kwpy3ky3340000001571861188037"
r = requests.get(URL)

def store_data(models_tables):
    dbfile = open('models_tables', 'wb')
    pickle.dump(models_tables, dbfile)
    dbfile.close()

def load_data_links():
    dbfile = open('model_links', 'rb')
    model_links = pickle.load(dbfile)
    dbfile.close()
    return model_links

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
    m = len(pairs)
    f1 = open(name, 'w')
    for i in range(m):
        cur = pairs[i]
        size = len(cur)
        # print("cur", cur)
        s = "Feature: " + "\t" + str(cur[0])  # Size =1
        if size == 2:
            s += ("\n" + "Value: " + "\t" + str(cur[1]))
        s += "\n"
        f1.write(s)

def get_universe_pairs_model(URL):
    #returns feature-value list of tv model corresponding to URL
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    text = soup.prettify()
    write_to_file(text, "data.txt")
    master_table = soup.findAll("table", attrs={"class": "_3ENrHu"})
    num_table = len(master_table)
    universe_pairs = []
    for i in range(num_table):
        # print("Table No. ", i)
        gdp_table = master_table[i]
        gdp_table_data = gdp_table.tbody.find_all("tr")
        headings = []
        write_to_file(gdp_table_data, "rows.txt", True)

        feature_value_pairs = []
        l = len(gdp_table_data)
        for i in range(l):
            feature = []
            cnt_feature = 1
            for td in gdp_table_data[i].find_all("td"):
                # if cnt_feature == 1:
                    # print()
                    # print("Feature: ")
                # else:
                    # print()
                    # print("Value: ")
                # print(td.text, end=" ")
                feature.append(td.text)
                cnt_feature *= -1

            feature_value_pairs.append(feature)

        write_to_file(feature_value_pairs, "final_pairs.txt", True)
        universe_pairs.extend(feature_value_pairs)
    return universe_pairs

def pilot(model_links):
    #returns feature-value lists of all the models
    models_tables = []
    cnt = 0
    for url in model_links:
        cnt+=1
        print(cnt)
        table = get_universe_pairs_model(url)
        models_tables.append(table)
    return models_tables

def test_model_tables(models_tables):
    write_pairs_to_file(models_tables[0], "Universe_pairs_0.txt")

if __name__ == '__main__':
    model_links = load_data_links()
    models_tables = pilot(model_links)
    test_model_tables(models_tables)
    store_data(models_tables)

    # print()
    # print("rows", len(universe_pairs))
    # print("cols", len(universe_pairs[0]))
    # write_pairs_to_file(universe_pairs, "Universe_pairs.txt")
