from time import sleep
import requests  # type: ignore
import pandas as pd  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # type: ignore
import os

# Suppress certificate verification warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

def soup2list(src, list_, attr=None):
    """Extracts text or attribute from BeautifulSoup elements and adds them to a list."""
    if attr:
        for val in src:
            list_.append(val.get(attr))
    else:
        for val in src:
            list_.append(val.get_text())

def fetch_reviews(company, from_page, to_page):
    """Main function to scrape reviews."""
    users = []
    userReviewNum = []
    ratings = []
    locations = []
    dates = []
    reviews = []

    for i in range(from_page, to_page + 1):
        try:
            url = f"https://www.trustpilot.com/review/{company}?page={i}"
            result = requests.get(url, verify=False)  # Disable certificate verification
            result.raise_for_status()  # Raise an error for unsuccessful responses
            soup = BeautifulSoup(result.content, 'html.parser')

            # Extract review data
            soup2list(soup.find_all('span', {'class', 'typography_heading-xxs__QKBS8 typography_appearance-default__AAY17'}), users)
            soup2list(soup.find_all('div', {'class', 'typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua'}), locations)
            soup2list(soup.find_all('span', {'class', 'typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l'}), userReviewNum)
            soup2list(soup.find_all('div', {'class', 'styles_reviewHeader__iU9Px'}), dates)
            soup2list(soup.find_all('div', {'class', 'styles_reviewHeader__iU9Px'}), ratings, attr='data-service-review-rating')
            soup2list(soup.find_all('div', {'class', 'styles_reviewContent__0Q2Tg'}), reviews)

            # Wait one second to avoid throttling
            sleep(1)

        except requests.RequestException as e:
            print(f"Error making request to page {i}: {e}")

    return users, userReviewNum, ratings, locations, dates, reviews

def main():
    # Get the absolute path of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Paths to the source files
    company_file_path = os.path.join(script_dir, '..', 'source', 'company.txt')
    num_pages_file_path = os.path.join(script_dir, '..', 'source', 'number_of_review_pages.txt')

    # Read company name from the file
    with open(company_file_path, 'r') as file:
        company = file.read().strip()  # Remove any leading/trailing whitespace

    # Read number of pages from the file
    with open(num_pages_file_path, 'r') as file:
        to_page = int(file.read().strip())  # Convert to integer

    from_page = 1  # We assume the scraping starts from the first page

    users, userReviewNum, ratings, locations, dates, reviews = fetch_reviews(company, from_page, to_page)

    # Validate the length of all lists
    list_lengths = [len(users), len(userReviewNum), len(ratings), len(locations), len(dates), len(reviews)]
    min_length = min(list_lengths)  # Find the minimum length among all lists

    # Ensure all lists have the same length
    users = users[:min_length]
    userReviewNum = userReviewNum[:min_length]
    ratings = ratings[:min_length]
    locations = locations[:min_length]
    dates = dates[:min_length]
    reviews = reviews[:min_length]

    # Create DataFrame
    review_data = pd.DataFrame({
        'Username': users,
        'Total reviews': userReviewNum,
        'Location': locations,
        'Date': dates,
        'Content': reviews,
        'Rating': ratings
    })

    # Get the absolute path of the 'data' folder
    data_folder = os.path.join(script_dir, '..', 'data')
    
    # Check if the 'data' folder exists, and if not, create it
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Save to the 'data' folder
    output_path = os.path.join(data_folder, 'reviews_raw.csv')
    review_data.to_csv(output_path, index=False)
    print(f'CSV saved as "{output_path}"')

if __name__ == "__main__":
    main()
