
import os
import sys
import json
import subprocess
from unittest import TestResult

## -------- Command from csv File ---------
# command = ""
# with open('command.txt', 'r') as file:
#     command = file.read().rstrip()
# command = command.replace("jest", "jest --json --outputFile=testReport.json --testSequencer=../RandomSequencerCompiled.js")
# command = command.replace("jest", "jest --json --outputFile=testReport.json")
# print("TEST COMMAND: " + command)
# -----------------------------------------

os.chdir("package") # May need to update to not use os
counter = 0
flakyDetected=False
numPreviousFailedTests=-1
numFlakyTests=0
numODFlakyTests=0
testSuites = {}
ODflaky = []
NODflaky = []
flakiesAll = []
# update = int(sys.argv[3])
update = 1

print("In PYTHON")
flaky_file = sys.argv[1] + '_flakies.txt'
flaky_file = flaky_file.replace("/", "_")
flaky_file = "../" + flaky_file
testResultsFull_Old = {}

while (counter < int(sys.argv[2])):
    # os.system(sys.argv[3]) # Uses inputted command, not working would use command variable instead. May need to update to not use os
    if update == 0:
        os.system("jest --verbose --json --outputFile=../testReport.json") # May need to update to not use os
    else:
    #     os.system("jest --json --runInBand --outputFile=../testReport.json --testSequencer=/home/flakie/RandomSequencerCompiled.js") # Used for amzn
        with open('../testReport.json') as f:
            data = json.load(f)
    print("Renaming Test Reults")
    os.rename('../testReport.json', '../testReport' + str(counter) + '.json')
    counter = counter + 1
numNODFlakyTests = numFlakyTests - numODFlakyTests
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