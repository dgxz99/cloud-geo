<template>
    <div class="layer-container">
        <h3 style="margin: 0;">Layer</h3>
        <el-table :data="uploadedFiles" style="width: 100%">
            <!-- 显示文件名 -->
            <el-table-column prop="filename"></el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    computed: {
        uploadedFiles() {
            // 从 Vuex 获取文件列表
            return this.$store.getters['fileManagement/uploadedFiles'];
        }
    }
};
</script>

<style scoped>
h3 {
    color: #888888; /* 表头字体颜色 */
}

.el-table th {
    background-color: #f2f2f2; /* 表头背景色 */
    color: #888888; /* 表头字体颜色 */
}

.el-table td {
    font-size: 14px; /* 设置字体大小 */
    color: #555; /* 设置字体颜色 */
}
</style>
