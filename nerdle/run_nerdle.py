import nerdle_cfg
import d6tflow

from build_nerdles import buildNerdles

d6tflow.run(buildNerdles(nerdle_cfg.nerdle_len))   