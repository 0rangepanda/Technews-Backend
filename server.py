# Library
from flask import Flask, request
from flask.ext import restful
from flask_cors import CORS

import os
import uuid

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

#------------------------ Test ----------------------------------#
class Test(restful.Resource):
    def get(self):
        run_cmd(['/Users/roger/usr/local/hadoop-2.8.2/bin/hadoop', 'fs', '-ls', '/'])
        #e.g.: http://127.0.0.1:5000/test
        return {"Hello":"World"}

api.add_resource(Test, '/test')

#------------------------ WordCount ----------------------------#
class WordCount(restful.Resource):
    def to_json(self, rows):
        json = []
        for item in rows:
            json.append({"word":item[0], "score":item[1]})
        return json


    def hadoop_stream_job(self, url_file, SessionID):
        input_path =  conf.INPUT_PATH+'/'+SessionID
        output_path = conf.OUTPUT_PATH+'/'+SessionID
        result_path = conf.RESULT_FOLDER+'/'+SessionID

        hadoop.mkdir(input_path)
        hadoop.delete(output_path)

        hadoop.put(url_file, input_path)
        hadoop.stream(conf.MAPPER_PATH,conf.REDUCER_PATH,input_path,output_path)
        run_cmd(['rm','-rf',result_path])
        run_cmd(['mkdir',result_path])
        hadoop.get(output_path+'/*', result_path)

        # NOTE: clean up
        hadoop.delete(input_path)
        hadoop.delete(output_path)
        run_cmd(['rm','-rf',"Mapper.py"])
        run_cmd(['rm','-rf',"Reducer.py"])

        return cal_score(result_path+'/part-00000', conf.TECHWORD, topK=10)

    def get(self):
        '''
            RESTful API
            e.g.: http://127.0.0.1:5000/wordcount?start_time=1351623092&end_time=1468446826&LIMIT=10
        '''
        def write_rows(rows, path):
            with open(path, 'a') as f:
                for item in rows:
                    try:
                        f.write(item[1]+'\n')
                    except Exception as e:
                        pass
            return

        SessionID  = str(uuid.uuid1())
        start_time = int(request.args.get('start_time'))
        end_time   = int(request.args.get('end_time'))
        limit = 0
        try:
            limit  = int(request.args.get('LIMIT'))
        except Exception as e:
            pass

        #TODO: validate timestamp

        #bigquery
        rows = hacker_news_query(start_time, end_time, limit)
        url_file_path = conf.URL_LIST_FOLDER+'/url_list_'+SessionID
        write_rows(rows, url_file_path)

        score = self.hadoop_stream_job(url_file_path, SessionID)

        return self.to_json(score)

api.add_resource(WordCount, '/wordcount')




#------------------------ Main -------------------------------#
if __name__ == '__main__':
    if conf.SETUP:
        setup_hadoop(hadoop)
    app.run(debug=conf.DEBUG, threaded=True)
