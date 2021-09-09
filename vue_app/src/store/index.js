import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    radius: "",
    LatLng: {},
    places: [],
    placeMap: "",
    latAdd: "",
    lngAdd: "",
    markerCoor: "",
    deleteLayer: "",
    nameAdd: "",
    typeAdd: "",
    circleLayer: "",
    type: "",

  },
  mutations: {
    setRadius(state, radius) {
      state.radius = radius;
    }
  },
  actions: {},
  modules: {}
})