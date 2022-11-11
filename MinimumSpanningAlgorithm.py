import numpy as np
import sys
from ManhattanDistance import manhattandistanceMatrix
from EuclideanDistance import euclideanDistanceMatrix
cities_truck_travel_route,cities_drone_travel_route,truckdronepath_coord=([] for _ in range(10))
total_distance_route = 0

import time

def minimumspanningTSP (truckDroneDict):
    start_time_MS=time.time()
    # Truck Data coordinates
    total_distance_route = 0.0
    truckdronepath_coord = []
    TruckData = [sub["coord"] for sub in truckDroneDict.values() if "coord" in sub.keys()]
    # Calculating Manhattan Distance Matrix for the Truck
    distanceMatrix=manhattandistanceMatrix(TruckData)
    # Applying MST to the above distanceMatrix
    [truck_min_distance, truck_travel_route]=mst(distanceMatrix)
    for i in range(0,len(truck_travel_route)):
        truck_coordinate=TruckData[truck_travel_route[i]]
        for k, v in truckDroneDict.items():
            for k1, v1 in v.items():
                if(v1==truck_coordinate ):
                    cities_truck_travel_route.append(k if k1 == "coord" else k1)
    cities_truck_travel_route.append(cities_truck_travel_route[0])
    total_distance_route = float(total_distance_route) + float(truck_min_distance)

    # The Drone path
    for i in range(0, len(cities_truck_travel_route)-1):
        l = []
        for k, v in truckDroneDict.items():
            for k1, v1 in v.items():
                if k == cities_truck_travel_route[i]:
                    l.append(v1)
        edistanceMatrix = euclideanDistanceMatrix(l)

        [drone_min_distance, drone_travel_route] = mst(edistanceMatrix)
        drone_travel_route.append(drone_travel_route[0])

        total_distance_route = float(total_distance_route)+float(drone_min_distance)
        for i in range(0, len(drone_travel_route)):
            drone_coordinate = l[drone_travel_route[i]]

            for k, v in truckDroneDict.items():
                for k1, v1 in v.items():
                    if v1 == drone_coordinate:
                        truckdronepath_coord.append(v1)
                        cities_drone_travel_route.append(k if k1 == "coord" else k1)
    cities_drone_travel_route.append('A')
    truckdronepath_coord.append(truckdronepath_coord[0])
    return(cities_drone_travel_route,total_distance_route,truckdronepath_coord)


def mst(distanceMatrix):
    # Read the first line for node number
    node_no = len(distanceMatrix)
    graph = distanceMatrix
    min_distance = np.zeros((node_no,), dtype=float)  # distances with starting node as min_distance[i]
    travel_route = [[] for y in range(0, node_no)]
    parents = [[0 for x in range(0, node_no)] for y in range(0, node_no)]

    # Step 1
    #print("Prim's mst:")
    for start_node in range(0, node_no):
        parents[start_node] = prims_algorithm(start_node, node_no, graph)

    # Assume triangle inequality holds for nodes, if it doesn't, min spanning tree doesnt give
    # a solution closer to optimal

    # For each mst with a start_node
    for start_node, parent in enumerate(parents):
        if(start_node==0):
            #print("\nStartnode:" + str(start_node))
            pass
        #print()
        travel_route[start_node].append(start_node)

        # For each node in a specific mst, find the travel route
        index = 1
        while index < node_no:
            list = []
            for node, parent_node in enumerate(parent):
                if in_travel_route(parent_node, travel_route[start_node]) and not in_travel_route(node,
                                                                                                            travel_route[
                                                                                                                start_node]):
                    list.append(node)
                    index = index + 1
            for l in list:
                travel_route[start_node].append(l)

        # Find distance of travel route
        prev_node = start_node
        cur_node = -1
        for i in range(1, node_no):
            cur_node = travel_route[start_node][i]
            if graph[prev_node][cur_node] <= 0:
                min_distance[start_node] = 0
            else:
                min_distance[start_node] = min_distance[start_node] + graph[prev_node][cur_node]
            if(start_node==0):
                #print("from " + str(prev_node) + " to " + str(cur_node) + " distance: " + str(graph[prev_node][cur_node]))
                pass
            prev_node = cur_node

        if graph[cur_node][start_node] <= 0:
            min_distance[start_node] = 0
        else:
            min_distance[start_node] = min_distance[start_node] + graph[cur_node][start_node]

    #print("Prim's heuristic:")
    [shortest_min_distance, shortest_travel_route] = find_best_route(node_no, travel_route, min_distance)
    return shortest_min_distance, shortest_travel_route


def prims_algorithm(start_node, node_no, graph):
    keys = [float('inf') for x in range(0, node_no)]
    parent = [-1 for x in range(0, node_no)]

    # Step 3
    unvisited = np.ones((node_no,), dtype=int)  # all nodes are unvisited
    keys[start_node] = 0

    # Step 2
    iteration = 1
    while check_unvisited_node(unvisited) and iteration < node_no:
        # Find the unvisited node with minimum key
        min_key_val = sys.maxsize
        min_node = node_no
        for index, key_val in enumerate(keys):
            if unvisited[index] == 1 and key_val < min_key_val:
                min_key_val = key_val
                min_node = index

        unvisited[min_node] = 0

        # Update adjacent nodes
        for node, val in enumerate(keys):
            if keys[node] > graph[min_node][node] > 0 and unvisited[node] == 1:
                keys[node] = graph[start_node][node]
                parent[node] = min_node

        iteration = iteration + 1

    #print_mst(parent, node_no, graph)

    return parent


def print_mst(parent, node_no, graph):
    print("Edge \tWeight")
    for i in range(0, node_no):
        print(parent[i], "-", i, "\t", graph[i][parent[i]])


def check_unvisited_node(unvisited):
    for u in unvisited:
        if u == 1:
            return True
    return False


def get_unvisited_node(unvisited):
    for index, node in enumerate(unvisited):
        if node == 1:
            return index
    return -1


def find_best_route(node_no, travel_route, min_distance):
    shortest_travel_route = travel_route[0]
    shortest_min_distance = min_distance.item(0)
    for start_node in range(0, node_no):
        if min_distance[start_node] < shortest_min_distance:
            shortest_min_distance = min_distance.item(start_node)
            shortest_travel_route = travel_route[start_node]

    return str(min_distance[0]), travel_route[0]


def in_travel_route(node, travel_route):
    for t in travel_route:
        if t == node:
            return True
    return False
