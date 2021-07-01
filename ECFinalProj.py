"""
Name: Ethan Clabaugh
CS230: Section SN2F
Data: 'nyc_veh_crash_sample'
URL:

Description:

This program will dive into the frequencies of car crashes in New York City. Various topics will be addressed such as:
the average number of car crashes per year, month, week, day, and minute; the areas in the city where car
crashes occur most frequently broken down by borough, zip code, and street, with bar charts to support this data; the
basic statistics of the number of injury-causing crashes; and the probability of there being a crash,
injury-causing crash on any given day on any chosen street in NYC with an accompanying pie chart showing
these probabilities.
"""
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import math

plt.rcParams['axes.facecolor'] = 'darkgrey'     #sets background color for graphs on whole program

df = pd.read_csv('nyc_veh_crash_sample.csv')        #read in csv file into a dataframe

total_crashes = df.index[-1] + 1
only_injuries = (df[df['PERSONS INJURED']>0])      #set variable for total crashes and a df for only crashes w injuries

def crashes_per(df, time_frame, total_crashes):
    crashes_per_year = total_crashes / 2  #total crashes are over 2015/16 - two years
    crashes_per_month = crashes_per_year / 12
    crashes_per_week = crashes_per_year / 52
    crashes_per_day = crashes_per_year / 365
    crashes_per_hour = crashes_per_day / 24         #use easy math to change units
    crashes_per_minute = crashes_per_hour / 60

    if time_frame == 'Year':
        st.write(f'{crashes_per_year:0.0f}')
    elif time_frame == 'Month':
        st.write(f'{crashes_per_month:0.4f}')       #if statements for selection tool
    elif time_frame == 'Week':
        st.write(f'{crashes_per_week:0.4f}')
    elif time_frame == 'Day':
        st.write(f'{crashes_per_day:0.4f}')
    elif time_frame == 'Hour':
        st.write(f'{crashes_per_hour:0.4f}')
    else:
        st.write(f'{crashes_per_minute:0.4f}')

def find_injury_percent(df=df, total_crashes=total_crashes, only_injuries=only_injuries):
    injury_causing_count = len(only_injuries)
    injury_percent = injury_causing_count / total_crashes * 100     #find percent of crashes that injure

    return injury_percent

def injury_stats(df=df):
    injury_stats = df['PERSONS INJURED'].describe()
    st.write(injury_stats)                                  #basic stats on injuries

def which_injury_stats(injury_selector):
    if injury_selector == 'Yes':
        st.subheader('Basic injury statistics including non-injury crashes:')
        injury_stats()
    else:                               #use all crashes or only injuries
        st.subheader('Basic injury statistics of only injury-causing crashes:')
        injury_stats(df=only_injuries)

def borough_breakdown(df=df):
    borough_count = df['BOROUGH'].value_counts()
    st.write(borough_count)     #use value counts to make series of borough names and total crashes in each

    borough_dict = borough_count.to_dict()
    borough_names_list = list(borough_dict.keys())          #make into dict and then lists for graphing
    borough_counts_list = list(borough_dict.values())

    graph = plt.figure(figsize=(4,3))
    graph.patch.set_facecolor('grey')
    graph.patch.set_alpha(0.625)
    plt.bar(range(len(borough_dict)), borough_counts_list, tick_label=borough_names_list, color='midnightblue')
    plt.xticks(size=6)
    plt.yticks(size=6)
    plt.xlabel('Borough', fontweight='bold', size=8)        #create graph
    plt.ylabel('Crashes', fontweight='bold', size=8)
    plt.title('Number of Crashes per Borough', fontweight='bold', size=10)
    st.pyplot(graph)

def zip_breakdown(df=df):
    pd.set_option('precision', 0)     #no decimals for ZIP code
    zip_count = df['ZIP CODE'].value_counts()

    zip_dict = zip_count.to_dict()      #make a dict

    filtered_zip_dict = {k: zip_dict[k] for k in list(zip_dict)[:how_many]}
    df_zip_filtered = pd.DataFrame(list(filtered_zip_dict.items()),columns = ['ZIP Code','Crashes'])
    df_zip_filtered = df_zip_filtered.assign(blank_index='').set_index('blank_index')     #remove index to print
    st.write(df_zip_filtered)

    zip_list = list(filtered_zip_dict.keys())
    zip_list = ['%.0f' % n for n in zip_list]     #format entire ZIP code list to show no decimals
    zip_count_list = list(filtered_zip_dict.values())

    graph = plt.figure(figsize=(4,3))
    graph.patch.set_facecolor('grey')
    graph.patch.set_alpha(0.625)
    plt.bar(range(len(filtered_zip_dict)), zip_count_list, tick_label=zip_list, color='midnightblue')
    plt.xticks(rotation=45, size=6)
    plt.yticks(size=6)                                      #create graph
    plt.xlabel('ZIP Code', fontweight='bold', size=8)
    plt.ylabel('Crashes', fontweight='bold', size=8)
    plt.title(f'{how_many} ZIP Codes With The Most Crashes', fontweight='bold', size=10)
    st.pyplot(graph)

