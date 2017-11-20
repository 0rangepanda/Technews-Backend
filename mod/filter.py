import difflib
import os

def similarity(str1, str2):
    # Short string
    if len(str1) < 5 or len(str2) < 5:
        if str1 == str2:
            return 1
        seq = difflib.SequenceMatcher(None, str1, str2)
        return seq.ratio() if seq.ratio() > 0.8 else 0
    # Normal string
    else:
        if (str1 in str2) or (str2 in str1):
            return 1
        seq = difflib.SequenceMatcher(None, str1, str2)
        return seq.ratio() if seq.ratio() > 0.5 else 0


def cal_score(result_path, tech, topK=10):
    tech_list = {}
    with open(tech, 'r') as f:
        for line in f:
            tech_list[line[:-1]] = 0

    # TODO: read all the file under result_path
    files= os.listdir(result_path)
    for _file in files:
         if not os.path.isdir(_file):
              f = open(result_path+"/"+_file);
              iter_f = iter(f);
              for line in f:
                  word,score = line.rstrip().split(',', 1)
                  for tech_word in tech_list:
                      tech_list[tech_word] += int(score) * similarity(tech_word, word)

    '''
    with open(result, 'r') as f:
        for line in f:
            word,score = line.rstrip().split(',', 1)

            for tech_word in tech_list:
                tech_list[tech_word] += int(score) * similarity(tech_word, word)
    '''


    tech_sort = sorted(tech_list, key=tech_list.get, reverse=True)
    ret = []
    for item in tech_sort[:topK]:
        ret.append([item, tech_list[item]])
    return ret
