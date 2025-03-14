import datetime

start_date = datetime.datetime(2024, 1, 1, 0, 0)
end_date = datetime.datetime(2024, 1, 20, 0, 0)


# MongoDB
username_mongo = 'chelsie_hu'
password_mongo = 'q3AFVXhvENGbVHw4'

# Yes Energy
username_yes = 'lzhao@arevonenergy.com1'
password_yes = 'eiB!8AJm5eN7LYw'
base_url = "https://services.yesenergy.com/PS/rest/timeseries"

params = {
    "startdate": start_date,
    "enddate": end_date,
    "agglevel": "hour"
}

price_nodes = {
    "CAISO_SP15": "20000004682",
    "CONDOR": "20000003090",
    "COSO": "20000003203",
    "SATICOY": "10016484939",
}

yes_energy_data = {}

for region, node in price_nodes.items():
    yes_energy_data[region.lower()] = {
        f"DALMP_{region}": ("DALMP", node),
        f"FMM_{region}": ("LMP_15MIN", node),
    }