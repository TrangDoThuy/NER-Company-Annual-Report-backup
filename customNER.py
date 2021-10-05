# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 13:02:27 2021

@author: trang
"""

import spacy
import random
from spacy.url import minibatch, compounding
from pathlib import Path
#%%
nlp = spacy.load('en_core_web_sm')
nlp.pipe_names

train = [
    ("Money transfer from my checking account is not working",{"entities":[(6,13,"ACTIVITY"),(23,39,"PRODUCT")]}),
    ("I want to check balance in my savings account",{"entitites":[(16,23,"ACTIVITY"),(38,45,"PRODUCT")]})
    ]
print(nlp.pipe_names)
ner = nlp.get_pipe("ner")

for _,annotations in train:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])
        
disable_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*disable_pipes):
    optimizer = nlp.resume_training()
    for iteration in range(100):
        random.shuffle(train)
        losses = {}
        batches = minibatch(train,size=compounding(1.0,4.0,1.001))
        for batch in batches:
            text, annotation = zip
