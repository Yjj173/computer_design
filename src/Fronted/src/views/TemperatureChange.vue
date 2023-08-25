<template>
    <div class="temperature-change">
      <h2 class="title">历史温度变化</h2>
      <div class="chart-container">
        <div ref="chart" class="chart"></div>
      </div>
    </div>
  </template>
  

  
  <script>
  import axios from 'axios'
  import * as echarts from 'echarts'
  
  export default {
    name: 'TemperatureChange',
  
    data() {
      return {
        chartOptions: {
          title: {
            text: '历史温度变化',
            subtext: '最近一小时内各传感器温度变化',
          },
          tooltip: {
            trigger: 'axis',
          },
          legend: {
            data: ['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5'],
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [],
          },
          yAxis: {
            type: 'value',
          },
          series: [
            {
              name: 'Sensor 1',
              type: 'line',
              smooth: true,
              data: [],
            },
            {
              name: 'Sensor 2',
              type: 'line',
              smooth: true,
              data: [],
            },
            {
              name: 'Sensor 3',
              type: 'line',
              smooth: true,
              data: [],
            },
            {
              name: 'Sensor 4',
              type: 'line',
              smooth: true,
              data: [],
            },
            {
              name: 'Sensor 5',
              type: 'line',
              smooth: true,
              data: [],
            },
          ],
        },
      }
    },
  
    mounted() {
      // 获取传感器历史温度数据
      axios
        .get('http://127.0.0.1:5000/temperature_change')
        .then((response) => {
          const data = response.data.data
          const xAxisData = data['Sensor sensor1']['timestamps']
          const seriesData = [
            data['Sensor sensor1']['temperatures'],
            data['Sensor sensor2']['temperatures'],
            data['Sensor sensor3']['temperatures'],
            data['Sensor sensor4']['temperatures'],
            data['Sensor sensor5']['temperatures'],
          ]
          this.chartOptions.xAxis.data = xAxisData
          this.chartOptions.series.forEach((series, index) => {
            series.data = seriesData[index]
          })
          this.$nextTick(() => {
            const chart = echarts.init(this.$refs.chart)
            chart.setOption(this.chartOptions)
          })
        })
        .catch((error) => {
          console.log(error)
        })
    },
  }
  </script>

  
  
  <style scoped>
  .temperature-change {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .title {
    font-size: 20px;
    margin-top: 20px;
  }
  
  .chart-container {
    width: 800px;
    height: 400px;
    margin-top: 20px;
    border: 1px solid #ccc;
    box-shadow: 0 0 10px #ccc;
  }
  
  .chart {
    width: 100%;
    height: 100%;
  }
  </style>
  