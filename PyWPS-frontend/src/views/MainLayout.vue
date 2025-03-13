<!--src/views/MainLayout.vue-->
<template>
    <el-container style="height: 100vh;">
        <el-header>
            <NavBar @toggle-files-drawer="toggleDrawer" @toggle-toolbox="toggleToolbox"
                @show-knowledge-graph="showKnowledgeGraph" @reset-view="resetView"
                @show-operator-overview="showOperatorOverview" @show-operator-workflow="showOperatorWorkflow" />
        </el-header>
        <el-container>
            <el-aside width="200px">
                <LayerManagement />
            </el-aside>
            <el-main>
                <!-- 根据状态显示视图 -->
                <MapContainer
                    v-if="!isKnowledgeGraphVisible && !isOperatorOverviewVisible && !isOperatorWorkflowActive" />
                <KnowledgeGraph v-else-if="isKnowledgeGraphVisible" />
                <OperatorOverview v-else-if="isOperatorOverviewVisible" />
                <!-- 使用新的变量来控制 OperatorWorkflow 画布区域 -->
                <OperatorWorkflow v-else-if="isOperatorWorkflowActive" />
            </el-main>
            <!-- 工具箱区域，根据 isToolboxVisible、isOperatorDetailVisible 和 isWorkflowIdentifierVisible 控制显示内容 -->
            <OperatorToolbox v-if="isToolboxVisible && !isOperatorDetailVisible" :toggleToolbox="toggleToolbox"
                :is-toolbox-visible="isToolboxVisible" v-model:activeTab="toolboxActiveTab" />

            <OperatorIdentifier v-if="isOperatorDetailVisible" :toggleToolbox="toggleToolbox" />

            <WorkflowIdentifier v-if="isWorkflowIdentifierVisible" :toggleToolbox="toggleToolbox" />

        </el-container>
        <el-drawer title="导入数据" v-model="isDrawerVisible" direction="rtl" custom-class="drawer-class" size="1200px">
            <FilesDrawer @update:filesContainerVisible="isDrawerVisible = false" />
        </el-drawer>
    </el-container>
</template>

<script setup>
import { ref, watch, onMounted, nextTick, provide } from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';
import { useDrawerRoute } from '@/composables/useDrawerRoute';

import NavBar from '../components/NavBar.vue';
import FilesDrawer from '../components/FilesDrawer.vue';
import OperatorToolbox from '../components/OperatorToolbox.vue';
import OperatorIdentifier from '../components/OperatorIdentifier.vue';
import KnowledgeGraph from '@/components/KnowledgeGraph.vue';
import MapContainer from '../components/MapContainer.vue';
import OperatorOverview from '../components/OperatorOverview.vue';
import LayerManagement from '@/components/LayerManagement.vue';
import OperatorWorkflow from '@/components/OperatorWorkflow.vue';
import WorkflowIdentifier from '@/components/WorkflowIdentifier.vue';

// Store, Route, and Router
const store = useStore();
const route = useRoute();
const router = useRouter();

// Drawer and Toolbox states
const { isDrawerVisible, toggleDrawer } = useDrawerRoute('/files');
const isKnowledgeGraphVisible = ref(false);
const isOperatorOverviewVisible = ref(false);
const isToolboxVisible = ref(false);
const isOperatorDetailVisible = ref(false);
// 新增：画布区域的状态
const isOperatorWorkflowActive = ref(false);
const toolboxActiveTab = ref('toolbox');
const isWorkflowIdentifierVisible = ref(false);

// Toolbox Control Object
const showToolboxAndSwitchToProcessedData = () => {
    console.log("调用 showToolboxAndSwitchToProcessedData 方法");
    isOperatorDetailVisible.value = false;
    if (!isToolboxVisible.value) {
        isToolboxVisible.value = true;
    }
    nextTick(() => {
        toolboxActiveTab.value = 'results'; // 切换到 Processed Data 标签页
        console.log("切换到 Processed Data 标签页");
    });
};
const toolboxControl = { showToolboxAndSwitchToProcessedData };
provide('toolboxControl', toolboxControl);

