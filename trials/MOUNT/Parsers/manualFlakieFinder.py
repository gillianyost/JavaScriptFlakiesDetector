import sys
import json
import os
from pathlib import Path

#   Example of how testResultsFull_Old will look
# 	suite named FileSuite1
# 		status is passed
# 	tests named 
# 		test1 - passed
# 		test2 - passed
# 		test3 - passed
#   suite named FileSuite2
# 		status is failed
# 	tests named 
# 		test1 - passed
# 		test2 - failed
# 		test3 - passed
		
# {"FileSuite1": {"status":passed, "assertionResults": {"test1":passed,"test2":passed,"test3":passed}},
# "FileSuite2": {"status":failed, "assertionResults": {"test1":passed,"test2":failed,"test3":passed}}}



if __name__ == '__main__':
    path = sys.argv[1]
    obj = os.scandir(path)
    for entry in obj: # Entry is folder name
        folder = path + entry.name 
        counter = 0
        flaky_file = folder + '/' + entry.name + '_flakies.txt'
        testResultsFull_Old = {}
        flakiesAll = []
        numFlakyTests = 0
        fileName = folder +'/testReports/testReport' + str(counter) + '.json'
        fileNamePath = Path(fileName)
        if (fileNamePath.is_file()):
            flakies = open(flaky_file, 'w')
            while (counter < int(sys.argv[2])):
                print(counter)
                fileName = folder +'/testReports/testReport' + str(counter) + '.json'
                with open(fileName) as f:
                    data = json.load(f)
                if (counter > 0):
                    for testSuite_Current in data['testResults']:
                        OLD_testsuite = testResultsFull_Old[testSuite_Current['name']]
                        currentSuite = testSuite_Current['name']
                        for testResult in testSuite_Current['assertionResults']:
                            OLD_testResult = OLD_testsuite["assertionResults"]
                            key = 'fullName'
                            if key in testResult:
                                fullCatName = testResult['title'] + testResult['fullName']
                            else:
                                fullCatName = testResult['title']
                            if fullCatName in OLD_testResult:
                                if testResult['status'] != OLD_testResult[fullCatName]:
                                    flakyDetected = True
                                    print("Flaky Detected")
                                    print("First Run: " + OLD_testResult[fullCatName])
                                    print("Next Run: " + testResult['status'])
                                    print("Flakie: " + testSuite_Current['name'] + testResult['title'] + " " + testResult['fullName'])
                                    fullName = testSuite_Current['name'] + " " + testResult['title'] + " " + testResult['fullName']
                                    if fullName not in flakiesAll:
                                        flakiesAll.append(fullName)
                                        numFlakyTests = numFlakyTests + 1
                                        flakies.write(sys.argv[1]+" : "+testSuite_Current['name']+" : "+testResult['title']+ " : " + testResult['fullName'] +" : NEW: "+testResult['status']+ " : FIRST RUN: " + OLD_testResult[fullCatName] + "\n")
                if (counter == 0):
                    for testSuite_Old in data['testResults']:
                        suite = {}
                        results = {}
                        for testResult in testSuite_Old['assertionResults']:
                            key = 'fullName'
                            if key in testResult:
                                fullCatName = testResult['title'] + testResult['fullName']
                            else:
                                fullCatName = testResult['title']
                            results[fullCatName] = testResult['status']
                        suite["assertionResults"] = results
                        testResultsFull_Old[testSuite_Old['name']] = suite
                counter = counter + 1
            flakies.close()
    print("Manual Flakie Finder run on testReport Data for " + sys.argv[1] + ".\n")
            