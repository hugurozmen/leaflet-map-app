<template>
  <div id="myMap" class="box"></div>
</template>

<script>
// @ is an alias to /src

import axios from "axios";
import * as L from "leaflet";
import "leaflet-draw";
import store from "../store";
import KML from "leaflet-kml";
export default {
  name: "myMap",
  data() {
    return {
      AllPlaces: [],
      mark: [],
      placeMap: "",
      radius: "1",
    };
  },
  components: {},
  mounted() {
    this.setupLeafletMap();
    store.state.placeMap = this.placeMap;
    this.placeMap = store.state.placeMap;
    this.setToolbar();
    //this.insertKml();
  },
  methods: {
    //initialize leaflet map
    setupLeafletMap() {
      var center = [39.962768554688, 32.836761474609];

      this.placeMap = L.map("myMap").setView(center, 13);

      L.tileLayer(
        "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaHVndXJvem1lbiIsImEiOiJja3NvanVqcnMwNWpnMnVsZ3Y2YXBlaG54In0.pIevWndwjifmRyuoi37Gbw",
        {
          attribution:
            'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
          maxZoom: 18,
          id: "mapbox/streets-v11",
          tileSize: 512,
          zoomOffset: -1,
          accessToken:
            "pk.eyJ1IjoiaHVndXJvem1lbiIsImEiOiJja3NvanVqcnMwNWpnMnVsZ3Y2YXBlaG54In0.pIevWndwjifmRyuoi37Gbw",
        }
      ).addTo(this.placeMap);

      var editableLayers = new L.FeatureGroup();
      this.placeMap.addLayer(editableLayers);

      var drawPluginOptions = {
        position: "topright",
        draw: {
          polyline: false,
          polygon: false,
          circle: true,
          rectangle: false,
          marker: true,
          circlemarker: false,
        },
        edit: {
          featureGroup: editableLayers, //REQUIRED!!
          remove: false,
        },
      };

      // Initialise the draw control and pass it the FeatureGroup of editable layers
      var drawControl = new L.Control.Draw(drawPluginOptions);
      this.placeMap.addControl(drawControl);
    },
    setToolbar() {
      var editableLayers = new L.FeatureGroup();
      this.placeMap.addLayer(editableLayers);
      this.placeMap.on("draw:created", function(e) {
        var type = e.layerType,
          layer = e.layer;

        if (type === "circle") {
          if (store.state.circleLayer != "") {
            store.state.placeMap.removeLayer(
              store.state.circleLayer
            );
          }
          store.state.radius = layer._mRadius;
          store.state.LatLng = layer._latlng;
          store.state.circleLayer = layer;
        }
        if (type === "marker") {
          if (store.state.deleteLayer != "") {
            store.state.placeMap.removeLayer(
              store.state.deleteLayer
            );
          }
          layer.bindPopup("A popup!");
          store.state.latAdd = layer._latlng["lat"];
          store.state.lngAdd = layer._latlng["lng"];
          store.state.markerCoor =
            layer._latlng["lat"] + ", " + layer._latlng["lng"];
          store.state.deleteLayer = layer;
        }

        editableLayers.addLayer(layer);
      });
    },

    insertKml() {
      axios.get("api/v1/get-kml").then((response) => {
        const kmltext = response.data;

        const parser = new DOMParser();
        const kml = parser.parseFromString(kmltext, "text/xml");

        const track = new L.KML(kml);

        this.placeMap.addLayer(track);
        const bounds = track.getBounds();

        this.placeMap.fitBounds(bounds);
      });
    },
  },
};
</script>

<style scoped>
#myMap {
  height: 600px;
}
.columns {
  margin-left: 1rem;
  margin-right: 0.25rem;
  margin-top: 0.25rem;
}
</style>
