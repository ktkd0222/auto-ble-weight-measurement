#!/usr/bin/env python3

import sys
import asyncio
import requests
import warnings
from datetime import datetime
from logging import Logger, getLogger, StreamHandler, DEBUG
from typing_extensions import Final
from bleak import BleakClient
from bleak import _logger as logger

WEIGHT_MEASUREMENT:Final[str] = "<weight measurement uuid>"

warnings.simplefilter('ignore', FutureWarning)

class BleHandler():
    """ble handler.
    """
    SLEEP_TIME:Final[int] = 2
    TIME_OUT:Final[int] = 20

    def __init__(self, address:str, is_request:bool=True, debug:bool=False) -> None:
        self.address:str = address
        self.is_request:bool = is_request
        self._logger:Logger = getLogger()

        if debug:
            l = getLogger("asyncio")
            l.setLevel(DEBUG)
            h = StreamHandler(sys.stdout)
            h.setLevel(DEBUG)
            l.addHandler(h)
            logger.addHandler(h)

    async def __call__(self) -> None:
        """when call, connect to target address device.
        """
        self._logger.info(f'connect to device({self.address}) start.')
        await self.connect_to_device()
    
    def _calculate_weight(self, data) -> float:
        """calculate weight value from bytearray.
        Args:
            data ([type]): [description]
        Returns:
            float: weight(format : xxx.xx)
        """
        return (data[1] + data[2] * 256) * 0.005

    def _weight_measurement_notification_handler(self, sender, data:bytearray):
        """Weight measurement notification handler."""
        weight:float = (data[1] + data[2] * 256) * 0.005
        self._logger.info(f'weight measurement notification handler: {data.hex()} / {weight} kg')

        if self.is_request:
            self._logger.info(f'request send.')
            send_date:str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            response = requests.post(
                '<your gas url>',
                {'weight': weight, 'date': send_date})

    def _disconnect_callback(self, client: BleakClient):
        """disconnect callback. only logging message."""
        self._logger.info(f'Client with address {client.address} got disconnected. try to reconnect.')

    async def connect_to_device(self):
        while True:
            self._logger.info("Waiting connect to device.")
            try:
                async with BleakClient(self.address, timeout=self.TIME_OUT, disconnected_callback=self._disconnect_callback) as client:

                    if await client.is_connected():
                        self._logger.info("Connect to device successfuly.")
                        await client.start_notify(
                            WEIGHT_MEASUREMENT, self._weight_measurement_notification_handler
                        )

                        while True:
                            if not await client.is_connected():
                                self._logger.debug("Device disconnected.")
                                break
                            await asyncio.sleep(self.SLEEP_TIME)
                            self._logger.debug("wait for message arraived from device.")
                    else:
                        self._logger.debug("Device disconnected.")
            except Exception as e:
                self._logger.error(f"Exception when connect: {e}")
            
            await asyncio.sleep(self.SLEEP_TIME)
