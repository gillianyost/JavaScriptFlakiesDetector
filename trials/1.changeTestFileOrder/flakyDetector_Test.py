# Working for Inializer and Consumer

import os
import sys
import json

counter = 0
flakyDetected=False
numFlakyTests=0
numODFlakyTests=0
numPreviousFailedTests=-1
testSuites = {}
ODflaky = []
NODflaky = []
flakiesAll = []

while (counter < int(sys.argv[2])):
    os.system("jest --testSequencer=./RandomSequencerCompiled.js --json --outputFile=testReport.txt") 
    with open('testReport.txt') as f:
        data = json.load(f)
    if (counter > 0):
        for testResult in data['testResults']:
            for assertionResult in testResult['assertionResults']:
                if(testSuites[testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1]][assertionResult['title']] != assertionResult["status"]):
                    flakyDetected = True
                    if testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1] not in flakiesAll:
                        flakiesAll.append(testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1])
                        numFlakyTests = numFlakyTests + 1
                    with open('./flakies.txt', 'a') as flakies:
                        flakies.write(sys.argv[1]+" : "+testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1]+" : "+assertionResult['title']+"\n")
    testSuites = {}
    for testResult in data['testResults']:
        testSuites[testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1]] = {}
        for assertionResult in testResult['assertionResults']:
            testSuites[testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1]][assertionResult['title']] = assertionResult["status"]

    with open('test.json') as g:
        seedTest = json.load(g)
    seedTest[-1]['flakyTestDetected'] = flakyDetected
    with open('test.json', 'w') as h:
        json.dump(seedTest, h)
    if (flakyDetected):
        flakyDetected = False
        os.system("jest --testSequencer=./RandomSequencerCompiled.js --json --outputFile=flakytestReport.txt") 
        with open('flakytestReport.txt') as l:
            flakyData = json.load(l)

        for testResult in flakyData['testResults']:
            for assertionResult in testResult['assertionResults']:
                if(testSuites[testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1]][assertionResult['title']] == assertionResult["status"]):
                    if testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1] in flakiesAll:
                        if testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1] not in ODflaky:
                            numODFlakyTests = numODFlakyTests + 1
                            ODflaky.append(testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1])
                            with open('./ODflakies.txt', 'a') as ODflakies:
                                ODflakies.write(sys.argv[1]+" : "+testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1]+" : "+assertionResult['title']+"\n")
                else:
                    if testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1] in flakiesAll:
                        with open('./NODflakies.txt', 'a') as NODflakies:
                            NODflakies.write(sys.argv[1]+" : "+testResult['name'].split('/home/projects/1.changeTestFileOrder/src/')[1]+" : "+assertionResult['title']+"\n")

        with open('test.json') as g:
            seedTest = json.load(g)
        seedTest[-1]['flakyTestDetected'] = False
        with open('test.json', 'w') as h:
            json.dump(seedTest, h)
        os.system("rm flakytestReport.txt")
    os.system("rm testReport.txt")
    counter = counter + 1

print("Flaky Tests: ", numFlakyTests)
print("OD Flaky Tests: ", numODFlakyTests)
print("NOD Flaky Tests: ", numFlakyTests - numODFlakyTests)
numNODFlakyTests = numFlakyTests - numODFlakyTests

os.system("jest --testSequencer=./RandomSequencerCompiled.js --json --outputFile=testReport.txt")
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

row = "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
    sys.argv[1],numFlakyTests,numODFlakyTests,numNODFlakyTests,numFailedTestSuites,numFailedTests,numPassedTestSuites,numPassedTests,numPendingTestSuites,numPendingTests,numRuntimeErrorTestSuites,numTotalTestSuites,numTotalTests)

with open('data.csv','a') as fd:
    fd.write(row)

with open('test.json', 'w') as d:
    Dict = [{"seed":1234567,"flakyTestDetected":False}]
    json.dump(Dict, d)