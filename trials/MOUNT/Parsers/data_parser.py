import json
import sys
import csv


if __name__ == '__main__':
    f = open(sys.argv[2], 'w')
    writer = csv.writer(f)

    with open(sys.argv[1]) as file:
        data = json.load(file)
        subjects = data['Tests']
        subject_keys = list(subjects.keys())
        for sub_key in subject_keys:
            # print(sub_key)
            test_dict = subjects[sub_key]
            tests_keys = list(test_dict)
            for key in tests_keys:
                row = []
                row.append(sub_key)
                # print(key)
                row.append(key)
                # print(test_dict[key]['failures'])
                row.append(test_dict[key]['failures'])
                failMsg = 'timeout'
                for msg in test_dict[key]['Failure Messages']:
                    if 'timeout' not in msg:
                        failMsg = 'OtherFlakie'
                if test_dict[key]['failures'] == 0:
                    failMsg = 'SuiteFailRun'
                row.append(failMsg)
                writer.writerow(row)
    f.close()
    print("Data parsed for " + sys.argv[1] + " into " + sys.argv[2] + ".\n")
