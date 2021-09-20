# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 17:57:09 2021

@author: trang
"""

import pandas as pd
import datatime
print(pd.Timestamp(2019,9,30,6,1,0))
#%%
input = {

  "shift": {

    "start": "2038-01-01T20:15:00",

    "end": "2038-01-02T04:15:00"

},

  "roboRate": {

    "standardDay": {

      "start": "07:00:00",

      "end": "23:00:00",

      "value": 20

    },

    "standardNight": {

      "start": "23:00:00",

      "end": "07:00:00",

      "value": 25

    },

    "extraDay": {

      "start": "07:00:00",

      "end": "23:00:00",

      "value": 30

    },

    "extraNight": {

      "start": "23:00:00",

      "end": "07:00:00",

      "value": 35

    }

  }

}
