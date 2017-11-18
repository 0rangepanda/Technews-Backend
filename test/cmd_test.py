import sys
sys.path.append("..")

from mod.SysCommand import HadoopCmd, run_cmd
import uuid

# local path
STREAM_JAR_PATH = "/Users/roger/usr/local/hadoop-2.8.2/share/hadoop/tools/lib/hadoop-streaming-2.8.2.jar"
MAPPER_PATH  = "/Users/roger/Documents/code/Python/BigQuery/python2/BQ_project/hadoop/Mapper.py"
REDUCER_PATH = "/Users/roger/Documents/code/Python/BigQuery/python2/BQ_project/hadoop/Reducer.py"
URL_LIST_FOLDER = "/Users/roger/Documents/code/Python/BigQuery/python2/BQ_project/tmp/url_list"
RESULT_FOLDER = "/Users/roger/Documents/code/Python/BigQuery/python2/BQ_project/tmp/result"

# hdfs path
INPUT_PATH   = "/tmp/url_list"
OUTPUT_PATH  = "/tmp/output"

STREAM_JAR_PATH = "/Users/roger/usr/local/hadoop-2.8.2/share/hadoop/tools/lib/hadoop-streaming-2.8.2.jar"
HADOOP_BIN_PATH = "/Users/roger/usr/local/hadoop-2.8.2/bin/hadoop"


def test():
    hadoop = HadoopCmd(HADOOP_BIN_PATH, STREAM_JAR_PATH)

    maper_path = "/Users/roger/Documents/code/Python/BigQuery/python2/test/Mapper.py"
    reducer_path = "/Users/roger/Documents/code/Python/BigQuery/python2/test/Reducer.py"
    input_path = "/tmp/hadoop_testdata/*"
    output_path = "/tmp/output"

    try:
        hadoop.delete(output_path)
    except Exception as e:
        pass
    hadoop.stream(maper_path,reducer_path,input_path,output_path)
    run_cmd(['rm','-rf','tmp_output'])
    run_cmd(['mkdir','tmp_output'])
    hadoop.get(output_path+'/*', './tmp_output')


def hadoop_stream_job(url_file, SessionID):
    hadoop = HadoopCmd(HADOOP_BIN_PATH, STREAM_JAR_PATH)
    input_path = INPUT_PATH+'/'+SessionID
    output_path = OUTPUT_PATH+'/'+SessionID
    result_path = RESULT_FOLDER+'/'+SessionID

    hadoop.mkdir(input_path)
    try:
        hadoop.delete(output_path)
    except Exception as e:
        pass

    hadoop.put(url_file, input_path)
    hadoop.stream(MAPPER_PATH,REDUCER_PATH,input_path+'/*',output_path)
    run_cmd(['rm','-rf',result_path])
    run_cmd(['mkdir',result_path])
    hadoop.get(output_path+'/*', result_path)
    return

SessionID  = str(uuid.uuid1())
url_file_path = URL_LIST_FOLDER+'/url_list_'+SessionID
with open(url_file_path, 'a') as f:
    for i in range(100):
        f.write('hello world!\n')
hadoop_stream_job(url_file_path, SessionID)
