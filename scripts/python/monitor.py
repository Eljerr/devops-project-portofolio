import json
import logging
import argparse
import asyncio
import aiohttp


parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
args = parser.parse_args()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

target_service = [
    {"name": "Nginx Web", "url": "https://httpstat.us/200"},
    {"name": "NodeJS API", "url": "https://httpstat.us/502"},
    {"name": "Payment Gateway", "url": "https://domain-ini-pasti-error-123.com"},
]


async def fetch_status(session, target):
    try:
        async with session.get(target["url"]) as response:
            if response.status == 200:
                return {"name": target["name"], "status": "UP"}
            else:
                logging.warning(
                    f"Perlu tindak lebih lanjut pada server {target['name']}"
                )
                return {"name": target["name"], "status": "DOWN"}
    except aiohttp.ClientError as e:
        logging.error(f"Server {target['name']} tidak merespon")
        return {"name": target["name"], "status": "ERROR", "detail": str(e)}


async def check_services(service, output_file):
    logging.info("Memulai pengecekan kesehatan server secara asinkron...")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_status(session, target) for target in service]

        result = await asyncio.gather(*tasks)

        with open(output_file, "w") as file:
            json.dump(result, file, indent=4)


asyncio.run(check_services(target_service, args.output))
