
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

while (counter < int(sys.argv[2])):
    os.system(sys.argv[3])
    with open('testReport.txt') as f:
        data = json.load(f)
    numCurrentFailedTests = data['numFailedTests']
    if (numPreviousFailedTests != -1) and (numCurrentFailedTests != numPreviousFailedTests):
        flakyDetected = True
        numFlakyTests = numFlakyTests + 1
    else:
        numPreviousFailedTests = numCurrentFailedTests
    with open('test.json') as g:
        seedTest = json.load(g)
    seedTest[-1]['flakyTestDetected'] = flakyDetected
    with open('test.json', 'w') as h:
        json.dump(seedTest, h)
    if (flakyDetected):
        flakyDetected = False
        os.system(sys.argv[4])
        with open('flakytestReport.txt') as l:
            flakyData = json.load(l)
        if (numCurrentFailedTests == flakyData['numFailedTests']):
            numODFlakyTests = numODFlakyTests + 1
        with open('test.json') as g:
            seedTest = json.load(g)
        seedTest[-1]['flakyTestDetected'] = False
        with open('test.json', 'w') as h:
            json.dump(seedTest, h)
        os.system("rm flakytestReport.txt")
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

with open('test.json', 'w') as d:
    Dict = [{"seed":1234567,"flakyTestDetected":False}]
    json.dump(Dict, d)