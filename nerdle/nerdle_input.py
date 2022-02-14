import nerdle_cfg

'''
This is the main game input.  The guess consists of numerics and operators as strings.  The return is either 0,1,2 indicating classes of 'not in',
'in but not in right spot', and 'in and in right spot.'  The user would input the guesses and results after a guess has been made.

'''

nerdle_dict = {
            'guess_1':{'guess':(),'guess_ret':()},
            'guess_2':{'guess':(),'guess_ret':()},
            'guess_3':{'guess':(),'guess_ret':()},
            'guess_4':{'guess':(),'guess_ret':()},
            'guess_5':{'guess':(),'guess_ret':()},
            'guess_6':{'guess':(),'guess_ret':()},
            }

def nerdle_dict_unit_test(nerdle_dict):
    if nerdle_dict['guess_1']['guess'] == ():
        for k in nerdle_dict.keys():
            for kk in nerdle_dict[k].keys():
                return nerdle_dict[k][kk] == ()
    else:
        testbool=True
        for k in nerdle_dict.keys():
            for kk in nerdle_dict[k].keys():
                testbool += len(nerdle_dict[k][kk])==nerdle_cfg.nerdle_len
                if kk=='guess':
                    testbool += all(x in nerdle_cfg.nerd_list for x in nerdle_dict[k][kk])
                elif kk=='guess_ret':
                    testbool += all(x in [0,1,2] for x in nerdle_dict[k][kk])
                else:
                    testbool += False
        return testbool

assert(nerdle_dict_unit_test(nerdle_dict))