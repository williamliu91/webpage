import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

# Streamlit App Title
st.title("Google Sheets Web Scraper & Stock Chart")

# Instructions
st.write("Enter the URL of your publicly accessible Google Sheet to fetch columns A to F.")

# Input for Google Sheet URL
sheet_url = st.text_input("Enter Google Sheet URL", "")

# Button to fetch data
if st.button("Fetch Data"):
    if not sheet_url:
        st.error("Please enter a valid Google Sheet URL.")
    else:
        try:
            # Send a GET request to the URL
            response = requests.get(sheet_url)

            # Check if the request was successful
            if response.status_code != 200:
                st.error("Failed to fetch the Google Sheet. Please check the URL and try again.")
            else:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, "html.parser")

                # Extract table data
                table = soup.find("table")
                if table:
                    rows = table.find_all("tr")  # Get all rows
                    data = []

                    # Extract stock name from Cell A1 (first cell of the first row)
                    stock_name = "Unknown Stock"
                    if rows:
                        stock_name_row = rows[1]  # Row 1 is the first row (index 0)
                        stock_name_cell = stock_name_row.find("td")  # Get the first cell in Row 1 (Cell A1)
                        if stock_name_cell:
                            stock_name = stock_name_cell.text.strip()
                    st.write(f"Stock Name: {stock_name}")

                    # Extract headers from the second row (Row 2)
                    if len(rows) > 1:
                        header_row = rows[2]  # Row 2 is the second row (index 1)
                        headers = [header.text.strip() for header in header_row.find_all("td")[:6]]

                        if not headers or len(set(headers)) != len(headers):
                            headers = [f"Column {i+1}" for i in range(6)]
                            st.warning("Invalid headers found. Using default column names.")

                        # Start processing from Row 3 (index 2) to skip the stock name and header rows
                        for row in rows[2:]:
                            cells = row.find_all("td")[:6]
                            if cells:
                                data.append([cell.text.strip() for cell in cells])

                        if data:
                            # Convert to DataFrame
                            df = pd.DataFrame(data, columns=headers)

                            # Convert first column to datetime format
                            if "Date" in df.columns:
                                df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
                                df = df.dropna().sort_values(by="Date", ascending=True)

                            # Convert relevant columns to numeric
                            if "Close" in df.columns:
                                df["Close"] = pd.to_numeric(df["Close"], errors='coerce')
                                df = df.dropna()

                            # Display the last 5 rows
                            st.table(df.tail(5))

                            # Create a stock price chart
                            fig = px.line(df, x="Date", y="Close", title=f"{stock_name} Closing Price Trend")
                            st.plotly_chart(fig)
                        else:
                            st.warning("No data found in the table.")
                    else:
                        st.warning("No rows found in the table.")
                else:
                    st.warning("No table found on the page. Google Sheets may not be scrapable due to dynamic content loading.")
        except Exception as e:
            st.error(f"An error occurred: {e}")