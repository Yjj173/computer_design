#!/bin/bash

# MySQL数据库连接参数
mysql_user="root"
mysql_pass="123456"
mysql_host="localhost"
mysql_port=3306
mysql_db="agriculture"

# 创建 detail_data 表
mysql -u $mysql_user -p$mysql_pass -h $mysql_host -P $mysql_port $mysql_db << EOF
DROP TABLE IF EXISTS detail_data;
CREATE TABLE detail_data (
    id          VARCHAR(255) NULL COMMENT '传感器的id',
    temperature INT          NULL COMMENT '温度',
    wet         DOUBLE       NULL COMMENT '湿度',
    update_time DATETIME     NULL COMMENT '更新时间'
);
EOF

# 创建 real_time_state 表
mysql -u $mysql_user -p$mysql_pass -h $mysql_host -P $mysql_port $mysql_db << EOF
DROP TABLE IF EXISTS real_time_state;
CREATE TABLE real_time_state (
    id          INT          NOT NULL COMMENT '传感器的id',
    oid         INT          NOT NULL COMMENT '子传感器id',
    height      VARCHAR(255) NULL COMMENT '生长状况',
    update_time DATETIME     NULL COMMENT '更新时间',
    PRIMARY KEY (id, oid)
);
EOF

# 创建 temperature_adjust 表
mysql -u $mysql_user -p$mysql_pass -h $mysql_host -P $mysql_port $mysql_db << EOF
DROP TABLE IF EXISTS temperature_adjust;
CREATE TABLE temperature_adjust (
    id          INT      NOT NULL PRIMARY KEY,
    origin_temp INT      NULL,
    new_temp    INT      NULL,
    update_time DATETIME NULL
);

EOF

mysql -u $mysql_user -p$mysql_pass -h $mysql_host -P $mysql_port $mysql_db << EOF
DROP TABLE IF EXISTS user_info;
create table user_info
(
    username varchar(255) not null
        primary key,
    password varchar(255) null comment '密码的hash'
);
EOF

