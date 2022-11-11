import os
from locationGenerator import locationGenerationTruck
from locationGenerator import locationGenerationTruckDrone
from nearestInsertion import NearestInsertionSolver
from util import read_data1
from util import read_data2
from datetime import datetime
from itertools import chain
ni_solution_truck=[]
ni_solution_DroneFinal2=[]
NearestInsertionDistance=0
l={}
l2=[]
ni_solution_DroneFinal=[]
NearestInsertionDistanceTruck=0
NearestInsertionDistanceDrone=0
def NearestInsertion2(truckDroneDict):
    start_time_NI=datetime.now()
    NearestInsertionDistanceTruck=0
    NearestInsertionDistanceDrone=0
    locationGenerationTruck(truckDroneDict)
    #print("Truck drone dict",truckDroneDict)
    node_locations, node_distances = read_data1('Trucklocation.txt')
    node_labels = (node_locations.keys())
    ni_solver = NearestInsertionSolver(node_labels, node_distances)
    ni_solution_truck = ni_solver.run()

    ni_average_distance_truck = ni_solver.get_total_distance()
    NearestInsertionDistanceTruck = NearestInsertionDistanceTruck+ni_average_distance_truck
    #print("Truck distance",NearestInsertionDistanceTruck)
    for i in range(0, len(ni_solution_truck)-1):
        l = {}

        for k, v in truckDroneDict.items():
            if(ni_solution_truck[i]==k):
                for k1, v1 in v.items():
                    if k1 == "coord" :
                        g=k
                    else:
                        g=k1
                    l.update({ g : v1})


                locationGenerationTruckDrone(l)

                node_labels = (node_locations.keys())
                ni_solverDrone = NearestInsertionSolver(node_labels, node_distances)
                ni_solution_Drone = ni_solverDrone.run()

                ni_solution_DroneFinal.append(ni_solution_Drone)
                open("TruckDronelocation.txt", 'w').close()
                NearestInsertionDistanceDrone=NearestInsertionDistanceDrone+ni_average_distance
                #print("Drone distance", NearestInsertionDistanceDrone)

    new_d = [val for sublist in ni_solution_DroneFinal for val in sublist]

    new_d.append('A0')
    for t in range(0, len(new_d)):
        for k, v in truckDroneDict.items():
            for k1, v1 in v.items():
                if new_d[t] == k1:
                    l2.append(v1)
                    break
                elif(new_d[t] == k):
                    l2.append(v1)
                    break

    print("The total distance travelled",NearestInsertionDistanceTruck+NearestInsertionDistanceDrone)


    end_time_NI=datetime.now()
    return (new_d,l2)

