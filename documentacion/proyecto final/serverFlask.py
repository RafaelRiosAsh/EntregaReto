from flask import Flask, request, jsonify
from mesa import model
from agent import Car, Obstacle, Destination, Origin
from model import *

width = 28
height= 28

app = Flask("Traffic example")

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, trafficModel
    if request.method == 'POST':
        currentStep = 0

        print(request.form)
        # print(width, height)
        trafficModel = TrafficModel()

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/updateTrafficLights', methods=['GET'])
def getGreenTrafficLights():
    global trafficModel
    if request.method == 'GET':
        greenPositions = [{"x": x, "y":0,"z":y} for (a, x, y) in  trafficModel.grid.coord_iter() for i in a if isinstance(i, Traffic_Light)]
        state = [i.state for (a,x,y) in  trafficModel.grid.coord_iter() for i in a if isinstance(i, Traffic_Light)]
        print(greenPositions)
        print("state: ",state)
        return jsonify({'positions':greenPositions,"state":state})


@app.route('/getCars', methods=['GET'])
def getCars():
    global trafficModel

    if request.method == 'GET':

        robots = [a for a in trafficModel.grid.coord_iter() if isinstance(a,Car)]

        carPositions = [({"x": x, "y":0.1, "z": y}, i.unique_id) for (a,x,y) in trafficModel.grid.coord_iter() for i in a if isinstance(i,Car)]
        #print(carPositions)
        sortedPositions = sorted(carPositions, key= lambda a: a[1])

        carPositions = [p for (p,a) in sortedPositions] 
        return jsonify({'positions':carPositions})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep,trafficModel 
    if request.method == 'GET':
        trafficModel.step()
        currentStep += 1
        #print("moves: ", trafficModel.count_moves(trafficModel))
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)

# @app.route('/updatelights', methods=['GET'])
# def getLights():
#     global trafficModel

#     if request.method == 'GET':
#         carPositions = [a for a in trafficModel.grid.coord_iter() if isinstance(a,Robot)]
#         print("lights: ",carPositions)
#         sortedPositions = sorted(carPositions, key= lambda a: a[1])
#         print("sorted lights: ",sortedPositions)

#         carPositions = [p for (p,a) in sortedPositions] 
#         return jsonify({'positions':carPositions})

#@app.route('/getDestinations', methods=['GET'])
# def getDestinations():
#     global trafficModel
#     if request.method == 'GET':
#         destinyPositions = [{"x": x*10, "y":2.52,"z":y*10} for (a, x, y) in  trafficModel.grid.coord_iter()if isinstance(a, Destination)]
#         return jsonify({'positions':destinyPositions})

# @app.route('/getOrigins', methods=['GET'])
# def getOrigins():
#     global trafficModel
#     if request.method == 'GET':
#         originPositions = [{"x": x*10, "y":2.52,"z":y*10} for (a, x, y) in  trafficModel.grid.coord_iter()if isinstance(a, Origin)]
#         return jsonify({'positions':originPositions})

# @app.route('/getRoads', methods=['GET'])
# def getRoads():
#     global trafficModel
#     if request.method == 'GET':
#         roadPositions = [{"x": x*10, "y":2.52,"z":y*10} for (a, x, y) in  trafficModel.grid.coord_iter()if isinstance(a, Road)]
#         return jsonify({'positions':roadPositions})
# @app.route('/getObstacles', methods=['GET'])
# def getObstacles():
#     global trafficModel
#     if request.method == 'GET':
#         obstaclePositions = [{"x": x*10, "y":2.52,"z":y*10} for (a, x, y) in  trafficModel.grid.coord_iter()if isinstance(a, Obstacle)]
#         return jsonify({'positions':obstaclePositions})