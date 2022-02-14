import nerdle_cfg

import re
import luigi
import d6tflow
import itertools
import pandas as pd
import numpy as np

#helper functions
def check_len_int(nerdle):
    nerdle_str = ''.join(nerdle)
    try:
        return all(len(x)==len(str(int(x))) for x in re.split('\+|\-|\*|\/|==',nerdle_str))
    except:
        return False

def rt_is_num(nerdle):
    rt_arr = nerdle[np.where(np.array(nerdle)=='==')[0][0]+1:]
    test_str = ''.join(rt_arr)
    return test_str.isnumeric()

def join_elems_of_tups(list_o_tups):
    return list(map(lambda x: ''.join(x),list_o_tups))

def test_eval(nerdle):
    test_str = ''.join(nerdle)
    try:
        return eval(test_str)
    except:
        return False

class buildNerdles(d6tflow.tasks.TaskPqPandas):
    nerdle_len = luigi.IntParameter()

    def run(self):

        nerdle_len = self.nerdle_len
        
        nerdles = list(itertools.combinations_with_replacement(nerdle_cfg.nerd_list,nerdle_len))

        #TODO: Optimize second list comprehension using filter if possible
        nerdles = list(filter(
            lambda nerdle: ('==' in nerdle)&
            bool(any(i in nerdle for i in [x for x in nerdle_cfg.nerd_op_list if x!="=="])),nerdles))

        nerdle_ser = pd.Series(nerdles)
        nerdle_df = pd.DataFrame(nerdle_ser)
        nerdle_df.columns=['nerdle_combinations']

        #for each nerdle combination create permutations
        nerdle_df['perms'] = nerdle_df['nerdle_combinations'].apply(itertools.permutations,nerdle_len)
        # can't start or end with an equals sign and turns permutation tuples into a list
        nerdle_df['perm_red_stend_equal'] = nerdle_df['perms'].apply(lambda y: filter(lambda x:(list(x)[0]!='==')&(list(x)[-1]!='=='),y))
        # equal sign appears only once
        nerdle_df['perm_equal_once'] = nerdle_df['perm_red_stend_equal'].apply(lambda y: filter(lambda x: x.count('==')==1,y))
        # elements to the right of the equal sign must be a number
        nerdle_df['right_equal_must_be_number'] = nerdle_df['perm_equal_once'].apply(lambda y: filter(lambda x: rt_is_num(x),y))
        #length of string has to be 9
        nerdle_df['len_check'] = nerdle_df['right_equal_must_be_number'].apply(lambda y: filter(lambda x: len(x)==nerdle_len,y))
        #check that non operater numbers are of proper length
        nerdle_df['non_op_num_check'] = nerdle_df['len_check'].apply(lambda y: filter(lambda x: check_len_int(x),y))
        #check that string evals properly
        nerdle_df['eval_check'] = nerdle_df['non_op_num_check'].apply(lambda y: filter(lambda x: test_eval(x),y))

        self.save(nerdle_df)


         


