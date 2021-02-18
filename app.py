import pandas as pd
import streamlit as st 
import numpy as np

st.title('Q-Week Results')

df = pd.read_html('https://docs.google.com/spreadsheets/d/1UCrSZrIX45MlKz6EQfEVJ-9dHjLw7xeTpg77lujknEw/edit#gid=1779447167', flavor='bs4', encoding='utf8', skiprows=[0])[0]

df = df[[col for col in df.columns if 'Unnamed' not in col and col != '1']]
df = df.dropna(axis = 'index', how = 'all')
df = df.dropna(axis = 'columns', how = 'all')

mapping = {
    "What is your quad name?": "Quad",
    "What is your kerb (no @mit.edu)?": "Kerb",
    "What event are you recording participation/submission for?": "Event",
    "If participation, how many people from the quad attended or participated?": "Participation",
    "If participation, how many people are in your quad?": "Quad Total"
}

df = df.rename(columns=mapping)

df['Quad Total'] = df['Quad Total'].fillna('4 ppl')
df['Participation'] = df['Participation'].fillna(3)

df['Quad Total'] = df['Quad Total'].apply(lambda x: x[0])

events = ['All'] + sorted(list(df['Event'].dropna().unique()))
events = st.multiselect('Event', options=events, default=['All'])

if 'All' not in events:
    df = df[df['Event'].isin(events)]

df['Kerb'] = 'bottom text'

# for each quad, get the events they've been to and the participation points

# for each quad, sum points over all events

quad_groups = df.groupby('Quad')
for quad, group in sorted(quad_groups, key=lambda x: str(x[1]['Quad'])):
    
    points_df = group.groupby('Event').agg('max')
    event_names = points_df.index.values
    puntos = [int(i)/int(j)*400 for i, j in zip(points_df['Participation'].to_list(), points_df['Quad Total'].to_list())]
    display_df = {'Event Name': event_names, 'Attendance Points': puntos}

    f'### {quad}'
    f"**Total Points**: {sum(puntos)}"

    # display_df['Event Points'] = int(group.groupby('Event').agg('min')['Participation'])/int(group.groupby('Event').agg('min'))*400


    # for event_frame in group.groupby('Event').agg({'min'}):
    #     print(event_frame)
    #     if event_frame.shape[0] == 1:
    #         display_df['Event Name'].append(event_name)
    #         display_df['Attendance Points'].append(int(event_frame['Participation'])/int(event_frame['Quad Total'])*400)
    #     else:
    #         display_df['Event Name'].append(event_name)
    #         points = event_frame.groupby('Event').agg({'Participation': 'max'}).iloc[0]

    display_df = pd.DataFrame(display_df)
    display_df = display_df.sort_values(by=['Attendance Points'], ascending=False).reset_index(drop=True)
    st.table(display_df)
