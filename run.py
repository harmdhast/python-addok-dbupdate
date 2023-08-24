import json
import logging
import subprocess
from wget import download
import sys
import redis
import gzip
import shutil
import config
import os
import time
from urllib.request import urlopen

logging.getLogger().setLevel(logging.INFO)

try:
    r = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REDIS_DB,
    )
    r.ping()
    r.config_set("save", "")
    r.config_rewrite()
except Exception as e:
    logging.error("REDIS: Couldn't connect to the server: %s", e)
    sys.exit(1)

logging.info("REDIS: Server OK")

logging.info("Downloading last adresses database...")
download(config.ADDOK_DB, "db.ndjson.gz")

logging.info("Decompressing database file...")
with gzip.open("db.ndjson.gz", "rb") as f_in:
    with open("db.ndjson", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


logging.info("REDIS: Cleaning all keys")
r.flushall()
logging.info("Importing data...")
subprocess.call(["addok", "batch", "--conf", "addok.conf", "db.ndjson"])
subprocess.call(["addok", "ngrams", "--conf", "addok.conf"])

logging.info("Cleaning up workspace...")
os.remove("db.ndjson.gz")
os.remove("db.ndjson")

if r.info("keyspace")["db0"]["keys"] > 1000:
    logging.info("REDIS: Import OK")

logging.info("Testing API")
with subprocess.Popen(["addok", "--conf", "addok.conf", "serve"]) as sproc:
    time.sleep(3)  # Wait for the server
    with urlopen("http://127.0.0.1:7878/search/?q=epinay+sur+seine") as req:
        res = req.read().decode("utf-8")
        if len(json.loads(res)["features"]) > 0:
            logging.info("API OK")
        else:
            logging.error("Error while testing API")
            sys.exit(1)
    sproc.terminate()

logging.info("Saving database")
r.save()
logging.info("Database updated successfully")
