import networkx as nx
import matplotlib.pyplot as pyplot

line1 = ['Helwan', 'Ain Helwan', 'Helwan University', 'Wadi Hof', 'Hadayek Helwan', 'El-Maasara', 'Tora El-Asmant', 'Kozzika', 'Tora El-Balad', 'Sakanat El-Maadi', 'Maadi', 'Hadayek El-Maadi', 'Dar El-Salam', "El-Zahraa'", 'Mar Girgis', 'El-Malek El-Saleh', 'Al-Sayeda Zeinab', 'Saad Zaghloul', 'Sadat', 'Nasser', 'Orabi', 'Al-Shohadaa', 'Ghamra', 'El-Demerdash', 'Manshiet El-Sadr', 'Kobri El-Qobba', 'Hammamat El-Qobba', 'Saray El-Qobba', 'Hadayeq El-Zaitoun', 'Helmeyet El-Zaitoun', 'El-Matareyya', 'Ain Shams', 'Ezbet El-Nakhl', 'El-Marg', 'New El-Marg']
line2 = ['El-Mounib', 'Sakiat Mekky', 'Omm El-Masryeen', 'Giza', 'Faisal', 'Cairo University', 'El Bohoth', 'Dokki', 'Opera', 'Mohamed Naguib', 'Attaba', 'Masarra', 'Rod El-Farag', 'St. Teresa', 'Khalafawy', 'Mezallat', 'Kolleyyet El-Zeraa', 'Shubra El-Kheima']
line3 = ['Al-Ahram', 'Koleyet El-Banat', 'Stadium', 'Fair Zone', 'Abbassiya', 'Abdou Pasha', 'El-Geish', 'Bab El-Shaaria']

pos = {}
for i, station in enumerate(line1):
    if station in ['Al-Shohadaa', 'Sadat']:
        pos[station] = (2.5, i * 10)
    else:
        pos[station] = (3, i * 10)

for i, station in enumerate(line2):
    if station == 'Attaba':
        pos[station] = (1.5, (i * 10) + 100)
    else:
        pos[station] = (2, (i * 10) + 100)
    
for i, station in enumerate(line3):
    pos[station] = (1, 270 - (i * 10))

metroStationsNetwork = nx.Graph()

metroStationsNetwork.add_nodes_from(line1, line=1)
metroStationsNetwork.add_nodes_from(line2, line=2)
metroStationsNetwork.add_nodes_from(line3, line=3)

for edge in zip(line1, line1[1:]):
    metroStationsNetwork.add_edge(*edge)

for edge in zip(line2, line2[1:]):
    metroStationsNetwork.add_edge(*edge)

for edge in zip(line3, line3[1:]):
    metroStationsNetwork.add_edge(*edge)

metroStationsNetwork.add_edge('Masarra', 'Al-Shohadaa')
metroStationsNetwork.add_edge('Al-Shohadaa', 'Attaba')
metroStationsNetwork.add_edge('Attaba', 'Bab El-Shaaria')
metroStationsNetwork.add_edge('Mohamed Naguib', 'Sadat')
metroStationsNetwork.add_edge('Sadat', 'Opera')

metroStationsNetwork.remove_edge('Mohamed Naguib', 'Opera')
metroStationsNetwork.remove_edge('Masarra', 'Attaba')

# nx.draw(metroStationsNetwork, pos, with_labels=True, font_size=8)
# pyplot.show()
# pyplot.savefig(r'D:\Programming\MetroStationsNetwork\fig.png')


def shortestPath(source, destination):

    return nx.shortest_path_length(metroStationsNetwork, source, destination)

def path(source, destination):

    paths =  [x for x in nx.all_shortest_paths(metroStationsNetwork, source, destination)]

    if len(paths) > 1:
        scores = [0 for i in paths]

        for i, path in enumerate(paths):
            prevLine = metroStationsNetwork.node[path[0]]['line']

            for station in path[1:]:
                if station in ['Al-Shohadaa', 'Attaba', 'Sadat']:
                    continue

                currentLine = metroStationsNetwork.node[station]['line']
                if currentLine != prevLine:
                    scores[i] += 1

        return paths[scores.index(min(scores))]

    else:
        return paths[0]

def main():
    while True:

        while True:
            source = input('Enter source: ')
            destination = input('Enter destination: ')
            
            try:
                numberStations = shortestPath(source, destination)

            except nx.exception.NodeNotFound:
                print('Please review your input and spelling, either {0} or {1} is not correctly spelled.\n\n'.format(source, destination))

            else:
                break

        print('', 'Number of stations:', numberStations, sep='\n')
        print()

        if numberStations <= 9:
            print('Yellow ticket')

        elif numberStations <= 16:
            print('Green ticket')

        else:
            print('Red ticket')

        print()
        print('Your path will be:')
        for i, s in enumerate(path(source, destination)):
            if i == 0:
                print(s, end='')
            else:
                print(' >> ', end='')
                print(s, end='')

        print('\n')
        again = input('Again?\n("y" or "n")\n\n')

        if again == 'y':
            print('\n\n')
            continue

        else:
            break

    SystemExit

if __name__ == '__main__':
    main()