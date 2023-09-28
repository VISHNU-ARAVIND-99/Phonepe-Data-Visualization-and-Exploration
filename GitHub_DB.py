import pandas as pd
import json
import os
import sqlite3


def github_to_sql():
    path1 = ("D:/Data science/Projects/Phonepe Pulse Data Visualization and Exploration/pulse-master/data/aggregated/"
             "transaction/country/india/state/")
    agg_trans_list = os.listdir(path1)

    columns1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
                'Transaction_amount': []}
    for state in agg_trans_list:
        cur_state = path1 + state + "/"
        agg_year_list = os.listdir(cur_state)

        for year in agg_year_list:
            cur_year = cur_state + year + "/"
            agg_file_list = os.listdir(cur_year)

            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                A = json.load(data)

                for i in A['data']['transactionData']:
                    name = i['name']
                    count = i['paymentInstruments'][0]['count']
                    amount = i['paymentInstruments'][0]['amount']
                    columns1['Transaction_type'].append(name)
                    columns1['Transaction_count'].append(count)
                    columns1['Transaction_amount'].append(amount)
                    columns1['State'].append(state)
                    columns1['Year'].append(year)
                    columns1['Quarter'].append(int(file.strip('.json')))

    df_agg_trans = pd.DataFrame(columns1)

    path2 = ("D:/Data science/Projects/Phonepe Pulse Data Visualization and Exploration/pulse-master/data/aggregated"
             "/user/country/india/state/")

    agg_user_list = os.listdir(path2)

    columns2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [], 'Percentage': []}
    for state in agg_user_list:
        cur_state = path2 + state + "/"
        agg_year_list = os.listdir(cur_state)

        for year in agg_year_list:
            cur_year = cur_state + year + "/"
            agg_file_list = os.listdir(cur_year)

            for file in agg_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                B = json.load(data)
                try:
                    for i in B["data"]["usersByDevice"]:
                        brand_name = i["brand"]
                        counts = i["count"]
                        percents = i["percentage"]
                        columns2["Brands"].append(brand_name)
                        columns2["Count"].append(counts)
                        columns2["Percentage"].append(percents)
                        columns2["State"].append(state)
                        columns2["Year"].append(year)
                        columns2["Quarter"].append(int(file.strip('.json')))
                except:
                    pass

    df_agg_user = pd.DataFrame(columns2)

    path3 = ("D:/Data science/Projects/Phonepe Pulse Data Visualization and Exploration/pulse-master/data/map/"
             "transaction/hover/country/india/state/")

    map_trans_list = os.listdir(path3)

    columns3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [], 'Amount': []}

    for state in map_trans_list:
        cur_state = path3 + state + "/"
        map_year_list = os.listdir(cur_state)

        for year in map_year_list:
            cur_year = cur_state + year + "/"
            map_file_list = os.listdir(cur_year)

            for file in map_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                C = json.load(data)

                for i in C["data"]["hoverDataList"]:
                    district = i["name"]
                    count = i["metric"][0]["count"]
                    amount = i["metric"][0]["amount"]
                    columns3["District"].append(district)
                    columns3["Count"].append(count)
                    columns3["Amount"].append(amount)
                    columns3['State'].append(state)
                    columns3['Year'].append(year)
                    columns3['Quarter'].append(int(file.strip('.json')))

    df_map_trans = pd.DataFrame(columns3)

    path4 = ("D:/Data science/Projects/Phonepe Pulse Data Visualization and Exploration/pulse-master/data/map/user/"
             "hover/country/india/state/")
    map_user_list = os.listdir(path4)

    columns4 = {"State": [], "Year": [], "Quarter": [], "District": [], "RegisteredUser": [], "AppOpens": []}

    for state in map_user_list:
        cur_state = path4 + state + "/"
        map_year_list = os.listdir(cur_state)

        for year in map_year_list:
            cur_year = cur_state + year + "/"
            map_file_list = os.listdir(cur_year)

            for file in map_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                D = json.load(data)

                for i in D["data"]["hoverData"].items():
                    district = i[0]
                    registered_user = i[1]["registeredUsers"]
                    appOpens = i[1]['appOpens']
                    columns4["District"].append(district)
                    columns4["RegisteredUser"].append(registered_user)
                    columns4["AppOpens"].append(appOpens)
                    columns4['State'].append(state)
                    columns4['Year'].append(year)
                    columns4['Quarter'].append(int(file.strip('.json')))

    df_map_user = pd.DataFrame(columns4)

    path5 = ("D:/Data science/Projects/Phonepe Pulse Data Visualization and Exploration/pulse-master/data/top/"
             "transaction/country/india/state/")
    top_trans_list = os.listdir(path5)
    columns5 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [],
                'Transaction_amount': []}

    for state in top_trans_list:
        cur_state = path5 + state + "/"
        top_year_list = os.listdir(cur_state)

        for year in top_year_list:
            cur_year = cur_state + year + "/"
            top_file_list = os.listdir(cur_year)

            for file in top_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                E = json.load(data)

                for i in E['data']['pincodes']:
                    name = i['entityName']
                    count = i['metric']['count']
                    amount = i['metric']['amount']
                    columns5['Pincode'].append(name)
                    columns5['Transaction_count'].append(count)
                    columns5['Transaction_amount'].append(amount)
                    columns5['State'].append(state)
                    columns5['Year'].append(year)
                    columns5['Quarter'].append(int(file.strip('.json')))

    df_top_trans = pd.DataFrame(columns5)

    path6 = ("D:/Data science/Projects/Phonepe Pulse Data Visualization and Exploration/pulse-master/data/top/user"
             "/country/india/state/")

    top_user_list = os.listdir(path6)
    columns6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [],
                'RegisteredUsers': []}

    for state in top_user_list:
        cur_state = path6 + state + "/"
        top_year_list = os.listdir(cur_state)

        for year in top_year_list:
            cur_year = cur_state + year + "/"
            top_file_list = os.listdir(cur_year)

            for file in top_file_list:
                cur_file = cur_year + file
                data = open(cur_file, 'r')
                F = json.load(data)

                for i in F['data']['pincodes']:
                    name = i['name']
                    registered_users = i['registeredUsers']
                    columns6['Pincode'].append(name)
                    columns6['RegisteredUsers'].append(registered_users)
                    columns6['State'].append(state)
                    columns6['Year'].append(year)
                    columns6['Quarter'].append(int(file.strip('.json')))

    df_top_user = pd.DataFrame(columns6)

    conn = sqlite3.connect("Phonepe.db")
    df_agg_trans.to_sql('agg_trans', conn, if_exists='append')
    df_agg_user.to_sql('agg_user', conn, if_exists='append')
    df_map_trans.to_sql('map_trans', conn, if_exists='append')
    df_map_user.to_sql('map_user', conn, if_exists='append')
    df_top_trans.to_sql('top_trans', conn, if_exists='append')
    df_top_user.to_sql('top_user', conn, if_exists='append')

    df_agg_trans.to_csv('agg_trans.csv', index=False)
    df_agg_user.to_csv('agg_user.csv', index=False)
    df_map_trans.to_csv('map_trans.csv', index=False)
    df_map_user.to_csv('map_user.csv', index=False)
    df_top_trans.to_csv('top_trans.csv', index=False)
    df_top_user.to_csv('top_user.csv', index=False)


github_to_sql()