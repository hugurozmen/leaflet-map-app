<template>
    <div>
        <select @change="set()" v-model="aselected"  class="form-control">
            <option 
            :selected="type == 'Camii'"
            v-for="type in types"
            :key="type">
                {{type}}
            </option>
        </select>
    </div>
</template>

<script>
import axios from "axios";
export default {
    
    data() {
        return{
            aselected: '',
            types: []
        }
    },
    mounted(){
        this.getTypes()
    },
    methods: {
        //get place type from database
        getTypes(){
            axios
                .get('api/v1/get-types')
                .then((response) => {
                    this.$store.state.types = response.data;
                    console.log(response.data);
                    for (let i=0; i<this.$store.state.types.length; i++){

                        this.types.push(this.$store.state.types[i].type)
                       
                    }
                })
        },
        set(){
            this.$store.state.types = this.aselected 
        }
    }
}
</script>