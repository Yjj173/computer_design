import paho.mqtt.client as mqtt
import threading
import time
import random
import json
import datetime

# MQTT 代理地址和端口
broker_address = "localhost"
broker_port = 1883

# 传感器节点的 ID 前缀
sensor_prefix = "sensor"

# 传感器数据的主题
sensor_topic = "sensors/{}/data"

# 连接到 MQTT 代理的回调函数
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # 订阅传感器控制的主题
    client.subscribe("sensors/+/control")

# 接收到 MQTT 消息的回调函数
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# 发布传感器数据的函数
def publish_data(client, sensor_id):
    topic = sensor_topic.format(sensor_id)
    while True:
        # 生成随机的温度数据
        temperature = random.randint(20, 30)
        wet = random.randint(10,40)
        now = datetime.datetime.now()
        # 将温度数据打包成 JSON 数据包
        data = json.dumps({
            "sensor_id": sensor_id,
            "temperature": temperature,
            "wet" : wet,
            "update_time" : now.strftime("%Y-%m-%d %H:%M:%S")
        })
        # 发布数据到 MQTT 主题
        client.publish(topic, data)
        # 等待一段时间
        time.sleep(1)

# 创建多个传感器节点并模拟它们
num_sensors = 5
sensors = []

# 创建 MQTT 客户端对象
client = mqtt.Client()

# 设置连接和消息处理的回调函数
client.on_connect = on_connect
client.on_message = on_message

# 连接到 MQTT 代理
client.connect(broker_address, broker_port)

# 开启 MQTT 客户端的网络循环
client.loop_start()

# 创建多个传感器节点
for i in range(num_sensors):
    # 生成传感器节点的 ID
    sensor_id = "{}{}".format(sensor_prefix, i+1)
    # 创建发布传感器数据的线程
    publish_thread = threading.Thread(target=publish_data, args=(client, sensor_id))
    publish_thread.start()
    # 记录传感器节点和线程
    sensors.append((sensor_id, publish_thread))

# 等待所有线程结束
for sensor in sensors:
    sensor[1].join()

# 停止 MQTT 客户端的网络循环
client.loop_stop()
