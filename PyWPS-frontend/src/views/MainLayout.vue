<!--src/views/MainLayout.vue-->
<template>
    <el-container style="height: 100vh;">
        <el-header>
            <NavBar
                @toggle-files-drawer="toggleDrawer"
                @toggle-toolbox="toggleToolbox"
                @show-knowledge-graph="showKnowledgeGraph"
                @reset-view="resetView"
                @show-operator-overview="showOperatorOverview"
            />
        </el-header>
        <el-container>
            <el-aside width="200px">
                <LayerManagement/>
            </el-aside>
            <el-main>
                <!-- 根据不同的状态显示不同的视图 -->
                <MapContainer
                    v-if="!isKnowledgeGraphVisible && !isOperatorOverviewVisible"
                />
                <KnowledgeGraph v-else-if="isKnowledgeGraphVisible"/>
                <OperatorOverview v-else-if="isOperatorOverviewVisible"/>
            </el-main>
            <OperatorToolbox
                v-if="isToolboxVisible && !isOperatorDetailVisible"
                :toggleToolbox="toggleToolbox"
                :is-toolbox-visible="isToolboxVisible"
                :is-operator-detail-visible="isOperatorDetailVisible"
                :activeTab.sync="toolboxActiveTab"
            />
            
            <OperatorIdentifier
                v-if="isToolboxVisible && isOperatorDetailVisible"
                :toggleToolbox="toggleToolbox"
            />
        </el-container>
        <el-drawer
            title="导入数据"
            v-model="isDrawerVisible"
            direction="rtl"
            custom-class="drawer-class"
            size="1200px"
        >
            <FilesDrawer
                @update:filesContainerVisible="isDrawerVisible = false"
            />
        </el-drawer>
    </el-container>
</template>

<script setup>
import {ref, watch, onMounted, nextTick, provide} from 'vue';
import {useStore} from 'vuex';
import {useRoute, useRouter} from 'vue-router';
import {useDrawerRoute} from '@/composables/useDrawerRoute';

import NavBar from '../components/NavBar.vue';
import FilesDrawer from '../components/FilesDrawer.vue';
import OperatorToolbox from '../components/OperatorToolbox.vue';
import OperatorIdentifier from '../components/OperatorIdentifier.vue';
import KnowledgeGraph from '@/components/KnowledgeGraph.vue';
import MapContainer from '../components/MapContainer.vue';
import OperatorOverview from '../components/OperatorOverview.vue';
import LayerManagement from '@/components/LayerManagement.vue';

// Store, Route, and Router
const store = useStore();
const route = useRoute();
const router = useRouter();

// Drawer and Toolbox states
const {isDrawerVisible, toggleDrawer} = useDrawerRoute('/files');
const isKnowledgeGraphVisible = ref(false);
const isOperatorOverviewVisible = ref(false);
const isToolboxVisible = ref(false);
const isOperatorDetailVisible = ref(false);

// // Methods for Toolbox Control
// const showToolboxAndSwitchToProcessedData = () => {
//     console.log("调用 showToolboxAndSwitchToProcessedData 方法");
//     if (!isToolboxVisible.value) {
//         console.log("工具箱当前未打开，准备打开工具箱");
//         isToolboxVisible.value = true;
//     }
//     nextTick(() => {
//         const operatorToolbox = document.querySelector('.toolbox-container .el-tabs');
//         if (operatorToolbox) {
//             const processedTab = operatorToolbox.querySelector('[aria-controls="tab-results"]');
//             processedTab?.click();
//             console.log("切换到 Processed Data 标签页");
//         }
//     });
// };

// Provide a ref for the active tab to the toolbox
const toolboxActiveTab = ref('toolbox');

// Replace the direct DOM manipulation
const showToolboxAndSwitchToProcessedData = () => {
    console.log("调用 showToolboxAndSwitchToProcessedData 方法");
    if (!isToolboxVisible.value) {
        console.log("工具箱当前未打开，准备打开工具箱");
        isToolboxVisible.value = true;
    }
    // Delay to ensure the toolbox is fully visible
    nextTick(() => {
        toolboxActiveTab.value = 'results'; // Set the active tab to 'Processed Data'
        console.log("切换到 Processed Data 标签页");
    });
};

// Toolbox Control Object
const toolboxControl = {
    showToolboxAndSwitchToProcessedData
};

// Provide the control object for child components
provide('toolboxControl', toolboxControl);

// View Management
const toggleToolbox = (identifier = null) => {
    console.log("调用 toggleToolbox，参数 identifier:", identifier);
    if (identifier) {
        isToolboxVisible.value = true;
        isOperatorDetailVisible.value = true;
        router.push({name: 'OperatorIdentifier', params: {Identifier: identifier}});
    } else {
        isToolboxVisible.value = !isToolboxVisible.value;
        isOperatorDetailVisible.value = false;
    }
};

const resetView = () => {
    isKnowledgeGraphVisible.value = false;
    isOperatorOverviewVisible.value = false;
    isOperatorDetailVisible.value = false;
};

const closeToolbox = () => {
    isToolboxVisible.value = false;
    isOperatorDetailVisible.value = false;
};

const showKnowledgeGraph = () => {
    isKnowledgeGraphVisible.value = true;
    isOperatorOverviewVisible.value = false;
    closeToolbox();
};

const showOperatorOverview = () => {
    isOperatorOverviewVisible.value = true;
    isKnowledgeGraphVisible.value = false;
    closeToolbox();
};

// Watch for route changes
watch(
    () => route.params.Identifier,
    (identifier) => {
        console.log("监听路由变化，identifier:", identifier);
        if (identifier) {
            isToolboxVisible.value = true;
            isOperatorDetailVisible.value = true;
        } else {
            isOperatorDetailVisible.value = false;
        }
    }
);

// Fetch initial data on mount
onMounted(() => {
    store.dispatch('operator/fetchOperators');
    console.log('工具箱控制方法已提供:', {showToolboxAndSwitchToProcessedData});
});
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
   