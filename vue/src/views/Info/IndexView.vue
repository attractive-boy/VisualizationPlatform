<template>
  <div>
    <!-- 新增按钮 -->
    <el-button type="primary" style="margin-bottom: 20px; width: 100%;" @click="showAddDialog">新增成绩</el-button>
    <el-table :data="scores" style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="year" label="年份"></el-table-column>
      <el-table-column prop="score" label="总分"></el-table-column>
      <el-table-column prop="province" label="省份"></el-table-column>
      <el-table-column prop="city" label="城市"></el-table-column>
      <el-table-column prop="language" label="语文"></el-table-column>
      <el-table-column prop="mathematics" label="数学"></el-table-column>
      <el-table-column prop="english" label="英语"></el-table-column>
      <el-table-column prop="chemistry" label="化学"></el-table-column>
      <el-table-column prop="physics" label="物理"></el-table-column>
      <el-table-column prop="biology" label="生物"></el-table-column>
      <el-table-column prop="geography" label="地理"></el-table-column>
      <el-table-column prop="politics" label="政治"></el-table-column>
      <el-table-column prop="history" label="历史"></el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button type="text" @click="handleEdit(row)"><el-icon>
              <Edit />
            </el-icon></el-button>
          <el-button type="text" @click="handleDelete(row)"><el-icon>
              <Delete />
            </el-icon></el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination :total="total" :page-size="pageSize" @current-change="handlePageChange"></el-pagination>

    <el-dialog v-model="dialogVisible" title="成绩录入">
      <el-form :model="currentScore" label-width="80px">
        <el-form-item label="年份">
          <el-select v-model="currentScore.year">
            <el-option v-for="year in YEAR_RANGE" :key="year" :label="year" :value="year"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="总分">
          <el-input v-model="currentScore.score" disabled="true"></el-input>
        </el-form-item>


        <el-form-item label="省份/城市">
          <!-- @vue-ignore -->
          <el-cascader style="width: 100%;" v-model="currentScore.provinceCity"
            :options="REGIONAL_SCOPE.map(province => ({ label: province, value: province, children: CITY_SCOPE[province].map(city => ({ label: city, value: city })) }))"
            clearable></el-cascader>
        </el-form-item>

        <el-form-item label="语文">
          <el-input v-model="currentScore.language"></el-input>
        </el-form-item>
        <el-form-item label="数学">
          <el-input v-model="currentScore.mathematics"></el-input>
        </el-form-item>
        <el-form-item label="英语">
          <el-input v-model="currentScore.english"></el-input>
        </el-form-item>
        <el-form-item label="化学">
          <el-input v-model="currentScore.chemistry"></el-input>
        </el-form-item>
        <el-form-item label="物理">
          <el-input v-model="currentScore.physics"></el-input>
        </el-form-item>
        <el-form-item label="生物">
          <el-input v-model="currentScore.biology"></el-input>
        </el-form-item>
        <el-form-item label="地理">
          <el-input v-model="currentScore.geography"></el-input>
        </el-form-item>
        <el-form-item label="政治">
          <el-input v-model="currentScore.politics"></el-input>
        </el-form-item>
        <el-form-item label="历史">
          <el-input v-model="currentScore.history"></el-input>
        </el-form-item>
      </el-form>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveScore">确 定</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, getCurrentInstance } from 'vue'
import { ElMessage } from 'element-plus'
import { Delete } from '@element-plus/icons-vue';

// @ts-ignore
const { proxy } = getCurrentInstance()
const dialogVisible = ref(false)
const scores = ref([])
const currentScore: any = ref({})
const total = ref(0)
const pageSize = ref(10)
let currentPage = 1

// 获取成绩列表
const fetchScores = () => {
  proxy.$http.get('/scores', {
    params: {
      page: currentPage,
      // pageSize: pageSize.value
    }
  }).then((res: { data: { results: never[]; count: number; }; }) => {
    scores.value = res.data.results
    total.value = res.data.count
  }).catch((err: any) => {
    console.error('Failed to fetch scores: ', err)
    ElMessage.error('获取成绩列表失败')
  })
}

// 编辑成绩
const handleEdit = (row: any) => {
  currentScore.value = { ...row }
  currentScore.value.provinceCity = [`${currentScore.value.province}`, `${currentScore.value.city}`];
  dialogVisible.value = true
}

// 删除成绩
const handleDelete = (row: { id: any; }) => {
  proxy.$http.delete(`/scores/delete/${row.id}`).then(() => {
    fetchScores()
  }).catch((err: any) => {
    console.error('Failed to delete score: ', err)
    ElMessage.error('删除成绩失败')
  })
}

// 保存成绩
const saveScore = () => {
  // Calculate total score before saving
  const totalScore = (
    Number(currentScore.value.language) +
    Number(currentScore.value.mathematics) +
    Number(currentScore.value.english) +
    Number(currentScore.value.chemistry) +
    Number(currentScore.value.physics) +
    Number(currentScore.value.biology) +
    Number(currentScore.value.geography) +
    Number(currentScore.value.politics) +
    Number(currentScore.value.history)
  ).toString();

  currentScore.value.score = totalScore; // Assign the total score to the current score object

  currentScore.value.province = currentScore.value.provinceCity[0]

  currentScore.value.city = currentScore.value.provinceCity[1]


  let url;
  if (currentScore.value.id) {
    url = `/scores/update/${currentScore.value.id}/`
  } else {
    url = `/scores/create/`
  }
  proxy.$http.post(url, currentScore.value).then(() => {
    dialogVisible.value = false
    fetchScores()
  }).catch((err: any) => {
    console.error('Failed to save score: ', err)
    ElMessage.error('保存成绩失败')
  })
}

// 显示新增成绩对话框
const showAddDialog = () => {
  currentScore.value = {} // 清空当前成绩数据
  dialogVisible.value = true
}

// 分页改变事件处理函数
const handlePageChange = (newPage: number) => {
  currentPage = newPage
  fetchScores()
}

onMounted(() => {
  fetchScores()
})

const REGIONAL_SCOPE = [
  '江苏省', '浙江省', '广东省', '四川省', '河南省'
];

const CITY_SCOPE = {
  '江苏省': ['南京市', '苏州市', '无锡市'],
  '浙江省': ['杭州市', '宁波市', '温州市'],
  '广东省': ['广州市', '深圳市', '东莞市'],
  '四川省': ['成都市', '绵阳市', '德阳市'],
  '河南省': ['郑州市', '洛阳市', '开封市']
};

const YEAR_RANGE = ['2020', '2021', '2022', '2023'];

const getCitiesByProvince = (province: string | number) => {
  //@ts-ignore
  return CITY_SCOPE[province] || [];
};
</script>

<style scoped>
/* 样式可以根据需求添加 */
</style>
