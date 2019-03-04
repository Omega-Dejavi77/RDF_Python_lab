from tabulate import tabulate
import pandas as pd
from sodapy import Socrata
import rdflib
import urllib.request
import json
import requests

print("Loading data... Please wait.")

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

    elif menu == '1':  # SODA API
        print("Generating table... Please wait.")
        socrata_domain = 'analisi.transparenciacatalunya.cat'
        socrata_dataset_identifier = 'p6e5-hq22'

        # Unauthenticated client only works with public data sets. Note 'None'
        # in place of application token, and no username or password:
        client = Socrata(socrata_domain, None)

        # results returned as JSON from API / converted to Python list of
        # dictionaries by sodapy.
        results = client.get(socrata_dataset_identifier)

        # Convert to pandas DataFrame
        df = pd.DataFrame.from_dict(results)
        print(tabulate(df.head(n=10), headers=df.keys(), tablefmt='grid',
                       stralign='center', numalign='center', showindex=False,))

    elif menu == '2':  # CSV
        print("Generating table... Please wait.")
        data = pd.read_csv('Equipaments_de_Catalunya.csv', sep=',',
                           encoding='utf-8', index_col=False,)

        print(tabulate(data.head(n=10), headers=data.keys(), tablefmt='grid', stralign='center', numalign='center',
                       showindex=False))

    elif menu == '3':  # rdf
        g = rdflib.Graph()
        g.load('rows.rdf')

        for s, p, o in g:
            print(s, p, o)

    elif menu == '4':  # JSON
        with urllib.request.urlopen("https://analisi.transparenciacatalunya.cat/resource/p6e5-hq22.json") as url:
            data = json.loads(url.read().decode())

        print(json.dumps(data, indent=2))

    elif menu == '5':  # OData
        url = 'https://analisi.transparenciacatalunya.cat/api/odata/v4/8gmd-gz7i'
        r = requests.get(url)
        r_json = r.json()
        print(json.dumps(r_json, indent=2))

    else:
        print('Incorrect value')
