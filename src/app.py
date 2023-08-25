from flask import Flask, jsonify,request
import Dbconn
from Common import Resp
from Common import Config
from Auth import Auth
import datetime
from flask_cors import CORS
from datetime import datetime, timedelta
import random

app = Flask(__name__)
CORS(app)








# 处理最大温湿度变化的函数
def get_max_sensor():
    # 获取最近10分钟内的数据
    db = Dbconn.Mysql()
    sql_select = ("SELECT id, (MAX(temperature) - MIN(temperature)) + (MAX(wet) - MIN(wet)) AS temp_change_sum,(MAX(temperature) - MIN(temperature)) AS temperature_change,(MAX(wet) - MIN(wet)) AS wet_change FROM detail_data WHERE update_time >= DATE_SUB(NOW(), INTERVAL 10 MINUTE) GROUP BY id ORDER BY temp_change_sum DESC LIMIT 1;")
    result = db.dbSelect(sql_select)
    json_result = {}
    if len(result) > 0:
        json_result['sensor_id'] = result[0][0]
        json_result['temp_change_sum'] = result[0][1]
        json_result['temperature_change'] = result[0][2]
        json_result['wet_change'] = result[0][3]
    return json_result


# 定义接口路由
@app.route('/max_sensor', methods=['GET'])
def max_sensor():
    # 调用函数获取最大温湿度变化的传感器
    result = get_max_sensor()
    # 将结果以JSON格式返回
    return jsonify(result)


@app.route('/user_login', methods=['POST'])
def user_login():

    data = request.get_json()
    username = data.get('loginName')
    password = data.get('loginPwd')
    db = Dbconn.Mysql()
    ret = db.dbSelect("SELECT username,password FROM user_info WHERE username= '{}' ".format(username))
    if not len(ret) == 1:
        return Resp.error('用户名或密码错误')

    passhash = ret[0][1]
    if not Auth.check_password(passhash, password):
        return Resp.error('用户名或密码错误')


    JWT = Auth.encode_jwt(ret[0][1])
    userinfo = {
        'username': ret[0][1],

    }
    return Resp.success(body={
        'token': JWT,
        'userinfo': userinfo

    })

def get_sensor_data():
    sensors_data = []
    for i in range(5):
        sensor_data = {}
        sensor_data['id'] = 'Sensor ' + str(i + 1)
        sensor_data['temperature'] = round(random.uniform(20.0, 30.0), 2)
        sensor_data['humidity'] = round(random.uniform(40.0, 60.0), 2)
        sensor_data['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sensors_data.append(sensor_data)
    return sensors_data

# 定义接口路由
@app.route('/sensors_data', methods=['GET'])
def get_sensors_data():
    db = Dbconn.Mysql()
    try:
        sql = "SELECT id, AVG(temperature) AS avg_temp,AVG(wet) AS avg_wet FROM detail_data WHERE update_time >= DATE_SUB(NOW(), INTERVAL 10 MINUTE) GROUP BY id;"
        results = db.dbSelect(sql)
        sensors_data = []
        for row in results:
            sensor_data = {}
            sensor_data['sensor_id'] = row[0]
            sensor_data['avg_temperature'] = row[1]
            sensor_data['avg_humidity'] = row[2]
            sensors_data.append(sensor_data)
        return jsonify({'code': 0, 'data': sensors_data})
    except Exception as e:
        print("Error fetching data from database: {}".format(str(e)))
        return jsonify({'code': -1, 'message': 'Error fetching data from database'})

@app.route('/temperature_change', methods=['GET'])
def get_temperature_change():
    db = Dbconn.Mysql()
    try:
        sql = "SELECT id, update_time, temperature FROM detail_data WHERE update_time >= DATE_SUB(NOW(), INTERVAL 1 HOUR) ORDER BY update_time ASC;"
        results = db.dbSelect(sql)
        sensors_data = {}
        for row in results:
            sensor_id = 'Sensor ' + str(row[0])
            timestamp = row[1].strftime('%Y-%m-%d %H:%M:%S')
            temperature = row[2]
            if sensor_id not in sensors_data:
                sensors_data[sensor_id] = {
                    'timestamps': [],
                    'temperatures': []
                }
            sensors_data[sensor_id]['timestamps'].append(timestamp)
            sensors_data[sensor_id]['temperatures'].append(temperature)
        return jsonify({'code': 0, 'data': sensors_data})
    except Exception as e:
        print("Error fetching data from database: {}".format(str(e)))
        return jsonify({'code': -1, 'message': 'Error fetching data from database'})



def adjust_temperature(data):
    db = Dbconn.Mysql()
    cur = db.conn.cursor()
    for item in data:
        sensor_id = item['id']
        origin_temp = item['origin_temp']
        new_temp = item['new_temp']
        update_time_str = item['update_time']
        update_time = datetime.fromisoformat(update_time_str[:-1])  # 解析时间字符串并去掉末尾的Z
        update_time= update_time.strftime("%Y-%m-%d %H:%M:%S")  # 将时间转换为MySQL的DATETIME格式

        # 将update_time_formatted作为参数传递给SQL语句执行插入操作

        sql_insert = "INSERT INTO temperature_adjust (id, origin_temp, new_temp, update_time) VALUES ('%s', '%s', '%s', '%s')" % (sensor_id, origin_temp, new_temp, update_time)
        cur.execute(sql_insert)
        sql_change = ""
    db.conn.commit()

# 定义接口路由
@app.route('/temperature_adjust', methods=['POST'])
def temperature_adjust():
    data = request.get_json()
    adjust_temperature(data)
    return jsonify({'status': 'success'})






if __name__ == '__main__':
    app.run(debug=True,port=Config.APP_PORT)
