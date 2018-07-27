from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import json
import requests
import json
from collections import defaultdict


counter = 0
index = 0
filePath = '/home/parvez/Documents/newConverted.json'
apiKey = 'my_api_key'


target = 'de'

app = Flask(__name__)
api = Api(app)


def arraytojson(arry, jsonFile):

    counter = 0

    for i in jsonFile["child"]:
        if ('tag' in i and i['tag'] == 'p'):
            for j in i['child']:
                if ('tag' in j and j['tag'] == 'strong'):
                    for k in j['child']:
                        if ('node' in k and k['node'] == 'text'):
                            k['text'] = str(arry[counter])
                            counter += 1
                        else:
                            pass
                elif ('node' in j and j['node'] == "text"):
                    j['text'] = str(arry[counter])
                    counter += 1
        else:
            pass

    print(jsonFile)
    return jsonFile

def translateDocument(doc):
    params ={'key':apiKey,'q':doc,'soure':'en','target':target}
    response = requests.post('https://www.googleapis.com/language/translate/v2',params=params)
    result = json.loads(response.content)['data']['translations']
    #print(result)
    payload = []
    for i in result:
        payload.append(str(i['translatedText']))
    return payload


def getSubject(data):
    counter = 0
    index = 0
    pdfFile = defaultdict(list)
    for i in data['result']:
        for j in i['segments']:
            # print(j)
            # print(index)
            # print(counter)
            if(j.get('page_number')==counter):
                if(j.get('heading')):
                    pdfFile['subject'][index-1]+="  "+j['heading']['content']
                    if(j.get('content')):
                        for msg in j['content']:
                            pdfFile['text'][index-1]+="\n"+msg['content']
                    else:
                        pass
                elif(j.get('content')):
                    for msg in j['content']:
                        pdfFile['text'][index-1]+="\n"+msg['content']
                else:
                    pass
            else:
                pdfFile['pageNumber'].append(j['page_number'])
                if(j.get('heading')):
                    pdfFile['subject'].append(j['heading']['content'])
                    if(j.get('content')):
                        for msg in j['content']:
                            pdfFile['text'].append(msg['content'])
                    else:
                        pdfFile['text'].append('')
                elif(j.get('content')):
                    print('...')
                    pdfFile['subject'].append('')
                    for msg in j['content']:
                        pdfFile['text'].append(msg['content'])
                else:
                    pdfFile['text'].append('')
                counter = j['page_number']
                index+=1
    return json.dumps(pdfFile)

class jsontoarray(Resource):
    def post(self):
        payload = request.get_data()
        jsonData = json.loads(request.get_data())

        arry = []

        for i in jsonData["child"]:
            if ('tag' in i and i['tag'] == 'p'):
                for j in i['child']:
                    if ('tag' in j and j['tag'] == 'strong'):
                        for k in j['child']:
                            if ('node' in k and k['node'] == 'text'):
                                arry.append(k['text'])
                                k['text'] = ''
                            else:
                                pass
                    elif ('node' in j and j['node'] == "text"):
                        arry.append(j['text'])
                        j['text'] = ''
            else:
                pass

        result = translateDocument(arry)
        tarray = arraytojson(result, jsonData)
        return tarray

    #pdf parser api

    def get(self):
        with open(filePath) as json_file:
            json_data = json.load(json_file)
            #print(json_data['result'])
            jsonObject = getSubject(json_data)
            print(jsonObject)
            return jsonObject


api.add_resource(jsontoarray, "/jsontoarray/")
app.run(debug=True)

