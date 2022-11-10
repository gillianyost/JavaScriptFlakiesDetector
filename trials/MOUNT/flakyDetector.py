
import os
import sys
import json
import subprocess
from unittest import TestResult

command = ""
with open('command.txt', 'r') as file:
    command = file.read().rstrip()

# print(command)
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
flaky_file = sys.argv[1] + '_flakies.txt'
flaky_file = flaky_file.replace("/", "_")
flaky_file = "../" + flaky_file
testResultsFull_Old = {}
# command = command.replace("jest", "jest --json --outputFile=testReport.json --testSequencer=../RandomSequencerCompiled.js")
# command = command.replace("jest", "jest --json --outputFile=testReport.json")
command = "jest --json --outputFile=testReport.json --testSequencer=../RandomSequencerCompiled.js --version"
# command = "jest --json --outputFile=testReport.json"
print("TEST COMMAND: " + command)

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


while (counter < int(sys.argv[2])):
    # os.system(sys.argv[3])
    # os.system("jest --version")
    subprocess.call(["jest", "--version"], shell=True)
    with open('testReport.json') as f:
        data = json.load(f)
    if (counter > 0):
        for testSuite_Current in data['testResults']:
            OLD_testsuite = testResultsFull_Old[testSuite_Current['name']]
            if testSuite_Current['status'] != OLD_testsuite['status']:
                for testResult in testSuite_Current['assertionResults']:
                    OLD_testResult = OLD_testsuite["assertionResults"]
                    # if testResult['status'] != OLD_testResult[testResult['fullName']]:
                    if testResult['status'] != OLD_testResult[testResult['title']]:
                        flakyDetected = True
                        print("Flakie: " + testResult['fullName'])
                        print("Flakie: " + testSuite_Current['name'] + testResult['title'])
                        # if testResult['fullName'] not in flakiesAll:
                        #     flakiesAll.append(testResult['fullName'])
                        #     numFlakyTests = numFlakyTests + 1
                        #     with open(flaky_file, 'a') as flakies:
                        #         print("Writing to " + flaky_file)
                        #         flakies.write(sys.argv[1]+" : "+testSuite_Current['name']+" : "+testResult['fullName']+" : NEW: "+testResult['status']+ " : FIRST RUN: " + OLD_testResult[testResult['fullName']] + "\n")
                        fullName = testSuite_Current['name'] + " " + testResult['title']
                        if fullName not in flakiesAll:
                            flakiesAll.append(fullName)
                            numFlakyTests = numFlakyTests + 1
                            with open(flaky_file, 'a') as flakies:
                                print("Writing to " + flaky_file)
                                flakies.write(sys.argv[1]+" : "+testSuite_Current['name']+" : "+testResult['title']+" : NEW: "+testResult['status']+ " : FIRST RUN: " + OLD_testResult[testResult['title']] + "\n")
    # testResultsFull_Old = {}
    if (counter == 0):
        for testSuite_Old in data['testResults']:
            suite = {}
            results = {}
            # suite['suiteName'] = testSuite_Old['name']
            suite['status'] = testSuite_Old['status']
            for testResult in testSuite_Old['assertionResults']:
                # results['fullName'] = testResult['fullName']
                # results[testResult['fullName']] = testResult['status']
                results[testResult['title']] = testResult['status']
            suite["assertionResults"] = results
            testResultsFull_Old[testSuite_Old['name']] = suite
    print("Renaming Test Reults")
    os.rename('testReport.json', 'testReport' + str(counter) + '.json')
    counter = counter + 1

numNODFlakyTests = numFlakyTests - numODFlakyTests
# os.system(sys.argv[3])
# os.system("jest --json --outputFile=testReport.json")
numFailedTestSuites = data['numFailedTestSuites']
numFailedTests = data['numFailedTests']
numPassedTestSuites = data['numPassedTestSuites']
numPassedTests = data['numPassedTests']
numPendingTestSuites = data['numPendingTestSuites']
numPendingTests = data['numPendingTests']
numRuntimeErrorTestSuites = data['numRuntimeErrorTestSuites']
numTotalTestSuites = data['numTotalTestSuites']
numTotalTests = data['numTotalTests']

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