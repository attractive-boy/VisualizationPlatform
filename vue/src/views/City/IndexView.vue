<template>
  <el-tabs type="border-card">
    <el-tab-pane label="高考总平均分变化">
      <div id="label1" class="main"></div>
    </el-tab-pane>
    <el-tab-pane label="各科成绩平均分">
      <el-form-item label="选择城市：" class="select-container">
        <el-select v-model="selectedProvince2" placeholder="请选择城市" @change="updateLable2">
          <el-option v-for="province in provinces" :key="province" :label="province" :value="province"></el-option>
        </el-select>
      </el-form-item>
      <div id="label2" class="main"></div>
    </el-tab-pane>
    <el-tab-pane label="高考及格率趋势">
      <div id="label3" class="main"></div>
    </el-tab-pane>
    <el-tab-pane label="具体年份各科成绩平均分">
      <el-form-item label="选择城市：" class="select-container">
        <el-select v-model="selectedProvince4" placeholder="请选择城市" @change="updateLable4">
          <el-option v-for="province in provinces" :key="province" :label="province" :value="province"></el-option>
        </el-select>
      </el-form-item>
      <div id="label4" class="main"></div>
    </el-tab-pane>
  </el-tabs>
</template>

<script setup lang="ts">
import * as echarts from "echarts"
import { onMounted, getCurrentInstance, ref } from "vue"
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

const provinces: any = ref([])

const selectedProvince2 = ref()
const selectedProvince4 = ref()

const subject_avg_score_by_city = ref()
const subject_avg_score_by_city_and_year = ref()
//声明周期函数，自动执行初始化
onMounted(async () => {
  await initLable1();
  await initLable2();
  await initLabel3();
  await initLable4();
});
//初始化函数
const initLable1 = async () => {
  try {
    // 从服务器获取数据
    const response = await proxy.$http.get('/scorestatistics/city_average_score_trend/');
    const city_average_score_trend = response.data.city_average_score_trend;

    // 解析数据，获取年份和各省份的平均分
    const years = city_average_score_trend[Object.keys(city_average_score_trend)[0]].map(item => item.year);
    const provinces = Object.keys(city_average_score_trend);
    const scoresByProvince = provinces.map(province => city_average_score_trend[province].map(item => parseFloat(item.average_score).toFixed(2)));

    // 初始化 ECharts 实例并获取折线图容器
    const chart = echarts.init(document.getElementById('label1'));

    // 配置折线图选项
    const option = {
      xAxis: {
        type: 'category',
        data: years, // 使用年份作为 x 轴数据
      },
      yAxis: {
        type: 'value',
      },
      legend: {
        data: provinces, // 添加图例
        top: 'top', // 设置图例在上方
      },
      series: provinces.map((province, index) => ({
        name: province,
        type: 'line',
        data: scoresByProvince[index], // 使用各省份的平均分作为 y 轴数据
        label: { // 显示数据标签
          show: true, // 显示标签
          position: 'top', // 标签位置
        },
      })),
    };

    // 渲染图表
    chart.setOption(option);
  } catch (error) {
    // 处理错误
    console.error('Failed to fetch data:', error);
  }
};


// 定义初始化柱状图的函数
const initLable2 = async () => {
  const response = await proxy.$http.get('/scorestatistics/subject_avg_score_by_city/');
  subject_avg_score_by_city.value = response.data.subject_avg_score_by_city;
  provinces.value = Object.keys(subject_avg_score_by_city.value);
  selectedProvince2.value = provinces.value[0]
  updateLable2()
};

