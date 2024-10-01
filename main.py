import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from functions import get_datatype
from functions import get_allfaults
from functions import get_discretefaults
from functions import get_visual

with open("styles.css") as f:
   st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

st.title("Fault Reactivation Application")

fault_regime=st.sidebar.selectbox("Stress Regime",("Normal Faulting","Thrust Faulting","Strike-Slip"))

S1 = st.sidebar.number_input("Sigma 1 (psi)")
S2 = st.sidebar.number_input("Sigma 2 (psi)")
S3 = st.sidebar.number_input("Sigma 3 (psi)")
Pp= st.sidebar.number_input("Pore Pressure (psi)")
w=st.sidebar.slider("Maximum Horizontal Stress Azimuth (Degree)",min_value=0,max_value=360,step=1)
C=st.sidebar.slider("Fault Cohesion (psi)",min_value=0,max_value=1000,step=1)
fa=st.sidebar.slider("Friction Angle (Degree)",min_value=0,max_value=50,step=1)

uploaded_file = st.sidebar.file_uploader("Fault Data File  (Azimuth, Dip) .cvs format")
if uploaded_file is not None:
  df = pd.read_csv(uploaded_file)


ok=st.sidebar.button('Submit')
if ok:
  m=get_datatype(S1,S2,S3,fault_regime)

  strk, dip, NN1 =get_allfaults(S1,S2,S3,w,Pp,C,fa,m)
  df1 = pd.DataFrame({'Strike':strk, 'Dip':dip, 'Pc':NN1})

  strk2, dip2, NN2 =get_discretefaults(S1,S2,S3,w,Pp,C,fa,m,df)
  df2 = pd.DataFrame({'Strike':strk2, 'Dip':dip2, 'Critical Pressure (psi)':NN2})
  df2.index.name = 'Fault'
  
  
  #AgGrid(df2)
  styled_df = df2.style.set_properties(**{
    "background-color": "white", 
    "color": "black", 
    'text-align': 'center'})
  
  def color_columns(df):
    styles = {
    'Strike': 'background-color: lightblue; color: black;',
    'Dip': 'background-color: lightgreen; color: black;',
    'Critical Pressure (psi)': 'background-color: lightcoral; color: black;'
    }
    return df2.style.apply(lambda x: [styles[col] for col in df2.columns], axis=1)

# Apply the styles to the DataFrame
  styled_df2 = color_columns(df)
  #st.dataframe(styled_df)
  st.write(styled_df2.to_html(), unsafe_allow_html=True)

  sss=get_visual(df1,df2)
  st.pyplot(sss)
