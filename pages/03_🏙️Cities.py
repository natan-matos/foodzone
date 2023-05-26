import pandas as pd
import inflection
import plotly.express as px
import streamlit as st

from PIL import Image


# load dataset
def load_data(path):
   data = pd.read_csv(path)
   return data

# rename columns set underscore
def rename_columns(dataframe):
    df = dataframe.copy()
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

# data cleaning and transformation
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

# Data visualization
def data_viz(df):
    # set streamlit page
    st.set_page_config(layout='wide')

    
    st.sidebar.header('Food Zone')
    st.sidebar.subheader('Your food in your zone')
    st.sidebar.write("""___""")

    # Filter
    st.sidebar.markdown('# Filters')
    country_filter = st.sidebar.multiselect(
        label='Choose the countries',
        options=df['country_code'].unique(),
        default=df['country_code'].unique()
        )

    
    # Filter functionality 
    select_row = df['country_code'].isin(country_filter)
    df = df.loc[select_row, :]

    st.sidebar.write("""___""")

    # Home Page
    st.title('🏙️City Vision')

    # Top 10 Cities with more restaurants Chart
    with st.container():
        restaurant_by = df[['city', 'restaurant_id', 'country_code']].groupby(['city', 'country_code']).nunique().sort_values('restaurant_id', ascending=False).reset_index()
        top_10_cities = restaurant_by.sort_values('restaurant_id', ascending=False).head(10)
        fig = px.bar(top_10_cities, x='city', y='restaurant_id',
                        title= 'Top 10 Cities with more restaurants',
                        color='country_code',
                        text_auto=True,
                        labels={'city': 'City', 'restaurant_id': 'Restaurants'})
        st.plotly_chart(fig, use_container_width=True)

    # Top 7 charts
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            # Top 7 Cities with more restaurants rating > 4 chart
            df1 = df[df['aggregate_rating'] >= 4.0]
            rating_by_city = df1[['restaurant_id', 'city', 'country_code']].groupby(['city', 'country_code']).count().sort_values('restaurant_id', ascending=False).reset_index()
            top_7_cities = rating_by_city.sort_values('restaurant_id', ascending=False).head(7)
            fig = px.bar(top_7_cities, x = 'city', y= 'restaurant_id',
                        title= 'Top 7 Cities with more restaurants rating > 4',
                        text_auto=True,
                        color='country_code',
                        labels={'city': 'City', 'restaurant_id': 'Restaurants'})
            st.plotly_chart(fig, use_container_width=True)

        # Top 7 Cities with more restaurants rating < 2,5
        with col2:
            df1 = df[
                (df['aggregate_rating'] <= 2.5) 
                    ]
            rating_by_city = df1[['restaurant_id', 'city', 'country_code']].groupby(['city', 'country_code']).count().sort_values('restaurant_id', ascending=False).reset_index()
            top_7_cities = rating_by_city.sort_values('restaurant_id', ascending=False).head(7)
            fig = px.bar(top_7_cities, 
                         x = 'city', 
                         y= 'restaurant_id',
                        title= 'Top 7 Cities with more restaurants rating < 2,5',
                        text_auto=True,
                        color='country_code',
                        labels={'city': 'City', 'restaurant_id': 'Restaurants'}
                        )
            st.plotly_chart(fig, use_container_width=True)

    # Top 10 Cities with more different cuisines
    with st.container():
        cuisines_by_city = df[['city', 'cuisines', 'country_code']].groupby(['city', 'country_code']).nunique().sort_values('cuisines', ascending=False).reset_index()
        top_10_cuisines = cuisines_by_city.sort_values('cuisines', ascending=False).head(10)
        fig = px.bar(top_10_cuisines,
                    x='city',
                    y='cuisines',
                    title= 'Top 10 Cities with more different cuisines',
                    text_auto=True,
                    color='country_code',
                    labels={'city': 'City', 'cuisines': 'Cuisines'}
                    )
        st.plotly_chart(fig, use_container_width=True)

# call functions
    data = load_data('dataset\zomato.csv')
    data = rename_columns(data)
    data['country_code'] = data['country_code'].map(country_name)
    data["amount_usd"] = data.apply(lambda row: convert_to_usd(row["average_cost_for_two"], row["currency"]), axis=1)
    df = data_transform(data)

def main():
    #Load data
    data = load_data('zomato.csv')

    # Rename columns
    data = rename_columns(data)

    # Map country codes to names
    data['country_code'] = data['country_code'].map(country_name)

    # Convert avg cost to USD
    data["amount_usd"] = data.apply(lambda row: convert_to_usd(row["average_cost_for_two"], row["currency"]), axis=1)

    # Apply data cleaning and transformation
    df = data_transform(data)

    # Perform data viz
    data_viz(df)

# Run the main function
if __name__ == '__main__':
    main()
