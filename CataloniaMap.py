import folium
import webbrowser
import requests
import pandas as pd
from branca.colormap import LinearColormap
import json
from sodapy import Socrata

category = ""
print("Enter a Category: ")
category = input()

# gather via soda api
response = requests.get("https://analisi.transparenciacatalunya.cat/resource/p6e5-hq22.json")

# parse into json
equipaments_json = response.json()

# print('Generating data, please wait...')
# client = Socrata("analisi.transparenciacatalunya.cat", None)
# equipaments_json = client.get("p6e5-hq22", limit=40000)
# data manage

data = ''
with open('shapefiles_catalunya_comarcas.geojson', encoding='utf8') as f: #very important encode utf8 !!!
    data = json.load(f)

comarques_by_number = dict()
i = 0
for i in range(0, 40):
    comarques_by_number[(data['features'][i]['properties']['nom_comar'])] = i
    i += 1

categories = list()
comarques = list()
for equipament in equipaments_json:
    if('categoria' in equipament and equipament['categoria'] not in categories):
        categories.append(equipament['categoria'])
    if('comarca' in equipament and equipament['comarca'] not in categories):
        comarques.append(equipament['comarca'])

my_dict = dict()
num = 0
for comarca in comarques:
    if not (comarca == 'Alt Penedès' or comarca == 'Moianès'):
        id = comarques_by_number[comarca]
        my_dict[id] = 0
        for equipament in equipaments_json:
            if (equipament['comarca'] == comarca):
                if ('categoria' in equipament and equipament['categoria'] == category):
                    my_dict[id] += 1


# center map to catalonia frame
latitud = equipaments_json[0]['latitud']
longitud = equipaments_json[0]['longitud']

# name of the output html map
html_filename = "output.html"

# setting map county to paint
cat_map = pd.DataFrame({'comarca': list(my_dict.keys()), 'value': list(my_dict.values())})  # 21 -> Maresme
map_dict = cat_map.set_index('comarca')['value'].to_dict()

color_scale = LinearColormap(['#00AEBC', 'purple'], vmin=min(map_dict.values()), vmax=max(map_dict.values()))


def get_color(feature):
    value = map_dict.get(feature['properties']['comarca'])
    if value is None:
        return '#00AEBC' # MISSING -> gray
    else:
        return color_scale(value)


# setting map frame position
cat_map = folium.Map(location=[float(latitud), float(longitud)],  zoom_start=7)

# apply geojson
folium.GeoJson(
    data = 'shapefiles_catalunya_comarcas.geojson',
    style_function=lambda feature:
    {
        'fillColor': get_color(feature),
        'fillOpacity': 0.5,
        'color' : 'darkblue',
        'weight': 1,
    }
).add_to(cat_map)


# saving as html and opening from the default browser
cat_map.save(html_filename)
webbrowser.open(html_filename)
