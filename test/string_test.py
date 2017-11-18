import sys
sys.path.append("..")

from mod.filter import cal_score
import conf

result = './part-00000'
tech = conf.CUR_PATH + "/data/techlist"

techscore = cal_score(result, tech, topK=10)
print techscore
