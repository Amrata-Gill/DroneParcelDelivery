import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import time
TruckDroneMapping = {}
dronedict = {}
p = []
NN_TSP_total_path = []


def NearestNeighbourTSP(truckDroneDict):

    TruckTourLength = 0
    TruckDroneTourLength = 0
    TruckPath = []
    TruckData = [sub["coord"] for sub in truckDroneDict.values() if "coord" in sub.keys()]
    pathTruck = nearest_neighbourTSP(set(TruckData), TruckData[0], 1)
    TruckTourLength += tour_length(pathTruck, 1)
    for t in range(0, len(pathTruck)):
        for k, v in truckDroneDict.items():
            for k1, v1 in v.items():
                if pathTruck[t] == v1:
                    TruckPath.append(k)

    l = []
    Truck_Drone_path = []
    c = 65
    total_tour_length = 0
    tourpathTruck = []
    total_tour_path = []
    for i in range(0, len(TruckPath)):
        for k, v in truckDroneDict.items():
            if (k == TruckPath[i]):
                for k1, v1 in v.items():
                    l.append(v1)
        TruckDronePath = nearest_neighbourTSP(set(l), l[0], 0)
        TruckDroneTourLength += tour_length(TruckDronePath, 0)
        l = []
        Truck_Drone_path.append(TruckDronePath)

    temp = []
    t = 0
    flat_truck_dronepath=[]
    for item in Truck_Drone_path:
        flat_truck_dronepath+=item
    t = 0
    for i in range(0, len(Truck_Drone_path) - 1):
        for j in range(0, len(Truck_Drone_path[i])):
            for k, v in truckDroneDict.items():
                for k1, v1 in v.items():
                    if (Truck_Drone_path[i][j] == v1):
                        NN_TSP_total_path.append(k if k1 == "coord" else k1)
    NN_TSP_total_path.append(TruckPath[0])
    temp.append(TruckDronePath[-2])
    temp.append(TruckDronePath[-1])
    TruckDroneTourLength += tour_length(temp, 0)
    return (NN_TSP_total_path,flat_truck_dronepath)


# ExecuteNN_TSP(TruckDroneMapping)
def nearest_neighbourTSP(cities, start, status):
    """Start the tour at the first city; at each step extend the tour
    by moving from the previous city to its nearest neighbor
    that has not yet been visited."""
    tour = [start]
    unvisited = set(cities - {start})
    while unvisited:
        C = nearest_neighbor(tour[-1], unvisited, status)
        tour.append(C)
        R = unvisited.remove(C)
    tour.append(start)
    return (tour)


def nearest_neighbor(A, cities, status):
    "Find the city in cities that is nearest to city A."
    return min(cities, key=lambda c: distance(c, A, status))


def first(collection):
    "Start iterating over collection, and return the first element."
    return next(iter(collection))


def distance(A, B, status):
    "The distance between two points.Eucleadian Distance"
    if (status == 0):
        return pow(pow(A.real - B.real, 2) + pow(A.imag - B.imag, 2), .5)
    else:
        return (abs(A.real - B.real) + abs(A.imag - B.imag))


def tour_length(tour, status):
    "The total of distances between each pair of consecutive cities in the tour."
    return sum(distance(tour[i], tour[i - 1], status)
               for i in range(len(tour)))

