<!-- ParamPopup.vue -->
<template>
    <!-- 移除 el-popover，改为手动控制div位置 -->
    <div v-if="visible" class="param-popup" :style="{
        left: `${position.x}px`,
        top: `${position.y}px`
    }">
        <div class="popover-content">
            <el-table :data="paramList" size="small" @row-click="row => handleParamSelect(row)">
                <el-table-column prop="id" label="参数名" width="120" />
                <el-table-column label="连接数" width="80">
                    <template #default="{ row }">
                        {{ row.connected }}/{{ row.max }}
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script setup>
defineProps({
    visible: Boolean,
    position: Object,
    paramList: Array
});
const emit = defineEmits(['param-selected']);

const handleParamSelect = (row) => {

    // 这里是新增的console日志 ↓↓↓
    console.log('用户点击的参数数据:', row);

    emit('param-selected', row.id);
};
</script>


<style scoped>
.param-popup {
    position: fixed;
    /* 使用固定定位 */
    z-index: 9999;
    background: white;
    border: 1px solid #ebeef5;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
    padding: 12px;
}

.popover-content {
    width: 200px;
    max-height: 300px;
    overflow-y: auto;
}
</style>