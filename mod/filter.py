import difflib
import os

def similarity(str1, str2):
    if (str1 in str2) or (str2 in str1):
        return 1
    seq = difflib.SequenceMatcher(None, str1, str2)
    return seq.ratio() if seq.ratio() > 0.6 else 0

def cal_score(result_path, tech, topK=10):
    tech_list = {}
    with open(tech, 'r') as f:
        for line in f:
            tech_list[line[:-1]] = 0

    # TODO: read all the file under result_path
    files= os.listdir(result_path) #得到文件夹下的所有文件名称  
    for file in files: #遍历文件夹
         if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
              f = open(path+"/"+file); #打开文件
              iter_f = iter(f); #创建迭代器
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
