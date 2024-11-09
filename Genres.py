import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the CSV file
#For each song change the csv name wich you have after running LinkesProfiles.py 
csv_file_path = 'influencer_profilessinf.csv'  # Update with your CSV file path
df = pd.read_csv(csv_file_path)

# Assuming the column containing URLs is named 'link'
results = []

# Iterate through each URL in the CSV
for url in df['link']:
    # Check if the URL is empty
    if pd.isna(url) or url.strip() == "":
        results.append({'url': "Empty URL", 'genres': "Empty link column"})
        continue  # Skip to the next iteration

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the section that contains the phrase
        phrase_div = soup.find(string="They want to receive...")

        if phrase_div:
            # Navigate up to the parent div
            parent_div = phrase_div.find_parent('div')

            # Find the 'ul' that contains the genres
            genres_ul = parent_div.find_next('ul')  # Look for the next <ul> after the parent div

            # Initialize a list to hold genres
            genres_list = []
            
            # Check if the <ul> is found
            if genres_ul:
                # Find all genre items
                genre_items = genres_ul.find_all('div', class_='name ellipsis')
                genres_list = [item.text.strip() for item in genre_items]

            # Store genres in results
            results.append({'url': url, 'genres': ', '.join(genres_list) if genres_list else "No genres found"})
        else:
            results.append({'url': url, 'genres': "Phrase not found"})
    else:
        results.append({'url': url, 'genres': f"Failed to retrieve page, status code: {response.status_code}"})

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a new CSV file
results_df.to_csv('resulttsInfinite.csv', index=False)

print("Processing complete. Results saved to 'resultsBefore.csv'.")
