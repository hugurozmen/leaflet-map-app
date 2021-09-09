<template>
  <div>
    <div class="field">
      <p class="control has-icons-left has-icons-right">
        <input
          class="input is-medium"
          type="text"
          v-model="name"
          placeholder="Mekan Adı"
        />
        <span class="icon is-smal is-left">
          <i class="fas fa-map-marker"></i>
        </span>
        <span class="icon is-small is-right">
          <i class="fas fa-check"></i>
        </span>
      </p>
    </div>
    <div class="field">
      <p class="control has-icons-left has-icons-right">
        <input
          class="input is-medium"
          type="text"
          v-model="type"
          placeholder="Mekan Tipi"
        />
        <span class="icon is-smal is-left">
          <i class="fas fa-home"></i>
        </span>
        <span class="icon is-small is-right">
          <i class="fas fa-check"></i>
        </span>
      </p>
    </div>
    <div class="field">
      <p class="control has-icons-left has-icons-right">
        <input
          class="input is-medium"
          type="text"
          v-model="this.$store.state.markerCoor"
          placeholder="Koordinant"
        />
        <span class="icon is-smal is-left">
          <i class="fas fa-map-marked-alt"></i>
        </span>
        <span class="icon is-small is-right">
          <i class="fas fa-check"></i>
        </span>
      </p>
    </div>
    <div class="field is-grouped">
      <p class="control">
        <button @click="addKML()" class="button is-success">
          KML'ye Ekle
        </button>
      </p>
      <p class="control">
        <button @click="addDB()" class="button is-primary is-outlined">
          DB'ye Ekle
        </button>
      </p>
      <p class="control">
        <button @click="deleteDB()" class="button is-danger is-outlined">
          DB'den Sil
        </button>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store from "../store";
export default {
  data() {
    return {
      name: "",
      type: "",
    };
  },

  methods: {
    addKML: function() {
      //axios sent data to be added in kml

      let name = this.name;
      let type = this.type;
      let latlng = store.state.markerCoor;
      axios
        .post("api/v1/write-kml", { name, type, latlng })
        .then((response) => {
          alert("KML Dosyasına Eklendi")
        });
      store.state.placeMap.removeLayer(store.state.deleteLayer);
      this.name = ""
      this.type = ""
      store.state.markerCoor = ""
    },
    addDB: function() {
      axios
        .get('api/v1/add-db')
        .then((response) => {
          alert("KML dosyası DB'ye Aktarıldı")
        })
     
    },
    deleteDB: function() {
      let deletedName = this.name
      axios
        .post('api/v1/delete-place', {deletedName})
        .then((response) => {
          alert(deletedName+" DB'den Silindi")
        })

    }
  },
};
</script>
