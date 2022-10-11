import json
  
# Opening JSON file
w = open('Final_list.txt', 'w')

for x in range(0, 34):
    f = open('./output/reponse' + str(x) + '.json')
  
# returns JSON object as 
# a dictionary
    data = json.load(f)
  
# Iterating through the json
# list
# print(data['total_count'])
    for i in data['items']:
        w.write(i['name'])
        w.write('\n')
        w.write(i['html_url'])
        w.write('\n')
  
# Closing file
f.close()