import csv
import requests
import json

def ReadFile(filePath):
    InputRecords = {}
    inputIds = []
    # desturl = []
    with open(filePath, 'r') as input:
        csvreader = csv.reader(input, delimiter=',', quotechar='"')
        next(csvreader, None)
        for row in csvreader:
            id = row[0]
            destination = (row[3], row[4])
            if(id in inputIds):
                # We already have in in the InputRecords List
                InputRecords[id]['dest'].append(destination)
                InputRecords[id]['records'].append(row)
            else:
                # we are seeing this source for the first time
                srcPoistion = (row[1], row[2])
                obj = {'src': srcPoistion, 'dest': [
                    destination], 'records': [row]}
                InputRecords[id] = obj
                inputIds.append(id)
    return InputRecords,inputIds

csvfile = open('bank_drive_dist_output_slot1'+".csv", 'ab')

def getDistances(count,src,destinations):
    # URL should be as follows:
    # Base parameters
    baseUrl = 'https://matrix.route.api.here.com/routing/7.2/calculatematrix.json?'
    # free key
    key = r'your key'
    code ='your code'
       add_param = 'fastest;car;traffic:disabled'
    dist_param='distance'   
    # make the URL
    url = baseUrl + "app_id ={0}&app_code={1}&start0={2},{3}".format(key,code,src[0],src[1])
    # print(url)

    # for each tuple in destination
    # desturl = []
    for i in range(0, len(destinations)):
        d = destinations[i]
        url = url + "&destination"+str(i)+"={0},{1}".format(d[0],d[1])
    # print(url)

    # finally set the mode
    url = url + "&mode=fastest;car;traffic:disabled&summaryAttributes=distance"
    print(url)
    r = requests.get(url).json()
    # print(r)
    # dist = r['response']['matrixEntry'][0]['summary']['distance']
    dist = r['response']['matrixEntry']
    for k in range(0,len(dist)):
        d1 = destinations[k]
        try:
            distances = r['response']['matrixEntry'][k]['summary']['distance']
            travelTime = r['response']['matrixEntry'][k]['summary']['costFactor']
            # print(distances)
        except:
            status = r['response']['matrixEntry'][k]['status']
            if status == 'failed':
                distances = 'NA'
                travelTime = 'NA'
        data = "~".join([count,src[0],src[1],d1[0],d1[1],str(distances),str(travelTime)])
        print(data)
        csvfile.write(data.encode("utf-8")+"\n".encode("utf-8"))

        
    # Now make the request

inputRecord,inputID = ReadFile('bank_drive_dist_input.csv')
source = []
destination = []
ids = []
for item,k in zip(inputRecord,inputID):
    val= inputRecord[item]
    # print(k)
    src = val.get('src')
    dest = val.get('dest')
    source.append(src)
    destination.append(dest)
    ids.append(k)
# print(ids)
# for k in ids:
#     print(k)
# # print(ls)
for k,i,j in zip(ids,source,destination):
    getDistances(k,i,j)


    







