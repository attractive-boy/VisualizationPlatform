<template>
  <div>
    <el-input
      class="search-input"
      prefix-icon="el-icon-search"
      v-model="keyword"
      placeholder="请输入搜索关键字"
    ></el-input>
    <el-button type="primary" @click="handleSearch">查询</el-button>
    <el-table :data="filteredCases" style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="title" label="案件标题"></el-table-column>
      <el-table-column prop="reportTime" label="创建时间"></el-table-column>
      <el-table-column prop="claimantUser.username" label="报案人"></el-table-column>
      <el-table-column prop="status" label="案件状态"></el-table-column>
      <!-- 新增的简介列 -->
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button type="text" @click="ShowCase(row)">查看详细</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="案件处理">
      <el-form :model="editedCase" label-width="80px">
        <el-form-item label="标题">
          <el-input v-model="editedCase.title" disabled></el-input>
        </el-form-item>
        <el-form-item label="案件情况">
          <div v-html="editedCase.claimantDescription"></div>
        </el-form-item>
        <el-form-item label="处理说明">
          <div v-html="editedCase.handlerDescription"></div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, getCurrentInstance } from 'vue'

const cases = ref([])
const keyword = ref('')
const editedCase = ref({})

const dialogVisible = ref(false)

const { proxy } = getCurrentInstance()

const fetchAllCases = () => {
  proxy.$http
    .get('/case/')
    .then((response) => {
      cases.value = response.data
      filteredCases.value = cases.value
    })
    .catch((error) => {
      console.error('Error fetching cases:', error)
    })
}
onMounted(() => {
  fetchAllCases()
})

// 根据关键字过滤案件数据
const filteredCases = ref([])
const handleSearch = () => {
  if (!keyword.value.trim()) {
    filteredCases.value = cases.value
    return
  }
  filteredCases.value = cases.value.filter((item) => {
    // 在案件标题和报案人中搜索关键字
    return (
      item.title.includes(keyword.value.trim()) ||
      item.claimantDescription.includes(keyword.value.trim()) ||
      item.handlerDescription.includes(keyword.value.trim())
    )
  })
}

const ShowCase = (Case) => {
  editedCase.value = { ...Case }

  dialogVisible.value = true
}
</script>

<style scoped>
.avatar-uploader {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 120px;
  height: 120px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  overflow: hidden;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.search-input {
  width: 80vw;
  margin-right: 20px;
}
</style>
