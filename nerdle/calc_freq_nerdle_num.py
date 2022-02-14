import nerdle_cfg
import nerdle_input
import d6tflow
import build_nerdles
from functools import map, reduce
import pandas as pd
import numpy as np

@d6tflow.requires(build_nerdles.buildNerdles)
class constructFilterBasedOnGuesses(d6tflow.tasks.TaskPickle):

    def run(self):
        nerdle_dict = nerdle_input.nerdle_dict
        