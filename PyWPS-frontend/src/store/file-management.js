export default {
    namespaced: true,
    state() {
        return {
            uploadedFiles: [],
        };
    },
    mutations: {
        addUploadedFile(state, {filename, url}) {
            // 存储文件名和 URL
            state.uploadedFiles.push({filename, url});
        },
    },
    actions: {
        addUploadedFile({commit}, fileData) {
            commit('addUploadedFile', fileData);
        },
    },
    getters: {
        uploadedFiles(state) {
            return state.uploadedFiles;
        },
    },
};
