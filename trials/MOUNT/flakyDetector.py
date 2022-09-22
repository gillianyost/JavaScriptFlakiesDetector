
import os
import sys
import json

os.chdir("package")
# print(os.getcwd)
counter = 0
flakyDetected=False
numPreviousFailedTests=-1
numFlakyTests=0
numODFlakyTests=0
testSuites = {}
ODflaky = []
NODflaky = []
flakiesAll = []

print("In PYTHON")
os.system("echo jest")
flaky_file = "../" + sys.argv[1] + '_flakies.txt'
flaky_file = flaky_file.replace("/", "_")
# os.system("alias jest='jest --json --outputFile=testReport.txt'")
while (counter < int(sys.argv[2])):
    # os.system(sys.argv[3])
    os.system("jest --json --outputFile=testReport.txt")
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
                        with open(flaky_file, 'a') as flakies:
                            flakies.write(sys.argv[1]+" : "+testResult['name'].split('package/')[1]+" : "+assertionResult['title']+"\n")
    testSuites = {}
    for testResult in data['testResults']:
        testSuites[testResult['name'].split('package/')[1]] = {}
        for assertionResult in testResult['assertionResults']:
            testSuites[testResult['name'].split('package/')[1]][assertionResult['title']] = assertionResult["status"]
    os.system("rm testReport.txt")
    counter = counter + 1

numNODFlakyTests = numFlakyTests - numODFlakyTests
# os.system(sys.argv[3])
os.system("jest --json --outputFile=testReport.txt")
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
output_file = sys.argv[1] + '_data.csv'
output_file = output_file.replace("/", "_")
print(output_file)
with open(output_file,'a') as fd:
    fd.write(row)

# with open('test.json', 'w') as d:
#     Dict = [{"seed":1234567,"flakyTestDetected":False}]
#     json.dump(Dict, d)