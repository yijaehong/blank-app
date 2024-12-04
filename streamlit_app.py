
from requests.api import options
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

import requests


import numpy as np
import folium
import time

st.set_page_config(page_title="Table Crawler", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

connection = False
tables=[]
csv_count=0

def korea():
    return False

# Sidebar config
with st.sidebar:
    st.title("Table Crawler")
    st.write("A simple table crawler built with Python")
    
    # Input for URL
    url_w = st.text_input("Please enter the URL to scrape the tables", key="text", value="https://www.mofa.go.kr/www/brd/m_4052/list.do?page=")
    col1, col2 = st.columns([1,1])
    
    
    genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[외교부]🎈", "조달청(Crawing 대기)🧊", "한국투자공사(Crawing 대기)🧊 "],
    index=0
    )

    st.write("You selected:", genre)
    # Clicked status for click me button
    if 'clicked' not in st.session_state:
        st.session_state.clicked = False

    # Function for enabling clicked 
    def click_button():
        st.session_state.clicked = True

    # Function for enabling clicked 
    def clear_button():
        st.session_state.clicked = False
        st.session_state.text = ""
    
    with col1:
        # Button for click me
        st.button('Click me', on_click=click_button,type='primary', use_container_width=True)
                  
    with col2:
        st.button('Clear',on_click=clear_button, type='secondary',use_container_width=True)
        


    if st.session_state.clicked:

        number_compare_bool=True
        table_count_all=0
        for i in range(1):
            a = url_w + str(i+1) 
            html = requests.get(url=str(a), verify=False)
            
            if number_compare_bool:
                if html.status_code in [200]:
                    st.write("The connection successful")
                    connection = True          
                    data = html.text
                    soup = BeautifulSoup(data, 'lxml')
                    tables.append(soup.select('table'))
                    
                    if number_compare_bool:
                        df_2 = pd.read_csv('houseprice.csv', sep=',',engine='python')
                        csv_count=df_2.iloc[0,0]

                        table_dict = pd.read_html(str(tables),header=0)[0]
                        
                        table_count_all=table_dict.iloc[0,0]
                        
                        if ( table_count_all > csv_count):
                            number_compare_bool=False
                            table_count_all > csv_count
                            i
                                            
                else:
                    st.write(f"Status Code: {html.status_code}")
                    st.write("Seems the entered url is not valid")
                pd.DataFrame(tables)
                time.sleep(1)
            else:
                break
    st.write("Note: This app searches for table tag in the html page, so it returns the table only if concern tags exists.")

# Main Container config
with st.container():
    st.title("🎉 KEDA(Kepco global bidding Data)")
    st.markdown("#  :blue[태양의 후예] ☀️")
    success_b=True
    map_data=pd.DataFrame()
    # if tables:
    #     table_dict = {}    
    #     header_b=True
    #     mode_b='w'
    #     for i,tab in enumerate(tables):
    #         table_dict[i+1] = pd.read_html(str(tab),header=0)[0]           
    #         table_dict[i+1].to_csv("houseprice.csv", index = False, header=header_b, sep=',', mode=mode_b)
    #         header_b=False
    #         mode_b='a'
    #         success_b=True
    if success_b:        
        df_2 = pd.read_csv('houseprice.csv', sep=',',engine='python')

        bid_toal_count=df_2.iloc[0,0]
        st.write("외교부 해외입찰 데이터:", bid_toal_count, "건이 수집되었습니다.")
        df_2
        country=df_2['제목'].str.split("[", expand=True)[1]
        country=country.str.split("]", expand=True)[0]
        
        if country is not None:
        # contents=pd.DataFrame(country)
            country.value_counts().to_csv("national_count.csv",  header=True, sep=',', mode='w')
            
            df_3 = pd.read_csv('national_count.csv', sep=',',engine='python')
            df_3.columns = ['Country', 'Count']   
            st.subheader("Number of bids by country")   
            df_3      
        

            country_search = pd.read_csv('country.csv', sep=',',engine='python')
            as1=country_search['Name']

            china=df_3['Country']
            df_3.set_index(['Country'],inplace=True)
            for item in china:
                
                a=country_search[country_search['Name'].str.contains(item)][['latitude']].values
                b=country_search[country_search['Name'].str.contains(item)][['longitude']].values
                df_3.loc[item,['latitude']]=a[0]
                df_3.loc[item,['longitude']]=b[0]
                # df_3.loc[item,['latitude','longitude']]=country_search[country_search['Name'].str.contains(item)][['latitude','longitude']]

            df_3=df_3.reset_index()

            
            st.title('Map with Location Data')
            st.caption(
                "Displaying geographical data on a map using Streamlit and Folium")
            
            st.subheader("World Map :: Streamlit map")
            
            list_from_df = df_3['latitude'].tolist()
            list_from_df = list(map(float, list_from_df)) 
            list_from_df2 = df_3['longitude'].tolist()
            list_from_df2 = list(map(float, list_from_df2)) 
            list_from_df3 = (df_3['Count']).tolist()
            list_from_df3 = list(map(int, list_from_df3))
            list_from_df4 = (df_3['Country']).tolist()
            
            data = pd.DataFrame({
                'latitude':list_from_df ,
                'longitude':list_from_df2,
                'Size': list_from_df3
            })            
            
            st.map(data)
            


            # 데이터
            # map_data = pd.DataFrame({
            #     'lat': [-34, 49, -38, 59.93, 5.33, 45.52, -1.29, -12.97],
            #     'lon': [-58, 2, 145, 30.32, -4.03, -73.57, 36.82, -38.5],
            #     'name': ['Buenos Aires', 'Paris', 'Melbourne', 'St Petersburg', 
            #             'Abidjan', 'Montreal', 'Nairobi', 'Salvador'],
            #     'value': [10, 12, 40, 70, 23, 43, 100, 43] 
            # })
            map_data = pd.DataFrame({
                'lat':list_from_df ,
                'lon':list_from_df2,
                'name': list_from_df4,
                'value': list_from_df3
            }) 

            #1 지도 객체 생성
            my_map = folium.Map(
                location=[map_data['lat'].mean(), map_data['lon'].mean()], 
                zoom_start=2)
           #2 지도 커스텀
            # 지도에 원형 마커와 값 추가
            for index, row in map_data.iterrows():       # 데이터프레임 한 행 씩 처리
                folium.CircleMarker(                     # 원 표시
                    location=[row['lat'], row['lon']],   # 원 중심- 위도, 경도
                    radius=row['value']*0.5,             # 원의 반지름
                    color='pink',                        # 원의 테두리 색상
                    fill=True,                           # 원을 채움
                    fill_opacity=0.5                     # 원의 내부를 채울 때의 투명도
                ).add_to(my_map)                         # my_map에 원형 마커 추가

                folium.Marker(                           # 값 표시
                    location=[row['lat'], row['lon']],   # 값 표시 위치- 위도, 경도
                    icon=folium.DivIcon(
                        html=f"<div>{row['name']}<br> {row['value']}</div>"), # 값 표시 방식
                ).add_to(my_map)                         # my_map에 값 추가
                
                
            #3 지도 제목과 캡션 추가

            st.subheader("Map with Location Data : Folium feat")
            #4 지도 시각화
            st.components.v1.html(my_map._repr_html_(),height=600)

