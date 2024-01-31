import requests
import json
import jsonpath
from datetime import datetime
import pandas as pd

Id_G = []
Name_G = []
Broker_Finra_G = []
Investment_advisor_G = []
Bc_disclosure_fl_G = []
Approved_finra_registration_count_G = []
Employments_count_G = []
Experience_G = []
Current_employments_G = []

#a bis z
suchstrings = ['a', 'e', 'i','o','u'] # eine Geeignete finden soll
for j in suchstrings:
    print(j)
    pointer = 0
    url0 = 'https://api.brokercheck.finra.org/search/individual?query=' + j +'&filter=active=true,prev=true,bar=true,broker=true,ia=true,brokeria=true&includePrevious=true&hl=true&nrows=12&start=' + str(pointer) + '&r=25&sort=score%2Bdesc&wt=json'
    res0 =  requests.get(url0)
    res0.encoding = "utf-8"
    html0 = res0.text
    #print(html)
    html0 = json.loads(html0)
    Anzahl_Record = jsonpath.jsonpath(html0,"$..total")
    #print(Anzahl_Record[0])


    Id_total = []
    Name_total = []
    Broker_Finra_total = []
    Investment_advisor_total = []
    Bc_disclosure_fl_total = []
    Approved_finra_registration_count_total = []
    Employments_count_total = []
    Experience_total = []
    Current_employments_total = []

    print(int(Anzahl_Record[0]))
    jjj = min(9000, int(Anzahl_Record[0]))
    print(jjj)
    i = 0
    while i < jjj: #len(int(Anzahl_Record[0]))
        url = 'https://api.brokercheck.finra.org/search/individual?query=' + str(j) + '&filter=active=true,prev=true,bar=true,broker=true,ia=true,brokeria=true&includePrevious=true&hl=true&nrows=12&start=' + str(i) + '&r=25&sort=score%2Bdesc&wt=json' 
        res = requests.get(url) 
        #print(res.status_code) 

        res.encoding = "utf-8"
        html = res.text
        html1 = json.loads(html)
        #print(html1)
        result = jsonpath.jsonpath(html1,"$.._source")
        Id = jsonpath.jsonpath(result, "$..ind_source_id")
        first_name = jsonpath.jsonpath(result, "$..ind_firstname")
        last_name = jsonpath.jsonpath(result, "$..ind_lastname")
        Name = []
        if isinstance(first_name,bool) == False:
            for h in range(len(first_name)):
                print(h)
                name0 = first_name[h] + "." + last_name[h]
                Name.append(name0)
        else:
            for h in range(12):
                Name.append(0)
        print(Name)
        Broker_Finra = jsonpath.jsonpath(result, "$..ind_bc_scope")
        Investment_advisor = jsonpath.jsonpath(result, "$..ind_ia_scope")

        #\*Die drei Attribute unten bin ich nixht sicher, ob es geraucht wird
        Bc_disclosure_fl = jsonpath.jsonpath(result, "$..ind_bc_disclosure_fl")
        Approved_finra_registration_count = jsonpath.jsonpath(result, "$..ind_approved_finra_registration_count")
        Employments_count = jsonpath.jsonpath(result, "$..ind_employments_count")
        #\*

        Experience = []

        if isinstance(result,bool) == False:
            for w in range(len(result)):
                experience = jsonpath.jsonpath(result[w], "$..ind_industry_cal_date")
                if experience != False:
                    experience__1 = datetime.now() - datetime.strptime(experience[0], "%Y-%m-%d")
                    experience = str(experience__1.days)
                else:
                    experience = jsonpath.jsonpath(result[w], "$..ind_industry_days")
                    if experience != False:
                        experience = experience[0]
                    else:
                        experience = str(0)
                Experience.append(experience)
        else:
            for w in range(12):
                Experience.append(0)
        #print(Experience)


        Current_employments = jsonpath.jsonpath(result, "$..ind_current_employments")

        i = i + 12
        print(i)
        Id_total.extend(Id)
        Name_total.extend(Name)
        Broker_Finra_total.extend(Broker_Finra)
        Investment_advisor_total.extend(Investment_advisor)
        Bc_disclosure_fl_total.extend(Bc_disclosure_fl)
        Approved_finra_registration_count_total.extend(Approved_finra_registration_count)
        Employments_count_total.extend(Employments_count)
        Experience_total.extend(Experience)
        Current_employments_total.extend(Current_employments)

    #print(Id_total)

    Id_G.extend(Id_total)
    Name_G.extend(Name_total)
    Broker_Finra_G.extend(Broker_Finra_total)
    Investment_advisor_G.extend(Investment_advisor_total)
    Bc_disclosure_fl_G.extend(Bc_disclosure_fl_total)
    Approved_finra_registration_count_G.extend(Approved_finra_registration_count_total)
    Employments_count_G.extend(Employments_count_total)
    Experience_G.extend(Experience_total)
    Current_employments_G.extend(Current_employments_total)
    #添加所有的长度，看哪里不一样
    print(len(Id_G))
    print(len(Name_G))
    print(len(Broker_Finra_G))
    print(len(Investment_advisor_G))
    print(len(Bc_disclosure_fl_G))
    print(len(Approved_finra_registration_count_G))
    print(len(Employments_count_G))
    print(len(Experience_G))
    print(len(Current_employments_G))

output = pd.DataFrame({'Id':Id_G,'Name':Name_G, 'Broker_Finra':Broker_Finra_G, "Investment_advisor":Investment_advisor_G, "Bc_disclosure_fl": Bc_disclosure_fl_G, "Approved_finra_registration_count":Approved_finra_registration_count_G, "Employments_count": Employments_count_G, "Experience": Experience_G, "Current_employments": Current_employments_G})
output = output.drop_duplicates(keep='first', subset=['Id'])
#print(output)
output.to_csv('./test.csv',index = None,encoding = 'utf8')