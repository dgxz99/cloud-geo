// src/store/knowledge-graph.js
import axios from 'axios';

const state = {
    nodes: [],
    edges: [],
};

const getters = {
    getNodes: (state) => state.nodes,
    getEdges: (state) => state.edges,
};

const mutations = {
    SET_NODES(state, nodes) {
        state.nodes = nodes;
    },
    SET_EDGES(state, edges) {
        state.edges = edges;
    },
};

const actions = {
    async fetchKnowledgeGraph({ commit }, { limit = 100, skip = 0 } = {}) {
        try {
            const response = await axios.get('http://localhost:3000/api/knowledge-graph', {
                params: { limit, skip },
            });
            commit('SET_NODES', response.data.nodes);
            commit('SET_EDGES', response.data.edges);
        } catch (error) {
            console.error('Error fetching knowledge graph data:', error);
        }
    },
};

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions,
};
