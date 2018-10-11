'''
Flask page to display various home smart device data
Could host serverless via AWS lambda
'''
from flask import Flask, render_template, redirect
from flask import request as r
import GetStationData

HOME_NAME = "Krueger 42 Primrose Bank Road"
NETATMO_KEYS_TO_CHECK = ["user","devices"]#["user","devices","modules","dashboard_data","places"]


app = Flask(__name__)


def nested_get(input_dict, nested_key):
    internal_dict_value = input_dict
    for k in nested_key:
        internal_dict_value = internal_dict_value.get(k, None)
        if internal_dict_value is None:
            return None
    return internal_dict_value

def results_formatting(station_dict,keystocheck):
    for k, v in station_dict.items():
        if k in keystocheck:
            yield v
        elif isinstance(v, dict):
            for id_key,id_val in v.items():
                if id_key in keystocheck:
                    yield id_val
        elif isinstance(v, list):
            for listitems in v:
                yield listitems



@app.route('/showall', methods=['GET'])
@app.route('/showall/<homename>', methods=['GET'])
def showall(homename=None):

    netatmopayload = GetStationData.get_netatmo(auth)
    nestpayload = GetStationData.get_nest(nestauth)
	
    NetatmoToFormat = results_formatting (netatmopayload,NETATMO_KEYS_TO_CHECK)
    formattednetatmodata = ""
    for item in NetatmoToFormat:
        formattednetatmodata = formattednetatmodata + "<br><br>" + (str(item))
        
    #print (formattednetatmodata)



    '''doc sections to break down
        - Welcome Message
        - Weather Panel (netatmo)
        - Home Heat Panel (nest)
    '''
   
    weatherpanel = "<p>NETATMO DATA:" + formattednetatmodata + "</p>"
    heatingpanel = "<p> NEST DATA:" + str(nestpayload) + "</p>"

    showallcontent = weatherpanel + "<br>" + heatingpanel

    devicenamebody = nested_get(netatmopayload,["devices"]) #this is a list

    devicenamekvs = {} #dict for storing stuff to be displayed

    devicedata = { d['_id'] : d for d in devicenamebody }
    for t,v in devicedata.items():
        stationname = v['station_name']
        for m in v['modules']:
            devicename = m['module_name']
            batterystatus = m['battery_percent']
            devicenamekvs[devicename] = batterystatus		
            
    return render_template('show_home_template.html', 
           homename=homename,devicename=devicename,batterystatus=batterystatus,
           devicenamekvs=devicenamekvs)

if __name__ == "__main__":
    auth = GetStationData.get_netatmo_access_token()
    nestauth = GetStationData.get_nest_access_token()
    app.run(port=5001)

    
