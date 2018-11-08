<template>
    <div class="card-body">
        <draggable v-model="animals" :options="{group: 'animals'}" element="ul" class="list-unstyled small">
            <li v-for="animal in enclosure.animals">
                <img :src="'/static/img/icons/animals/' + animal.type_animal_icon" :alt="animal.type_animal" width="25">
                {{ animal.type_animal }}
                <strong>{{ animal.name }}</strong>
            </li>
            <div slot="footer" style="height: 1em;"></div>
        </draggable>
        <span v-if="!enclosure.animals.length">No animals in enclosure at this moment.</span>
    </div>
</template>
<script>
    import {mapActions} from 'vuex'
    import Draggable from 'vuedraggable'

    export default {
        name: 'AnimalList',
        components: {Draggable},
        props: {
            enclosure: {},
        },
        methods: mapActions(['updateAnimals']),
        computed: {
            animals: {
                get() {
                    return this.enclosure.animals
                },
                set(animals) {
                    this.updateAnimals({enclosure: this.enclosure, animals});
                }
            }
        }
    }
</script>
