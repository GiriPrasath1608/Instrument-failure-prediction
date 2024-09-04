import streamlit as st
import Bcode.DatabaseCode as DatabaseCode
import Bcode.mlCode as mlCode

st.set_page_config(page_title = 'IFDS',
                   page_icon='🔍',
                   layout ='wide',
                   initial_sidebar_state='collapsed',
                   )

st.title('Instrument Failure Detection System')
st.header('Instrument Readings')

#UDI,Product ID,Type,Air temperature [K],Process temperature [K],Rotational speed [rpm],Torque [Nm],Tool wear [min],

Product_ID = st.text_input(label = 'Enter Product_ID',value = 'M14860' ,max_chars= 6,placeholder = 'Max character is 6, first character L or M or H, reamining character 5 numbers')
Type = st.text_input(label = 'Enter Type',value = 'M', max_chars= 1, placeholder = 'Max character is 1, character L or M or H')
Air_temperature = st.number_input(label = 'Enter Air_temperature', min_value= 295.3, max_value= 304.5, placeholder = 'Max character is 5, ranges from 295.3 to 304.5')
Process_temperature = st.number_input(label = 'Enter Process_temperature',  min_value= 304.5, max_value= 313.8,placeholder = 'Max character is 5, ranges from 304.5 to 313.8')
Rotational_speed = st.number_input(label = 'Enter Rotational_speed',  min_value= 1168, max_value= 2886, placeholder = 'Max character is 4, ranges from 1168 to 2886')
Torque = st.number_input(label = 'Enter Torque', min_value= 3.8, max_value= 76.6,placeholder = 'Max character is 4, ranges from 3.8 to 76.6')
Tool_wear = st.number_input(label = 'Enter Tool_wear',  min_value= 0, max_value= 253,placeholder = 'Max character is 3, ranges from 0 to 253')

check_button = st.button('Check Failure/No_Failure')

if check_button:
    instrument_readings = {'Product ID':Product_ID,
                           'Type':Type,
                           'Air temperature [K]':Air_temperature,
                           'Process temperature [K]':Process_temperature,
                           'Rotational speed [rpm]':Rotational_speed,
                           'Torque [Nm]':Torque,
                           'Tool wear [min]':Tool_wear,}
    with st.container(border = True):
        st.write('✅----------Input Readings----------')
        input_dataframe = DatabaseCode.to_dataframe(instrument_readings)
        st.dataframe(input_dataframe)

        st.write('✅---------Data Engineering----------')
        instrument_readings_df = mlCode.data_engineering(instrument_readings)
        st.dataframe(instrument_readings_df)

        st.write('✅----------Data Labeling----------')
        X = mlCode.data_encoder(instrument_readings_df)
        st.dataframe(X)

        st.write('✅------------Fail/No Fail Prediction------------')
        prediction = mlCode.IFDS_model(instrument_readings)
        st.write(prediction)

        st.write('✅------------Input Reading Pushing to MongoDB Raw Collection------------')
        MongodbPush = DatabaseCode.DataPush_mongoDB(instrument_readings)
        if MongodbPush['acknowledge']:
            st.write(MongodbPush['return_data'])
       