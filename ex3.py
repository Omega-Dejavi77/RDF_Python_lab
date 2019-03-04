from sodapy import Socrata

print('Generating data, please wait...')
client = Socrata("analisi.transparenciacatalunya.cat", None)
data = client.get("p6e5-hq22", limit=40000)

d_equipments = {}
for i in range(len(data)):
    if 'categoria' in data[i]:
        categoria = data[i]['categoria']
        comarca = data[i]['comarca']

        if categoria in d_equipments.keys():
            d_equipments[categoria]['Catalunya'] += 1
            if comarca in d_equipments[categoria].keys():
                d_equipments[categoria][comarca] += 1
            else:
                d_equipments[categoria][comarca] = 1
        else:
            d_equipments[categoria] = {'Catalunya': 1, comarca: 1}

for key, value in d_equipments.items():
    print('TYPE: {}'.format(key))
    for comarca, num in d_equipments[key].items():
        if comarca in "Catalunya":
            print('\t equipments in {} :{}'.format(comarca, num))
        else:
            print('\t\t equipments in {} :{}'.format(comarca, num))
