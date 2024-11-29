import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export function initializeTianditu(container) { // 接收 map 容器
    let map = L.map(container, {
        minZoom: 3,
        maxZoom: 18,
        center: L.latLng(33.89945, 103.40769),
        zoom: 5,
        zoomControl: false,
        attributionControl: false,
    });

    const createTileLayer = (layer, subLayer) => {
        return L.tileLayer(`http://t{s}.tianditu.gov.cn/${layer}_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=${subLayer}&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TileMatrix={z}&TileRow={y}&TileCol={x}&tk=a9ddfcb66bcde64828a714ef5d4456e3`, {
            subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
            tileSize: 256,
            minZoom: 3,
            maxZoom: 18,
        });
    };

    // Tianditu Layers
    const vecLayer = createTileLayer('vec', 'vec');
    const imgLayer = createTileLayer('img', 'img');
    const terLayer = createTileLayer('ter', 'ter');
    const vecAnnotationLayer = createTileLayer('cva', 'cva');
    const imgAnnotationLayer = createTileLayer('cia', 'cia');
    const terAnnotationLayer = createTileLayer('cta', 'cta');

    // OpenStreetMap Layer with English Labels
    const osmLayer = L.tileLayer('https://tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', {
        subdomains: ['a', 'b', 'c'],
        tileSize: 256,
        minZoom: 3,
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    const esriSatelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; <a href="https://www.esri.com/">Esri</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});


    // Mapbox Layer (requires an access token)
    // const mapboxLayer = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox-official/ckpqknefy216x17t9b07w8xmf/tiles/{z}/{x/2}/{y/2}?access_token=pk.eyJ1IjoibWFwYm94LW9mZmljaWFsIiwiYSI6ImNrcHBnMG5yMDA2eWgyb2s5MDI4NG10OXAifQ.S65o8bcu6oqsp6HQnWYJfw', {
    //     attribution: '&copy; <a href="https://www.mapbox.com/about/maps/">Mapbox</a>',
    //     id: 'mapbox/streets-v11', // Map style (e.g. 'streets-v11', 'satellite-v9', etc.)
    //     tileSize: 512,
    //     zoomOffset: -1,
    //     accessToken: 'your_mapbox_access_token' // Replace with your Mapbox access token
    // });


    // Google Maps Layer (requires Google Maps API Key)
    // const googleLayer = L.gridLayer.googleMutant({
    //     maxZoom: 19,
    //     type: 'roadmap',  // Other types: 'satellite', 'hybrid', 'terrain'
    //     attribution: '&copy; <a href="https://www.google.com/permissions/geoguidelines/">Google</a>'
    // });

    // OpenTopoMap Layer (open source topographic map)
    const openTopoMapLayer = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.opentopomap.org/copyright">OpenTopoMap</a>'
    });

    // CartoDB Layers with multiple styles
    const cartoDBLayerLight = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://carto.com/attributions">CartoDB</a>'
    });

    const cartoDBLayerDark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://carto.com/attributions">CartoDB</a>'
    });

    // Stamen Design Maps
    // const stamenTerrainLayer = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://stamen.com">Stamen Design</a>',
    //     subdomains: ['a', 'b', 'c'],
    //     tileSize: 256,
    //     minZoom: 3,
    //     maxZoom: 18,
    // });
    //
    // const stamenTonerLayer = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://stamen.com">Stamen Design</a>',
    //     subdomains: ['a', 'b', 'c'],
    //     tileSize: 256,
    //     minZoom: 3,
    //     maxZoom: 18,
    // });
    //
    // const stamenWatercolorLayer = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg', {
    //     attribution: '&copy; <a href="https://stamen.com">Stamen Design</a>',
    //     subdomains: ['a', 'b', 'c'],
    //     tileSize: 256,
    //     minZoom: 3,
    //     maxZoom: 18,
    // });

    // Esri Basemaps
    const esriStreetsLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; <a href="https://www.esri.com">Esri</a>',
        tileSize: 256,
        minZoom: 3,
        maxZoom: 18,
    });

    const esriTopographicLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; <a href="https://www.esri.com">Esri</a>',
        tileSize: 256,
        minZoom: 3,
        maxZoom: 18,
    });

    const esriNatGeoLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}', {
        attribution: '&copy; <a href="https://www.esri.com">Esri</a>',
        tileSize: 256,
        minZoom: 3,
        maxZoom: 18,
    });

    // // OpenMapTiles
    // const openStreetMapBrightLayer = L.tileLayer('https://tiles.nextzen.org/tilezen/bright/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://nextzen.org">Nextzen</a>',
    //     tileSize: 256,
    //     minZoom: 3,
    //     maxZoom: 18,
    // });
    //
    // const openStreetMapPositronLayer = L.tileLayer('https://tiles.nextzen.org/tilezen/positron/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://nextzen.org">Nextzen</a>',
    //     tileSize: 256,
    //     minZoom: 3,
    //     maxZoom: 18,
    // });



    //  const cartoDBLayerVoyager = L.tileLayer('https://{s}.basemaps.cartocdn.com/voyager/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://carto.com/attributions">CartoDB</a>'
    // });
    //
    // const cartoDBLayerPositron = L.tileLayer('https://{s}.basemaps.cartocdn.com/positron/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://carto.com/attributions">CartoDB</a>'
    // });
    //
    // const cartoDBLayerBasic = L.tileLayer('https://{s}.basemaps.cartocdn.com/basic/{z}/{x}/{y}.png', {
    //     attribution: '&copy; <a href="https://carto.com/attributions">CartoDB</a>'
    // });

    // const baseLayers = {
    //     "OSM 地图": osmLayer,
    //     "矢量图": vecLayer,
    //     "影像图": imgLayer,
    //     "地形图": terLayer,
    // };
    //
    // const overlayLayers = {
    //     "矢量注记": vecAnnotationLayer,
    //     "影像注记": imgAnnotationLayer,
    //     "地形注记": terAnnotationLayer,
    // };

    // Base layers to switch between
    const baseLayers = {
        "OSM Map": osmLayer, // OpenStreetMap
        "OSM Satellite Map":esriSatelliteLayer,
        "Vector Map": vecLayer, // Tianditu Vector Map
        "Satellite Imagery": imgLayer, // Tianditu Satellite Imagery
        "Topographic Map": terLayer, // Tianditu Topographic Map
        // "Mapbox": mapboxLayer, // Mapbox Streets
        "OpenTopoMap": openTopoMapLayer, // OpenTopoMap
        "CartoDB Light": cartoDBLayerLight, // CartoDB Light
        "CartoDB Dark": cartoDBLayerDark, // CartoDB Dark
        // "CartoDB Voyager": cartoDBLayerVoyager, // CartoDB Voyager
        // "CartoDB Positron": cartoDBLayerPositron, // CartoDB Positron
        // "CartoDB Basic": cartoDBLayerBasic, // CartoDB Basic
        // "Google Maps": googleLayer, // Google Maps
        // "Stamen Terrain": stamenTerrainLayer, // Stamen Terrain
        // "Stamen Toner": stamenTonerLayer, // Stamen Toner
        // "Stamen Watercolor": stamenWatercolorLayer, // Stamen Watercolor
        "Esri Streets": esriStreetsLayer, // Esri Streets
        "Esri Topographic": esriTopographicLayer, // Esri Topographic
        "Esri NatGeo": esriNatGeoLayer, // Esri National Geographic
        // "OpenStreetMap Bright": openStreetMapBrightLayer, // OpenStreetMap Bright
        // "OpenStreetMap Positron": openStreetMapPositronLayer, // OpenStreetMap Positron
    };

    // Overlay layers (annotations)
    const overlayLayers = {
        "Vector Annotations": vecAnnotationLayer, // Tianditu Vector Annotations
        "Satellite Annotations": imgAnnotationLayer, // Tianditu Satellite Annotations
        "Topographic Annotations": terAnnotationLayer // Tianditu Topographic Annotations
    };

    // Add the layers control to the map
    L.control.layers(baseLayers, overlayLayers).addTo(map);

    // Default map layer
    osmLayer.addTo(map); // 默认加载 OSM 图层

    return map;
}
