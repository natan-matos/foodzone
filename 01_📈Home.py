import pandas as pd
import inflection
import folium
from folium.plugins import MarkerCluster
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static

# Load dataset
def load_data(path):
    data = pd.read_csv(path)
    return data

# Rename columns with underscore
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
    148: "New Zealand",
    162: "Philippines",
    166: "Qatar",
    184: "Singapore",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES.get(country_id, "")

# Convert values to USD
EXCHANGE_RATES = {
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
    'Dollar($)': 1.0
}

def convert_to_usd(amount, currency):
    exchange_rate = EXCHANGE_RATES.get(currency)
    if exchange_rate is not None:
        return amount * exchange_rate
    else:
        return None

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

# Data cleaning and transformation
def data_transform(df):
    # Drop rows with null values
    df = df.dropna()

    # Drop duplicate values
    df = df.drop_duplicates().reset_index(drop=True)

    # Simplify the cuisines column
    df["cuisines"] = df["cuisines"].str.split(",").str[0]

    # Drop outliers
    df = df[df['amount_usd'] != 25000017.0]

    return df

# Data visualization
def data_viz(df):
    # Set Streamlit page
    st.set_page_config(layout='wide')

    image = Image.open('logo.png')
    st.sidebar.image(image, width=150)
    st.sidebar.header('Food Zone')
    st.sidebar.subheader('Your food in your zone')
    st.sidebar.write("""___""")

    # Filters
    st.sidebar.markdown('# Filters')
    country_filter = st.sidebar.multiselect(
        label='Choose the countries',
        options=df['country_code'].unique(),
        default=df['country_code'].unique()
    )

    # Filter functionality
    df_filtered = df[df['country_code'].isin(country_filter)]

    st.title('Food Zone')
    st.markdown('#### Your food, in your Zone')
    st.markdown('### We have the following metrics in our company')

    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(value=df_filtered.shape[0], label='Restaurants')
        with col2:
            st.metric(value=df_filtered['country_code'].nunique(), label='Countries')
        with col3:
            st.metric(value=df_filtered['city'].nunique(), label='Cities')
        with col4:
            st.metric(value=df_filtered['votes'].sum(), label='Total Votes')
        with col5:
            st.metric(value=df_filtered['cuisines'].nunique(), label='Cuisines')

    with st.container():
        map = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=2)
        make_cluster = MarkerCluster().add_to(map)
        for _, row in df_filtered.iterrows():
            popup = folium.Popup('Price: ${0}, {1}'.format(row['amount_usd'], row['rating_text']))
            folium.Marker(location=[row['latitude'], row['longitude']], popup=popup,
                          icon=folium.Icon(icon='home', color=row['color_name'])).add_to(make_cluster)

        folium_static(map, width=1024, height=600)

# Main function
def main():
    # Load data
    data = load_data('dataset/zomato.csv')

    # Rename columns
    data = rename_columns(data)

    # Map country codes to names
    data['country_code'] = data['country_code'].map(country_name)

    # Convert average cost to USD
    data["amount_usd"] = data.apply(lambda row: convert_to_usd(row["average_cost_for_two"], row["currency"]), axis=1)

    # Map the colors name
    data['color_name'] = data['rating_color'].map(color_name)

    # Apply data cleaning and transformation
    df = data_transform(data)

    # Perform data visualization
    data_viz(df)

# Run the main function
if __name__ == '__main__':
    main()
