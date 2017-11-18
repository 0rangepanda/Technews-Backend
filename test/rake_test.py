#------------------------------------------------------------------------#
stoplist = []
with open('stopword', 'r') as f:
    for line in f:
        stoplist.append(line[:-1])

#print stoplist

#------------------------------------------------------------------------#
from rake_nltk import Rake
import operator

rake_object = Rake()

text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility " \
       "of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. " \
       "Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating"\
       " sets of solutions for all types of systems are given. These criteria and the corresponding algorithms " \
       "for constructing a minimal supporting set of solutions can be used in solving all the considered types of " \
       "systems and systems of mixed types."

rake_object.extract_keywords_from_text(text)
#print rake_object.get_ranked_phrases()


#------------------------------------------------------------------------#
import sys
sys.path.append("..")

import mod.rake as rake
import operator

rake_object_1 = rake.Rake("./stopword", 2, 3, 1)
keywords = rake_object_1.run(text)
print "Keywords:", keywords
