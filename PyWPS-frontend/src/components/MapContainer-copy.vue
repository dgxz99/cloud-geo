<template>
    <div id="MapContainer" ref="mapContainer">
        <!-- 地图容器 -->
    </div>
</template>

<script>
import {initializeTianditu} from "@/tianditu"; // 天地图初始化工具
import L from "leaflet";

export default {
    name: "MapContainer",
    data() {
        return {
            map: null, // 用于存储 Leaflet 地图实例
            jsonDataUrl: "/nanan.json", // GeoJSON 文件路径
        };
    },
    mounted() {
        // 初始化天地图
        console.log("尝试初始化天地图...");
        this.map = initializeTianditu(this.$refs.mapContainer);
        
        // 加载 GeoJSON 数据并添加到地图
        this.loadGeoJSONData(this.jsonDataUrl);
    },
    beforeUnmount() {
        // 组件卸载前销毁地图实例，避免内存泄漏
        if (this.map) {
            this.map.remove();
            this.map = null;
            console.log("地图实例已销毁");
        }
    },
    methods: {
        loadGeoJSONData(url) {
            fetch(url)
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("无法加载 GeoJSON 数据：" + response.statusText);
                    }
                    return response.json();
                })
                .then((data) => {
                    // 添加 GeoJSON 数据到地图
                    const geoJsonLayer = L.geoJSON(data, {
                        style: {
                            color: "blue", // 边界颜色
                            weight: 1, // 边界宽度
                            opacity: 0.8, // 边界透明度
                        },
                        onEachFeature: (feature, layer) => {
                            // 添加弹窗显示属性信息
                            if (feature.properties && feature.properties.name) {
                                layer.bindPopup(`区域：${feature.properties.name}`);
                            }
                        },
                    });
                    geoJsonLayer.addTo(this.map);
                    
                    // 调整地图视图以适应 GeoJSON 边界
                    this.map.fitBounds(geoJsonLayer.getBounds());
                })
                .catch((error) => {
                    console.error("加载 GeoJSON 数据出错：", error);
                });
        },
    },
};
</script>

<style scoped>
#MapContainer {
    width: 100%;
    height: 100%;
}
</style>
