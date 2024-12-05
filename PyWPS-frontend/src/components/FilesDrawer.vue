<template>
  <div class="files-container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="栅格数据" name="raster">
        <el-form>
          <el-form-item label="影像名称">
            <el-input placeholder="请输入"></el-input>
          </el-form-item>
          <el-form-item label="采集时间">
            <el-date-picker type="date" placeholder="请选择日期"></el-date-picker>
          </el-form-item>
          <el-form-item label="上传时间">
            <el-date-picker type="date" placeholder="请选择日期"></el-date-picker>
          </el-form-item>
          <el-form-item label="所属区域">
            <el-select placeholder="请选择">
              <el-option label="区域1" value="区域1"></el-option>
              <!-- 根据需要添加更多选项 -->
            </el-select>
          </el-form-item>
          <el-form-item label="分辨率">
            <el-input placeholder="请输入"></el-input>
          </el-form-item>
          <el-form-item label="影像状态">
            <el-select placeholder="请选择">
              <el-option label="状态1" value="状态1"></el-option>
              <!-- 根据需要添加更多选项 -->
            </el-select>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="矢量数据" name="vector">
        <h4>矢量数据</h4>
        <!-- 矢量数据相关操作 -->
      </el-tab-pane>
    </el-tabs>
     <div class="dataset-display">
      <h4>数据集</h4>
      <!-- 数据集展示 -->
      <el-table :data="datasetData" style="width: 100%">
        <el-table-column prop="name" label="影像名称"></el-table-column>
        <el-table-column prop="date" label="采集时间"></el-table-column>
        <el-table-column prop="region" label="所属区域"></el-table-column>
        <el-table-column prop="resolution" label="分辨率"></el-table-column>
        <el-table-column prop="status" label="影像状态"></el-table-column>
      </el-table>
    </div>
    <el-button type="primary" @click="importData">上传数据</el-button>
    <el-button @click="closeContainer">取消</el-button>
  </div>
</template>

<script setup>
import { defineEmits, ref } from 'vue'

// 定义 emits 用于触发父组件的方法
const emit = defineEmits(['update:filesContainerVisible'])

// 定义当前激活的选项卡
const activeTab = ref('raster')

// 模拟数据集数据
const datasetData = ref([
  { name: '232_Level_1.TIF', date: '2024-10-21', region: '区域1', resolution: '2米', status: '发布完成' },
  { name: '233.TIF', date: '2024-10-19', region: '区域1', resolution: '2米', status: '发布完成' }
])

const importData = () => {
  console.log('导入数据')
}

const closeContainer = () => {
  // 触发父组件的更新方法，关闭对话框
  emit('update:filesContainerVisible', false)
}
</script>

<style scoped>
.files-container {
  padding: 20px;
}
.dataset-display {
  margin-top: 20px;
}
</style>