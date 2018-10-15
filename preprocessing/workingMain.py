"""
all_hospitals_preCSV

1. Reads in main text file
2. Identifies each hospital object
3. For each hospital object, calls Function single_hospital_csv()
"""


class Hospital:
    def __init__(self,id,categories,details):
        self.id = id
        self.categories = categories
        self.details = details
        self.d3_feature_object = self.make_d3_feature_object()


    def make_d3_feature_object(self):
        return {"type":"Feature",
                "id":self.id,
                "geometry":
                {"type":"Point",
                "coordinates":[self.details[-2],self.details[-1]]
                },
                "properties": self.return_single_hospital_dict()
                }


    def return_single_hospital_dict(self):
        import json
        thisDict = {}
        for i in range(len(self.details)):
            thisDict[self.categories[i]] = self.details[i]
        return thisDict

    def cleanAll(self):
        self._cleanLonLat()
        self._cleanCurrentStatus()
        self._cleanAddress()
        self._cleanListStrings()
        self._cleanCategories()

    def _cleanInnerLists(self):
        innerLists = ["Closure Year","Number of Beds"]

    def _cleanLonLat(self):
        if self.categories[-1] == "Coordinates":
            theseCoords = self.details[-1][0].split(",")
            lon = theseCoords[0]
            lat = theseCoords[1]

            self.categories.pop()
            self.details.pop()

            self.categories.append("Longitude")
            self.categories.append("Latitude")
            self.details.append(float(lon))
            self.details.append(float(lat))

        elif self.categories[-1] == "Latitude":
            self.details[-1] = float(self.details[-1][0])
            self.details[-2] = float(self.details[-2][0])

    def _cleanCurrentStatus(self):
        if len(self.categories) == 11:
            self.categories.insert(-3,"Current Status")
            self.details.insert(-3,"unknown")

    def _cleanAddress(self):
        try:
            addressIndex = self.categories.index("Address")
            self.categories.pop(addressIndex)
            self.details.pop(addressIndex)
        except ValueError:
            return

    def _cleanListStrings(self):
        for i in range(len(self.details)):
            if type(self.details[i]) == list:
                if len(self.details[i]) == 3:
                    focusIndex = -1
                    self.details[i] = int(self.details[i][focusIndex])
                else:
                    focusIndex = 0
                    self.details[i] = self.details[i][focusIndex]
            else:
                self.details[i] = self.details[i]

    def _cleanCategories(self):
        for i in range(len(self.categories)):
            self.categories[i] = self.categories[i].replace(" ","_")

    def __str__(self):
        return str(self.details[:])

class Hospitals:
    def __init__(self):
        self.numHospitals = 0
        self.hospitalList = [] # list of hospital objects

    def getInfo(self):
        from random import randint
        print("Number of Hospitals: ",self.numHospitals)
        print("Random Hospital Data:\n"+ self.hospitalList[randint(0,self.numHospitals)].__str__())

    def cleanHospitals(self):
        for hospital in self.hospitalList:
            hospital.cleanAll()

    def createHospital(self,hosString):
        """Creates new hospital object, appends it to list of hospitals """
        newId = self.numHospitals
        categories, details = self._parseHospital(hosString)
        newHospital = Hospital(newId,categories,details)
        self.hospitalList.append(newHospital)
        self.numHospitals+=1

    def _parseHospital(self,thisHospital):
        thisHospital = thisHospital.replace("\\","").replace("\\n","")
        thisHospital = thisHospital.replace("n,1]n","]").replace("n,3]n","]").replace("null","None")

        thisHospital_data = eval(thisHospital)
        categories = []
        details  = []
        for item in thisHospital_data:
            categories.append(item[0])
            details.append(item[1])
        return categories, details

    def _findAll(self,big_string,hosStart,hosEnd):
        import re
        startList = []
        for start in re.finditer(hosStart, big_string):
            startList.append(start.start()-3)

        endList = []
        for end in re.finditer(hosEnd, big_string):
            endList.append(end.end())

        return startList, endList


    def parseMainData(self,fileName):
        """Method to parse a specific text file with hospital information"""
        file = open(fileName,"r",encoding='utf-8')
        data_string = file.read()

        hosStart = '"Hospital\\\\",'
        hosEnd = '\\\\n,1]\\\\n]'

        startList, endList = self._findAll(data_string,hosStart,hosEnd)

        hospital_string_list = []
        for i in range(len(startList)):
            this_hospital_string = data_string[startList[i]:endList[i]]
            hospital_string_list.append(this_hospital_string)

        return hospital_string_list

    def createAllHospitals(self,hospital_string_list):
        for each_hospital in hospital_string_list:
            self.createHospital(each_hospital)

    def doMagic(self,filename):
        firstParse = self.parseMainData(filename)
        self.createAllHospitals(firstParse)
        self.cleanHospitals()


    def makeJSON(self):
        import json
        myDict = [] #overall dictionary
        for hospital in self.hospitalList:
            myDict.append(hospital.return_single_hospital_dict())


        jsonData = json.dumps(myDict)
        with open('hospitals.json', 'w') as f:
            json.dump(jsonData, f)
        return jsonData

    def makeD3_JSON(self):
        import json
        myDict = {"type":"FeatureCollection"}


        feature_object_list = [] #overall dictionary
        for hospital in self.hospitalList:
            feature_object_list.append(hospital.make_d3_feature_object())

        myDict["features"] = feature_object_list
        jsonData = json.dumps(myDict)
        with open('hospitals.json', 'w') as f:
            json.dump(jsonData, f)
        return jsonData


    def __str__(self):
        returnList = []
        for item in self.hospitalList: returnList.append(item.details)
        return str(returnList)

def main():
    h = Hospitals()
    file = "pre-parse-hospitals.txt"
    h.doMagic(file)
    print(h.makeD3_JSON())

if __name__ == '__main__':
    main()
