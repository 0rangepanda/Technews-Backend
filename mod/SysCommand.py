import subprocess

def run_cmd(args_list, debug=True):
    if debug:
        print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    (output, errors) = proc.communicate()
    if proc.returncode:
        raise RuntimeError(
            'Error running command: %s. Return code: %d, Error: %s' % (
                ' '.join(args_list), proc.returncode, errors))
    return (output, errors)

class HadoopCmd(object):
    """python run hadoop commands"""
    def __init__(self, HADOOP_BIN_PATH, STREAM_JAR_PATH, DEBUG=True):
        self.hadoop = HADOOP_BIN_PATH
        self.STREAM_JAR_PATH = STREAM_JAR_PATH
        self.DEBUG = DEBUG

    def mkdir(self, hdfs_file_path):
        args_list = [self.hadoop, 'fs', '-mkdir', hdfs_file_path]
        run_cmd(args_list, debug=self.DEBUG)
        return

    def put(self, local_file, hdfs_file_path):
        args_list = [self.hadoop, 'fs', '-put', local_file, hdfs_file_path]
        run_cmd(args_list, debug=self.DEBUG)
        return

    def get(self, hdfs_file, local_file):
        args_list = [self.hadoop, 'fs', '-get', hdfs_file, local_file]
        run_cmd(args_list, debug=self.DEBUG)
        return

    def delete(self, filepath):
        args_list = [self.hadoop, 'fs', '-rm', '-r', filepath]
        try:
            run_cmd(args_list, debug=self.DEBUG)
        except Exception as e:
            pass

    def stream(self, maper_path,reducer_path,input_path,output_path):
        args_list = [self.hadoop, 'jar', self.STREAM_JAR_PATH, \
                    '-file', maper_path, '-mapper', maper_path, \
                    '-file', reducer_path, '-reducer', reducer_path, \
                    '-input', input_path, '-output', output_path]
        run_cmd(args_list, debug=self.DEBUG)
        return

    def check(self, hdfs_file_path):
        self.delete(hdfs_file_path)
        self.mkdir(hdfs_file_path)
        return