const updateLable2 = () => {
  // 获取选中省份的数据
  const selectedData = selectedProvince2.value;

  const chart = echarts.init(document.getElementById('label2'));

  // 解析数据，获取年份和各科目的平均分

  const years = Object.keys(subject_avg_score_by_city.value[selectedData]).map((year) => year);
  const firstYearData = subject_avg_score_by_city.value[selectedData][Object.keys(subject_avg_score_by_city.value[selectedData])[0]];
  const subjects = Object.keys(firstYearData);
  console.log(subject_avg_score_by_city.value[selectedData])
  // 构建数据集对象
  const dataset = {
    dimensions: ['year', ...subjects], // 维度包括年份和所有科目
    //@ts-ignore
    source: Object.keys(subject_avg_score_by_city.value[selectedData]).map(year => {
      const item = subject_avg_score_by_city.value[selectedData][year];
      return {
        year: year,
        ...subjects.reduce((acc, subject) => ({ ...acc, [subject]: parseFloat(item[subject]).toFixed(2) }), {})
      };
    })
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
}


const initLabel3 = async () => {
  try {
    // Fetch data from the API
    const response = await proxy.$http.get('/scorestatistics/city_pass_rate_trend/');
    const city_pass_rate_trend = response.data.city_pass_rate_trend;

    // Prepare data for ECharts
    const years = [];
    const passRates = {};
    const legendData = [];
    const seriesData = [];

    // Extract years and pass rates for each province
    for (const province in city_pass_rate_trend) {
      //@ts-ignore
      legendData.push(province);
      const passRateData = [];

      city_pass_rate_trend[province].forEach(entry => {
        //@ts-ignore
        if (!years.includes(entry.year)) {
          //@ts-ignore
          years.push(entry.year);
        }
        //@ts-ignore
        passRateData.push({
          year: entry.year,
          value: entry.pass_rate
        });
      });
      passRates[province] = passRateData;
    }

    // Sort years in ascending order
    years.sort((a, b) => a - b);

    // Generate series data for each province
    for (const province in passRates) {
      const passRateData = passRates[province];
      const seriesItem = {
        name: province,
        type: 'line',
        data: []
      };
      years.forEach(year => {
        const passRate = passRateData.find(entry => entry.year === year);
        if (passRate) {
          //@ts-ignore
          seriesItem.data.push((passRate.value * 100).toFixed(2));
        } else {
          //@ts-ignore
          seriesItem.data.push(null);
        }
      });
      //@ts-ignore
      seriesData.push(seriesItem);
    }

    // Configure ECharts instance and render chart
    const chartDom = document.getElementById('label3');
    const myChart = echarts.init(chartDom);
    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: function (params) {
          const data = params[0].data;
          if (data !== null) {
            return `${params[0].axisValue}: ${data}`;
          } else {
            return `${params[0].axisValue}: N/A`;
          }
        }
      },
      legend: {
        data: legendData,
        top: 'top'
      },
      xAxis: {
        type: 'category',
        data: years
      },
      yAxis: {
        type: 'value'
      },
      series: seriesData
    };
    myChart.setOption(option);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};




const initLable4 = async () => {
  const response = await proxy.$http.get('/scorestatistics/subject_avg_score_by_city_and_year/');
  subject_avg_score_by_city_and_year.value = response.data.subject_avg_score_by_city_and_year;
  selectedProvince4.value = provinces.value[0]
  updateLable4()
};

const updateLable4 = async () => {
  // Filter data based on selected province
  const provinceData = subject_avg_score_by_city_and_year.value[selectedProvince4.value];

  // Generate chart data
  const years = Object.keys(provinceData);
  const subjects = Object.keys(provinceData[years[0]]);
  const subjects_translate = Object.keys(provinceData[years[0]]).map(subject => subjectMap[subject]); // 将科目名称翻译成中文
  const xAxisData = years;

  // Prepare dataset
  const dataset = {
    dimensions: ['year', ...subjects_translate], // 维度包括年份和所有科目
    source: years.map(year => {
      const item = provinceData[year];
      const dataObj = { year };
      subjects.forEach(subject => {
        const chineseSubject = subjectMap[subject]; // 将科目名称翻译成中文
        dataObj[chineseSubject] = parseFloat(item[subject]).toFixed(2);
      });
      return dataObj;
    })
  };

  // Render chart
  const chartDom = document.getElementById('label4');
  const myChart = echarts.init(chartDom);
  const option = {
    legend: {},
    tooltip: {},
    dataset: dataset,
    xAxis: { type: 'category', data: xAxisData },
    yAxis: {},
    series: subjects.map(subject => ({ type: 'bar' })) // Declare several bar series, each will be mapped to a column of dataset.source by default
  };

  myChart.setOption(option);
};


</script>

<style scoped>
.main {
  width: 90vw;
  height: 80vh;
}

.select-container {
  margin-bottom: 20px;
}
</style>