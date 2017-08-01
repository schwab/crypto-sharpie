import abc
import bs4
import os
def make_t(row) :
    tds = row.findAll("td")
    text = [filter(None,t.text.replace(' ',',').replace('\n','').split(',')) for t in tds]
    return tuple(text)

class notify(object):
    coin_symbol = ""
    date = ""
    exchange = ""
    signal = 0
    max_1hr = 0
    max_6hr =  0
    max_24hr = 0
    max_48hr = 0
    max_7day = 0
    def __init__(self, data_row):
        self.coin_symbol = data_row[0][0]
        self.date = "%sT%s" % (data_row[1][0][-10:], data_row[1][1])
        self.signal = float(data_row[1][0][:-10])
        self.max_1hr = float(data_row[2][0])
        self.max_6hr = float(data_row[3][0])
        self.max_24hr = float(data_row[4][0])
        self.max_48hr = float(data_row[5][0])
        self.max_7day = float(data_row[6][0])
        self.exchange = data_row[7][0]
    def __repr__(self):
        return "%s %s %s %s" % (self.coin_symbol, self.date, self.signal, self.exchange)
    


#signals = map(notify, row_tuples[2:])
#print signals
#print row_tuples
#tables = soup.findAll("table",{"class":"results"}) 
#print tables
def main():
    file_path = "Examples/crypto_sharpie/cryptoping_data/pg1.html"
    if os.path.exists(file_path):
        try:
            with open(file_path) as f:
                soup = bs4.BeautifulSoup(f,'lxml')
        except IOError:
            print "file not found"
            return None
        tables= soup.findAll('tbody')
        column_names =  [th.text for th in tables[0].findAll("th")]
        #print column_names
        rows = [tr for tr in tables[0].findAll("tr") ][1:]
        row_tuples = [ make_t(row) for row in rows]
        notify_items = [notify(x) for x in row_tuples]
        print notify_items
if __name__ == "__main__":
    main()