# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 10:27:21 2021

@author: trang
"""
# import spacy
# nlp = spacy.load("en_core_web_sm")
# sent = "We believe Adjusted EBITDA is useful to an investor in evaluating our operating performance for the following reasons:"
# doc=nlp(sent)

# sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]

# print(sub_toks) 
#%%
import spacy
nlp = spacy.load('en_core_web_sm')
sentences=["The big black cat stared at the small dog.",
           "Jane watched her brother in the evenings."]
#%%
def get_subject_phrase(doc):
    for token in doc:
        if ("subj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]
#%%
def get_object_phrase(doc):
    for token in doc:
        if ("dobj" in token.dep_):
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            return doc[start:end]
#%%
#sent = "Higher collection amounts or cash collections that occur sooner than projected will have a favorable impact on reversal of impairments or an increase in yields and revenues."
#sent = "We cannot determine the actual amount of these new stock-related compensation and benefit expenses at this time because applicable accounting practices require that they be based on the fair market value of the shares of common stock at specific points in the future." 
#sent = "In the future, the Company, as the holding company of the Bank, will be authorized to pursue other business activities permitted by applicable laws and regulations for savings and loan holding companies, which may include the acquisition of banking and financial services companies."
sent = "we will, however, use the support staff of the Bank from time to time. All of these persons are paid by the Bank under the terms of a management agreement with the Company.  The Company may hire additional employees, as appropriate, to the extent it expands its business in the future."
doc=nlp(sent)
subject_phrase = get_subject_phrase(doc)
object_phrase = get_object_phrase(doc)
print(subject_phrase)
