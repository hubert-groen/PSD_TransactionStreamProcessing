import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from kafka import KafkaConsumer

user_details = {
    1: 'Warszawa',
    2: 'Los Angeles',
    3: 'Berlin',
    4: 'Paryż',
    5: 'Madryt',
    6: 'Rzym',
    7: 'Toronto',
    8: 'São Paulo',
    9: 'Sydney',
    10: 'Tokio',
}

user_colors = {
    1: ("#ff7069", "#fa0202"),
    2: ("#fcfb97", "#c2bb02"),
    3: ("#9af78f", "#12a102"),
    4: ("#75fafa", "#027878"),
    5: ("#5f67f5", "#0f03fc"),
    6: ("#aa69f5", "#7803ff"),
    7: ("#d86ef5", "#c603fc"),
    8: ("#f763da", "#fc00ca"),
    9: ("#c2c4c3", "#6e706f"),
    10: ("#f7d5a8", "#f78c00"),
}

def get_color(alert, user_id):
    light_color, dark_color = user_colors.get(user_id, ("lightgray", "gray"))
    return light_color if alert == 'None' else dark_color

if __name__ == '__main__':
    st.set_page_config(
        page_title="Real-Time Anomalous Transaction Detection Dashboard",
        page_icon="✅",
        layout="wide",
    )
    st.title("Real-Time / Anomalous Transaction Detection Dashboard")
    
    placeholder = st.empty()
    
    consumer = KafkaConsumer(
        'TOPIC-NA2',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
    
    df = pd.DataFrame()

    for message in consumer:
        try:
            json_str = message.value.decode('utf-8')
            json_str = json_str.replace('\'', '\"')
            
            with placeholder.container():
                data = json.loads(json_str)
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                
                fig_earth, fig_chart = st.columns(2)
                with fig_earth:
                    df['color'] = df.apply(lambda row: get_color(row['alert'], row['user_id']), axis=1)
                    color_discrete_map = {color: color for color in df['color'].unique()}
                    fig = px.scatter_geo(
                        data_frame=df,
                        lat='latitude',
                        lon='longitude',
                        color='color',
                        hover_name='user_id',
                        hover_data={'amount': True, 'alert': True},
                        title='Transaction Locations and Anomaly Predictions',
                        color_discrete_map=color_discrete_map
                    )
                    fig.update_traces(marker=dict(size=10))
                    fig.update_layout(showlegend=False)
                    st.write(fig)
                
                with fig_chart:
                    counts = df.groupby(['user_id', 'alert']).size().unstack(fill_value=0)
                    counts['total'] = counts.sum(axis=1)
                    
                    counts['normal_ratio'] = counts.get('None', 0) / counts['total']
                    counts['alert_ratio'] = (counts.sum(axis=1) - counts.get('None', 0)) / counts['total']

                    bars = []
                    for user_id in user_colors.keys():
                        if user_id in counts.index:
                            light_color, dark_color = user_colors[user_id]
                            normal_ratio = counts.loc[user_id, 'normal_ratio']
                            alert_ratio = counts.loc[user_id, 'alert_ratio']
                            bars.append(go.Bar(
                                name=f'User {user_id} - Normal ({user_details[user_id]})',
                                x=[f'User {user_id}'],
                                y=[normal_ratio],
                                marker_color=light_color
                            ))
                            bars.append(go.Bar(
                                name=f'User {user_id} - Alert ({user_details[user_id]})',
                                x=[f'User {user_id}'],
                                y=[alert_ratio],
                                marker_color=dark_color,
                                base=[normal_ratio]
                            ))

                    fig = go.Figure(data=bars)
                    fig.update_layout(
                        barmode='stack', 
                        title='User Transaction Counts with Alerts',
                        yaxis=dict(title='Percentage', tickformat='.0%', range=[0, 1])
                    )
                    st.write(fig)

                # st.markdown("### User Color Legend")
                # for user_id, (light_color, dark_color) in user_colors.items():
                #     st.markdown(f"**User {user_id}:** <span style='color:{dark_color}'>●</span> (Alert), <span style='color:{light_color}'>●</span> (No Alert) - {user_details[user_id]}", unsafe_allow_html=True)
                
        except json.decoder.JSONDecodeError:
            print('omitting message\n')
