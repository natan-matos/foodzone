import pandas as pd
import streamlit as st
import inflection
import plotly.express as px

from streamlit_folium import folium_static, folium
from folium.plugins import MarkerCluster
from PIL import Image

# load dataset
def load_data(path):
   data = pd.read_csv(path)
   return data

# price range category
def create_price_tye(price_range):
    if price_range == 1:
     return "cheap"
    elif price_range == 2:
     return "normal"
    elif price_range == 3:
     return "expensive"
    else:
     return "gourmet"

# colors
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

# rename columns set underscore
def rename_columns(dataframe):
    df = data.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

# country names function
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

# convert values to us dollar
exchange_rates = {
    'Botswana Pula(P)': 0.018,
    'Brazilian Real(R$)': 0.20,
    'Emirati Diram(AED)': 0.27,
    'Indian Rupees(Rs.)': 0.012,
    'Indonesian Rupiah(IDR)': 0.000067,
    'NewZealand($)': 0.62,
    'Pounds(£)': 1.24,
    'Qatari Rial(QR)': 0.27,
    'Rand(R)': 0.053,
    'Sri Lankan Rupee(LKR)': 0.0033,
    'Turkish Lira(TL)': 0.050,
    'Dollar($)' : 1.0
}
def convert_to_usd(amount, currency):
    if currency in exchange_rates:
        return amount * exchange_rates[currency]
    else:
        return None

# data cleaning
def data_transform(df):
   # drop rows with null values
    df = df.dropna()

    # drop duplicate values
    df = df.drop_duplicates().reset_index(drop=True)

    #simplify the cuisines column
    df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

    # drop outliers
    filt = df['amount_usd'] != 25000017.0
    df = df.loc[filt, :]
    return df

    # set streamlit page
st.set_page_config(layout='wide')

# call functions
data = load_data('dataset\zomato.csv')
data = rename_columns(data)
data['country_code'] = data['country_code'].map(country_name)
data["amount_usd"] = data.apply(lambda row: convert_to_usd(row["average_cost_for_two"], row["currency"]), axis=1)
data['color_name'] = data['rating_color'].map(color_name)
df = data_transform(data)    


    ################################################################################################
image = Image.open('dataset\logo.png')
st.sidebar.image(image, width=150)
st.sidebar.header('Food Zone')
st.sidebar.subheader('Your food in your zone')
st.sidebar.write("""___""")

    # filter
st.sidebar.markdown('# Filters')
country_filter = st.sidebar.multiselect(label='Choose the countries',
                        options=df['country_code'].unique(),
                        default=df['country_code'].unique())

    #__________________________________________________________________________________________
    # filter functionality 
select_row = df['country_code'].isin(country_filter)
df = df.loc[select_row, :]

st.title('Food Zone')
st.markdown('#### Your food, in your Zone')
st.markdown('### We have the following metrics in our company')

with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(value=df.shape[0], label='Restaurants')
        with col2:
            df1 = df['country_code'].unique().shape[0]
            st.metric(value=df1, label='Countries')
        with col3:
            df1 = df['city'].unique().shape[0]
            st.metric(value=df1, label='Cities')
        with col4:
            df1 = df['votes'].sum()
            st.metric(value=df1, label='Total Votes')
        with col5:
            df1 = df['cuisines'].unique().shape[0]
            st.metric(value=df1, label='Cuisines')

with st.container():
    
        map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=2)
        make_cluster = MarkerCluster().add_to(map)
        for i, row in df.iterrows():
            popup = folium.Popup('Price:${0}, {1}'.format(row['amount_usd'], row['rating_text']))
            folium.Marker(location=[row['latitude'], row['longitude']], popup=popup,
                        icon=folium.Icon(icon='home', color=row['color_name'])).add_to(make_cluster)
            

        folium_static(map, width=1024, height=600)

    


# call functions
data = load_data('zomato.csv')
data = rename_columns(data)
data['country_code'] = data['country_code'].map(country_name)
data["amount_usd"] = data.apply(lambda row: convert_to_usd(row["average_cost_for_two"], row["currency"]), axis=1)
data['color_name'] = data['ratinsg_color'].map(color_name)
df = data_transform(data)

