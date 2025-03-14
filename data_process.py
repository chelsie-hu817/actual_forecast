from pymongo import MongoClient
import pandas as pd
import datetime


def connect_to_mongodb(db_username, db_password, database='price_forecast'):
    # Create a connection string
    connection_string = f"mongodb+srv://{db_username}:{db_password}@analyticsdata.oxjln.mongodb.net"

    # Connect to MongoDB
    client = MongoClient(connection_string)

    # Return the database object
    db = client[database]
    return db

# ------------------- Get Forecasted Data from MongoDB

def get_forecast_times(start_date, end_date):
    start_date = (start_date - datetime.timedelta(days = 1)).replace(hour = 9, minute = 0, second = 0)  # Set time to 9 AM
    end_date = (end_date - datetime.timedelta(days = 1)).replace(hour = 9, minute = 0, second =0)  # Set time to 9 AM

    forecast_times = []
    current_time = start_date

    while current_time <= end_date:
        forecast_times.append(current_time)
        current_time += datetime.timedelta(days=1)  # Move to next day at 9 AM

    return forecast_times

def get_forecast_price(collection, forecast_type, forecast_times):
    results_list = []  # Store results

    # Precompute trade hour ranges for all forecast_times
    queries = []
    for forecast_time in forecast_times:
        trade_hour_start = (forecast_time + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0)
        trade_hour_end = trade_hour_start + datetime.timedelta(hours=24)  # Full 24-hour period

        queries.append({
            "_id.forecast_time": forecast_time,
            "_id.trade_hour": {"$gte": trade_hour_start, "$lt": trade_hour_end},
            "_id.forecast_type": forecast_type
        })

    # Execute all queries in batch (avoiding loop-over-fetch)
    query_results = collection.find({"$or": queries})  # Batch query execution

    # Process results using list comprehension
    results_list = [
        {
            "forecast_time": entry["_id"]["forecast_time"],
            "trade_hour": entry["_id"]["trade_hour"],
            f"{forecast_type} forecast": entry.get("value", None)  # Handle missing values safely
        }
        for entry in query_results if "_id" in entry and "trade_hour" in entry["_id"]
    ]

    # Convert to DataFrame
    df = pd.DataFrame(results_list)
    return df
