import nerdle_cfg
import d6tflow
import build_nerdles
import collections
from functools import reduce
import pandas as pd

@d6tflow.requires(build_nerdles.convertNerdles)
class calcNumberFreqInNerdles(d6tflow.tasks.TaskPqPandas):

    def run(self):
        nerdle_list = self.input().load()

        big_nerd_list = ''.join(nerdle_list)

        big_string_nerd_list = [list(n) for n in big_nerd_list]

        freq_dict = collections.Counter(big_string_nerd_list)

        nerd_sum = dict((n,[sum(dict(k,freq_dict[k]).values()) for k in n]) for n in nerdle_list)

        nerd_sum_df = pd.DataFrame.from_dict(nerd_sum,orient='index')

        nerd_sum_df = nerd_sum_df.reset_index()

        self.save(nerd_sum_df)