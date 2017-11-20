# Library
from flask import Flask, request
from flask.ext import restful
from flask_cors import CORS
from flask import g
from flask import jsonify

import os
import uuid
import subprocess

# Modules
from mod.Query import hacker_news_query
from mod.SysCommand import HadoopCmd, run_cmd
from mod.filter import cal_score
import conf

app = Flask(__name__)
CORS(app) #NOTE: Access Control
api = restful.Api(app)
hadoop = HadoopCmd(conf.HADOOP_BIN_PATH, conf.STREAM_JAR_PATH, DEBUG=conf.DEBUG)

def setup_hadoop(hadoop):
    hadoop.check(conf.HDFS_PATH)
    hadoop.check(conf.INPUT_PATH)
    hadoop.check(conf.OUTPUT_PATH)
    return


#------------------------ After request setup -------------------------#
def after_this_request(func):
    if not hasattr(g, 'call_after_request'):
        g.call_after_request = []
    g.call_after_request.append(func)
    return func

@app.after_request
def per_request_callbacks(response):
    for func in getattr(g, 'call_after_request', ()):
        response = func(response)
    return response


#------------------------ Test ----------------------------------#
class Test(restful.Resource):
    def get(self):
        run_cmd([conf.HADOOP_BIN_PATH, 'fs', '-ls', '/'])
        #e.g.: http://127.0.0.1:5000
        return {"Hello":"World"}

api.add_resource(Test, '/')


#------------------------ Rake -------------------------------#
@app.route('/rake', methods=['GET'])
def Rake():
    @after_this_request
    def run_hadoop_job(response):
        try:
            SessionID  = response.get_data()
            start_time = request.args.get('start_time')
            end_time   = request.args.get('end_time')
            print_num  = request.args.get('Num')
            limit = '0'
            try:
                limit  = request.args.get('LIMIT')
            except Exception as e:
                pass
        except Exception as e:
            raise

        # Run hadoop stream job UNBLOCK!
        subprocess.Popen(['python','hadoop_stream_job.py',SessionID, start_time, end_time, limit, print_num])
        return response

    SessionID = str(uuid.uuid1())
    return SessionID

#------------------------ Get Result ----------------------------------#
class GetResult(restful.Resource):
    def get(self):
        SessionID = request.args.get('SessionID')
        # TODO: read file from path
        result_file = conf.RESULT_FOLDER + "/" + SessionID + "/result"
        ret = []

        try:
            with open(result_file, 'r') as f:
                for line in f:
                    word,score = line.rstrip().split(',', 1)
                    ret.append({"word":word, "score": float(score)})
            return jsonify(ret)

        except Exception as e:
            try:
                result_file = conf.RESULT_FOLDER + "/" + SessionID + "/__FAIL__"
                if result_file.is_file():
                    return {"Status" : "Failed"}
            except Exception as e:
                return {"Status" : "Uncompleted"}


api.add_resource(GetResult, '/result')


#------------------------ Clean Up -------------------------------------#
class CleanUp(restful.Resource):
    def get(self):
        #e.g.: http://127.0.0.1:5000/test
        run_cmd(['sudo', 'rm', '-rf', conf.INPUT_PATH+ '/*'])
        run_cmd(['sudo', 'rm', '-rf', conf.OUTPUT_PATH+'/*'])
        return {"Clean":"Up"}

api.add_resource(CleanUp, '/cleanup')



#------------------------------ Main ----------------------------------#
if __name__ == '__main__':
    if conf.SETUP:
        setup_hadoop(hadoop)
    app.run(debug=conf.DEBUG, threaded=True, port=5000)
