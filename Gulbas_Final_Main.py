import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

csvFile = "Final_Proj/California_Fire_Incidents.csv"

# Title and Header for page
st.title('California Wildfires Between 2013 - 2020')
st.write('Between the years 2013 and 2020, a total of 1636 wildfires raged in California. Interact with this page to learn more about them!')



def main():
    df = pd.read_csv(csvFile)
    # Line Plot
    st.sidebar.subheader('Adjust for Line Plot')
    num = st.sidebar.slider('Select a number of Crews:', 0, 80, 1)
    lineData = getLineData(df, num)
    plotLine(lineData)
    # Bar chart
    st.sidebar.subheader('Adjust for Barchart')
    c = st.sidebar.multiselect('Select multiple Counties', df['Counties'].tolist())
    c, a = getBarData(df, c)
    plotBar(c, a)
    # Pie chart
    st.sidebar.subheader('Percent Fires Major Incidents')
    st.sidebar.caption('')
    piePlot(df)
    # map
    st.sidebar.subheader('Adjust for Map')
    county = st.sidebar.selectbox('Select county to see map:', df['Counties'].tolist())
    makeMap(df, county)


def getLineData(df, num):
    # get value counts
    data = df['CrewsInvolved'].value_counts()
    # change series to df, reset index to rename
    data = data.to_frame()
    data.reset_index(inplace=True)
    data.columns = ['Crews', 'Amount']
    # filter based off of slider
    data = data[data['Crews'] <= num]
    data = data.sort_values('Crews')
    return data


def plotLine(d):
    crews = d['Crews'].tolist()
    amts = d['Amount'].tolist()
    fig, ax = plt.subplots()
    ax.plot(crews, amts)
    ax.set_xlabel('Number of Crews')
    ax.set_ylabel('Fire Count')
    ax.set_title('Number of Fires per Number of Crews')
    st.header('Line Plot')
    st.write('Use the side bar to adjust the number of crews, and the plotline will display the number of fires based on your selected range.')
    st.pyplot(fig)


def getBarData(df, counties):
    data = df['Counties'].value_counts().to_frame().reset_index()
    data.columns = ['County', 'Count']
    data = data[data['County'].isin(counties)]
    countyList = data['County'].tolist()
    amtList = data['Count'].tolist()
    return countyList, amtList


def plotBar(c, a):
    fig, ax = plt.subplots()
    ax.bar(c, a)
    ax.set_xlabel('County Name')
    ax.set_ylabel('Number of Fires')
    ax.set_title('Number of Fire per County')
    ax.tick_params(labelrotation=45)
    st.header('Bar Chart')
    st.write('Use the sidebar to select one or more counties, and the graph will output the number of fires per your selected counties.')
    st.pyplot(fig)


def piePlot(df):
    data = df['MajorIncident'].value_counts()
    labels = data.index
    fig, ax = plt.subplots()
    ax.pie(data, autopct='%1.1f%%')
    ax.legend(labels, loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title("Percent of Fires being Major Incidents")
    st.header('Pie Chart')
    st.write('A portion of the wildfires were denoted as accidents, while some where not. The pie chart below displays these distinctions.')
    st.pyplot(fig)


def makeMap(df, county):
    df = df[df.Latitude != 0]
    df = df[df.Longitude != 0]
    df.index = df['Counties']
    df = df[['Latitude', 'Longitude']]
    df.columns = ['lat', 'lon']
    df = df.loc[[county]]
    st.header('Map of Wildfires Between 2013-2020')
    st.write('This pie chart uses the the latitude and longitude to plot each fire. Please select a county display the wildfires that occurred in your selected county.')
    st.map(df)


main()
