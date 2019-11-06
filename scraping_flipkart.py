import requests
import random as randi
from bs4 import BeautifulSoup

URL = "https://www.flipkart.com/lg-108cm-43-inch-ultra-hd-4k-led-smart-tv/p/itma1038b75c4b3f?pid=TVSFJY52G4XYG7TA&srno=b_1_4&otracker=browse&lid=LSTTVSFJY52G4XYG7TA13WKXK&fm=organic&iid=4b979445-3b1b-4f1d-a451-67c3ca4cf7c6.TVSFJY52G4XYG7TA.SEARCH&ssid=986ztb6erk0000001569949096511"
r = requests.get(URL)


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
        print("cur", cur)
        s = "Feature: " + "\t" + str(cur[0])  # Size =1
        if size == 2:
            s += ("\n" + "Value: " + "\t" + str(cur[1]))
        s += "\n"
        f1.write(s)


if __name__ == '__main__':
    soup = BeautifulSoup(r.content, 'html5lib')
    text = soup.prettify()
    write_to_file(text, "data.txt")
    master_table = soup.findAll("table", attrs={"class": "_3ENrHu"})
    num_table = len(master_table)
    universe_pairs = []
    for i in range(num_table):
        print("Table No. ", i)
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
                if cnt_feature == 1:
                    print()
                    print("Feature: ")
                else:
                    print()
                    print("Value: ")
                print(td.text, end=" ")
                feature.append(td.text)
                cnt_feature *= -1

            feature_value_pairs.append(feature)

        write_to_file(feature_value_pairs, "final_pairs.txt", True)
        universe_pairs.extend(feature_value_pairs)
    print()
    print("rows", len(universe_pairs))
    print("cols", len(universe_pairs[0]))
    write_pairs_to_file(universe_pairs, "Universe_pairs.txt")