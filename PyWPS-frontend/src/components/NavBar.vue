<!-- src/components/NavBar.vue -->
<template>
  <el-menu mode="horizontal" background-color="#FFFFFF" text-color="#000000" active-text-color="#409EFF"
    :default-active="activeIndex" class="navbar">
    <el-menu-item index="1" @click="switchComponent('files', toggleFilesDrawer)">文件</el-menu-item>
    <el-menu-item index="2" @click="switchComponent('toolbox',null,toggleToolbox)">算子工具箱</el-menu-item>
    <el-menu-item index="3" @click="switchComponent('operator-overview', null, '/operator-overview')">算子概览</el-menu-item>
    <el-menu-item index="4" @click="switchComponent('knowledge-graph', null, '/knowledge-graph')">知识图谱</el-menu-item>
    <el-menu-item index="5" @click="switchComponent('search', null, '/search')">算子溯源</el-menu-item>
    <el-menu-item index="6" @click="switchComponent('user', null, '/user')">用户</el-menu-item>
  </el-menu>
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
.navbar {
    border-bottom: 1px solid #f0f0f0;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.el-menu-item {
    font-size: 16px;
    font-weight: 500;
}

.el-menu-item:hover {
    background-color: #f5f7fa !important;
}

.el-menu-item.is-active {
    border-bottom: 2px solid #409EFF;
    color: #409EFF !important;
}
</style>


