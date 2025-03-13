// src/cesium.js

import {Ion} from 'cesium';
import 'cesium/Build/Cesium/Widgets/widgets.css';
import * as Cesium from "cesium";

Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2NjFmM2I5Ny1mYmQ3LTQzZDAtODIxZC0zNjZiZDk0MGRjZjkiLCJpZCI6MjI4MTk2LCJpYXQiOjE3MzY0MDI3OTZ9.qDi4bkyTFjyfYqRjUC6NMz7vsohooaiHRipVyjZND5I'

export function initializeCesium(container) {
    return new Cesium.Viewer(container, {
        imageryProviderViewModels: Cesium.createDefaultImageryProviderViewModels(),
        selectionIndicator: false, // 不显示选中指示器
        terrainProviderViewModels: Cesium.createDefaultTerrainProviderViewModels(),
        terrainProvider: Cesium.createWorldTerrain(), // 默认地形
        sceneMode: Cesium.SceneMode.COLUMBUS_VIEW, // 设置为2D模式
        clockViewModel: false,
        navigationHelpButton: false,
        homeButton: false,
        scene3DOnly: false,
        timeline: false,
        fullscreenButton: false,
        animation: false
    });
}

