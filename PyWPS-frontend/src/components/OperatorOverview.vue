<template>
    <div class="operator-overview">
        <!-- 搜索输入框 -->
        <el-input v-model="searchQuery" placeholder="搜索算子" clearable @clear="fetchOperators"
                  @input="filterOperators"
                  style="margin-bottom: 10px;">
        </el-input>
        
        <!-- 表格部分 -->
        <el-table :data="paginatedOperators" stripe>
            <!-- 在Title列添加 show-overflow-tooltip -->
            <el-table-column prop="Identifier" label="算子名称" width="180" sortable
                             show-overflow-tooltip></el-table-column>
            <el-table-column prop="Abstract" label="算子描述" show-overflow-tooltip></el-table-column>
            <el-table-column prop="Identifier" label="标识符" width="150" sortable></el-table-column>
            
            <el-table-column label="操作" width="120">
                <template #default="scope">
                    <el-button size="mini" @click="handleOperatorClick(scope.row)">查看详情</el-button>
                </template>
            </el-table-column>
        </el-table>
        
        <!-- 分页部分 -->
        <el-pagination style="margin-top: 10px;" background layout="total, sizes, prev, pager, next, jumper"
                       :total="totalOperators"
                       :page-size="pageSize" :current-page="currentPage" @size-change="handleSizeChange"
                       @current-change="handleCurrentChange"></el-pagination>
    </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import {useStore} from 'vuex';

const store = useStore();

const searchQuery = ref('');
const paginatedOperators = ref([]);
const currentPage = ref(1);
const pageSize = ref(10);

// 获取 operators 和 loading
const operators = computed(() => {
    const ops = store.state.operator.operators || [];
    return ops;
});

// 获取算子数据
const fetchOperators = async () => {
    try {
        console.log("Fetching operators...");
        await store.dispatch('operator/fetchOperators');
        console.log("Operators fetched successfully");
    } catch (error) {
        console.error("Error fetching operators:", error);
    }
};

// 总算子数量
const totalOperators = computed(() => operators.value.length);

// 过滤算子数据
function filterOperators() {
    if (searchQuery.value) {
        const lowerQuery = searchQuery.value.toLowerCase();
        paginatedOperators.value = operators.value.filter(
            operator =>
                operator.Title.toLowerCase().includes(lowerQuery) ||
                operator.Abstract.toLowerCase().includes(lowerQuery)
        );
    } else {
        updatePaginatedData();
    }
}

// 更新分页数据
function updatePaginatedData() {
    const start = (currentPage.value - 1) * pageSize.value;
    const end = start + pageSize.value;
    paginatedOperators.value = operators.value.slice(start, end);
}

// 处理分页大小变化
function handleSizeChange(newSize) {
    pageSize.value = newSize;
    currentPage.value = 1; // 重置为第一页
    updatePaginatedData();
}

// 处理当前页变化
function handleCurrentChange(newPage) {
    currentPage.value = newPage;
    updatePaginatedData();
}

// 查看算子详情
function handleOperatorClick(operator) {
    console.log("Operator clicked:", operator);
}

// 初始化操作
onMounted(async () => {
    await fetchOperators();
    updatePaginatedData();
});
</script>

<style scoped>
.operator-overview {
    padding: 16px;
}
</style>
