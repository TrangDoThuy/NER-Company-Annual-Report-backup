from datetime import datetime, timedelta

_str = """Image copyright Aimee Smith Image caption 'I don't think I have ever set foot in a Waitrose' - Amie Smith, with her family

Many families are struggling to put food on the table as the coronavirus lockdown robs them of their income. A report by food bank charities points to an alarming rise in the number of people in need of essential supplies. How are they coping and what more can be done to help?
We have gone without meals so the children can eat. It isn't nice when you are feeling hungry and you open the cupboard and there is nothing in there for you.
Amie Smith and her partner Marcus were just about getting by before the coronavirus lockdown. Now they have had to give up their zero hours contract jobs and are relying on universal credit payments, food vouchers from the government and the occasional food parcel from local schools.
Their biggest daily struggle is finding enough food in the shops for their four children, aged two to 13.
The family is getting by on a weekly budget of about £30. The children are entitled to free school meals, which translate into food vouchers during lockdown, but they can't find anywhere to spend them. Amie says she has about £200 worth of vouchers, but they are mostly for upmarket shops like Marks & Spencer and Waitrose, which are absent from their neck of South London.
I don't think I have ever set foot in a Waitrose in my life,' she said.

'Becoming expensive'
Their car has broken down, so they find themselves using local convenience stores - which charge higher prices.
It's becoming very expensive. I just paid £5 for 30 eggs. That was the cheapest we could find.
Image copyright Amie Smith Image caption Reid-Angel, two, and Bree, 11, are learning to cope with life in lockdown
Labour are calling on the government to 'expand which shops are able to accept free school meal vouchers to include those supermarkets most present in our poorest communities'.
Under the current scheme, run by private contractor Endenred, every eligible child is entitled to £15 a week in vouchers. The school or parent must choose a supermarket at which to redeem them, from the following list: Aldi, McColl's, Morrisons, Tesco, Sainsbury's, Asda, Waitrose and M&S.

'Tidal wave'
The government says it recognises it may not be convenient for some families to visit one of these shops. It is 'working to see if additional supermarkets can be added to this list'. In the meantime, it is advising schools to prepare food parcels for pupils on free meals.
Image copyright PA Media Image caption People are seeking help from food banks in record numbers
Many families - who may not have children on free school meals - are turning to food banks for essential supplies. This is putting an enormous strain on charities that provide them.
A new report by the UK's biggest food bank network, the Trussell Trust, said it handed out 81% more emergency food parcels in the last two weeks of March, than at the same time last year. People struggling with the amount of income they were receiving from working or benefits was the main reason for the increase, the trust said.
Like a tidal wave gathering pace, an economic crisis is sweeping towards us, but we don't all have lifeboats,' said chief executive Emma Revie.

'Fresh faces'
Sonya Johnson, who runs Ediblelinks, an independent food bank in North Warwickshire, has noticed a big increase in families with previously comfortable incomes seeking help.
'There are fresh faces coming through the door,' she said. 'People who really don't want to be here, who have never used a food bank but suddenly find themselves at a point of crisis.'
These new clients tend to be small business owners, or sole traders, such a hairdressers or cafe proprietors. They are waiting for universal credit payments or money from the government's business loan scheme. The food bank has seen a 20% increase in demand week-on-week since coronavirus took hold.

What can be done?
Extreme financial hardship exists even outside a global pandemic. Debt charity Christians Against Poverty says one in 10 of its clients live without a bed or mattress, or skip meals on a daily basis. It, and others in the sector, fear coronavirus will mean more people living like this - perhaps for the first time.
Payment 'holidays' put off, rather than cancel, regular bills such as rent or council tax. There is concern people are simply piling up unmanageable debt for the future.
But there is support. Credit unions can offer low-cost loans for small amounts. People are also donating generously in this crisis and some of that money is given in grants so those in crippling hardship.
Charity Turn2us has a search tool to check eligibility for these non-repayable grants. The Child Poverty Action Group has also launched a tool to help people find support during the pandemic.
No government has had to cope with a crisis on this scale in peacetime and poverty campaigners have welcomed actions to help those in most need, through the benefits system. But a group of charities, including the Trussell Trust, is calling now for a coronavirus emergency income support scheme.
They say many families need money urgently, to prevent them being from being 'swept into destitution'.

'Grateful'
A government spokesman said it was 'committed to supporting all those affected... through these unprecedented times'.
'We've implemented an enormous package of measures to do so, including income protection schemes and mortgage holidays For those in most need, we've injected more than £6.5bn into the welfare system, including an increase to universal credit of up to £1,040 a year. No-one has to wait five weeks for money as urgent payments are available.'
Amie and Marcus are just about managing to feed their children each day. But they are worried what the future holds, if they can't get back to work soon.
'There have been times when we have had nothing but maybe beans on toast to give them,' says Amie. 'We have to remind ourselves that there are people out there with absolutely nothing. We should be grateful for what we have.'"""


res = [('Aimee Smith Image', (16, 33)), ('Waitrose', (83, 91)), ('Amie', (95, 99)), ('Amie Smith', (95, 105)), ('Amie', (561, 565)), ('Amie Smith', (561, 571)), ('Marcus', (588, 594)), ('coronavirus', (633, 644)), ('Amie', (1154, 1158)), ('Marks & Spencer', (1246, 1261)), ('Waitrose', (1266, 1274)), ('South London', (1312, 1324)), ('Waitrose', (1366, 1374)), ('Amie', (1643, 1647)), ('Amie Smith', (1643, 1653)), ('Amie Smith Image', (1643, 1659)), ('Reid-Angel', (1668, 1678)), ('Bree', (1689, 1693)), ('McColl', (2144, 2150)), ('Morrisons', (2154, 2163)), ('Tesco', (2165, 2170)), ("Sainsbury's", (2172, 2183)), ('Emma Revie', (3238, 3248)), ('Sonya Johnson', (3265, 3278)), ('Amie', (5696, 5700)), ('Marcus', (5705, 5711)), ('Amie', (5943, 5947))]



color = "#8aff92"
tag = "PEOPLE"
path = 1
out = []
last_b,last_c = 0,0
for a,(b,c) in res:
    t = int((datetime.now()-datetime(1970,1,1)).total_seconds()*1000)
    offset = b-last_c
    if offset>-1:
        tmp = {"timestamp":str(t),"content":str(a),"path":str(path),"offset":offset,"length":c-b,"color":color,"tag":tag}
        path+=1 if path==1 else 2
        last_b,last_c = b,c
        out.append(tmp)


print(out)
