# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import json
import time
import random

from azure.iot.device import Message
from azure.iot.device.aio import IoTHubDeviceClient


def load_file(path):
    with open(path) as f:
        return f.read()


async def send_messages(messages: list):
    # Load the connection string from an environment variable
    conn_str = load_file("connection-string.txt")

    # Create instance of the device client using the connection string
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    # Send all messages that we are given
    for message in messages:
        print("Sending message...")
        await device_client.send_message(message)
        print("Message successfully sent!")

    # Finally, shut down the client
    await device_client.shutdown()


def get_random_datum():
    return {
        "id": "sim-device",
        "timestamp": time.time_ns() // 1_000_000,
        "temperature": random.uniform(0.0, 35.0),
        "humidity": random.uniform(0.0, 100.0),
        "window": random.choice([True, False])
    }


async def main():
    for i in range(10):
        # payload = [get_random_datum(), get_random_datum(), get_random_datum()]
        payload = get_random_datum()
        payload = json.dumps(payload)
        print(f"Message payload: {payload}")
        message = Message(payload, content_encoding="utf-8", content_type="application/json")
        await send_messages([message])


if __name__ == "__main__":
    asyncio.run(main())
    print("Sent 10 messages to Azure. Check database.")
