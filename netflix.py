

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Path to your dataset (update path if needed)
DATA_PATH = Path("Netflix Dataset_1.csv")

# Read dataset
df = pd.read_csv(DATA_PATH)
df.columns = [c.strip() for c in df.columns]  # clean column names

# Map actual column names from your CSV
col_map = {c.lower(): c for c in df.columns}
type_col = col_map.get('type')        # 'Type' column
country_col = col_map.get('country')  # 'Country' column
genre_col = col_map.get('category') or col_map.get('listed_in') or col_map.get('genres')
release_col = col_map.get('release_date') or col_map.get('release_year') or col_map.get('date_added')

# Extract release year if available
if release_col:
    df['release_year_extracted'] = pd.to_datetime(df[release_col], errors='coerce').dt.year

# ----- Analysis -----
if type_col:
    print("\nMovies vs TV Shows:")
    print(df[type_col].value_counts())

if genre_col:
    genres = df[genre_col].dropna().str.split(',').explode().str.strip()
    print("\nTop Genres:")
    print(genres.value_counts().head(10))

if country_col:
    countries = df[country_col].dropna().str.split(',').explode().str.strip()
    print("\nTop Countries:")
    print(countries.value_counts().head(10))

if 'release_year_extracted' in df.columns:
    print("\nYear Range:", df['release_year_extracted'].min(), "-", df['release_year_extracted'].max())

# ----- Charts -----
charts_dir = Path("charts")
charts_dir.mkdir(exist_ok=True)

# Movies vs TV Shows
if type_col:
    df[type_col].value_counts().plot(kind='bar')
    plt.title("Movies vs TV Shows - Distribution")
    plt.xlabel("Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(charts_dir / "type_distribution.png")
    plt.clf()

# Top Genres
if genre_col:
    genres.value_counts().head(10).plot(kind='bar')
    plt.title("Top Genres")
    plt.xlabel("Genre")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(charts_dir / "top_genres.png")
    plt.clf()

# Top Countries
if country_col:
    countries.value_counts().head(10).plot(kind='bar')
    plt.title("Top 10 Countries by Content Count")
    plt.xlabel("Country")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(charts_dir / "top_countries.png")
    plt.clf()

# Yearly Trend
if 'release_year_extracted' in df.columns:
    yearly = df.groupby('release_year_extracted').size()
    yearly.plot(kind='line', marker='o')
    plt.title("Content Released per Year")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(charts_dir / "yearly_trend.png")
    plt.clf()

print("\nAnalysis complete. Charts saved in 'charts/' folder.")
