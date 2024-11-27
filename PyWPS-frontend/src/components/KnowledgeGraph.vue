<template>
    <div>
        <div id="cytoscape-container" style="width: 100%; height: 700px; overflow: auto;"></div>

        <!-- 页脚内容，显示选中节点信息和加载更多按钮 -->
        <div class="footer-content">
            <!-- 左侧显示选中节点信息 -->
            <div v-if="selectedNode.id || selectedNode.label" class="info-box">
                <div class="info-row">
                    <span><strong>ID:</strong> {{ selectedNode.id || 'N/A' }}</span>
                    <span><strong>Title:</strong> {{ selectedNode.label || 'N/A' }}</span>
                </div>
            </div>
            <!-- 占位元素，用于将按钮推到右侧 -->
            <div style="flex-grow: 1;"></div>
            <!-- 右侧的 "加载更多" 按钮 -->
            <el-button class="load-more-btn" @click="loadMoreGraphData" type="primary">加载更多</el-button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';

import cytoscape from 'cytoscape';

import coseBilkent from 'cytoscape-cose-bilkent'; // 导入 cose-bilkent 插件
cytoscape.use(coseBilkent); // 注册 cose-bilkent 插件


const store = useStore();
const cy = ref(null);
const skip = ref(0);
const limit = ref(100);
const selectedNode = ref({});


const nodes = computed(() => store.getters['knowledgeGraph/getNodes']);
const edges = computed(() => store.getters['knowledgeGraph/getEdges']);

const getElements = (nodes, edges) => {
    console.log("当前节点数据:", nodes.value);
    console.log("当前边数据:", edges.value);

    return [
        ...nodes.value.map(node => ({
            data: {
                id: node.data.id,
                label: node.data.label || node.data.id,
                labels: node.data.labels
            }
        })),
        ...edges.value.map(edge => ({
            data: {
                id: `${edge.data.source}-${edge.data.target}`,
                source: edge.data.source,
                target: edge.data.target,
                label: edge.data.label || `${edge.data.source} -> ${edge.data.target}`
            }
        }))
    ];
};

const renderKnowledgeGraph = () => {
    const newElements = getElements(nodes, edges); // 先获取新的元素

    console.log("准备渲染的节点数据:", nodes.value); // 输出当前的节点数据
    console.log("准备渲染的边数据:", edges.value); // 输出当前的边数据

    if (!cy.value) {
        cy.value = cytoscape({
            container: document.getElementById('cytoscape-container'),
            elements: newElements, // 使用准备好的元素
            style: [
                {
                    selector: 'node', // 定义节点的样式
                    style: {
                        'label': 'data(label)', // 使用数据中的 label 作为节点的标签
                        'font-size': '14px',
                        'text-outline-color': '#fff',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'color': '#000',
                        'width': '60px',
                        'height': '60px',
                        'text-outline-width': 0,
                        'text-wrap': 'ellipsis',
                        'text-max-width': '50px'
                    }
                },
                {
                    selector: 'node[labels = "Database"]',
                    style: {
                        'background-color': '#f79767'
                    }
                },
                {
                    selector: 'node[labels = "Message"]',
                    style: {
                        'background-color': '#57c7e3'
                    }
                },
                {
                    selector: 'node[labels = "ComplexData"]',
                    style: {
                        'background-color': '#ecb5c9'
                    }
                },
                {
                    selector: 'node[labels = "Algorithm"]',
                    style: {
                        'background-color': '#f16667'
                    }
                },
                {
                    selector: 'node[labels = "GenericInput"]',
                    style: {
                        'background-color': '#d9c8ae'
                    }
                },
                {
                    selector: 'node[labels = "GenericOutput"]',
                    style: {
                        'background-color': '#8dcc93'
                    }
                },
                {
                    selector: 'node[labels = "GeoData"]',
                    style: {
                        'background-color': '#ffc454'
                    }
                },
                {
                    selector: 'node[labels = "Input"]',
                    style: {
                        'background-color': '#569480'
                    }
                },
                {
                    selector: 'node[labels = "Raster"]',
                    style: {
                        'background-color': '#da7194'
                    }
                },
                {
                    selector: 'node[labels = "Vector"]',
                    style: {
                        'background-color': '#4c8eda'
                    }
                },
                // 定义边的样式
                {
                    selector: 'edge',
                    style: {
                        'width': 1,
                        'font-size': '10px',
                        'line-color': '#a5abb6',
                        'target-arrow-color': '#a5abb6',
                        'target-arrow-shape': 'triangle',
                        'curve-style': 'bezier',
                        'label': 'data(label)',
                        'text-rotation': 'autorotate'
                    }
                }
            ],
            layout: {
                name: 'cose-bilkent',
                idealEdgeLength: 100,
                nodeRepulsion: 4500,
                gravity: 0.25,
                animate: 'end', // 只在结束时动画
                fit: true
            }
        });
        console.log("Cytoscape 实例创建成功");
        cy.value.on('tap', 'node', (event) => {
            const node = event.target;
            selectedNode.value = {
                id: node.data('id'),
                label: node.data('label'),
                labels: node.data('labels') || 'N/A'
            };
            console.log('Selected node:', selectedNode.value);
        });


    } else {
        cy.value.json({ elements: newElements }); // 更新元素
        cy.value.layout({ name: 'cose-bilkent', fit: true }).run();
        console.log("Cytoscape 数据更新成功");
    }
};


const loadMoreGraphData = async () => {
    skip.value += limit.value;
    await store.dispatch('knowledgeGraph/fetchKnowledgeGraph', {
        skip: skip.value,
        limit: limit.value
    });

    const newElements = getElements(nodes, edges).filter(element => {
        return !cy.value.hasElementWithId(element.data.id);
    });

    if (cy.value) {
        cy.value.add(newElements);
        // 之后使用更复杂布局
        setTimeout(() => {
            cy.value.layout({ name: 'cose-bilkent', fit: true, animate: true }).run();
        }, 2000);
    } else {
        renderKnowledgeGraph();
    }
};





onMounted(async () => {
    console.log(`初始数据加载: skip=${skip.value}, limit=${limit.value}`);
    await store.dispatch('knowledgeGraph/fetchKnowledgeGraph', {
        skip: skip.value,
        limit: limit.value
    });
    console.log("初始图数据加载成功");
    renderKnowledgeGraph();
});
</script>


<style scoped>
#cytoscape-container {
    border: 1px solid #ddd;
}

.footer-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
}

.info-box {
    display: flex;
    flex-direction: column;
    color: #333;
    flex-grow: 1;
    /* 使节点信息区域占据可用空间 */
}

.info-row {
    display: flex;
    gap: 15px;
}

.load-more-btn {
    background-color: #007bff;
    color: #fff;
    border-radius: 4px;
    padding: 5px 15px;
    text-align: right;
    /* 确保按钮对齐到右侧 */
}

.load-more-btn:hover {
    background-color: #0056b3;
    color: #fff;
}
</style>