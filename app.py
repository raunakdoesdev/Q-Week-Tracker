import pandas as pd
import streamlit as st 

st.title('Q-Week Results')

df = pd.read_html('https://docs.google.com/spreadsheets/d/1UCrSZrIX45MlKz6EQfEVJ-9dHjLw7xeTpg77lujknEw/edit#gid=1779447167', flavor='bs4', encoding='utf8', skiprows=[0])[0]

df = df[[col for col in df.columns if 'Unnamed' not in col and col != '1']]

mapping = {
    "What is your quad?": "Quad",
    "What is your kerb (no @mit.edu)?": "Kerb",
    "What event?": "Event"
}

df = df.rename(columns=mapping)

events = ['All'] + sorted(list(df['Event'].dropna().unique()))
events = st.multiselect('Event', options=events, default=['All'])

if 'All' not in events:
    df = df[df['Event'].isin(events)]

quad_groups = df.groupby('Quad')
for quad, group in sorted(quad_groups, key=lambda x: -len(x[1]['Kerb'].dropna())):
    
    f'### {quad}'
    f"**Total Points**: {len(group['Kerb'].dropna())}"

    display_df = {'Kerb': [], 'Attendance Points': []}

    for kerb, kgroup in group.groupby('Kerb'):
        display_df['Kerb'].append(kerb)
        display_df['Attendance Points'].append(len(kgroup))

    display_df = pd.DataFrame(display_df)
    display_df = display_df.sort_values(by=['Attendance Points'], ascending=False).reset_index(drop=True)
    st.table(display_df)