// View Management
const toggleToolbox = (identifier = null, type = 'operator') => {
    if (identifier) {
        if (type === 'workflow') {
            isToolboxVisible.value = false;
            isWorkflowIdentifierVisible.value = true;
            isOperatorWorkflowActive.value = false; // 关闭画布
            router.push({
                name: 'WorkflowIdentifier',
                params: { Identifier: identifier }
            });
        } else {
            // 先关闭 OperatorToolbox
            isToolboxVisible.value = false;
            isOperatorWorkflowActive.value = false; // 关闭画布
            nextTick(() => {
                // 确保 OperatorIdentifier 正确显示
                isOperatorDetailVisible.value = true;
                isToolboxVisible.value = true;  // 重新打开工具箱，保证 OperatorIdentifier 也能显示
                router.push({
                    name: 'OperatorIdentifier',
                    params: { Identifier: identifier },
                });
            });
        }
    } else {
        if (isToolboxVisible.value) {
            // 关闭工具箱，但不影响 OperatorIdentifier
            isToolboxVisible.value = false;
        } else {
            // 重新打开工具箱，同时关闭画布
            isToolboxVisible.value = true;
            isOperatorWorkflowActive.value = false; // 关闭画布
        }
    }
};



// 重置工具箱/视图相关状态，但不重置画布区域状态
const resetView = () => {
    isKnowledgeGraphVisible.value = false;
    isOperatorOverviewVisible.value = false;
    isOperatorDetailVisible.value = false;
    isWorkflowIdentifierVisible.value = false;
    // 不重置 isOperatorWorkflowActive 以保持画布区域
};
// 提供 resetView 方法给子组件
provide('resetView', resetView);
const closeToolbox = () => {
    isToolboxVisible.value = false;
    isOperatorDetailVisible.value = false;
};

const showKnowledgeGraph = () => {
    resetView();
    isKnowledgeGraphVisible.value = true;
    isOperatorOverviewVisible.value = false;
    closeToolbox();
};

const showOperatorOverview = () => {

    isOperatorOverviewVisible.value = true;
    isKnowledgeGraphVisible.value = false;
    closeToolbox();
};

const showOperatorWorkflow = () => {
    resetView();
    isOperatorWorkflowActive.value = true;
    isToolboxVisible.value = false; // 确保工具箱关闭
    isOperatorDetailVisible.value = false;
    isWorkflowIdentifierVisible.value = false;
};

const showWorkflowIdentifier = (workflowId, operatorId) => {
    // 仅更新工具箱区域内容，不重置画布区域
    isOperatorDetailVisible.value = false;
    isWorkflowIdentifierVisible.value = true;
    router.push({
        name: 'WorkflowIdentifier',
        params: { workflowId, operatorId }
    });
};

provide('showWorkflowIdentifier', showWorkflowIdentifier);

// 监听路由变化（可按需调整）
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

// 获取初始数据
onMounted(() => {
    store.dispatch('operator/fetchOperators');
    console.log('工具箱控制方法已提供:', { showToolboxAndSwitchToProcessedData });
});
</script>



<style scoped>
:deep() {
    --el-color-primary: #409EFF;
    --el-color-primary-light-3: #79bbff;
    --el-color-primary-light-5: #a0cfff;
    --el-color-primary-light-7: #c6e2ff;
    --el-color-primary-light-8: #d9ecff;
    --el-color-primary-light-9: #ecf5ff;
    --el-color-primary-dark-2: #337ecc;
}

.el-container {
    background-color: #1e1e1e;
}

.el-header {
    padding: 0;
    background-color: #2d2d2d;
    border-bottom: 1px solid #404040;
}

.el-aside {
    overflow: auto;
    background-color: #2d2d2d;
    border-right: 1px solid #404040;
}

.el-main {
    padding: 0;
    height: calc(100vh - 60px);
    /* 60px是header高度 */
    overflow: hidden;
    background-color: #1e1e1e;
}

/* 文件操作抽屉样式 */
.drawer-class {
    padding-top: 0;
    background-color: #2d2d2d;
}
</style>
