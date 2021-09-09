<template>
  <div id="wrapper">
    <nav class="navbar is-success">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item">
          <strong @click="isGet = true">Getir</strong>
        </router-link>
        <router-link to="/" class="navbar-item"
          ><strong @click="isGet = false">Ekle/Sil</strong></router-link
        >
      </div>
    </nav>
    <div class="columns is-multiline ">
      <div class="column is-3 box " v-show="isGet">
        <!-- <div class="field">
          <p class="control has-icons-left has-icons-right">
            <input
              class="input is-medium"
              type="text"
              v-model="type"
              placeholder="Mekan Tipi"
            />
            <span class="icon is-smal is-left">
              <i class="fas fa-map-marker"></i>
            </span>
            <span class="icon is-small is-right">
              <i class="fas fa-check"></i>
            </span>
          </p>
        </div> -->
        <dropdown-app></dropdown-app>
        <div class="field is-grouped">
          <p class="control">
            <button @click="getPoints()" class="button is-success">
              Getir
            </button>
          </p>
          <p class="control">
            <button @click="insertKml()" class="button is-primary is-outlined">
              Getir
            </button>
          </p>
        </div>
        <div v-for="place in places" v-bind:key="place.id">
          <div class="card">
            <div class="card-content">
              <div class="content">
                {{ place.name }}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-3 box" v-show="!isGet">
        <add-app></add-app>
      </div>

      <section class="section column is-9">
        <keep-alive>
          <router-view />
        </keep-alive>
      </section>
    </div>

    <footer class="footer">
      <p class="has-text-centered">Copyright (c) 2021</p>
    </footer>
  </div>
</template>

<script>
import axios from "axios";
import Add from "./views/Add.vue";
import Dropdown from "./views/Dropdown.vue"
import * as L from "leaflet";
import "leaflet-draw";
export default {
  data: function() {
    return {
      type: "",
      places: [],
      AllPlaces: [],
      mark: [],
      isGet: true,
      markerList: [],
      length: "",
    };
  },
  components: {
    addApp: Add,
    DropdownApp: Dropdown
  },
  methods: {
    getPoints() {
      let radius = this.$store.state.radius;
      let latlng = this.$store.state.LatLng;
      let type = this.$store.state.types;
      axios
        .post("api/v1/get-places", { radius, latlng, type })
        .then((response) => {
          this.places = response.data;
          this.$store.state.places = this.places;
          this.AllPlaces = this.$store.state.places;

          if (this.length != 0) {
            for (let i = 0; i < this.length; i++) {
              let layer = {};

              layer = this.$store.state.placeMap._layers[this.markerList["0"]];
              this.$store.state.placeMap.removeLayer(layer);

              this.markerList.shift();
            }
          }
          for (let i = 0; i < this.AllPlaces.length; i++) {
            var a = this.AllPlaces[i].point.split(" ");

            var lat = parseFloat(a[1].split("(")[1]);

            var lng = parseFloat(a[2]);

            this.mark.push(lng);
            this.mark.push(lat);
            let layer = L.marker(this.mark, {
              title: this.AllPlaces[i].name,
            }).addTo(this.$store.state.placeMap);
            layer.bindPopup(this.AllPlaces[i].name);
            this.mark.pop();
            this.mark.pop();
            this.markerList.push(layer._leaflet_id);
          }

          this.length = this.markerList.length;
        });
    },
    insertKml() {
      axios.get("api/v1/get-kml").then((response) => {
        const kmltext = response.data;

        const parser = new DOMParser();
        const kml = parser.parseFromString(kmltext, "text/xml");

        const track = new L.KML(kml);

        this.$store.state.placeMap.addLayer(track);
        const bounds = track.getBounds();

        this.placeMap.fitBounds(bounds);
      });
    }
  },
};
</script>

<style lang="scss">
@import "../node_modules/bulma";
.columns {
  margin-left: 1rem;
  margin-right: 0.25rem;
  margin-top: 0.25rem;
}

.fas {
  color: rgb(68, 138, 68);
}
</style>
