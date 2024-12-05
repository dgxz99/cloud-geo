<!-- src/views/MainLayout.vue -->
<template>
    <el-container style="height: 100vh;">
        <el-header>
            <NavBar @toggle-files-drawer="toggleDrawer" @toggle-toolbox="toggleToolbox"
                    @show-knowledge-graph="showKnowledgeGraph" @reset-view="resetView"
                    @show-operator-overview="showOperatorOverview"/>
        </el-header>
        <el-container>
            <el-aside width="200px">
                <layerManagement/>
            </el-aside>
            <el-main>
                <!-- 根据不同的状态显示不同的视图 -->
                <MapContainer v-if="!isKnowledgeGraphVisible && !isOperatorOverviewVisible"/>
                <KnowledgeGraph v-if="isKnowledgeGraphVisible"/>
                <OperatorOverview v-if="isOperatorOverviewVisible"/>
            </el-main>
            <!-- 工具箱和算子详情的动态显示 -->
            <OperatorToolbox v-if="isToolboxVisible && !isOperatorDetailVisible" :toggleToolbox="toggleToolbox"
                             :is-toolbox-visible="isToolboxVisible"
                             :is-operator-detail-visible="isOperatorDetailVisible"/>
            
            <OperatorIdentifier v-show="isToolboxVisible && isOperatorDetailVisible"/>
        
        </el-container>
        
        <el-drawer title="导入数据" v-model="isDrawerVisible" direction="rtl" custom-class="drawer-class" size="1200px">
            <FilesDrawer @update:filesContainerVisible="isDrawerVisible = false"/>
        </el-drawer>
    </el-container>
</template>


<script setup>
import NavBar from '../components/NavBar.vue'
import FilesDrawer from '../components/FilesDrawer.vue'
import OperatorToolbox from '../components/OperatorToolbox.vue'
import OperatorIdentifier from '../components/OperatorIdentifier.vue'
import KnowledgeGraph from '@/components/KnowledgeGraph.vue'
import MapContainer from '../components/MapContainer.vue'
import OperatorOverview from '../components/OperatorOverview.vue'

import {ref, watch, onMounted} from 'vue'
import {useStore} from 'vuex'
import {useRoute, useRouter} from 'vue-router'
import {useDrawerRoute} from '@/composables/useDrawerRoute'
import LayerManagement from "@/components/LayerManagement.vue";

const store = useStore()
const route = useRoute()
const router = useRouter()

const {isDrawerVisible, toggleDrawer} = useDrawerRoute('/files')
const isKnowledgeGraphVisible = ref(false)
const isOperatorOverviewVisible = ref(false) // 控制算子概览的显示
const isToolboxVisible = ref(false); // 是否显示工具箱
const isOperatorDetailVisible = ref(false); // 是否显示算子详情视图

// 控制算子概览视图的显示
function showOperatorOverview() {
    isOperatorOverviewVisible.value = true;
    isKnowledgeGraphVisible.value = false;
    closeToolbox(); // 关闭工具箱
}

// 控制知识图谱视图的显示
function showKnowledgeGraph() {
    isKnowledgeGraphVisible.value = true;
    isOperatorOverviewVisible.value = false;
    closeToolbox(); // 关闭工具箱
}

// 打开工具箱并切换视图
function toggleToolbox(identifier = null) {
    if (identifier) {
        isToolboxVisible.value = true;
        isOperatorDetailVisible.value = true;
        isOperatorOverviewVisible.value = false;
        isKnowledgeGraphVisible.value = false;
        router.push({name: 'OperatorIdentifier', params: {Identifier: identifier}});
    } else {
        isToolboxVisible.value = !isToolboxVisible.value;
        
        if (!isToolboxVisible.value) {
            isOperatorDetailVisible.value = false;
        }
        isOperatorOverviewVisible.value = false;
        isKnowledgeGraphVisible.value = false;
    }
}

// 重置视图到地图视图
function resetView() {
    isKnowledgeGraphVisible.value = false;
    isOperatorOverviewVisible.value = false;
    // isToolboxVisible.value = false;
    isOperatorDetailVisible.value = false;
}

// 关闭工具箱并重置视图
function closeToolbox() {
    isToolboxVisible.value = false;
    isOperatorDetailVisible.value = false;
}

watch(
    () => route.params.Identifier,
    (identifier) => {
        if (identifier) {
            isToolboxVisible.value = true;
            isOperatorDetailVisible.value = true;
        } else {
            isOperatorDetailVisible.value = false;
        }
    }
);

onMounted(() => {
    store.dispatch('operator/fetchOperators')
})
</script>

<style scoped>
.el-header {
    padding: 0;
}

.el-aside {
    overflow: auto;
}

/* 文件操作抽屉样式 */
.drawer-class {
    padding-top: 0;
}

.el-main {
    padding: 0;
}
</style>