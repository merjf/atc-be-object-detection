import json
from datetime import datetime

def loadData():
    flightsFile = open('./data/flights.json')
    data = json.load(flightsFile)
    blackListCities = ["Milano", "Roma"]
    fligthCodes = []
    availableFlights = []
    thresholdTimeLowerBound = datetime.strptime("14:30", '%H:%M').time()
    thresholdTimeUpperBound = datetime.strptime("18:00", '%H:%M').time()
    for i in data["raw"]:
        fligthCodes.append(i)
    for code in fligthCodes:
        flights = data["raw"][code]["city"]["details"]["airport"]["flights"]
        for j in flights:
            currentFlight = data["raw"][code]["city"]
            startTimeFlight = datetime.strptime(j["time_start"], '%H:%M').time()
            if startTimeFlight >= thresholdTimeLowerBound and startTimeFlight <= thresholdTimeUpperBound and currentFlight["city"] not in blackListCities:
                flight = {
                    "from": "Catania",
                    "to": currentFlight["city"],
                    "airport Name": currentFlight["details"]["airport"],
                    "time": startTimeFlight
                }
                availableFlights.append(flight)
    for i in availableFlights:
        print("to: " + i["to"] + " - at: " + str(i["time"]))
    flightsFile.close()

loadData()
