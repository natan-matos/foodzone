import pandas as pd
import inflection
import plotly.express as px
import streamlit as st

from PIL import Image

# Load dataset
def load_data(path):
   data = pd.read_csv(path)
   return data

# Rename columns set underscore
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


# Data cleaning
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

def data_viz(df):
   # Set streamlit page
   st.set_page_config(layout='wide')

   # Sidebar configuration
   image = Image.open('logo.png')
   st.sidebar.image(image, width=150)
   st.sidebar.header('Food Zone')
   st.sidebar.subheader('Your food in your zone')
   st.sidebar.write("""___""")

   # Country filter
   st.sidebar.markdown('# Filters')
   country_filter = st.sidebar.multiselect(label='Choose the countries',
                        options=df['country_code'].unique(),
                        default=df['country_code'].unique())

   # Resturant number filter
   number_filter = st.sidebar.slider(label='Number of Restaurants', max_value=20, min_value=1,
                     value=10)

   # Cuisine type filter
   cuisine_filter = st.sidebar.multiselect(label='Cuisines', 
                        options=df['cuisines'].unique(),
                        default=df['cuisines'].unique())
   
   # Country Filter functionality 
   select_row = df['country_code'].isin(country_filter)
   df = df.loc[select_row, :]

   # Cuisine type filter functionality
   cuisine_row_filter = df['cuisines'].isin(cuisine_filter)
   df = df.loc[cuisine_row_filter, :]

   st.sidebar.write("""___""")


   # Home Page
   #restaurant_by_cuisine = df[['restaurant_id', 'cuisines']].groupby('cuisines').count().sort_values('restaurant_id', ascending=False).reset_index()
   st.title('🍽️ Cuisines Vison')

   # Metrics
   with st.container():
      
      st.header('Best Restaurant of the Biggest Cuisines')
      col1, col2, col3, col4, col5 = st.columns(5)

      with col1: #North indian
         df1 = df[df['cuisines'] == 'Indian']
         df2 = df1[['restaurant_name', 'aggregate_rating', 'country_code', 'amount_usd', 'city' ]].groupby('restaurant_name').max().sort_values('aggregate_rating', ascending=False).reset_index()
         help1 = (f'Place: {df2.iloc[0,4]}/  {df2.iloc[0,2]} \n\n Price for Two: U${df2.iloc[0,3]} \n\n ' )
         st.metric(value=df2.iloc[0,1], 
                  label=(f'Indian: {df2.iloc[0,0]}'),
                  help= help1)
         

      with col2: # American
         df1 = df[df['cuisines'] == 'American']
         df2 = df1[['restaurant_name', 'aggregate_rating', 'country_code', 'amount_usd', 'city']].groupby('restaurant_name').max().sort_values('aggregate_rating', ascending=False).reset_index()
         help1 = (f'Place: {df2.iloc[0,4]}/  {df2.iloc[0,2]} \n\n Price for Two: U${df2.iloc[0,3]} \n\n ' )
         st.metric(value=df2.iloc[0,1], 
                  label=(f'American: {df2.iloc[0,0]}'),
                  help = help1)
      
      with col3: # Cafe
         df1 = df[df['cuisines'] == 'Cafe']
         df2 = df1[['restaurant_name', 'aggregate_rating', 'country_code', 'amount_usd', 'city']].groupby('restaurant_name').max().sort_values('aggregate_rating', ascending=False).reset_index()
         help1 = (f'Place: {df2.iloc[0,4]}/  {df2.iloc[0,2]} \n\n Price for Two: U${df2.iloc[0,3]} \n\n ' )
         st.metric(value=df2.iloc[0,1], 
                  label=(f'Cafe: {df2.iloc[0,0]}'),
                  help= help1)

      with col4: # Italian
         df1 = df[df['cuisines'] == 'Italian']
         df2 = df1[['restaurant_name', 'aggregate_rating', 'country_code', 'amount_usd', 'city']].groupby('restaurant_name').max().sort_values('aggregate_rating', ascending=False).reset_index()
         help1 = (f'Place: {df2.iloc[0,4]}/  {df2.iloc[0,2]} \n\n Price for Two: U${df2.iloc[0,3]} \n\n ' )
         st.metric(value=df2.iloc[0,1], 
                  label=(f'Italian: {df2.iloc[0,0]}'),
                  help=help1)
      
      with col5: # Pizza
         df1 = df[df['cuisines'] == 'Pizza']
         df2 = df1[['restaurant_name', 'aggregate_rating', 'country_code', 'amount_usd', 'city']].groupby('restaurant_name').max().sort_values('aggregate_rating', ascending=False).reset_index()
         help1 = (f'Place: {df2.iloc[0,4]}/  {df2.iloc[0,2]} \n\n Price for Two: U${df2.iloc[0,3]} \n\n ' )
         st.metric(value=df2.iloc[0,1], 
                  label=(f'Pizza: {df2.iloc[0,0]}'),
                  help= help1)




   # Top N Restaurants table
   with st.container():
      st.title(f'Top {number_filter} Resturants')
      df1 = df.sort_values('aggregate_rating', ascending=False).head(number_filter).reset_index(drop=True)
      df2 = df1.loc[:, ['restaurant_id', 'restaurant_name', 'country_code', 
                        'city', 'cuisines', 'amount_usd', 'aggregate_rating', 'rating_text']]
      st.dataframe(df2, use_container_width=True)


   # Best and Worst rated cuisines
   with st.container():
      col1, col2 = st.columns(2)

      # Top N best rated cuisines
      with col1:
         dff = df[df['votes'] >= 100]
         df1 = dff[['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=False).reset_index()
         df2 = df1[df1['cuisines'] != 'Others']
         df3 = df2.iloc[:number_filter, :]
         fig = px.bar(
            df3, 
            x='cuisines', 
            y='aggregate_rating',
            title=(f' Top {number_filter} best rated cuisines'),
            text_auto=True
         )
         st.plotly_chart(fig, use_container_width=True)

      # Top N worst rated cuisines
      with col2:
         df1 = df[['cuisines', 'aggregate_rating']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=True).reset_index()
         df2 = df1[df1['aggregate_rating'] >= 1]
         df3 = df2.iloc[:number_filter, :]
         fig = px.bar(
            df3,
            x='cuisines',
            y='aggregate_rating',
            title=(f' Top {number_filter} worst rated cuisines'),
            text_auto=True
         )
         st.plotly_chart(fig, use_container_width=True)
     
         
def main():      
   # Load data
   data = load_data('zomato.csv')

   # Raname columns
   data = rename_columns(data)

   # Map country codes to name
   data['country_code'] = data['country_code'].map(country_name)

   # Convert avg cost to USD
   data["amount_usd"] = data.apply(lambda row: convert_to_usd(row["average_cost_for_two"], row["currency"]), axis=1)
   
   # Apply data cleaning
   df = data_transform(data)

   # Perform data viz
   data_viz(df)

# Run the main functon
if __name__ == '__main__':
   main()
