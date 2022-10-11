
import os
import sys
import json

os.chdir(sys.argv[1])
print(os.getcwd)
os.system("npm run test")
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
commitNum = sys.argv[2]

os.chdir("..")

row = "{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
    package,commitNum,numFailedTestSuites,numFailedTests,numPassedTestSuites,numPassedTests,numPendingTestSuites,numPendingTests,numRuntimeErrorTestSuites,numTotalTestSuites,numTotalTests)

with open('data.csv','a') as fd:
    fd.write(row)