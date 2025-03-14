import datetime

start_date = datetime.datetime(2024, 1, 1, 0, 0)
end_date = datetime.datetime(2024, 1, 20, 0, 0)


# MongoDB
username_mongo = ''
password_mongo = ''

# Yes Energy
username_yes = ''
password_yes = ''
base_url = "https://services.yesenergy.com/PS/rest/timeseries"

params = {
    "startdate": start_date,
    "enddate": end_date,
    "agglevel": "hour"
}

price_nodes = {
    "CAISO_SP15": "20000004682",
    "CONDOR": "20000003090",
    "COSO": "20000002303",
    "SATICOY": "10016484939",
}

yes_energy_data = {}

for region, node in price_nodes.items():
    yes_energy_data[region.lower()] = {
        f"DALMP_{region}": ("DALMP", node),
        f"FMM_{region}": ("LMP_15MIN", node),
    }
