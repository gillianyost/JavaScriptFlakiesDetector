## argument 1: Results Folder
## argument 2: how many times tests were run
## argument 3: Output File
## argument 4: timeData File
## argument 5: clean or no_clean



import json
import sys
import os
import fnmatch
import csv

def clean_json(filename, newDirPath):
    f = open(filename, 'r')
    data = json.load(f)
    head, tail = os.path.split(filename)
    path = newDirPath + "/" + "CleanTestReports/" + tail
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as outfile:
        json.dump(data, outfile, indent=4)
    f.close()



def flakie_parser():
    path = sys.argv[1]
    package_flakies = {}
    flakie_text = []
    subjectsNoRun = []
    total_flakies = 0
    proj_flakie = 0
    flakie_proj = {}
    csvFiles = {}
    output = {}
    subjects = []
    numAllSubjects = 0
    all_tests = 0
    csv_found = False

    obj = os.scandir(path)
    for entry in obj:
        csv_found = False
        if entry.is_dir():
            inner = os.scandir(entry)
            for files in inner:
                outFile = path + entry.name + "/" + files.name
                head, tail = os.path.split(outFile)
                if files.is_file() and fnmatch.fnmatch(files.name, '*.csv'):
                    # with open(outFile) as csv_file:
                    #     data = list(csv.reader(csv_file))
                    numAllSubjects += 1
                    csvFiles[head] = outFile
                    csv_found = True
                elif files.is_file() and fnmatch.fnmatch(files.name, '*flakies.txt'):
                    flakie_text.append(outFile)
                elif files.is_file() and fnmatch.fnmatch(files.name, '*flakies.txt'):
                    print("test.json")
                elif files.is_dir() and fnmatch.fnmatch(files.name, 'testReports*') and sys.argv[5] == 'clean':
                    testReports = os.scandir(files)
                    # print(files.name)
                    for report in testReports:
                        if report.is_file() and fnmatch.fnmatch(report.name, 'testReport*'):
                            jsonFile = path + entry.name + "/" + files.name + "/" + report.name
                            pathNewDir = path + entry.name
                            # print(pathNewDir)
                            clean_json(jsonFile, pathNewDir)
            if not csv_found:
                subjectsNoRun.append(path + entry.name)
    output['Number of Subjects Run'] = numAllSubjects
    output['Subjects not Run'] = subjectsNoRun
    flakies_exist = False
    for fileName in flakie_text:
        flakieFiles = []
        flakieTest = {}
        flakies = {}
        agg_data = {}
        total_proj_flakie = 0  
        numFailures = 0  
        head, tail = os.path.split(fileName)
        subjects.append(head)
        f = open(fileName, "r")
        check = f.readline()
        if check == "":
            f.close()
            continue
        f.seek(0,0)
        proj_flakie += 1
        Lines = f.readlines()
        for line in Lines:
            tmp = line.split(' : ')
            total_proj_flakie += 1
            total_flakies += 1
            if tmp[1] not in flakieFiles:
                flakieFiles.append(tmp[1])
                tests = []
                tests.append(tmp[2])
                flakieTest[tmp[1]] = tests
            else:
                flakieTest[tmp[1]].append(tmp[2])
        # print("FLAKIE TEST:")
        # print(flakieTest)
        # print("FLAKY FILES")
        # print(flakieFiles)

        for i in range(int(sys.argv[2])):
            jsonFile = head + "/testReports/" + "testReport" + str(i) + ".json"
            with open(jsonFile) as file:
                data = json.load(file)
            for testSuite in data['testResults']:
                if testSuite['name'] in flakieFiles:
                    for testResult in testSuite['assertionResults']:
                        if testResult['title'] in flakieTest[testSuite['name']]:
                            key = testSuite['name'] + ":" + testResult['title'] + ":" + testResult['fullName']
                            flakies_exist = True
                            if key in flakies:
                                if testResult['status'] == 'failed':
                                    flakies[key]['failures'] += 1
                                    flakies[key]['Flake Rate for Test'] = flakies[key]['failures']/int(sys.argv[2])
                                    flakies[key]['Failure Messages'].append(testResult['failureMessages'][0])
                                    numFailures += 1
                                flakies[key]['RunStatus'].append(testResult['status'])
                            else:
                                tempDic = {}
                                failTemp = []
                                if testResult['status'] == 'failed':
                                    tempDic['failures'] = 1
                                    tempDic['Flake Rate for Test'] = tempDic['failures']/int(sys.argv[2])
                                    failTemp.append(testResult['failureMessages'][0])
                                    numFailures += 1
                                else:
                                    tempDic['failures'] = 0
                                temp = []
                                tempDic["Failure Messages"] = failTemp
                                temp.append(testResult['status'])
                                tempDic['RunStatus'] = temp
                                flakies[key] = tempDic
        package_flakies[head] = flakies
        agg_data['Flakie in Project'] = total_proj_flakie
        agg_data['Number of Tests'] = -1
        agg_data['Length of Running'] = -1
        agg_data['Number of Flakie Failures'] = numFailures
        agg_data["Flake Rate for Subject"] = numFailures/(int(sys.argv[2])*total_proj_flakie)
        flakie_proj[head] = agg_data
        output['Flakie Total'] = total_flakies
        output['Flakie numSubjects'] = proj_flakie
        output['Flakie Subjects'] = flakie_proj
        output['Tests'] = package_flakies
        

        # sys.argv[1],numFlakyTests,numODFlakyTests,numNODFlakyTests,numFailedTestSuites,numFailedTests,numPassedTestSuites,numPassedTests,numPendingTestSuites,numPendingTests,numRuntimeErrorTestSuites,numTotalTestSuites,numTotalTests)
    if flakies_exist == False:
        print("No Flakie tests Found")
        return

    for key in csvFiles:
        with open(csvFiles[key], newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            for row in data:
                all_tests += int(row[12])
                if key in output['Flakie Subjects']:
                    output['Flakie Subjects'][key]['Number of Tests'] = int(row[12])
                    output['Flakie Subjects'][key]['Precentage of Flake Tests'] = (output['Flakie Subjects'][key]['Flakie in Project']/int(row[12])) * 100

    # with open(sys.argv[4], newline='') as csvfile:
    #     data = csv.reader(csvfile)
    #     for row in data:
    #         header = path + row[0].replace("/", "_")
    #         if header in output['Flakie Subjects']:
    #             time = int(row[2]) - int(row[1])
    #             output['Flakie Subjects'][header]['Length of Running'] = time

    # output['All Test Total'] = all_tests
    # output['All Precetage Flakie'] = (output['Flakie Total']/all_tests) * 100
    # output['Average Flakie per Subject'] = (output['Flakie Total']/numAllSubjects)


    print("Total of " + str(total_flakies) + " Flakie tests across " + str(proj_flakie) + " subjects.")

    with open(sys.argv[3], "w") as outfile:
        json.dump(output, outfile, indent=4)

    print(path + " run " + sys.argv[2] + " times parsed into " + sys.argv[3] + ".\n")

if __name__ == '__main__':
    flakie_parser()
