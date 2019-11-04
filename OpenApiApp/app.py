from flask import Flask, redirect
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
import requests

sona_url = "https://sona.xn--wx-xka.de/openapi/openapi.json"
mensa_url = "https://mensa.xn--wx-xka.de/openapi/openapi.json"

openapiJson_urls = [mensa_url, sona_url]

getTimeout = 0.25 #250ms timout

# initialize app
app = Flask('Uni Würzburg API')
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = "/"
#TODO fix version of redoc to work again
app.config['OPENAPI_REDOC_PATH'] = "/viewRe"
app.config['OPENAPI_SWAGGER_UI_PATH'] = "/viewUi"
app.config['OPENAPI_SWAGGER_UI_VERSION'] = "3.18.3"

#register openapi.json mock route before api to mock it
@app.route("/openapi.json")
def openapi_json_combiner():
    base_json = {

        "servers": [
            {
                "url": "https://mensa.xn--wx-xka.de",
                "description": "Mensa api subdomain"
            },
            {
                "url": "https://sona.wüx.de",
                "description": "Sona api subdomain"
            }
        ],

        "paths": {
            #input paths here dynamically
        },
        "info": {
            "title": "Uni Würzburg API",
            "version": "1"
        },
        "tags": [
            #input tags here
        ],
        "openapi": "3.0.2",
        "components": {
            "schemas": {
                #input schemas dynamically here
            }
        }
    }
    return_json = base_json

    for url in openapiJson_urls:
        #TODO async get requests for faster responsiveness
        try:
            json = requests.get(url, timeout=getTimeout).json()
            # print(json)
            
            path_dict = return_json["paths"]
            in_path_dict = json["paths"]

            # in_path_dict["https://mensa.wüx.de/mensas/"] = in_path_dict.pop("/mensas/")
            # path_dict["https://mensa.wüx.de/mensas/"] = path_dict["/mensas/"]
            path_dict.update(in_path_dict)

            return_json["tags"].append(json["tags"])

            schema_dict = return_json["components"]["schemas"]
            schema_dict.update(json["components"]["schemas"])
        except requests.exceptions.ConnectionError as e:
            #TODO error handling
            print(e)
            pass

    return return_json

@app.route("/")
def index():
    return redirect("/viewUi")


# API initialize
api = Api(app)
#get blueprints and register them
# from MensaApp.routes.openapi import openapi

# api.register_blueprint(mensaBlp)
