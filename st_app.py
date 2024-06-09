import streamlit as st
import  numpy as np
import plotly.express as px
import pandas as pd
import json
from kafka import KafkaConsumer

USER_ID = 4

if __name__ == '__main__':
# stremlit app
    st.set_page_config(
        page_title="Real-Time Anomalous Transaction Detection Dashboard",
        page_icon="✅",
        layout="wide",
    )
    st.title("Real-Time / Anomalous Transaction Detection Dashboard")
    
    # creating a single-element container
    placeholder = st.empty()
    
    # Kafka Consumer
    consumer = KafkaConsumer(
        'TOPIC-A4',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
        )
    
    df = pd.DataFrame()
    
    for message in consumer:
        try:
            # print('transaction after processing:')
            json_str = message.value.decode('utf-8')
            json_str = json_str.replace('\'', '\"')
            # print(json.loads(json_str))
            
            with placeholder.container():
                # Load the data
                data = json.loads(json_str)
                # Create a DataFrame
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                user_df = df[df['user_id'] == USER_ID]
                # Create a scatter plot
                fig_earth, fig_chart = st.columns(2)
                with fig_earth:   
                    fig = px.scatter_geo(
                        data_frame=user_df,
                        lat='latitude',
                        lon='longitude',
                        color='alert',
                        hover_name='user_id',
                        hover_data={'amount': True, 'alert': True},
                        title='Transaction Locations and Anomaly Predictions'
                    )
                    st.write(fig)
                with fig_chart:
                    fig = px.line(user_df, x=user_df.index, y="amount", title='Amount of Transactions Over Time')
                    st.write(fig)
                
        except(json.decoder.JSONDecodeError):
            print('ommiting message/n')