<!-- src/components/OperatorToolbox.vue -->
<template>
    <!-- 工具箱容器，包含工具箱和结果展示的选项卡 -->
    <div class="toolbox-container">
        <!-- 使用 el-tabs 组件进行选项卡切换，绑定到 activeTab 属性 -->
        <el-tabs v-model="activeTab">
            <!-- 处理工具箱选项卡 -->
            <el-tab-pane label="Processing Toolbox" name="toolbox">
                <!-- 如果未加载，则显示操作符列表 -->
                <ul v-if="!loading">
                    <!-- 遍历操作符数组，为每个操作符生成一个列表项 -->
                    <li v-for="operator in operators" :key="operator.Identifier">
                        <!-- 文本按钮，点击时调用 selectOperator 方法 -->
                        <el-button type="text" @click="selectOperator(operator)">
                            {{ operator.Identifier }}
                        </el-button>
                    </li>
                </ul>
            </el-tab-pane>
            
            <!-- 处理结果选项卡 -->
            <el-tab-pane label="Processed Data" name="results">
                <div v-if="processedData.length">
                    <div class="results-container">
                        <el-card v-for="(data, index) in processedData" :key="index" class="result-card">
                            <h4>{{ data.operatorName || '未知算子' }}</h4>
                            <!--<p><strong>Job ID:</strong> {{ data.jobId || '无' }}</p>-->
                            <p><strong>状态:</strong>
                                <el-tag :type="statusTagType(data.status)">
                                    {{ formatStatus(data) }}
                                </el-tag>
                            </p>
                            <p v-if="data.errorMessage"><strong>错误信息:</strong> {{ data.errorMessage }}</p>
                            <p v-if="data.completionTime"><strong>完成时间:</strong>
                                {{ formatDateTime(data.completionTime) }}</p>
                            <p v-if="data.status === 'succeeded'"><strong>下载链接:</strong>
                                <el-link
                                    :href="data.output?.OUTPUT || data.output?.out || data.output?.output"
                                    target="_blank"
                                    type="primary"
                                >
                                    点击下载
                                </el-link>
                            </p>
                        </el-card>
                    </div>
                </div>
                <p v-else>暂无处理结果，请执行算子。</p>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
// 导入 Vue 响应式编程和 Vuex 相关函数
import {ref, computed, defineProps, watch} from 'vue';
import {useStore} from 'vuex';

// 定义组件属性
const props = defineProps({
    toggleToolbox: Function, // 切换工具箱的方法
    isToolboxVisible: Boolean, // 工具箱是否可见
    isOperatorDetailVisible: Boolean, // 操作符详情是否可见
    activeTab: String // 接收 activeTab 属性
});

// 初始化 Vuex 存储
const store = useStore();
// 计算属性，从 Vuex 存储中获取操作符列表
const operators = computed(() => store.state.operator.operators);
// 计算属性，从 Vuex 存储中获取加载状态
const loading = computed(() => store.state.operator.loading);
// 绑定本地 ref 到 activeTab 属性
const activeTab = ref(props.activeTab); // 绑定到 prop

/**
 * 选择操作符方法
 * @param {Object} operator - 被选择的操作符对象
 */
const selectOperator = (operator) => {
    props.toggleToolbox(operator.Identifier);
};

// 从 Vuex 获取处理结果数组
const processedData = computed(() => store.state.operator.processedData);

// 格式化时间
const formatDateTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleString();
};

// 根据状态返回标签类型
const formatStatus = (data) => {
    if (data.status === 'succeeded') return '成功';
    if (data.status === 'failed') return '失败';
    if (data.status === 'running' || data.status === 'pending') return '执行中';
    return '未知状态';
};

const statusTagType = (status) => {
    switch (status.toLowerCase()) {
        case 'succeeded':
            return 'success';
        case 'failed':
            return 'danger';
        case 'running':
        case 'pending':
            return 'warning';
        default:
            return 'info';
    }
};


// 监听 activeTab 属性的变化，并同步到本地 ref
watch(
    () => props.activeTab,
    (newTab) => {
        activeTab.value = newTab; // 同步 prop 变化到本地 ref
    }
);
</script>

<style scoped>
/* 工具箱容器样式 */
.toolbox-container {
    padding: 20px;
    height: calc(100vh - 100px);
    overflow-y: auto;
    width: 320px;
    position: relative;
    border-left: 1px solid #dcdfe6;
}

/* 返回按钮样式，绝对定位在顶部左侧 */
.back-button {
    position: absolute;
    top: 10px;
    left: 10px;
    font-size: 12px;
}

.results-container {
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
}

.result-card {
    --el-card-padding: 0 10px 20px 20px; /* 设置上下内边距为0，左右内边距保持20px */
}

/* 单个结果卡片样式 */
.result-card {
    width: 320px; /* 卡片宽度 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 卡片阴影 */
    border-radius: 8px; /* 卡片圆角 */
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.result-card:hover {
    transform: translateY(-5px); /* 鼠标悬停提升效果 */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* 卡片标题样式 */
.result-card h4 {
    margin-bottom: 8px;
    font-size: 16px;
    font-weight: bold;
    color: #333;
}

/* 状态标签容器 */
.result-card p {
    margin: 4px 0; /* 减小段落间距 */
    font-size: 14px;
    line-height: 1.5;
    color: #666;
}

/* 状态标签样式 */
.result-card el-tag {
    display: block; /* 标签占一整行 */
    text-align: center;
    margin-top: 4px;
}

/* 下载链接样式 */
.result-card el-link {
    font-size: 14px;
    font-weight: bold;
    color: #409eff;
    display: inline-block;
    text-align: center;
    margin-top: 6px; /* 减小与其他内容的间距 */
    transition: color 0.2s ease;
}

.result-card el-link:hover {
    color: #66b1ff;
}

/* 空状态样式 */
.results-container + p {
    text-align: center;
    margin-top: 20px;
    font-size: 14px;
    color: #999;
}

</style>
