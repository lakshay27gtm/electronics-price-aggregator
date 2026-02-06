# Electronics Price Aggregator

A Skyscanner-style web application that aggregates and compares electronics product prices across multiple retailers such as Amazon, Flipkart, Croma, and Reliance Digital.

## Project Overview
The application standardizes product data from different e-commerce platforms and displays the lowest available price for each product to help users make informed purchasing decisions.

## Features
- Multi-retailer price comparison
- Category and brand-based filtering
- Product search functionality
- Lowest-price identification
- Interactive web interface using Streamlit

## Tech Stack
- Python
- Pandas
- NumPy
- Streamlit

## Project Structure
electronics-price-aggregator/
│
├── app.py
├── requirements.txt
├── README.md
│
├── amazon1.csv
├── amazon2.csv
├── croma.csv
├── flipkart_mobile_data.csv
├── flipkart_laptops.csv
├── flipkart_earphones.csv
├── Reliance Digital India Product Dataset.csv

## How to Run Locally
pip install -r requirements.txt
streamlit run app.py

## Deployment
The application can be deployed using Streamlit Cloud by connecting the GitHub repository and selecting app.py as the main file.

## Use Case
This project demonstrates data aggregation, cleaning, and comparison techniques commonly used in travel and e-commerce price comparison platforms such as Skyscanner.

## Future Enhancements
- Real-time price scraping
- Price trend analysis
- Click-through buy links
- User login and wishlist functionality
