<template>
    <div class="container">
      <div class="sidebar">
        <h1 class="logo">AgriAI智慧农业</h1>
        <el-menu default-active="1" class="el-menu-vertical-demo" @select="handleMenuSelect">
          <el-submenu index="1">
            <template slot="title">监测信息</template>
            <el-menu-item index="1-1">近10分钟平均温度和湿度</el-menu-item>
            <el-menu-item index="1-2">最高温度</el-menu-item>
            <el-menu-item index="1-3">历史温度变化</el-menu-item>
            <el-menu-item index="1-4">温度变化差</el-menu-item>
            <el-menu-item index="1-5">各分区生长状况</el-menu-item>
          </el-submenu>
          <el-menu-item index="2">手动调节温度</el-menu-item>
          <el-menu-item index="3">退出登录</el-menu-item>
        </el-menu>
      </div>
      <div class="main">
        <div class="header">
          <el-button class="export-button" type="primary" icon="el-icon-download">导出数据</el-button>
        </div>
        <div class="content">
            <component :is="currentComponent"></component>
        </div>
      </div>
    </div>
  </template>
  <script>


  import AverageTemp from './AverageTemp.vue';
  import TemperatureChange from './TemperatureChange.vue';
  import AdjustTemp from './AdjustTemp.vue'

  export default {
    name: "MainView",
    data() {
    return {
      currentComponent: null,
    } },
    methods: {
      handleMenuSelect(index) {
        switch (index) {
          case "1-1":
          this.currentComponent = AverageTemp;
            break;
          case "1-2":
            console.log("最高温度")
            break
          case "1-3":
          this.currentComponent = TemperatureChange;
            break;
          case "1-4":
            console.log("温度变化差");
            break;
          case "1-5":
            console.log("各分区生长状况");
            break;
          case "2":
          this.currentComponent = AdjustTemp;
            break;
          case "3":
            window.localStorage.removeItem('jwt');
            this.$router.push('/login');
            break;
        }
      },
    },
    components: {
    AverageTemp,
    TemperatureChange,
    AdjustTemp
  },
  };
  </script>
  <style scoped>
  .container {
    display: flex;
    height: 100%;
    width: 100%;
  }
  
  .sidebar {
    width: 250px;
    height: 100%;
    background-color: #fff;
  }
  
  .logo {
    font-size: 30px;
    color: #fff;
    background-color: #333;
    margin: 0;
    padding: 20px;
  }
  
  .main {
    flex-grow: 1;
    height: 100%;
    background-color: #f0f0f0;
    display: flex;
    flex-direction: column;
  }
  
  .el-menu-vertical-demo {
    height: 100%;
  }
  
  .export-button {
    margin: 10px;
  }
  
  .content {
    margin: 20px;
    background-color: #fff;
    flex-grow: 1;
  }
  </style>



