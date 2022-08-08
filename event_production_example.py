# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import json

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


def get_test_event():
    payload = {
        "category": "TEST",
        "message": "Dies ist ein Test-Event.",
        "timestamp": 9001
    }
    return json.dumps(payload)


def get_test_production():
    payload = {
        "serial": 0,
        "quality": 1,
        "cycleTime": 2,
        "timestamp": 9001
    }
    return json.dumps(payload)


def create_message(payload):
    return Message(payload,
                   content_encoding="utf-8",
                   content_type="application/json",
                   )


async def main():
    event_message = create_message(get_test_event())
    event_message.custom_properties = {
        "Table": "Events",
        "IngestionMappingReference": "EventMapping"
    }

    prod_message = create_message(get_test_production())
    prod_message.custom_properties = {
        "Table": "Productions",
        "IngestionMappingReference": "ProductionMapping"
    }

    await send_messages([event_message, prod_message])


if __name__ == "__main__":
    asyncio.run(main())
    print("Sent test messages to Azure, check database in 5 mins or so.")
