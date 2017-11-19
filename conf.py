import os

AWS = True

# file path
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
STOPWORD = CUR_PATH + "/data/stopword"
TECHWORD = CUR_PATH + "/data/techlist"


# google cloud api json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CUR_PATH +"/data/My Project 68452-ae0ad4fc4ab7.json"

# local hadoop path
if AWS:
    STREAM_JAR_PATH ="/usr/lib/hadoop-mapreduce/hadoop-streaming.jar"
    HADOOP_BIN_PATH = "/usr/bin/hadoop"
else:
    STREAM_JAR_PATH = "/Users/roger/usr/local/hadoop-2.8.2/share/hadoop/tools/lib/hadoop-streaming-2.8.2.jar"
    HADOOP_BIN_PATH = "/Users/roger/usr/local/hadoop-2.8.2/bin/hadoop"

# local io path
MAPPER_PATH  =    CUR_PATH + "/mapreduce" + "/rake" + "/Mapper.py"
REDUCER_PATH =    CUR_PATH + "/mapreduce" + "/rake" + "/Reducer.py"
URL_LIST_FOLDER = CUR_PATH + "/tmp/url_list"
RESULT_FOLDER =   CUR_PATH + "/tmp/result"


# hdfs io path
HDFS_PATH    = "/tmp/hottech"
INPUT_PATH   = HDFS_PATH+ "/url_list"
OUTPUT_PATH  = HDFS_PATH+ "/output"

# settings
DEBUG = True
SETUP = True
LOG = True
