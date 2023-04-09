# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 12:59:01 2023

@author: karth
"""

import streamlit as st
import pandas as pd
import datetime
#from datetime import datetime




st.title("Greyfeathers Technologies")
d = st.date_input("Please schdule ur order date :",datetime.date(2023, 7, 6))
st.write('Your schduled Date is :', d)




df1= pd.read_csv("customer_details.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
df2= pd.read_csv("merchant_orders.csv")  # read a CSV file inside the 'data" folder next to 'app.py'

#tab 1 customer analysis
#customers of other merchants
dnc=df1[~df1.merchant_ids.str.contains("d1e68f79-1504-41d3-839b-bd7347820cdb")]
dnc1=dnc[['customer_id',"user_name","phone_number","merchant_id"]]
dnc1["phone_number"]=dnc1["phone_number"].astype(str)
#customers of current merchant id "d1e68f79-1504-41d3-839b-bd7347820cdb"
dc_new=pd.DataFrame()
dc=df1[df1.merchant_ids.str.contains("d1e68f79-1504-41d3-839b-bd7347820cdb")]
dc_new=dc[["customer_id","user_name","merchant_ids"]]  

dm_new=df2[["customer_id","merchant_id","order_id","amount"]]
 

dr=pd.merge(dc_new, dm_new,on= 'customer_id') 

#customer with current merchant distribution
dr1=dr.groupby(["customer_id","user_name","order_id"]).sum()["amount"].reset_index()

#revenue per customer
dr2=dr1.groupby(["user_name"]).sum()["amount"].reset_index()
dr2.rename(columns={"amount": "Revenue"}, inplace=True)

#--------

#tab4 item analysis
item=df2['items_ordered'].str.split(',', expand=True)

item.iloc[31,1]=item.iloc[31,2]
item.iloc[32,1]=item.iloc[32,2]
item.iloc[31,2]=item.iloc[31,3]
item.iloc[32,2]=item.iloc[32,3]


for i in range(39, 67):
    item.iloc[i][2]=item.iloc[i][4]
    item.iloc[i][1]=item.iloc[i][3]

df_item= pd.DataFrame()
item_count=item[1].str.split(':', expand=True)
item_name=item[2].str.split(':', expand=True)
df_item["count"]=item_count[1]
df_item["name"]=item_name[1]

df_item["count"] = df_item["count"].astype(int)
df_finalitem=df_item.groupby(["name"]).sum()["count"]
#-----------

#tab 3 table analysis

#orders per table
dt1=df2.groupby(["table_number"]).count()["order_id"].reset_index()
dt1.rename(columns={"order_id": "Orders dined in"}, inplace=True)


#number of guest per table
dt2=df2.groupby(["table_number"]).sum()["no_of_guests"].reset_index()

#Revenue per guest
dt3=df2.groupby(["no_of_guests"]).sum()["amount"].reset_index()
dt3.rename(columns={"amount": "revenue"}, inplace=True)

#--------

tab1, tab2, tab3,tab4 = st.tabs(["Customers", "Orders","Tables", "Items"])


with tab1:
   st.header("Customers Analysis")
   st.subheader("New customers with other merchants")
   st.write(dnc1)
   st.subheader("Existing customers with current merchant")
   st.write(dr1)
   st.subheader("Revenue per customer")
   st.write(dr2)
   
   
with tab2:
   st.header("Orders Analysis")
   di=df2[df2["order_type"].str.contains('Dine-in')]
   ta=df2[df2["order_type"].str.contains('Take away')]  
   
   st.subheader("Orders Distribution")
   df2['Order_date'] =  pd.to_datetime(df2['created_on'])
   order_t=df2.groupby([pd.Grouper(key='Order_date', freq='60T'), 'order_id']).sum()['amount']
   st.write(order_t)
   st.subheader("Orders Dined in")
   orders_di=di.groupby(["order_id","table_number"]).sum()[["no_of_guests","amount"]]
   st.write(orders_di)
   st.subheader("Orders takeaway")
   orders_ta=ta.groupby(["order_id"]).sum()[["amount"]]
   st.write(orders_ta)
with tab3:
   st.header("Table Analysis")
   st.subheader("orders per table")
   st.write(dt1)
   st.subheader("number of guest per table")
   st.write(dt2)
   st.subheader("Revenue per guest")
   st.write(dt3)
with tab4:
   st.header("Items Analysis")
   st.subheader("Numeber of items ordered")
   st.write(df_finalitem)
   
   
   

