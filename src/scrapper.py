from tqdm import tqdm
from lxml import html
import pandas as pd
import requests
import time
import yaml
import re

class scrapper():

    def __init__(self):
        """Init using src/parameters.yaml file."""
        with open('src/parameters.yaml', 'r') as f:
            doc = yaml.load(f,Loader=yaml.BaseLoader)
            self.url = doc['url']
            self.api_path = doc['api_path']
            self.parser_parameters = doc['parser_parameters']
            self.max_offset = int(doc['max_offset'])
            self.time_sleep = float(doc['time_sleep'])
            self.columns_need_correction = doc['columns_need_correction']
            self.corrections = doc['corrections']


    def key_colletor(self):
        """Pick up a key, requiered as token by the ajax.php request."""
        url = self.url
        txt = requests.get(self.url).text
        key = re.search('searchNonce":".+?(?=")', txt).group(0)
        self.key = key.split('"')[2]


    def parser(self, tree, parser_param):
        """Parse the html following parsing parameters defined
        in src/parameters.yaml.

        tree: lxml.html.HtmlElement
        tree: tree comming from html.fromstring()

        parser_param: dict
        parser_param: dictionnary of xpath
        """
        res = dict()
        for elem in parser_param.keys():
            if elem != 'url':
                res[elem] = [x.text for x in tree.xpath(parser_param[elem])]
            else:
                res[elem] = tree.xpath(parser_param[elem])
        return res


    def data_collector(self, offset, print_out=False):
        """Collect the data through ajax.php request on the website.

        offset: int
        offset: integer used as offset in order to move into the listing

        print_out: bool
        print_out: if True payload is printed
        """
        payload = {'action':'search_process',
                   'nonce':self.key,
                   'offset':str(offset)}
        if print_out:
            print(payload)
        response = requests.post(self.api_path, data=payload).json()
        content = response['content']
        tree = html.fromstring(content)
        return pd.DataFrame(self.parser(tree, self.parser_parameters))


    def cleaning(self, db):
        """Simple regex replacement removing linebreak.
        """
        for col in self.columns_need_correction:
            for val in self.corrections:
                db[col] = db[col].str.replace(val,'')
        return db


    def collect(self):
        """Collect automaticaly all the available listing."""
        error_count = 0
        self.key_colletor()
        db = pd.DataFrame(columns=['affiliate','date','employer',
                                   'localization','title','topic','url'])
        for offset in tqdm(range(1,self.max_offset)):
            try:
                self.data_collector(offset)
            except:
                error_count += 1
                print(f"offset {offset} not working,",
                      f"which lead the number of error to -> {error_count}",
                      sep=' ')
                if error_count > 10:
                    print('It looks like you reach the end of the listing')
                    break
            else:
                db = pd.concat([db,self.data_collector(offset)]
                               ,ignore_index=True
                               ,sort=True)
        db_clean = self.cleaning(db)
        return db_clean
