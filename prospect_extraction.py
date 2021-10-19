# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 17:29:50 2021

@author: trang
"""
#%%

paragraph = "Income Taxes In October 2016, the Financial Accounting Standards Board (&#8220;FASB&#8221;) issued Accounting Standards Update (&#8220;ASU&#8221;) 2016-16, Income Taxes (Topic 740): Intra-Entity Transfer of Assets Other than Inventory (\"ASU 2016-16\"), which requires the recognition of the income tax consequences of an intra-entity transfer of an asset, other than inventory, when the transfer occurs. ASU 2016-06 will be effective for the Company in its first quarter of 2019. The Company is currently evaluating the impact of adopting ASU 2016-16 on its consolidated financial statements. Stock Compensation In March 2016, the FASB issued ASU No. 2016-09, Compensation &#8211; Stock Compensation (Topic 718): Improvements to Employee Share-Based Payment Accounting (&#8220;ASU 2016-09&#8221;), which simplified certain aspects of the accounting for share-based payment transactions, including income taxes, classification of awards and classification on the statement of cash flows. ASU 2016-09 will be effective for the Company beginning in its first quarter of 2018. The Company is currently evaluating the impact of adopting ASU 2016-09 on its consolidated financial statements. Apple Inc. | 2016 Form 10-K |  28 Leases &#32; In February 2016, the FASB issued ASU No. 2016-02, Leases (Topic 842) (&#8220;ASU 2016-02&#8221;), which modified lease accounting for both lessees and lessors to increase transparency and comparability by recognizing lease assets and lease liabilities by lessees for those leases classified as operating leases under previous accounting standards and disclosing key information about leasing arrangements. ASU 2016-02 will be effective for the Company beginning in its first quarter of 2020, and early adoption is permitted. The Company is currently evaluating the timing of its adoption and the impact of adopting ASU 2016-02 on its consolidated financial statements. Financial Instruments &#32; In January 2016, the FASB issued ASU No. 2016-01, Financial Instruments &#8211; Overall (Subtopic 825-10): Recognition and Measurement of Financial Assets and Financial Liabilities (&#8220;ASU 2016-01&#8221;), which updates certain aspects of recognition, measurement, presentation and disclosure of financial instruments. ASU 2016-01 will be effective for the Company beginning in its first quarter of 2019. The Company does not believe the adoption of ASU 2016-01 will have a material impact on its consolidated financial statements.  In June 2016, the FASB issued ASU No. 2016-13, Financial Instruments &#8211; Credit Losses (Topic 326): Measurement of Credit Losses on Financial Instruments (&#8220;ASU 2016-13&#8221;), which modifies the measurement of expected credit losses of certain financial instruments. ASU 2016-13 will be effective for the Company beginning in its first quarter of 2021 and early adoption is permitted. The Company does not believe the adoption of ASU 2016-13 will have a material impact on its consolidated financial statements.  Revenue Recognition &#32; In May 2014, the FASB issued ASU No. 2014-09, Revenue from Contracts with Customers (Topic 606) (&#8220;ASU 2014-09&#8221;), which amends the existing accounting standards for revenue recognition. ASU 2014-09 is based on principles that govern the recognition of revenue at an amount an entity expects to be entitled when products are transferred to customers. ASU 2014-09 will be effective for the Company beginning in its first quarter of 2019, and early adoption is permitted. Subsequently, the FASB has issued the following standards related to ASU 2014-09: ASU No. 2016-08, Revenue from Contracts with Customers (Topic 606): Principal versus Agent Considerations (&#8220;ASU 2016-08&#8221;); ASU No. 2016-10, Revenue from Contracts with Customers (Topic 606): Identifying Performance Obligations and Licensing (&#8220;ASU 2016-10&#8221;); and ASU No. 2016-12, Revenue from Contracts with Customers (Topic 606): Narrow-Scope Improvements and Practical Expedients (&#8220;ASU 2016-12&#8221;). The Company must adopt ASU 2016-08, ASU 2016-10 and ASU 2016-12 with ASU 2014-09 (collectively, the &#8220;new revenue standards&#8221;).  The new revenue standards may be applied retrospectively to each prior period presented or retrospectively with the cumulative effect recognized as of the date of adoption. The Company currently expects to adopt the new revenue standards in its first quarter of 2018 utilizing the full retrospective transition method. The Company does not expect adoption of the new revenue standards to have a material impact on its consolidated financial statements."

#%%
import spacy
nlp = spacy.load('en_core_web_sm')

import nltk
nltk.download('averaged_perceptron_tagger')
from nltk import word_tokenize, pos_tag

#%%
sentences = nltk.sent_tokenize(paragraph)
for sentence in sentences:
    text = word_tokenize(sentence)
    tagged = pos_tag(text)
    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
    if(tense["future"]+tense["present"]>tense["past"]):
        print(sentence)
    print(tense)
    print("*"*10)
    