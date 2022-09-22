#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:34:50 2022

@author: jtm545
"""
import numpy as np
import pandas as pd

from pyplr.stlab import SpectraTuneLab
from pyplr.stlabhelp import make_video_file, _video_file_row, _video_file_end
from pysilsub.problems import SilentSubstitutionProblem as SSP


ssp = SSP.from_json('/Users/jtm545/Projects/PySilSub/data/STLAB_1_York.json')

ssp.ignore = ['R']
ssp.minimize = ['L','S','I']
ssp.modulate = [ 'M']
ssp.target_contrast = 'min'
ssp.print_problem()

def callback(x0):
    print(x0)
    
solution = ssp.optim_solve(options={'iprint':2, 'disp':True})
fig = ssp.plot_solution(solution.x)

bg = ssp.w2s(solution.x[0:10])
mod = ssp.w2s(solution.x[10:])

vf = pd.concat([_video_file_row(time=0, spec=bg),
                _video_file_row(time=63,spec=mod),
                _video_file_row(time=126, spec=bg)]).reset_index(drop=True)


make_video_file(vf, fname='video1.json', repeats=10000)

#%%
d = SpectraTuneLab.from_config()
d.load_video_file('./video1.json')
d.play_video_file('./video1.json', 2)

