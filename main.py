from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
from data_process import *
from  config import *


def main():
    db = connect_to_mongodb(username_mongo, password_mongo, 'price_forecast')
    forecast_times = get_forecast_times(start_date, end_date)

    for asset in ['caiso_sp15', 'condor', 'saticoy', 'coso']:
        # Get Forecasted
        globals()[f"{asset}_forecast_da"] = get_forecast_price(db[asset], "da", forecast_times)
        globals()[f"{asset}_forecast_dart"] = get_forecast_price(db[asset], "dart", forecast_times)

        globals()[f"{asset}_forecast"] = globals()[f"{asset}_forecast_da"].merge(globals()[f"{asset}_forecast_dart"],
                                                                                 on=['forecast_time', 'trade_hour'],
                                                                                 how='outer')
        globals()[f"{asset}_forecast"]['hour_ending_time'] = globals()[f"{asset}_forecast"][
                                                                 'trade_hour'] + datetime.timedelta(hours=1)
        globals()[f"{asset}_forecast"]['HE'] = globals()[f"{asset}_forecast"]['hour_ending_time'].dt.hour
        globals()[f"{asset}_forecast"]['HE'] = globals()[f"{asset}_forecast"]['HE'].replace(0, 24)

        # Get Actual
        globals()[f"{asset}_actual"] = pd.DataFrame()

        for item in yes_energy_data[asset]:
            datatype = yes_energy_data[asset][item][0]
            object_id = yes_energy_data[asset][item][1]
            #print(datatype, object_id)

            url = f"{base_url}/{datatype}/{object_id}"

            response = requests.get(url, params=params, auth=HTTPBasicAuth(username_yes, password_yes))

            if response.status_code == 200 and "text/html" in response.headers.get("Content-Type", ""):
                tables = pd.read_html(response.text)
                tables[0] = tables[0].rename(columns={'AVGVALUE': item})
                globals()[f"{asset}_actual"][['DATETIME', 'HOURENDING']] = tables[0][['DATETIME', 'HOURENDING']]
                globals()[f"{asset}_actual"][item] = tables[0][item]
                #print(globals()[f"{asset}_actual"])

            globals()[f"{asset}_actual"]['DATETIME'] = pd.to_datetime(globals()[f"{asset}_actual"]['DATETIME'])
            globals()[f"{asset}_actual"]['hour_beginning_timestamp'] = globals()[f"{asset}_actual"][
                                                                           'DATETIME'] - datetime.timedelta(hours=1)

            globals()[f"{asset}"] = globals()[f"{asset}_actual"].merge(
                globals()[f"{asset}_forecast"][['da forecast', 'dart forecast', 'trade_hour', 'HE']],
                left_on=['hour_beginning_timestamp', 'HOURENDING'], right_on=['trade_hour', 'HE'], how='outer')

        globals()[f"{asset}"].to_excel(f'data/{asset}.xlsx', index = False)

if __name__ == "__main__":
    main()