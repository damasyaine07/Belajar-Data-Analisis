import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load datasets
bike_day_ds = pd.read_csv("bike_sharing_day_Result.csv")
bike_hour_ds = pd.read_csv("bike_sharing_hour_Result.csv")

# Merge datasets
bike_rental  = pd.merge(
    left=bike_day_ds,
    right=bike_hour_ds,
    how="left",
    left_on=["dteday","season","yr","mnth","workingday","holiday"],
    right_on=["dteday","season","yr","mnth","workingday","holiday"]
)

# Rename columns
bike_rental.rename(columns={
    "instant_x": "instant_day",
    "instant_y": "instant_hour",
    "weekday_x": "weekday_day",
    "weekday_y": "weekday_hour",
    "workingday_x": "workingday_day",
    "workingday_y": "workingday_hour",
    "temp_x": "temp_day",
    "temp_y": "temp_hour",
    "atemp_x": "atemp_day",
    "atemp_y": "atemp_hour",
    "hum_x": "hum_day",
    "hum_y": "hum_hour",
    "windspeed_x": "windspeed_day",
    "windspeed_y": "windspeed_hour",
    "casual_x": "casual_day",
    "casual_y": "casual_hour",
    "registered_x": "registered_day",
    "registered_y": "registered_hour",
    "dteday": "date",
    "cnt_x": "cnt_day",
    "cnt_y": "cnt_hour",
    "yr": "year",
    "mnth": "month",
    "hr": "hour"
}, inplace=True)

# New calculated columns
bike_rental['total_rentals'] = bike_rental['cnt_day'] + bike_rental['cnt_hour']
bike_rental['total_casual'] = bike_rental['casual_day'] + bike_rental['casual_hour']
bike_rental['total_registered'] = bike_rental['registered_day'] + bike_rental['registered_hour']
bike_rental['total_weekday'] = bike_rental['weekday_day'] + bike_rental['weekday_hour']
bike_rental['windspeed'] = (bike_rental['windspeed_day'] + bike_rental['windspeed_hour']) / 2
bike_rental['hum'] = (bike_rental['hum_day'] + bike_rental['hum_hour']) / 2
bike_rental['temp'] = (bike_rental['temp_day'] + bike_rental['temp_hour']) / 2

# Convert date column to datetime
bike_rental['date'] = pd.to_datetime(bike_rental['date'], errors='coerce').dt.date

min_date = bike_rental["date"].min()
max_date = bike_rental["date"].max()

# Streamlit Sidebar Inputs
with st.sidebar:
    st.image("D:/Damasya/Data Analyst/dashboard/gatto.jpg")
    
    # Date range input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, 
        max_value=max_date, value=[min_date, max_date]
    )

    # Filter data based on selected date range
    date_main = bike_rental[(bike_rental["date"] >= start_date) & (bike_rental['date'] <= end_date)]

st.header('Bike sharing dataset 🚲')
st.subheader('Dmasya Ine - pandamasya21')
st.write(bike_rental)
st.write(date_main)

date_main_grouped = date_main.groupby('date')['total_rentals'].sum().reset_index()

# Pertanyaan Pertama : Bagaimana pengaruh musim terhadap jumlah pemakaian sepeda?
st.write("Pertanyaan Pertama : Bagaimana pengaruh musim terhadap jumlah pemakaian sepeda?")
season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
bike_rental['season'] = bike_rental['season'].replace(season_mapping)

plt.figure(figsize=(12, 6))
date_main_grouped = bike_rental.groupby('season')['total_rentals'].sum().reset_index()
plt.bar(date_main_grouped['season'], date_main_grouped['total_rentals'], label='Total Rentals')

plt.xlabel('Season')
plt.ylabel('Total Rentals')
plt.title('Total Rentals by Season')
plt.legend()
plt.show()
st.pyplot(plt)




# Pertanyaan ke-2: Apakah lebih banyak pengguna sepeda pada hari kerja atau hari libur?
st.write("Pertanyaan ke-2: Apakah lebih banyak pengguna sepeda pada hari kerja atau hari libur?")
plt.figure(figsize=(10, 6))
sns.boxplot(x='workingday', y='total_rentals', data=date_main)
plt.title('Jumlah Pengguna Sepeda pada Hari Kerja vs Hari Libur')
plt.xlabel('Hari Kerja (1 = Yes, 0 = No)')
plt.ylabel('Jumlah Pengguna')
st.pyplot(plt)



# Pertanyaan ke-3: Bagaimana kondisi cuaca memengaruhi penggunaan sepeda?
st.write("Pertanyaan ke-3: Bagaimana kondisi cuaca memengaruhi penggunaan sepeda?")
plt.figure(figsize=(10,6))
sns.boxplot(x='weathersit_x', y='total_rentals', data=date_main)
plt.title('Pengguna Sepeda Berdasarkan Kategori Cuaca')
plt.xlabel('Weathersit (1 = Cerah, 2 = Mendung, 3 = Hujan)')
plt.ylabel('Jumlah Pengguna')
st.pyplot(plt)



# Pertanyaan ke-4: Apakah ada korelasi antara suhu dan jumlah pengguna sepeda?
st.write("Pertanyaan ke-4: Apakah ada korelasi antara suhu dan jumlah pengguna sepeda?")
plt.figure(figsize=(10,6))
plt.figure(figsize=(10,6))
sns.scatterplot(x='temp_day', y='total_rentals', data=date_main)
plt.title('Hubungan Suhu dengan Jumlah Pengguna')
plt.xlabel('Temperature')
plt.ylabel('Jumlah Pengguna')
st.pyplot(plt)


# Pertanyaan ke-5: Bagaimana distribusi pengguna casual dan registered pada data?
st.write("Pertanyaan ke-5: Bagaimana distribusi pengguna casual dan registered pada data?")
plt.figure(figsize=(10, 6))
sns.histplot(date_main['total_casual'], color='blue', kde=True, label='Casual')
sns.histplot(date_main['total_registered'], color='red', kde=True, label='Registered')
plt.title('Distribution of Casual vs Registered Users')
plt.xlabel('Number of Users')
plt.ylabel('Frequency')
plt.legend()
st.pyplot(plt)



# Pertanyaan ke-6: Bagaimana distribusi penggunaan sepeda pada jam kerja dan akhir pekan?
st.write("Pertanyaan ke-6: Bagaimana distribusi penggunaan sepeda pada jam kerja dan akhir pekan?")
plt.figure(figsize=(10, 6))
sns.boxplot(x='workingday', y='total_rentals', data=date_main)
plt.title('Distribusi Penggunaan Sepeda pada Jam Kerja vs Akhir Pekan')
plt.xlabel('Hari Kerja (0 = Akhir Pekan, 1 = Hari Kerja)')
plt.ylabel('Total Pengguna Sepeda')
st.pyplot(plt)



# Pertanyaan ke-7: Kapan jam sibuk penggunaan sepeda selama sehari?
st.write("Pertanyaan ke-7: Kapan jam sibuk penggunaan sepeda selama sehari?")
plt.figure(figsize=(10, 6))
sns.lineplot(x='hour', y='total_rentals', data=date_main, hue='total_weekday', palette='Set2')
plt.title('Jam Sibuk Penggunaan Sepeda (dibagi hari kerja dan akhir pekan)')
plt.xlabel('Jam')
plt.ylabel('Total Pengguna Sepeda')
st.pyplot(plt)