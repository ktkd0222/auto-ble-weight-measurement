#!/usr/bin/env python3

# [requirements]
# sudo apt-get install python-dev libbluetooth3-dev
# sudo apt-get install libglib2.0 libboost-python-dev libboost-thread-dev
# sudo pip3 install -r requirements.txt

# [execute]
# sudo python3 ble-tool.py

import sys
import asyncio
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO
from typing_extensions import Final
from blehandler import BleHandler
from typing import List
from bleak import discover

TARGET_ADDRESS:Final[str] = "<your ble device address>"

logger = getLogger()
logger.setLevel(INFO)
_streamHandler = StreamHandler(sys.stdout)
_streamHandler.setLevel(INFO)
_streamHandler.setFormatter(Formatter('[%(asctime)s][%(levelname)s] %(message)s'))
logger.addHandler(_streamHandler)

async def main():
    while True:
        logger.info('start device scan...')
        tasks = []
        devices:List = await discover()
        for device in devices:
            if device.address == TARGET_ADDRESS:
                handler = BleHandler(TARGET_ADDRESS, debug=True)
                tasks.append(asyncio.ensure_future(handler()))
                logger.info(f'found target device : {device}. discover process end.')
        
        if len(tasks) > 0:
            [await task for task in tasks]
        else:
            logger.info('target device not found. rescan after sleep 5s.')
        await asyncio.sleep(5)

asyncio.run(main())
