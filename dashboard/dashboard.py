# Importing library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Importing dataset
day_df = pd.read_csv('https://raw.githubusercontent.com/kkamall/Dicoding-ProyekAkhirAnalisisData/main/dashboard/main_data.csv')

# Change date range data type from object to date
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mendapatkan nilai min dan max date untuk filter
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

# Membuat sidebar
with st.sidebar:
    # Menambahkan logo
    st.image('https://github.com/kkamall/Dicoding-ProyekAkhirAnalisisData/blob/main/dashboard/logo.png')

    # Membuat filter date berdasarkan field order date
    start_date, end_date = st.date_input(
        label = 'Rentang Waktu',
        min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

# Dataset hasil filter date
main_df = day_df[(day_df['dteday'] >= str(start_date)) & (day_df['dteday'] <= str(end_date))]

# Membuat header
st.header('Bike Sharing Rental Dashboard')

# Membuat scorecard overall
col1, col2, col3 = st.columns(3)

with col1:
    total_rental = main_df.cnt.sum()
    st.metric("Total Rental Overall", value="{:,}".format(total_rental))

with col2:
    total_rental_registered = main_df.registered.sum()
    st.metric("Total Rental by Registered User", value="{:,}".format(total_rental_registered))

with col3:
    total_rental_casual = main_df.casual.sum()
    st.metric("Total Rental by Casual User", value="{:,}".format(total_rental_casual))

# [ Trend of rental bike in 2012 ]
st.subheader('Trend of Rental Bike Over Month in 2012')

# Menyiapkan dataset (rental sepeda per-bulan tahun 2012)
monthly_rental_bike = main_df[(main_df['yr'] == 1)].resample(rule='M', on='dteday').agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum'
})
monthly_rental_bike.index = monthly_rental_bike.index.strftime('%B')
monthly_rental_bike = monthly_rental_bike.reset_index()
monthly_rental_bike.rename(columns={
    'casual': 'Total Rental Bike by Casual User',
    'registered': 'Total Rental Bike by Registered User',
    'cnt': 'Total Rental Bike',
    'dteday': 'month'
}, inplace=True)

# Visualisasi data
fig = plt.figure(figsize=(15,5))
plt.plot(monthly_rental_bike['month'], monthly_rental_bike['Total Rental Bike'], marker='o', linewidth=2, color="#72BCD4")
plt.title("Numbers of Rental Bike per Month in 2012", loc='center', fontsize=20)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
st.pyplot(fig)

# [ Total of Rental Bike Based on Season ]
st.subheader('Total of Rental Bike based on Season')

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Menyiapkan dataset (total rental sepeda berdasarkan season)
by_season_df = main_df.groupby('season_name').cnt.sum().reset_index()
by_season_df.rename(columns={
    'cnt': 'Total Rental'
}, inplace=True)

# Visualisasi Data
fig, ax = plt.subplots(figsize=(15,8))
sns.barplot(x='season_name', y='Total Rental', data=by_season_df.sort_values(by='Total Rental', ascending=False), ax=ax, palette=colors, errorbar=None)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.set_title('Numbers of Rental Bike based on Season', loc='center', fontsize=20)
st.pyplot(fig)

# [ Total of Rental Bike based on Temperature ]
st.subheader('Total of Rental Bike based on Temperature')

colors = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3"]

# Menyiapkan dataset (total rental sepeda berdasarkan temperatur)
by_temp_df = main_df.groupby('temp_group').cnt.sum().reset_index()
by_temp_df.rename(columns={
    'cnt': 'Total Rental'
}, inplace=True)
by_temp_df['temp_group'] = pd.Categorical(by_temp_df['temp_group'], ["Very Cold", "Cold", "Normal", "Warm", "Very Hot"])

# Visualisasi data
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x='temp_group', y='Total Rental', data=by_temp_df.sort_values(by='temp_group', ascending=True), ax=ax, palette=colors)
ax.set_xlabel(None)
ax.set_ylabel(None)
ax.set_title('Numbers of Rental Bike based on Temperature', loc='center', fontsize=20)
st.pyplot(fig)

st.caption('Copyright © Kkamall 2023')
