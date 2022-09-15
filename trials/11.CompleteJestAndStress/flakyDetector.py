
import os
import sys
import json

os.chdir("package")
print(os.getcwd)
counter = 0
flakyDetected=False
numPreviousFailedTests=-1
numFlakyTests=0
numODFlakyTests=0
testSuites = {}
ODflaky = []
NODflaky = []
flakiesAll = []

while (counter < int(sys.argv[2])):
    os.system(sys.argv[3])
    with open('testReport.txt') as f:
        data = json.load(f)
    if (counter > 0):
        for testResult in data['testResults']:
            for assertionResult in testResult['assertionResults']:
                if (testSuites[testResult['name'].split('package/')[1]][assertionResult['title']] != assertionResult["status"]):
                    flakyDetected = True
                    if testResult['name'].split('package/')[1] not in flakiesAll:
                        flakiesAll.append(testResult['name'].split('/package')[1])
                        numFlakyTests = numFlakyTests + 1
                        with open('../flakies.txt', 'a') as flakies:
                            flakies.write(sys.argv[1]+" : "+testResult['name'].split('package/')[1]+" : "+assertionResult['title']+"\n")
    testSuites = {}
    for testResult in data['testResults']:
        testSuites[testResult['name'].split('package/')[1]] = {}
        for assertionResult in testResult['assertionResults']:
            testSuites[testResult['name'].split('package/')[1]][assertionResult['title']] = assertionResult["status"]
    os.system("rm testReport.txt")
    counter = counter + 1

numNODFlakyTests = numFlakyTests - numODFlakyTests
os.system(sys.argv[3])
numFailedTestSuites = data['numFailedTestSuites']
numFailedTests = data['numFailedTests']
numPassedTestSuites = data['numPassedTestSuites']
numPassedTests = data['numPassedTests']
numPendingTestSuites = data['numPendingTestSuites']
numPendingTests = data['numPendingTests']
numRuntimeErrorTestSuites = data['numRuntimeErrorTestSuites']
numTotalTestSuites = data['numTotalTestSuites']
numTotalTests = data['numTotalTests']
os.system("rm testReport.txt")

print("Flaky Tests: ", numFlakyTests)
print("OD Flaky Tests: ", numODFlakyTests)
print("NOD Flaky Tests: ", numFlakyTests - numODFlakyTests)

os.chdir("..")

row = "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
    sys.argv[1],numFlakyTests,numODFlakyTests,numNODFlakyTests,numFailedTestSuites,numFailedTests,numPassedTestSuites,numPassedTests,numPendingTestSuites,numPendingTests,numRuntimeErrorTestSuites,numTotalTestSuites,numTotalTests)

with open('data.csv','a') as fd:
    fd.write(row)

# with open('test.json', 'w') as d:
#     Dict = [{"seed":1234567,"flakyTestDetected":False}]
#     json.dump(Dict, d)