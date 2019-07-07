import paho.mqtt.client as mqtt

from bme280 import BME280
from pms5003 import PMS5003
from enviroplus import gas


class EnvLogger:
    def __init__(self, client_id, host, port, username, password, prefix, use_pms5003):
        self.bme280 = BME280()
        self.pms5003 = use_pms5003 and PMS5003() or None

        self.prefix = prefix

        self.connection_error = None
        self.client = mqtt.Client(client_id=client_id)
        self.client.on_connect = self.__on_connect
        self.client.username_pw_set(username, password)
        self.client.connect(host, port)
    

    def __on_connect(self, client, userdata, flags, rc):
        errors = {
            1: "incorrect MQTT protocol version",
            2: "invalid MQTT client identifier",
            3: "server unavailable",
            4: "bad username or password",
            5: "connection refused"
        }

        if rc > 0:
            self.connection_error = errors.get(rc, "unknown error")


    def publish(self, topic, value):
        topic = self.prefix.strip("/") + "/" + topic
        self.client.publish(topic, str(value))


    def update(self):
        self.publish("temperature", self.bme280.get_temperature())
        self.publish("pressure", self.bme280.get_pressure())
        self.publish("humidity", self.bme280.get_humidity())

        gas_data = gas.read_all()
        self.publish("gas/oxidising", gas_data.oxidising)
        self.publish("gas/reducing", gas_data.reducing)
        self.publish("gas/nh3", gas_data.nh3)

        if self.pms5003 is not None:
            pm_data = self.pms5003.read()
            self.publish("particulate/1.0", pm_data.pm_ug_per_m3(1.0))
            self.publish("particulate/2.5", pm_data.pm_ug_per_m3(2.5))
            self.publish("particulate/10.0", pm_data.pm_ug_per_m3(10))

        self.client.loop()
