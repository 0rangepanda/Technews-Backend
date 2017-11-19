#!/usr/bin/env python

import sys
import os

# Modules
from mod.Query import hacker_news_query
from mod.SysCommand import HadoopCmd, run_cmd
from mod.filter import cal_score
import conf

def write_rows(rows, path):
    with open(path, 'a') as f:
        for item in rows:
            try:
                f.write(item[1]+'\n')
            except Exception as e:
                pass
    return

def hadoop_stream_job(url_file, SessionID):
    hadoop = HadoopCmd(conf.HADOOP_BIN_PATH, conf.STREAM_JAR_PATH, DEBUG=conf.DEBUG)

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

    score = cal_score(result_path+'/part-00000', conf.TECHWORD, topK=10)
    print score
    return score

if __name__ == '__main__':
    print len(sys.argv)
    print str(sys.argv)

    SessionID = sys.argv[1]
    start_time = int(sys.argv[2])
    end_time   = int(sys.argv[3])
    limit = int(sys.argv[4])
    rows = hacker_news_query(start_time, end_time, limit)
    url_file_path = conf.URL_LIST_FOLDER+'/url_list_'+SessionID
    write_rows(rows, url_file_path)
    # Run hadoop stream job
    score = hadoop_stream_job(url_file_path, SessionID)
    # TODO: save result file
