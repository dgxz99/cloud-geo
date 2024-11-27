<!-- src/components/OperatorToolbox.vue -->
<template>
    <div class="toolbox-container">
        <el-tabs v-model="activeTab">
            <el-tab-pane label="工具箱" name="toolbox">
                <ul v-if="!loading">
                    <li v-for="operator in operators" :key="operator.Identifier">
                        <el-button type="text" @click="selectOperator(operator)">
                            {{ operator.Identifier }}
                        </el-button>
                    </li>
                </ul>
            </el-tab-pane>
            <el-tab-pane label="处理结果" name="results">
                <p>这里是处理结果的展示区域。</p>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
import { ref, computed, defineProps,onMounted } from 'vue';
import { useStore } from 'vuex';
// import { useRouter } from 'vue-router';
const props = defineProps({
    toggleToolbox: Function,
    isToolboxVisible: Boolean, // 接收 isToolboxVisible
    isOperatorDetailVisible: Boolean // 接收 isOperatorDetailVisible
});


const store = useStore();
// const router = useRouter();
const activeTab = ref("toolbox");

const operators = computed(() => store.state.operator.operators);
const loading = computed(() => store.state.operator.loading);

const selectOperator = (operator) => {
    props.toggleToolbox(operator.Identifier);
};

onMounted(() => {
    console.log("OperatorToolbox Mounted: Operators =", operators.value);
});



</script>



<style scoped>
.toolbox-container {
    padding: 20px;
    height: calc(100vh - 100px);
    overflow-y: auto;
    width: 320px;
    position: relative;
    border-left: 1px solid #dcdfe6;
}

.back-button {
    position: absolute;
    top: 10px;
    left: 10px;
    font-size: 12px;
}
</style>