<template>
    <div class="files-container">
        <h3>导入数据</h3>
        <div>
            <h4>栅格数据</h4>
            <p>数据集仅支持在开发者模式使用</p>
            <label>影像名称:</label>
            <input type="text" placeholder="请输入">
            <label>采集时间:</label>
            <input type="date">
            <label>上传时间:</label>
            <input type="date">
            <label>所属区域:</label>
            <select>
                <option>请选择</option>
            </select>
            <label>分辨率:</label>
            <input type="text" placeholder="请输入">
            <label>影像状态:</label>
            <select>
                <option>请选择</option>
            </select>
        </div>
        <div>
            <h4>矢量数据</h4>
            <!-- 矢量数据相关操作 -->
        </div>
        <div>
            <h4>数据集</h4>
            <!-- 数据集相关操作 -->
        </div>
        <button @click="importData">上传数据</button>
        <button @click="closeContainer">取消</button>
    </div>
</template>

<script setup>
import { defineEmits } from 'vue'

// 定义 emits 用于触发父组件的方法
const emit = defineEmits(['update:filesContainerVisible'])

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
    /* 根据需要添加样式 */
}
</style>