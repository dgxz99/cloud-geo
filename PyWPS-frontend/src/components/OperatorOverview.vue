<template>
    <div class="operator-overview">
        <!-- 搜索输入框 -->
        <el-input v-model="searchQuery" :prefix-icon="Search"
                  placeholder="Search operators..." clearable @clear="fetchOperators"
                  @input="filterOperators"
                  style="margin-bottom: 10px;">
        </el-input>
        
        <!-- 表格部分 -->
        <div class="table-container">
            <div class="table-wrapper">
                <el-table :data="paginatedOperators">
                    <!-- 在Title列添加 show-overflow-tooltip -->
                    <el-table-column
                        prop="Identifier"
                        label="Operator Name"
                        width="230"
                        sortable
                        show-overflow-tooltip
                    ></el-table-column>
                    <el-table-column
                        prop="Abstract"
                        label="Operator Description"
                        show-overflow-tooltip
                    ></el-table-column>
                    <el-table-column
                        prop="Identifier"
                        label="Identifier"
                        width="180"
                        sortable
                    ></el-table-column>
                    <el-table-column
                        label="Actions"
                        width="150"
                    >
                        <template #default="scope">
                            <el-button
                                size="mini"
                                @click="handleOperatorClick(scope.row)"
                            >View Details
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            
            <!-- 分页部分 -->
            <div class="pagination-container">
                <span class="total">Total：{{ totalOperators }}</span>
                <el-pagination
                    background
                    layout="sizes, prev, pager, next, jumper"
                    :total="totalOperators"
                    :page-size="pageSize"
                    :current-page="currentPage"
                    :page-sizes="[15, 30, 45]"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                ></el-pagination>
            </div>
        </div>
    </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import {useStore} from 'vuex';
import {Search} from '@element-plus/icons-vue';

const store = useStore();

const searchQuery = ref('');
const paginatedOperators = ref([]);
const currentPage = ref(1);
const pageSize = ref(15);

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

.table-container {
    height: calc(100vh - 160px);
    display: flex;
    flex-direction: column;
    border: 1px solid #444;
    border-radius: 4px;
    overflow: hidden;
}

.table-wrapper {
    flex: 1;
    overflow: auto;
}

/* 表格样式 */
:deep(.el-table) {
    height: 100%;
    --el-table-bg-color: #2d2d2d;
    --el-table-tr-bg-color: #2d2d2d;
    --el-table-row-hover-bg-color: #3a3a3a;
    --el-table-header-bg-color: #2d2d2d;
    --el-table-text-color: #e0e0e0;
    --el-table-border-color: #444;
}

/* 分页样式 */
:deep(.el-pagination) {
    --el-pagination-bg-color: #2d2d2d;
    --el-pagination-button-bg-color: #2d2d2d;
    --el-pagination-button-disabled-bg-color: #2d2d2d;
    --el-pagination-text-color: #e0e0e0;
    --el-pagination-button-color: #e0e0e0;
    --el-pagination-hover-color: #409eff;
}

/* 搜索框样式 */
:deep(.el-input) {
    --el-input-bg-color: #2d2d2d;
    --el-input-text-color: #e0e0e0;
    --el-input-border-color: #444;
    --el-input-icon-color: #e0e0e0;
}

.pagination-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 10px;
    margin-right: 30%;
}

.total {
    font-size: 14px;
    color: #e0e0e0;
}
</style>
