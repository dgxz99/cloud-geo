<template>
    <div class="tool-container">
        <el-button :icon="Pointer" @click="selectTool('select')" :type="tool === 'select' ? 'primary' : 'default'">
            Select
        </el-button>
        <el-button :icon="Plus" @click="selectTool('connect')" :type="tool === 'connect' ? 'primary' : 'default'">
            Connect
        </el-button>
        <el-button :icon="Delete" @click="selectTool('delete')" :type="tool === 'delete' ? 'primary' : 'default'">
            Delete
        </el-button>
        <el-button :icon="Edit" @click="editProperties">Edit</el-button>
        <!-- <el-button :icon="FolderChecked" @click="saveWorkflow">Save</el-button> -->
        <el-button :icon="FolderChecked" @click="selectTool('save')" :type="tool === 'save' ? 'primary' : 'default'">Save</el-button>
        <el-button :icon="Refresh" @click="undoAction">Refresh</el-button>
        <el-button :icon="Plus" @click="zoomIn">Zoom In</el-button>
        <el-button :icon="Minus" @click="zoomOut">Zoom Out</el-button>
    </div>
</template>

<script setup>
import {ref, defineEmits} from 'vue';
import {Edit, Plus, Pointer, Delete, FolderChecked, Refresh, Minus} from '@element-plus/icons-vue';
import {useStore} from 'vuex';

const store = useStore();
const tool = ref('select'); 

const emit = defineEmits(['tool-change']);

const selectTool = (toolName) => {
    tool.value = toolName;
    emit('tool-change', toolName);
};

const zoomIn = () => {
    const currentZoom = store.state.operator.workflow.zoomLevel;
    const newZoom = Math.min(currentZoom * 1.2, 3.0);
    store.dispatch('updateZoom', newZoom);
};

const zoomOut = () => {
    const currentZoom = store.state.operator.workflow.zoomLevel;
    const newZoom = Math.max(currentZoom / 1.2, 0.5);
    store.dispatch('updateZoom', newZoom);
};

const editProperties = () => { /* 编辑节点属性 */ };
// const saveWorkflow = () => { store.dispatch('saveWorkflow'); };
const undoAction = () => { /* 撤销操作 */ };
</script>

<style scoped>
.tool-container {
    display: flex;
    padding: 10px;
    background-color: #000000;
}

:deep(.el-button) {
    background-color: #333333;
    border-color: #333333;
    color: #ffffff;
}

:deep(.el-button:hover) {
    background-color: #444444;
    border-color: #444444;
}

:deep(.el-button:active) {
    background-color: #222222;
    border-color: #222222;
}

:deep(.el-button--primary) {
    background-color: #409eff;
    border-color: #409eff;
}
</style>
