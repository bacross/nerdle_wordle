import nerdle_cfg
import d6tflow

from calc_freq_nerdle_num import calcNumberFreqInNerdles

nerdle_df = calcNumberFreqInNerdles(nerdle_cfg.nerdle_len).output().load()

#print top ten highest information guesses
print(nerdle_df.head(10))