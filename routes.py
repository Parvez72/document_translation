from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import json
from google.cloud import translate

apiKey = 'AIzaSyDOnd3s6gMOHyUwesZMaHdq92LkgexGslI'

translate_client = translate.Client()


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
    result = translate_client.translate(doc,target_language=target, source_language='en')
    print(result)
    payload = []
    for i in result:
        payload.append(str(i['translatedText']))
    return payload

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


api.add_resource(jsontoarray, "/jsontoarray/")
app.run(debug=True)

