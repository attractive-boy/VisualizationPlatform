<template>
  <el-tabs type="border-card">
    <el-tab-pane label="全国总平均分趋势">
      <div id="label1" class="main"></div>
    </el-tab-pane>
    <el-tab-pane label="各科成绩平均分">
      <div id="label2" class="main"></div>
    </el-tab-pane>
    <el-tab-pane label="全国及格率趋势">
      <div id="label3" class="main"></div>
    </el-tab-pane>
    <el-tab-pane label="年份各科成绩平均分">
      <div id="label4" class="main"></div>
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
import * as echarts from "echarts"
import { onMounted,getCurrentInstance,ref } from "vue"
// @ts-ignore
const { proxy } = getCurrentInstance()
// 定义科目名称的英文到中文的映射关系
const subjectMap = {
  'language': '语文',
  'mathematics': '数学',
  'english': '英语',
  'chemistry': '化学',
  'physics': '物理',
  'biology': '生物',
  'geography': '地理',
  'politics': '政治',
  'history': '历史',
};

//声明周期函数，自动执行初始化
onMounted(async () => {
  await initLable1();
  await initLable2();
  await initLable3();
  await initLable4();
});
//初始化函数
const initLable1 = async () => {
  const response = await proxy.$http.get('/scorestatistics/national_average_score_trend/');
  const national_average_score_trend = response.data.national_average_score_trend;

  // 处理数据格式，将年份和平均分分别存储到数组中
  const years = national_average_score_trend.map((item: { year: any; })=> item.year);
  const scores = national_average_score_trend.map((item: { average_score: any; }) => parseFloat(item.average_score).toFixed(2)); // 保留两位小数
  
  let Chart = echarts.init(document.getElementById("label1"))
  
  // 绘制图表
  let option = {
    xAxis: {
      type: 'category',
      data: years // 使用年份作为 x 轴数据
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: scores, // 使用平均分作为 y 轴数据
        type: 'line',
        label: { // 显示数据标签
          show: true, // 显示标签
          position: 'top' // 标签位置，可选值：'top'、'bottom'、'insideTop'、'insideBottom'
        }
      }
    ]
  };
  
  // 渲染图表
  Chart.setOption(option);
}

// 定义初始化柱状图的函数
const initLable2 = async () => {
  try {
    // 从服务器获取数据
    const response = await proxy.$http.get('/scorestatistics/subject_avg_score_bar_chart/');
    const data = response.data.subject_avg_score_bar_chart;

    // 解析数据，获取年份和各科目的平均分
    const years = data.map((item: { year: any; }) => item.year);
    const subjects = Object.keys(data[0]).filter(key => key !== 'year'); // 获取除了年份外的所有科目
    const scoresBySubject = subjects.map(subject => data.map((item: { [x: string]: string; }) => parseFloat(item[subject]).toFixed(2)));

    // 初始化 ECharts 实例并获取柱状图容器
    const chart = echarts.init(document.getElementById('label2'));

    // 构建数据集对象
    const dataset = {
      dimensions: ['year', ...subjects], // 维度包括年份和所有科目
      //@ts-ignore
      source: data.map((item: { [x: string]: string; year: { toString: () => any; }; }) => ({
        year: item.year.toString(),
        ...subjects.reduce((acc, subject) => ({ ...acc, [subject]: parseFloat(item[subject]).toFixed(2) }), {})
      }))
    };
    console.log(dataset)
    // 配置柱状图选项
    const option = {
      legend: {},
      tooltip: {},
      dataset: dataset,
      xAxis: { type: 'category', data: years },
      yAxis: { type: 'value' },
      //@ts-ignore
      series: subjects.map(subject => ({ type: 'bar', name: subjectMap[subject], encode: { x: 'year', y: subject } }))
    };

    // 渲染柱状图
    chart.setOption(option);
  } catch (error) {
    // 处理错误
    console.error('Failed to fetch data:', error);
  }
};


const initLable3 = async () => {
  const response = await proxy.$http.get('/scorestatistics/national_pass_rate_trend/');
  const national_pass_rate_trend = response.data.national_pass_rate_trend;

  // 处理数据格式，将年份和平均分分别存储到数组中
  const years = national_pass_rate_trend.map((item: { year: any; })=> item.year);
  const rate = national_pass_rate_trend.map((item: { pass_rate: any; }) => (parseFloat(item.pass_rate)*100).toFixed(2)); // 保留两位小数
  
  let Chart = echarts.init(document.getElementById("label3"))
  
  // 绘制图表
  let option = {
    xAxis: {
      type: 'category',
      data: years // 使用年份作为 x 轴数据
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: rate, // 使用平均分作为 y 轴数据
        type: 'line',
        label: { // 显示数据标签
          show: true, // 显示标签
          position: 'top' // 标签位置，可选值：'top'、'bottom'、'insideTop'、'insideBottom'
        }
      }
    ]
  };
  
  // 渲染图表
  Chart.setOption(option);
}


const initLable4 = async () => {
  try {
    // 从服务器获取数据
    const response = await proxy.$http.get('/scorestatistics/subject_avg_score_bar_chart/');
    const data = response.data.subject_avg_score_bar_chart;

    // 解析数据，获取年份和各科目的平均分
    const years = data.map((item: { year: { toString: () => any; }; }) => item.year.toString());
    const subjects = Object.keys(data[0]).filter(key => key !== 'year'); // 获取除了年份外的所有科目
    const scoresBySubject = subjects.map(subject => data.map((item: { [x: string]: string; }) => parseFloat(item[subject]).toFixed(2)));

    // 初始化 ECharts 实例并获取柱状图容器
    const chart = echarts.init(document.getElementById('label4'));

    // 构建数据集对象
    const dataset = {
      dimensions: ['subject', ...years], // 维度包括科目和所有年份
      source: subjects.map(subject => ({
        //@ts-ignore
        subject: subjectMap[subject],
        //@ts-ignore
        ...data.reduce((acc: any, item: { [x: string]: string; year: { toString: () => any; }; }) => ({ ...acc, [item.year.toString()]: parseFloat(item[subject]).toFixed(2) }), {})
      }))
    };

    // 配置柱状图选项
    const option = {
      legend: {},
      tooltip: {},
      dataset: dataset,
      xAxis: { type: 'category', },
      yAxis: { type: 'value' },
      series: years.map((year: any) => ({ type: 'bar', name: year, encode: { x: 'subject', y: year } }))
    };

    // 渲染柱状图
    chart.setOption(option);
  } catch (error) {
    // 处理错误
    console.error('Failed to fetch data:', error);
  }
};


</script>

<style scoped>
.main {
  width: 90vw;
  height: 80vh;
}
</style>