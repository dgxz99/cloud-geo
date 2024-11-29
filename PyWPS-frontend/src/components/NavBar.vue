<!-- src/components/NavBar.vue -->
<template>
  <el-row class="navbar-container" type="flex" justify="space-between" align="middle">
    <!-- 左侧标题和图标 -->
    <el-col :span="8" class="navbar-title">
      <img src="../assets/favicon.png" alt="Logo" class="navbar-icon" style="width: 40px; height: 40px;">
      <span class="title-text" style="font-size:30px">Geospatial Platform</span>
    </el-col>

    <!-- 右侧菜单项 -->
    <el-col :span="16" class="navbar-menu" style="display: flex; justify-content: flex-end; flex-wrap: nowrap;">
      <el-menu
        mode="horizontal"
        background-color="#FFFFFF"
        text-color="#000000"
        active-text-color="#409EFF"
        :default-active="activeIndex"
        class="navbar"
        style="
          text-align: right;
          white-space: nowrap;
          overflow: visible;
          width: 100%;
        "
        :ellipsis="false"
      >
        <el-menu-item index="1" @click="switchComponent('files', toggleFilesDrawer)">
          Files
        </el-menu-item>
        <el-menu-item index="2" @click="switchComponent('toolbox', null, toggleToolbox)">
          Operator Toolbox
        </el-menu-item>
        <el-menu-item index="3" @click="switchComponent('operator-overview', null, '/operator-overview')">
          Operator Overview
        </el-menu-item>
        <el-menu-item index="4" @click="switchComponent('knowledge-graph', null, '/knowledge-graph')">
          Knowledge Graph
        </el-menu-item>
        <el-menu-item index="5" @click="switchComponent('search', null, '/search')">
          Operator Traceability
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref } from 'vue'
import { defineEmits } from 'vue'
import { useNavBar } from '@/composables/useNavBar'

const emit = defineEmits(['toggle-files-drawer', 'toggle-toolbox', 'show-knowledge-graph', 'reset-view']);
const { navigate } = useNavBar()

// 记录当前打开的组件
const currentComponent = ref('')

// 切换组件的方法
const switchComponent = (component, toggleFunction = null, route = '') => {
    console.log("Switching Component:", component);
    console.log("Current Component:", currentComponent.value);

    if (component === 'toolbox') {
        emit('toggle-toolbox');
        route = '/operator-toolbox';
    } else if (currentComponent.value === 'toolbox' && component !== 'toolbox') {
        emit('toggle-toolbox');
    }

    if (currentComponent.value === component && toggleFunction) {
        console.log("Toggling function for same component:", component);
        toggleFunction();
        return;
    }

    currentComponent.value = component;
    if (toggleFunction) toggleFunction();

    console.log("Emitting view state change for:", component);
    if (component === 'knowledge-graph') {
        emit('show-knowledge-graph');
    } else if (component === 'operator-overview') {
        emit('show-operator-overview');
    } else {
        emit('reset-view');
    }

    if (route) {
        navigate(route);
        console.log("Navigated to route:", route);
    }
};

const toggleToolbox = () => {
    emit('toggle-toolbox')
}
 // 控制文件抽屉显示
const toggleFilesDrawer = () => {
    emit('toggle-files-drawer')
}
</script>

<style scoped>
.navbar-container {
  height: 60px;
  padding: 10px 20px;
  display: flex;
  align-items: center; /* 确保上下居中对齐 */
  position: relative;
  z-index: 1000; /* 确保顶部栏的 z-index 高于地图 */
}

.navbar-title {
  display: flex;
  align-items: center; /* 垂直居中 */
  height: 100%; /* 确保左右两侧高度一致 */
}

.navbar-icon {
  margin-right: 8px;
  color: #409EFF;
  height: 30px; /* 设置图标高度 */
}

.title-text {
  font-weight: bold;
  color: #409EFF;
  line-height: 60px; /* 确保标题垂直居中 */
}

.navbar-menu {
  display: flex;
  align-items: center; /* 垂直居中 */
  justify-content: flex-end; /* 保证右侧对齐 */
  height: 100%; /* 确保与左侧栏一致 */
}

.el-menu-item {
  height: 100%; /* 每个菜单项的高度 */
  display: flex;
  align-items: center; /* 垂直居中 */
}

.el-menu {
  height: 100%;
  width: auto !important;
  margin-left: auto;
}

.el-menu--horizontal {
  float: right;
}

</style>

