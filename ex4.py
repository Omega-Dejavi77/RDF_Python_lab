import folium
from sodapy import Socrata
import webbrowser

print('Generating data, please wait...')
client = Socrata("analisi.transparenciacatalunya.cat", None)
data = client.get("p6e5-hq22", limit=40000)

llista = []
for i in range(len(data)):
    if 'categoria' in data[i]:
        llista.append(data[i]['categoria'])

chosen = input("Please enter a number to choose the type (1-{}): ".format(len(set(llista))))

type = llista[int(chosen) - 1]
print("equipment selected was: ", type)
points = -1
llista_type = []
for i in range(len(data)):
    if 'categoria' in data[i]:
        if data[i]['categoria'] == type:
            llista_type.append(data[i])

maxValue = len(llista_type)

while 0 > points or points > maxValue:
    points = int(input("How many points do you want to draw on the map? (0-{}): ".format(maxValue)))

map = folium.Map(location=(41.818111, 1.601079), zoom_start=8)

for i in range(points):
    if llista_type[i]['categoria'] == type:
        x = llista_type[i]['latitud']
        y = llista_type[i]['longitud']
        folium.Marker(location=[float(x), float(y)],
                      popup='<strong>categoria: {}</br>nom: {}</strong>'
                      .format(llista_type[i]['categoria'], llista_type[i]['nom']),
                      tooltip='Click for more info').add_to(map)

map.save('mapTask4.html')
webbrowser.open('mapTask4.html')
