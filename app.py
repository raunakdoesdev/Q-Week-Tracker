import pandas as pd
import streamlit as st 
import numpy as np

st.title('Q-Week Results')

df = pd.read_csv('https://docs.google.com/spreadsheets/d/1UCrSZrIX45MlKz6EQfEVJ-9dHjLw7xeTpg77lujknEw/export?format=csv&gid=1779447167')

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

quad_groups = df.groupby('Quad')
for quad, group in sorted(quad_groups, key=lambda x: str(x[1]['Quad'])):
    
    points_df = group.groupby('Event').agg('min')
    event_names = points_df.index.values
    puntos = [int(i)/int(j)*400 for i, j in zip(points_df['Participation'].to_list(), points_df['Quad Total'].to_list())]
    five_hundred_puntos = ['Quad Intro Video', 'Photo Contest', 'Door Tag Contest', 'COVID Friends Design Contest', 'Meme Contest', 'Outfit Photo']
    for event_name in event_names:
        if event_name in five_hundred_puntos:
            puntos[list(event_names).index(event_name)] *= 5/4 
        if event_name == '2/18: Wikipedia Game':
            puntos[list(event_names).index('2/18: Wikipedia Game')] = 400
    display_df = {'Event Name': event_names, 'Attendance Points': puntos}

    f'### {quad}'
    f"**Total Points**: {format(sum(puntos),'.2f')}"

    display_df = pd.DataFrame(display_df)
    display_df = display_df.sort_values(by=['Attendance Points'], ascending=False).reset_index(drop=True)
    st.table(display_df)