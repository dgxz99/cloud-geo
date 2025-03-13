// joints.js 持久化管理类
let globalPaper = null;
let globalGraph = null;

export const getGlobalPaper = () => globalPaper;
export const setGlobalPaper = (paper) => {
    if (globalPaper) globalPaper.remove();
    globalPaper = paper;
};

export const getGlobalGraph = () => globalGraph;
export const setGlobalGraph = (graph) => {
    if (globalGraph) globalGraph.clear();
    globalGraph = graph;
};
