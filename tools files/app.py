# In this script there are several tools which I have learnt, here are represented: HTTP, NSLOOKUP , SYNFLOOD
# In addition I share my knowledge of basic client - sever socket communication, witch is separate

# NOTE:
# In order to make everything work you will need to set the folder in the correct path
# or  writing  your path in the needed places ( I will mark them as *****   PATHS! ***** and ENDPATHS for the end.

# [127.0.0.1 = localhost]
# INSTRUCTIONS:
#    [a]
#    In order to see the HTTP tool you need to write in your browser the following:
#    first :  http://127.0.0.1:5000
#    After you see that the socket is listening to port 80,
#    second: http://127.0.0.1:80 /  or any other command (regarding HTTP) after "http://127.0.0.1:80".
#    plus:
#    make sure the PATHS in last lines the index.html files (there's 2) are correct ( in the "src = ... ")
#
#    [b]
#    In order to see the SynFlood tool you need to write in your browser the following:
#    http://127.0.0.1:5000/synflood
#    (You will see the output in the terminal)
#
#    [c]
#    In order to see the nslookup tool you need to write in your browser the following:
#    http://127.0.0.1:5000/nslookup/-type=PTR 1.2.3.4 or any other command (regarding nslookup)
#    after "http://127.0.0.1:5000/nslookup/"
#    (You will see the output in the terminal)


import HTTP_server_shell_2_1
import syn_flood_3_2
import nslookup_3_1
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


# Classes
# HTTP tool
class HTTP_CLASS(Resource):
    def get(self):
        return {'data': HTTP_server_shell_2_1.main()}


# SYN FLOOD tool
class SYNFLOOD_CLASS(Resource):
    def get(self):
        return {'data': syn_flood_3_2.main()}


# NS LOOKUP tool
class NSLOOKUP_CLASS(Resource):
    def get(self, command):
        return {'data': nslookup_3_1.main(command)}


# Api resources

# HTTP shell api, write http://localhost/5000/ and then http://localhost:80/ will run the http shell
api.add_resource(HTTP_CLASS, '/')

# FIX THIS IT DOESN"T WORK WELL YET
api.add_resource(SYNFLOOD_CLASS, '/synflood')
# Syn flood attack  api
api.add_resource(NSLOOKUP_CLASS, '/nslookup/<command>')
# Ns lookup api

if __name__ == '__main__':
    app.run()
