import sys
import uuid
sys.path.append("..")

import time
import conf
from mod.SysCommand import HadoopCmd, run_cmd

start = time.time()

MAPPER_PATH =  conf.CUR_PATH +"/rake/Mapper.py"
REDUCER_PATH = conf.CUR_PATH +"/rake/Reducer.py"


SessionID  = str(uuid.uuid1())

input_path =  conf.INPUT_PATH+'/'+SessionID
output_path = conf.OUTPUT_PATH+'/'+SessionID
result_path = conf.RESULT_FOLDER+'/'+SessionID

hadoop = HadoopCmd(conf.HADOOP_BIN_PATH, conf.STREAM_JAR_PATH)

hadoop.mkdir(input_path)
hadoop.delete(output_path)

hadoop.put("url_list", input_path)
hadoop.stream(MAPPER_PATH,REDUCER_PATH,input_path,output_path)
run_cmd(['rm','-rf',result_path])
run_cmd(['mkdir',result_path])
hadoop.get(output_path+'/*', result_path)


# NOTE: clean up
run_cmd(['rm','-rf',"Mapper.py"])
run_cmd(['rm','-rf',"Reducer.py"])
hadoop.delete(input_path)
hadoop.delete(output_path)

elapsed = (time.time() - start)
print "Time used:"+str(elapsed)+" sec"
