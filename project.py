import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df = pd.read_csv("data.csv")

df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce')
df['reg_year'] = df['registration_date'].dt.year
df['reg_month'] = df['registration_date'].dt.month
df.drop(columns=['registration_date'], inplace=True)

df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['price_in_euro'] = pd.to_numeric(df['price_in_euro'], errors='coerce')
df['reg_month'] = pd.to_numeric(df['reg_month'], errors='coerce')

current_year = 2025
df['car_age'] = current_year - df['reg_year']

fig, axes = plt.subplots(3, 2, figsize=(15, 15))

# الصف الأول: 1- متوسط السعر حسب سنة التسجيل
avg_price_per_reg_year = df.groupby('reg_year')['price_in_euro'].mean().sort_index()
sns.lineplot(x=avg_price_per_reg_year.index, y=avg_price_per_reg_year.values, marker='o', ax=axes[0,0])
axes[0,0].set_title('Average Price by Registration Year')
axes[0,0].set_xlabel('Registration Year')
axes[0,0].set_ylabel('Average Price in Euro')
axes[0,0].tick_params(axis='x', rotation=45)

# الصف الأول: 2- عدد السيارات حسب سنة التسجيل (countplot)
sns.countplot(x='reg_year', data=df, order=sorted(df['reg_year'].dropna().unique()), ax=axes[0,1])
axes[0,1].set_title('Number of Listings by Registration Year')
axes[0,1].set_xlabel('Registration Year')
axes[0,1].tick_params(axis='x', rotation=45)

# باقي الصفوف تبقى زي السابق

brand_avg_price = df.groupby('brand')['price_in_euro'].mean().sort_values(ascending=False).head(10)
sns.barplot(x=brand_avg_price.index, y=brand_avg_price.values, ax=axes[1,0])
axes[1,0].set_title('Top 10 Brands by Average Price')
axes[1,0].tick_params(axis='x', rotation=45)

brand_counts = df['brand'].value_counts().head(5)
axes[1,1].pie(brand_counts, labels=brand_counts.index, autopct='%1.1f%%', startangle=140)
axes[1,1].set_title('Most Common Car Brands Distribution')
axes[1,1].axis('equal')

sns.countplot(x='reg_month', data=df, ax=axes[2,0])
axes[2,0].set_title('Listings by Registration Month')

sns.scatterplot(x='car_age', y='price_in_euro', data=df, alpha=0.3, ax=axes[2,1])
axes[2,1].set_title('Car Age vs Price')

plt.tight_layout()
st.pyplot(fig)
