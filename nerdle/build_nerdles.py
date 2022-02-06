import nerdle_cfg

import re
import luigi
import d6tflow
import itertools
import pandas as pd

def check_len_int(nstr):
    try:
        return all(len(x)==len(str(int(x))) for x in re.split('\+|\-|\*|\/|==',nstr))
    except:
        return False

class buildNerdles(d6tflow.tasks.TaskPickle):
    nerdle_len = luigi.IntParameter()

    def run(self):

        nerdle_len = self.nerdle_len
        nerdle_len_py = nerdle_len+1  #for '=' vs '=='

        nerd_num_list = [str(x) for x in range(nerdle_len_py+2)]
        nerd_op_list = ['+','-','*','/','==']

        nerd_list = nerd_num_list+nerd_op_list

        nerdles = list(itertools.combinations_with_replacement(nerd_list,8))

        nerdles = [nerdle 
            for nerdle in nerdles if 
                ('==' in nerdle)&
                bool(any(i in nerdle for i in [x for x in nerd_op_list if x!="=="]))]

        valid_nerdle_list=[]

        for nerdle in nerdles:
            nerdle = nerdles[0]
            nerd_perm_list = list(itertools.permutations(nerdle,nerdle_len))
            
            # can't start or end with an equals sign and turns permutation tuples into a list
            nerd_perm_list = [list(x) for x in nerd_perm_list if (list(x)[0]!='==')&(list(x)[-1]!='==')]
            
            # equal sign appears only once
            nerd_perm_list = [n for n in nerd_perm_list if n.count('==')==1]
            
            #list of lists to list of strings
            nerd_perm_list = [''.join(n) for n in nerd_perm_list]
            
            # elements to the right of the equal sign must be a number
            nerd_perm_list = [n for n in nerd_perm_list if n.split('==')[1].isnumeric()]
            
            #length of string has to be 9
            nerd_perm_list = [n for n in nerd_perm_list if len(n)==nerdle_len_py]
            
            #check that non operater numbers are of proper length
            nerd_perm_list = list(filter(lambda n: check_len_int(n),nerd_perm_list))
            
            #check that string evals properly
            nerd_perm_list = [n for n in nerd_perm_list if eval(n)]
            
            #check if string not already in valid nerdles
            nerd_perm_list = [n for n in nerd_perm_list if n not in valid_nerdle_list]
            
            #remove duplicates from list
            nerd_perm_list = list(set(nerd_perm_list))
            #add to master valid list
            alid_nerdle_list = [n for n in nerd_perm_list if n not in valid_nerdle_list]

        self.save(valid_nerdle_list)

@d6tflow.requires(buildNerdles)
class convertNerdles(d6tflow.tasks.TaskPickle):

    def run(self):
        valid_nerdle_list = self.input().load()

        valid_nerdle_list = [n.replace('==','=') for n in valid_nerdle_list]

        self.save(valid_nerdle_list)


         