def street_breakdown(df=df):
    on_street_count = df['ON STREET NAME'].value_counts()
    cross_street_count = df['CROSS STREET NAME'].value_counts()         #creat series for cross and on street
    on_street_dict = on_street_count.to_dict()
    cross_street_dict = cross_street_count.to_dict()        #make each to a dictionary
    combined_street_dict = {}
    for key in on_street_dict:
        if key in cross_street_dict:            #ucombine the on street and cross street dictionaries
            combined_street_dict[key] = on_street_dict[key] + cross_street_dict[key]
        else:
            pass

    combined_street_dict = sorted(combined_street_dict.items(), key=lambda x: x[1],
                                  reverse=True)  #re-sort after combining
    combined_street_dict = dict(combined_street_dict)       #put back into dict since sort put into a list

    filtered_street_dict = {k: combined_street_dict[k] for k in list(combined_street_dict)[:how_many]}
    #filter the dictionary down to the amount specified

    df_street_filtered = pd.DataFrame(list(filtered_street_dict.items()),columns = ['Street','Crashes'])
    #back to dataframe to print
    df_street_filtered = df_street_filtered.assign(blank_index='').set_index('blank_index')     #remove index
    st.write(df_street_filtered)

    street_list = list(filtered_street_dict.keys())
    street_count_list = list(filtered_street_dict.values())     #make lists for graphing purposes

    graph = plt.figure(figsize=(4,3))
    graph.patch.set_facecolor('grey')
    graph.patch.set_alpha(.625)
    plt.bar(range(len(filtered_street_dict)), street_count_list, tick_label=street_list, color='midnightblue')
    plt.xticks(rotation=90, size=6)
    plt.yticks(size=6)                                      #create graph
    plt.ylabel('Crashes', fontweight='bold', size=8)
    plt.xlabel('Street', fontweight='bold', size=8)
    plt.title(f'{how_many} Streets with the Most Crashes', fontweight='bold', size=10)
    st.pyplot(graph)

def crash_probability(df=df):
    #same as street_breakdown function until combined_street_dict
    on_street_count = df['ON STREET NAME'].value_counts()
    cross_street_count = df['CROSS STREET NAME'].value_counts()
    on_street_dict = on_street_count.to_dict()
    cross_street_dict = cross_street_count.to_dict()
    combined_street_dict = {}
    for key in on_street_dict:
        if key in cross_street_dict:
            combined_street_dict[key] = on_street_dict[key] + cross_street_dict[key]
        else:
            pass

    combined_street_dict = sorted(combined_street_dict.items(), key=lambda x: x[1],
                                  reverse=True)   #re-sort after combining
    combined_street_dict = dict(combined_street_dict)       #put back into dict since sort put into a list
    street_list = list(combined_street_dict.keys())

    street_name = st.selectbox('Enter a street in New York City:', (street_list))

    crashes = combined_street_dict.get(street_name)     #get number of crashes for that street name
    crashes_per_day = crashes / 730        #730 days in 2 years
    crash_probability = 1 - math.exp(-crashes_per_day)   #mathematical formula for probability - exp is 'e' to a power
    injuries_per_day = crashes_per_day *.183    #18.3% of crashes cause an injury (found earlier)
    injury_probability =  1 - math.exp(-injuries_per_day)
    non_injury_crash_probability = crash_probability - injury_probability
    safe_probability = 1 - crash_probability

    st.write(f'There is a {crash_probability * 100:.2f}% chance of crashing today on {street_name}.')
    st.write(f'There is a {injury_probability * 100:.2f}% chance of being in an injury-causing crash on '
             f'{street_name} today.')
    st.write(f'Thankfully, there is a {safe_probability * 100:.2f}% chance of not crashing at all on'
             f' {street_name} today!')

    pie_data = [safe_probability, non_injury_crash_probability, injury_probability]
    pie_labels = ['Safe', 'Non-Injury Crash', 'Injury-Causing Crash']       #set lists for data, labels, and colors
    pie_colors = ['limegreen', 'yellow', 'red']
    graph = plt.figure(figsize=(4,3))
    graph.patch.set_facecolor('grey')                   #create graph with features
    graph.patch.set_alpha(.625)
    plt.pie(data=pie_data, x=pie_data, colors=pie_colors, autopct='%.2f%%', labels=pie_labels)
    plt.title(f'Chances of Crashing Today on {street_name}', size=10, fontweight='bold')

    st.pyplot(graph)



########Start main area of output coding#############
st.title('New York City Vehicle Collisions')
nav = st.sidebar.selectbox('Navigation', ('Crash Frequency', 'Injury-Causing', 'Crash Locations', 'Crash Probability'))
#create navigation bar

#if statements for navigation
if nav == 'Crash Frequency':
    st.header('How often do crashes occur?')
    st.write('Select a time frame to view the average number of crashes in NYC during that time frame')
    time_frame = st.selectbox('Time Frame', ('Year', 'Month', 'Week', 'Day', 'Hour', 'Minute'))
    st.write('Average number of crashes in NYC per', time_frame , ':')
    crashes_per(df, time_frame, total_crashes)

elif nav == 'Injury-Causing':
    st.header('How many crashes are injury-causing?')
    st.write('In this dataset, an injury occured in ', find_injury_percent() ,'% of crashes.')
    injury_selector = st.radio('Include non-injury crashes?', ('Yes', 'No'))
    which_injury_stats(injury_selector)

elif nav == 'Crash Locations':
    st.header('Where do the most vehicle crashes occur in NYC?')
    area = st.selectbox('What type of area would you like to filter by?', ('Borough', 'ZIP Code', 'Street'))
    if area == 'Borough':
        st.write('Here is the number of crashes in each borough from 2015-2016:')
        borough_breakdown()                     #split locations with if statements and add amounts for zip and street
    elif area == "ZIP Code":
        how_many = st.number_input('View the top _____ ZIP codes:', 5,20,5)
        st.write(f'Here are the number of crashes from the top {how_many} ZIP codes from 2015-2016:')
        zip_breakdown()
    else:
        how_many = st.number_input('View the top _____ streets:', 5,20,5)
        st.write(f'Here are the number of crashes from the top {how_many} streets from 2015-2016:')
        street_breakdown()

else:
    st.header('What is the probability of a crash on my (or any) street today?')
    crash_probability()










