import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('main_data.csv')

# Set the title and logo
st.title("🏍️ Dashboard Penyewaan Sepeda")
st.image("logo.png", width=120)  
# Sidebar for filtering options
st.sidebar.header("🔍 Pilihan Filter")
season = st.sidebar.selectbox("Pilih Musim:", df['season'].unique())
working_day = st.sidebar.selectbox("Pilih Hari Kerja:", df['workingday'].unique())
hour = st.sidebar.slider("Pilih Jam:", min_value=0, max_value=23, value=12)

# Filter data based on selections
filtered_data = df[(df['season'] == season) & (df['workingday'] == working_day)]

# Display filtered data
st.write("### 📊 Data Penyewaan Sepeda Berdasarkan Musim, Hari Kerja, dan Jam:")
st.dataframe(filtered_data)

# Plot average rentals by season and working day
st.subheader("📈 Rata-rata Penyewaan Sepeda Berdasarkan Musim dan Hari Kerja")
season_workingday_rentals = df.groupby(['season', 'workingday'])['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='season', y='cnt', hue='workingday', data=season_workingday_rentals, ax=ax, palette='Set2')
plt.title('Rata-rata Penyewaan per Musim dan Hari Kerja', fontsize=16, fontweight='bold')
plt.xlabel('Musim', fontsize=14)
plt.ylabel('Rata-rata Jumlah Penyewaan', fontsize=14)
plt.xticks(rotation=45)
plt.legend(title='Hari Kerja', title_fontsize='13', fontsize='11')
st.pyplot(fig)

# Plot hourly rentals for the selected hour
st.subheader(f"⏰ Penyewaan Sepeda pada Jam {hour}")
hourly_rentals = df[df['hr'] == hour].groupby(['hr'])['cnt'].sum().reset_index()  # Hitung total penyewaan pada jam yang dipilih
if not hourly_rentals.empty:  # Cek apakah ada data
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(x='hr', y='cnt', data=hourly_rentals, ax=ax2, palette='pastel')
    plt.title(f'Penyewaan Sepeda pada Jam {hour}', fontsize=16, fontweight='bold')
    plt.xlabel('Jam', fontsize=14)
    plt.ylabel('Jumlah Penyewaan', fontsize=14)
    plt.xticks(rotation=45)
    st.pyplot(fig2)
else:
    st.write("🚫 Tidak ada data untuk jam ini.")

# Show peak hours based on weather
st.subheader("🌤️ Penyewaan Sepeda Berdasarkan Jam dan Situasi Cuaca")
hour_weather_rentals = df.groupby(['hr', 'weathersit'])['cnt'].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.lineplot(x='hr', y='cnt', hue='weathersit', data=hour_weather_rentals, ax=ax3, palette='Set1', marker='o')
plt.title('Penyewaan Sepeda Berdasarkan Jam dan Situasi Cuaca', fontsize=16, fontweight='bold')
plt.xlabel('Jam', fontsize=14)
plt.ylabel('Jumlah Penyewaan', fontsize=14)
plt.legend(title='Situasi Cuaca', title_fontsize='13', fontsize='11')
st.pyplot(fig3)

# Additional interactive visualization: Heatmap of Rentals by Hour and Day
st.subheader("🌡️ Heatmap Penyewaan Sepeda per Jam dan Hari")
pivot_table = df.pivot_table(values='cnt', index='hr', columns='workingday', aggfunc='mean')
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt=".0f", ax=ax4, linewidths=.5)
plt.title('Heatmap Penyewaan Sepeda per Jam dan Hari Kerja', fontsize=16, fontweight='bold')
plt.xlabel('Hari Kerja', fontsize=14)
plt.ylabel('Jam', fontsize=14)
st.pyplot(fig4)

# Conclusion section
st.header("📝 Kesimpulan")
st.write("""
1. **Musim yang Meningkatkan Penyewaan**: Analisis menunjukkan bahwa musim tertentu memiliki rata-rata penyewaan yang lebih tinggi. 
2. **Hari Kerja dan Penyewaan**: Penyewaan sepeda cenderung lebih tinggi pada hari kerja dibandingkan akhir pekan.
3. **Waktu Puncak**: Data menunjukkan adanya waktu puncak tertentu dalam penyewaan, yang dapat diidentifikasi dari grafik per jam.
4. **Pengaruh Cuaca**: Situasi cuaca juga mempengaruhi jumlah penyewaan, dengan hari cerah menunjukkan angka penyewaan yang lebih tinggi.
5. **Pola Penyewaan per Jam dan Hari Kerja**: Heatmap menunjukkan pola penyewaan sepeda berdasarkan jam dan jenis hari kerja, membantu dalam perencanaan lebih lanjut.
""")

# Footer with additional information
st.write("### 🙏 Terima kasih telah mengunjungi dashboard ini!")
