import streamlit as st 
import pandas as pd 
import plotly.express as px 
st.set_page_config(layout="wide", page_title="Debt Analysis App") 
st.title("?? Financial Debt Analysis Dashboard") 
f = st.file_uploader("Upload your Excel file", type=["xlsx"]) 
if f: 
 try: 
  df = pd.read_excel(f) 
  df.columns = [str(c).strip() for c in df.columns] 
  v = next((c for c in df.columns if 'residual' in c.lower()), df.columns[0]) 
  TEN = next((c for c in df.columns if 'name' in c.lower() or 'ten' in c.lower()), df.columns[0]) 
  due = next((c for c in df.columns if 'due' in c.lower()), None) 
  delay = next((c for c in df.columns if 'delay' in c.lower()), None) 
  df[v] = pd.to_numeric(df[v], errors='coerce').fillna(0) 
  df[TEN] = df[TEN].astype(str) 
  def r(d): 
   if d <= 0: return 'AAA (Good)' 
   elif d <= 30: return 'A (Warning)' 
   return 'C (Danger)' 
  df['Rating'] = pd.to_numeric(df[delay], errors='coerce').fillna(0).apply(r) 
  csv = df.to_csv(index=False).encode('utf-8') 
  st.download_button("?? Download Analyzed Data (CSV)", csv, "Analysis.csv", "text/csv") 
  t1, t2 = st.tabs(["Credit Matrix", "Cash Flow Forecast"]) 
  with t1: 
   c1, c2 = st.columns(2) 
   with c1: st.plotly_chart(px.pie(df, values=v, names=TEN, hole=0.4, title='Debt Distribution by Customer Name'), use_container_width=True) 
   with c2: 
    sel = st.selectbox("Filter by Rating:", sorted(df['Rating'].unique())) 
    sub = df[df['Rating']==sel].groupby(TEN)[v].sum().reset_index().sort_values(v, ascending=False).head(15) 
    fig = px.bar(sub, x=v, y=TEN, orientation='h', title=f'Top 15 Customers - {sel}', color=v) 
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, yaxis_title='Customer Name', xaxis_title='Amount') 
    st.plotly_chart(fig, use_container_width=True) 
  with t2: 
   if due: 
    df['M'] = pd.to_datetime(df[due], errors='coerce').dt.to_period('M').astype(str) 
    cf = df.groupby('M')[v].sum().reset_index().sort_values('M') 
    st.plotly_chart(px.line(cf, x='M', y=v, markers=True, title='Monthly Cash Flow Trend'), use_container_width=True) 
    st.plotly_chart(px.bar(cf, x='M', y=v, title='Collection by Month'), use_container_width=True) 
 except Exception as e: st.error(f"Error: {e}") 
