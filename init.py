from tabulate import tabulate
import pandas as pd
import os
import folium
import reverse_geocoder
from sodapy import Socrata
import rdflib
import urllib.request
import json
import requests


def create_menu(df, select):
    llista = []
    for index, value in enumerate(df[select].drop_duplicates()):
        llista.append(value)
        print(index + 1, str(value))
    chosen = input("Please enter a number (1-{0}):".format(len(llista)))
    return llista[int(chosen) - 1]


print("Loading data... Please wait.")
# data = pd.read_csv('data.csv', sep=',')


while True:
    print("""Choose how to read information
            1. SODA API
            2. CSV 
            3. RDF
            4. JSON
            5. O DATA
            \rOr type "exit" to quit.""")
    menu = input("Please enter a number (1-5):")

    if menu.lower() == "exit":
        exit(0)

    if menu == '1':
        print("Generating table... Please wait.")
        '''
        Soda API example
        '''
        socrata_domain = 'analisi.transparenciacatalunya.cat'
        socrata_dataset_identifier = 'p6e5-hq22'

        client = Socrata(socrata_domain, None)
        # print("Domain: {domain:}\nSession: {session:}\nURI Prefix: {uri_prefix:}".format(**client.__dict__))

        results = client.get(socrata_dataset_identifier)
        df = pd.DataFrame.from_dict(results)
        df.head()
        print(df)

    if menu == '2':  # CSV
        print("Generating table... Please wait.")
        data = pd.read_csv('Equipaments_de_Catalunya.csv', sep=',', encoding='utf-8', index_col=False,)
        data.head(n=3)
        gb = data.groupby(by=['IDEQUIPAMENT']).first()
        gb.head()
        print(gb)

    if menu == '3':  # rdf
        g = rdflib.Graph()
        g.load('rows.rdf')

        for s, p, o in g:
            print(s, p, o)

    if menu == '4':  # JSON
        with urllib.request.urlopen("https://analisi.transparenciacatalunya.cat/resource/p6e5-hq22.json") as url:
            data = json.loads(url.read().decode())
            print(data)

    if menu == '5':  # OData
        url = 'https://analisi.transparenciacatalunya.cat/api/odata/v4/8gmd-gz7i'
        r = requests.get(url)
        r_json = r.json()
        print(r_json)
