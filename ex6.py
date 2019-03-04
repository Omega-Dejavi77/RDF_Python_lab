import folium
from sodapy import Socrata
import webbrowser
import json
import pandas as pd
from branca.colormap import LinearColormap


def fill_color(map, feature):
    value = map.get(feature['properties']['comarca'])
    if value is None:
        return 'gray'
    else:
        color_scale = LinearColormap(['lightblue', 'darkblue'], vmin=min(map.values()), vmax=max(map.values()))
        return color_scale(value)


print('Generating data, please wait...')
client = Socrata("analisi.transparenciacatalunya.cat", None)
data = client.get("p6e5-hq22", limit=40000)

with open('shapefiles_catalunya_comarcas.geojson', encoding='utf8') as f:
    geojson = json.load(f)


llista = []
for i in range(len(data)):
    if 'categoria' in data[i]:
        llista.append(data[i]['categoria'])

chosen = input("Please enter a number to choose the type (1-{}): ".format(len(set(llista))))
type = llista[int(chosen) - 1]
print("equipment selected was: ", type)
print('generating map...')

dict_n_comarques = {}
i = 0
for i in range(0, 40):
    dict_n_comarques[(geojson['features'][i]['properties']['nom_comar'])] = i
    i += 1

categories = []
comarques = []
for equipament in data:
    if 'categoria' in equipament and equipament['categoria'] not in categories:
        categories.append(equipament['categoria'])
    if 'comarca' in equipament and equipament['comarca'] not in categories:
        comarques.append(equipament['comarca'])

my_dict = {}
for comarca in comarques:
    if not (comarca == 'Alt Penedès' or comarca == 'Moianès'):
        id = dict_n_comarques[comarca]
        my_dict[id] = 0
        for equipament in data:
            if equipament['comarca'] == comarca:
                if 'categoria' in equipament and equipament['categoria'] == type:
                    my_dict[id] += 1

cat_map = pd.DataFrame({'comarca': list(my_dict.keys()), 'value': list(my_dict.values())})
map_dict = cat_map.set_index('comarca')['value'].to_dict()

map = folium.Map(location=[float(data[0]['latitud']), float(data[0]['longitud'])], zoom_start=8)

folium.GeoJson(
    data='shapefiles_catalunya_comarcas.geojson',
    style_function=lambda feature:
    {
        'fillColor': fill_color(map_dict, feature),
        'fillOpacity': 0.5,
        'color': 'darkblue',
        'weight': 1,
    }
).add_to(map)

map.save('mapTask6.html')
webbrowser.open('mapTask6.html')
