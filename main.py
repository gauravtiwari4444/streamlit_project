import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv("startup_cleaned.csv")
df["date"] = pd.to_datetime(df["date"])

df.investor=df.investor.fillna("undisclosed")

def show_investor(investor):
    st.title(investor)
    st.markdown(""" Recent investment""")
    st.dataframe(df[df.investor.str.contains(investor)][["date","startup","vertical","city","amount"]].head(5),hide_index=True)

    c1,c2=st.columns(2)
    with c1:
        st.subheader("Investment by Vertical")

        fig, ax = plt.subplots(figsize=(5, 5))

        df[df.investor.str.contains(investor)].vertical.value_counts().plot(
            kind="pie",
            ax=ax
        )

        st.pyplot(fig)

    with c2:
        st.subheader("Investment by City")

        fig, ax = plt.subplots(figsize=(5, 5))

        df[df.investor.str.contains(investor)].city.value_counts().plot(
            kind="pie",
            ax=ax
        )

        st.pyplot(fig)

def show_startup(startup):
    st.title(startup)
    founder=df[df.startup==startup].sort_values(by="amount",ascending=False).head(1)["investor"].values[0]
    st.write("founder : ",founder)
    st.subheader("Generally Works In Industry")
    fig, ax =plt.subplots()
    df[df.startup == startup].vertical.value_counts().plot(kind="pie", ax=ax)
    st.pyplot(fig)
st.sidebar.title("Overview")
option=st.sidebar.selectbox("Select One",["Overall Analysis","Investor Analysis","Startup Analysis" ])

if option =="Overall Analysis":
    st.title(" Overall Analysis ")
    col1,col2,col3=st.columns(3)

    with col1:
        st.metric("Total Funds",round(df.amount.sum(),2))

    with col2:
        st.metric("Max Fund",df.amount.max())

    with col3:
        st.metric("Average Fund",round(df.amount.mean(),2))

elif option=="Investor Analysis":
    selected_investor=st.sidebar.selectbox("Choose Investor",sorted(set(df.investor.str.split(",").sum())))
    btn1=st.sidebar.button("Find Details")
    st.title("Investor Analysis")
    if btn1:
        show_investor(selected_investor)
elif option=="Startup Analysis":
    selected_startup=st.sidebar.selectbox("Choose Startup", sorted(df.startup.unique()))
    btn2=st.sidebar.button("Find Details")
    st.title("Startup Analysis")
    if btn2:
        show_startup(selected_startup)