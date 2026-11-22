"""ESP32 MQTT publisher simulator for the REST API Node-RED lab."""
import json, os, random, time
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_HOST", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_SENSOR_TOPIC", "iot/sensor")
CLIENT_ID = os.getenv("MQTT_CLIENT_ID", "ESP32-Simulator-Rizky")


def main() -> None:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    client.connect(BROKER, PORT, 60)
    client.loop_start()
    print(f"Simulator terhubung ke {BROKER}:{PORT}, topic={TOPIC}. Ctrl+C untuk berhenti.")
    try:
        while True:
            payload = {
                "suhu": round(random.uniform(25.0, 34.0), 1),
                "kelembaban": round(random.uniform(50.0, 85.0), 1),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            info = client.publish(TOPIC, json.dumps(payload), qos=0)
            info.wait_for_publish()
            print("Publish:", payload)
            time.sleep(3)
    except KeyboardInterrupt:
        print("Simulator dihentikan.")
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
