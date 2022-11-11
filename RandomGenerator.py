import numpy as np
TruckDroneMapping,dronedict,truck_dict = ({}for _ in range(50))

truckCities,TruckData,truckCities,droneX1, droneY1,p = ([] for _ in range(50))


def randomgenerator (size, maxNoTruck, maxNoDrone):
    # size:Represents the maximum size of the Grid
    # maxNoTruck represents maximum number of Trucks
    # maxNoDrone represents maximum number of Drone
    truckX, truckY, droneX, droneY = ([] for i in range(4))
    # Randomising number of Drones
    tName = 65
    dName = 97
    dcounter=0
    tcounter = 0
    # Randomly generating maximum number of trucks and Drones based on Small Medium and Large scale instances
    noOfTruck = np.random.randint(3, 5)
    MAXnoOfDrone = np.random.randint(8, 10)
    c=0
    for i in range(0, noOfTruck):
        if (tName > 90):
            tcounter = tcounter + 1
            tName = 65

        # Random x and y coordinates for Truck Delivery
        Tx = np.random.randint(1, size - 15)
        Ty = np.random.randint(1, size - 15)
        truckX.append(Tx)
        truckY.append(Ty)
        # Randomising number of Drones
        n=MAXnoOfDrone
        noOfDrone = np.random.randint(1, 5)
        c=c+noOfDrone
        MAXnoOfDrone=MAXnoOfDrone-noOfDrone+1
        droneX.append([])
        droneY.append([])
        # Location of Truck in complex Format
        complexTruck = complex(Tx, Ty)
        TruckDroneMapping.update({(chr(tName)+str(tcounter)): {"coord": complexTruck}})
        for j in range(0, noOfDrone):
            if (dName > 122):
               dcounter = dcounter + 1
               dName = 97

            Dx = np.random.randint(abs(truckX[i] - abs(size / 5)), abs(truckX[i] + abs(size / 5)))
            Dy = np.random.randint(abs(truckY[i] - abs(size/ 5)), abs(truckY[i] + abs(size / 5)))
            droneX1.append(Dx)
            droneY1.append(Dy)
            droneX[i].append(Dx)
            droneY[i].append(Dy)
            complexDrone = complex(Dx, Dy)
            TruckDroneMapping[chr(tName)+str(tcounter)][chr(dName)+str(dcounter)] = complexDrone

            dName = dName + 1
        tName = tName + 1
    truckCities = [sub["coord"] for sub in TruckDroneMapping.values() if "coord" in sub.keys()]

    return (TruckDroneMapping,truckX,truckY,droneX1,droneY1)

