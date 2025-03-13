<!-- src/components/NavBar.vue -->
<template>
    <el-row class="navbar-container" type="flex" justify="space-between" align="middle">
        <!-- 左侧标题和图标 -->
        <el-col :span="8" class="navbar-title">
            <img src="../assets/favicon.png" alt="Logo" class="navbar-icon" style="width: 40px; height: 40px;">
            <span class="title-text" style="font-size:30px ">Geospatial Platform</span>
        </el-col>
        
        <!-- 右侧菜单项 -->
        <el-col :span="16" class="navbar-menu" style="display: flex; justify-content: flex-end; flex-wrap: nowrap;">
            <el-menu
                mode="horizontal"
                background-color="#FFFFFF"
                text-color="#ffffff"
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
                    <el-icon>
                        <Folder/>
                    </el-icon>
                    File Management
                </el-menu-item>
                <el-menu-item index="2" @click="switchComponent('toolbox', null, toggleToolbox)">
                    <el-icon>
                        <Tools/>
                    </el-icon>
                    Operator Toolbox
                </el-menu-item>
                <el-menu-item index="3" @click="switchComponent('operator-overview', null, '/operator-overview')">
                    <el-icon>
                        <Document/>
                    </el-icon>
                    Operator Overview
                </el-menu-item>
                <el-menu-item index="4" @click="switchComponent('knowledge-graph', null, '/knowledge-graph')">
                    <el-icon>
                        <Connection/>
                    </el-icon>
                    Knowledge Graph
                </el-menu-item>
                <el-menu-item index="5"
                              @click="switchComponent('operator-traceability', null, '/operator-traceability')">
                    <el-icon>
                        <Position/>
                    </el-icon>
                    Operator Traceability
                </el-menu-item>
                <el-menu-item index="6" @click="switchComponent('operator-workflow', null, '/operator-workflow')">
                    <el-icon>
                        <Paperclip/>
                    </el-icon>
                    Operator Workflow
                </el-menu-item>
            </el-menu>
        </el-col>
    </el-row>
</template>

<script setup>
import {ref} from 'vue'
import {defineEmits} from 'vue'
import {useNavBar} from '@/composables/useNavBar'
import {Folder, Tools, Document, Connection, Position, Paperclip} from '@element-plus/icons-vue';

const emit = defineEmits(['toggle-files-drawer', 'toggle-toolbox', 'show-knowledge-graph', 'show-operator-workflow', 'reset-view']);
const {navigate} = useNavBar()

// 记录当前打开的组件
const currentComponent = ref('')

// 切换组件的方法
const switchComponent = (component, toggleFunction = null, route = '') => {
    if (component === 'toolbox') {
        emit('toggle-toolbox');
        route = '/operator-toolbox';
    } else if (currentComponent.value === 'toolbox' && component !== 'toolbox') {
        emit('toggle-toolbox');
    }
    
    if (currentComponent.value === component && toggleFunction) {
        toggleFunction();
        return;
    }
    
    currentComponent.value = component;
    if (toggleFunction) toggleFunction();
    
    if (component === 'knowledge-graph') {
        emit('show-knowledge-graph');
    } else if (component === 'operator-overview') {
        emit('show-operator-overview');
    } else if (component === 'operator-workflow') {
        emit('show-operator-workflow');
    } else {
        emit('reset-view');
    }
    
    if (route) {
        navigate(route);
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
    align-items: center;
    position: relative;
    z-index: 1000;
    background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%);
    border-bottom: 1px solid #404040;
}

.navbar-title {
    display: flex;
    align-items: center;
    height: 100%;
}

.navbar-icon {
    margin-right: 8px;
    height: 30px;
}

.title-text {
    font-weight: bold;
    font-size: 30px;
    color: #ffffff;
    line-height: 60px;
    background: linear-gradient(90deg, #409EFF 0%, #64b5ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.navbar-menu {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 100%;
}

.el-menu {
    height: 100%;
    width: auto !important;
    margin-left: auto;
    background-color: transparent !important;
    border-bottom: none !important;
}

.el-menu--horizontal {
    float: right;
}

.el-menu-item {
    height: 100%;
    display: flex;
    align-items: center;
    margin: 0 16px;
    padding: 0 16px !important;
    border-radius: 4px;
    transition: all 0.3s ease;
    background-color: rgba(255, 255, 255, 0.1) !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.el-menu-item:hover {
    background-color: rgba(255, 255, 255, 0.2) !important;
}

.el-menu-item.is-active {
    background-color: rgba(64, 158, 255, 0.2) !important;
    color: #409EFF !important;
}

.el-menu-item .el-icon {
    margin-right: 8px;
    font-size: 18px;
}


</style>
