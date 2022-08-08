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


def get_random_data():
    rand_string = ""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for i in range(32):
        rand_string += random.choice(alphabet)

    return {
        "foo": "properties are part of custom properties in this case",
        "Table": "Test",
        "IngestionMappingReference": "TestMapping"
    }


async def main():
    for i in range(3):
        payload = get_random_data()
        payload = json.dumps(payload)
        print(f"Message payload: {payload}")

        message = Message(payload,
                          content_encoding="utf-8",
                          content_type="application/json",
                          )
        message.custom_properties = {
            "Table": "Test",
            "IngestionMappingReference": "TestMapping"
        }

        await send_messages([message])


if __name__ == "__main__":
    asyncio.run(main())
    print("Sent test messages to Azure, check database in 5 or so.")
