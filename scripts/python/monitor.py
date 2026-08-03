import requests
import json
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

target_service = [
    {"name": "Nginx Web", "url": "https://httpstat.us/200"},
    {"name": "NodeJS API", "url": "https://httpstat.us/502"},
    {"name": "Payment Gateway", "url": "https://domain-ini-pasti-error-123.com"},
]


def check_services(service):
    result = []
    logging.info("Memulai pengecekan kesehatan server...")
    for target in service:
        try:
            response = requests.get(target["url"])
            if response.status_code == 200:
                write = {"name": target["name"], "status": "UP"}
            else:
                write = {"name": target["name"], "status": "DOWN"}
                logging.warning(
                    f"Perlu tindak lebih lanjut pada server {target['name']}"
                )
        except requests.exceptions.RequestException as e:
            write = {"name": target["name"], "status": "ERROR", "detail": str(e)}
            logging.error(f"Server {target['name']} tidak merespon")

        result.append(write)

    with open("healt_report.json", "w") as file:
        json.dump(result, file, indent=4)


check_services(target_service)
