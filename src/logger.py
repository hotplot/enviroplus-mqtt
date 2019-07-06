import paho.mqtt.client as mqtt

from bme280 import BME280
from pms5003 import PMS5003
from enviroplus import gas


class EnvLogger:
    def __init__(self, client_id, host, port, username, password, prefix):
        self.bme280 = BME280()
        self.pms5003 = PMS5003()

        self.prefix = prefix

        self.client = mqtt.Client(client_id=client_id)
        self.client.username_pw_set(username, password)
        self.client.connect(host, port)


    def publish(self, topic, value):
        topic = self.prefix + "/" + topic
        self.client.publish(topic, str(value))


    def update(self):
        self.publish("temperature", self.bme280.get_temperature())
        self.publish("pressure", self.bme280.get_pressure())
        self.publish("humidity", self.bme280.get_humidity())

        gas_data = gas.read_all()
        self.publish("gas/oxidising", gas_data.oxidising)
        self.publish("gas/reducing", gas_data.reducing)
        self.publish("gas/nh3", gas_data.nh3)

        pm_data = self.pms5003.read()
        self.publish("particulate/1.0", pm_data.pm_ug_per_m3(1.0))
        self.publish("particulate/2.5", pm_data.pm_ug_per_m3(2.5))
        self.publish("particulate/10.0", pm_data.pm_ug_per_m3(10))

        self.client.loop()
