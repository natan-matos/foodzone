import pandas as pd
import inflection
import plotly.express as px
import streamlit as st

from PIL import Image

# Load dataset
def load_data(path):
   data = pd.read_csv(path)
   return data


# Rname columns set underscore
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

# Country names function
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

# Convert values to us dollar
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

# Data cleaning and transformation
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
    # Set streamlit page
    st.set_page_config(layout='wide')

    # Sidebar title
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
    st.title('🌎Country Vision')

    # Restaurants by country bar chart
    with st.container():

        
        restaurant_by_country = df[['restaurant_id', 'country_code']].groupby('country_code').nunique().sort_values('restaurant_id', ascending=False).reset_index()
        fig = px.bar(restaurant_by_country, 
                    x='country_code',
                    y='restaurant_id',
                    text_auto=True,
                    labels={'country_code': 'Country', 'restaurant_id': 'Nº Restaurants'},
                    title='Restaurants per Country'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Cities by country bar chart
    with st.container():
        country_by_city = df[['country_code', 'city']].groupby('country_code').nunique().sort_values('city', ascending=False).reset_index()
        fig = px.bar(country_by_city,
                    x='country_code',
                    y='city', text_auto=True, 
                    labels={'city': 'Cities', 'country_code': 'Country'},
                    title='Cities per Country'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Avg votes and price charts
    with st.container():
        col1, col2 = st.columns(2)

        # AVG votes by restaurant in each country'
        with col1:
            votes_by_country = df[['country_code', 'votes']].groupby('country_code').mean().sort_values('votes', ascending=False).reset_index()
            fig = px.bar(votes_by_country,
                        x='country_code',
                        y='votes', text_auto=True,
                        title='AVG votes by restaurant in each country',
                        labels={'country_code': 'Country', 'votes': 'Votes'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # AVG price for two by country
        with col2:
            votes_by_country = df[['country_code', 'amount_usd']].groupby('country_code').mean().sort_values('amount_usd', ascending=False).reset_index()
            fig = px.bar(votes_by_country, 
                        x='country_code',
                        y='amount_usd',
                        text_auto=True,
                        title='AVG price for two by country',
                        labels={'country_code': 'Country', 'amount_usd': 'Price'}
            )
            st.plotly_chart(fig, use_container_width=True)


# Main function
def main():
    # Load data
    data = load_data('zomato.csv')

    # Rename columns
    data = rename_columns(data)

    # Map country code to names
    data['country_code'] = data['country_code'].map(country_name)

    # Convert average cost to USD
    data["amount_usd"] = data.apply(lambda row: convert_to_usd(row["average_cost_for_two"], row["currency"]), axis=1)
    
    # Apply data cleaning and transformation
    df = data_transform(data)

    # Perform data visualization
    data_viz(df)

# Run the main function
if __name__ == '__main__':
    main()
