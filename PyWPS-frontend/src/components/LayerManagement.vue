<template>
    <div class="layer-container">
        <div class="layer-header">
            <h3>Layer</h3>
        </div>
        
        <div v-if="uploadedFiles.length" class="layer-content">
            <el-table
                :data="uploadedFiles"
                style="width: 100%"
                empty-text="No layers loaded"
            >
                <el-table-column prop="filename" label="Layer Name"></el-table-column>
                <el-table-column width="80">
                    <template #default="scope">
                        <el-button
                            type="danger"
                            size="small"
                            @click="removeLayer(scope.$index)"
                        >
                            Remove
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        
        <div v-else class="empty-state">
            <el-icon :size="48" color="#666">
                <FolderOpened/>
            </el-icon>
            <p>Load a layer to start visualizing data</p>
        </div>
    </div>
</template>

<script>
import {FolderOpened} from '@element-plus/icons-vue';

export default {
    components: {
        FolderOpened
    },
    computed: {
        uploadedFiles() {
            return this.$store.getters['fileManagement/uploadedFiles'];
        }
    },
    methods: {
        loadSampleData() {
            // 加载示例数据
            this.$store.dispatch('fileManagement/loadSampleData');
        },
        removeLayer(index) {
            this.$store.dispatch('fileManagement/removeFile', index);
        }
    }
};
</script>

<style scoped>
.layer-container {
    padding: 16px;
    height: calc(100% - 60px);
    display: flex;
    flex-direction: column;
}

.layer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

h3 {
    color: #ffffff;
    font-size: 16px;
    margin: 0;
}

.layer-content {
    flex: 1;
    overflow: auto;
}

.empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #666;
    text-align: center;
    padding: 20px;
}

.empty-state p {
    margin-top: 12px;
    font-size: 14px;
    color: #888;
}


</style>
