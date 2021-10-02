import heapq


class Node(object):

    def __init__(self, name):
        self.id = name
        self.connected_nodes = {}
        self.distance = float('inf')
        self.visited = False
        self.previous = None

    def add_connection(self, neighbor, weight=0):
        self.connected_nodes[neighbor] = weight

    def get_connections(self):
        return self.connected_nodes.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.connected_nodes[neighbor]

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    def set_previous(self, previous):
        self.previous = previous

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return f'{self.id}: {[x.id for x in self.connected_nodes]}'

    def __lt__(self, other):
        return self.distance < other.distance


class Network(object):

    def __init__(self):
        self.node_dict = {}
        self.num_nodes = len(self.node_dict)
        self.previous = None

    def __iter__(self):
        return iter(self.node_dict.values())

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        self.node_dict[node] = Node(node)
        self.num_nodes = len(self.node_dict)
        return self.node_dict[node]

    def get_node(self, n):
        return self.node_dict[n] if n in self.node_dict else None

    def add_edge(self, frm, to, cost=0.0):
        if frm not in self.node_dict:
            self.add_node(frm)
        if to not in self.node_dict:
            self.add_node(to)

        self.node_dict[frm].add_connection(self.node_dict[to], cost)
        self.node_dict[to].add_connection(self.node_dict[frm], cost)

    def get_nodes(self):
        return list(self.node_dict.keys())

    def set_previous(self, current):
        self.previous = current

    def get_previous(self):
        return self.previous


class Dijkstra(object):

    @staticmethod
    def compute(network, start):
        start.set_distance(0)

        # create the priority queue with nodes
        unvisited_queue = [(node.get_distance(), node) for node in network]
        heapq.heapify(unvisited_queue)

        while len(unvisited_queue):
            # pop a node with the smallest distance
            unvisited_node = heapq.heappop(unvisited_queue)
            current_node = unvisited_node[1]
            current_node.set_visited()

            for next_node in current_node.connected_nodes:
                if not next_node.visited:
                    new_dist = current_node.get_distance() + current_node.get_weight(next_node)
                    if new_dist < next_node.get_distance():
                        next_node.set_distance(new_dist)
                        next_node.set_previous(current_node)

            # Rebuild heap: Pop every item, Put all nodes not visited into the queue
            while len(unvisited_queue):
                heapq.heappop(unvisited_queue)
            unvisited_queue = [(n.get_distance(), n) for n in network if not n.visited]
            heapq.heapify(unvisited_queue)

    @staticmethod
    def compute_shortest_path(node, path):
        if node.previous:
            path.append(node.previous.get_id())
            Dijkstra.compute_shortest_path(node.previous, path)


def read_network_from_file(file_name, delimeter=','):
    cities = list()
    distances = dict()

    f = open(file_name, 'r')
    lines = f.readlines()
    for line in lines:
        fields = line.rstrip().split(delimeter)
        city_1 = fields[0].strip(' ')
        city_2 = fields[1].strip(' ')
        distance = float(fields[2])

        # build the list of nodes
        if city_1 not in cities:
            cities.append(city_1)
        if city_2 not in cities:
            cities.append(city_2)

        # build the dictionary based on node weights
        if cities.index(city_1) not in distances.keys():
            distances[cities.index(city_1)] = {cities.index(city_2): distance}
        if cities.index(city_2) not in distances[cities.index(city_1)].keys():
            distances[cities.index(city_1)][cities.index(city_2)] = distance

    return cities, distances

def gen_network(cities, distances):
    network = Network()
    network.add_nodes(cities)
    for connection in distances.items():
        frm = cities[connection[0]]
        for connection_to in connection[1].items():
            network.add_edge(frm, cities[connection_to[0]], connection_to[1])
    return network

def gen_path(cities, distances, start_city, end_city):
    network = gen_network(cities, distances)
    
    path = [network.get_node(end_city).get_id()]
    dij = Dijkstra()
    dij.compute(network, network.get_node(start_city))
    dij.compute_shortest_path(network.get_node(end_city), path)

    return path, network.get_node(end_city).get_distance()

def join_path(path1, path2):
    return path2 + path1[1:] 

def main():

    # application salutation
    #
    application_name = 'Trucking Analysis Network'
    print('-' * len(application_name))
    print(application_name)
    print('-' * len(application_name))

    # read network from file
    #
    file_name = 'Network.csv'
    cities, distances = read_network_from_file(file_name)

    # build the network
    #
    network = Network()
    network.add_nodes(cities)
    for connection in distances.items():
        frm = cities[connection[0]]
        for connection_to in connection[1].items():
            network.add_edge(frm, cities[connection_to[0]], connection_to[1])
            
    # print('Network')
    # for node in network:
    #     for connected_node in node.get_connections():
    #         node_id = node.get_id()
    #         connected_node_id = connected_node.get_id()
    #         print(f'{node_id}:{connected_node_id}={node.get_weight(connected_node)}')

    # determine the start city
    #

    for (index, city) in enumerate(network.get_nodes()):
        print(f'{index}: {city:s}')
    start_city_index = int(
        input(f'What is the start city by index (0 to {len(network.get_nodes())-1})? '))
    end_city_index = int(
        input(f'What is the end city by index (0 to {len(network.get_nodes())-1})? '))
    start_city = network.get_nodes()[start_city_index]
    end_city = network.get_nodes()[end_city_index]
    
    #init New_Orleans and St.Louis node
    NEW_ORLEANS = network.get_nodes()[12]
    ST_LIOUS = network.get_nodes()[13]

    path1, dis1 = gen_path(cities, distances, start_city, NEW_ORLEANS)
    temp_path, temp_dis = gen_path(cities, distances, NEW_ORLEANS, ST_LIOUS)
    path1 = join_path(path1, temp_path)
    dis1 += temp_dis
    temp_path, temp_dis = gen_path(cities, distances, ST_LIOUS, end_city)
    path1 = join_path(path1, temp_path)
    dis1 += temp_dis
    
    path2, dis2 = gen_path(cities, distances, start_city, ST_LIOUS)
    temp_path, temp_dis = gen_path(cities, distances, ST_LIOUS, NEW_ORLEANS)
    path2 = join_path(path2, temp_path)
    dis2 += temp_dis
    temp_path, temp_dis = gen_path(cities, distances, NEW_ORLEANS, end_city)
    path2 = join_path(path2, temp_path)
    dis2 += temp_dis
    if dis1 > dis2:
        print(f'1{start_city} to {end_city} is {path1[::-1]}')
    print(f'1{start_city} to {end_city} is {path1[::-1]}')
    
    '''
    for target_node in network.get_nodes():
        target_city = network.get_node(target_node)
        path = [target_city.get_id()]
        Dijkstra.compute_shortest_path(target_city, path)
        print(f'{start_city} to {target_node} is {path[::-1]}')

    '''
if __name__ == '__main__':
    main()
