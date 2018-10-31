<template>
    <div class="card-deck">
        <template
            v-for="enclosure in enclosures"
        >
            <div
                :style="{backgroundColor: enclosure.enclosure_color}"
                class="card"
            >
                <span class="card-header text-light">
                    {{ enclosure.name }}
                    <small class="float-right">{{ enclosure.type_enclosure }}</small>
                </span>
                <div class="card-body">
                    <ul>
                        <li v-for="animal in enclosure.animals">
                            {{ animal.type_animal }}
                            <strong>{{ animal.name }}</strong>
                        </li>
                        <li v-if="!enclosure.animals.length">No animals in enclosure at this moment.</li>
                    </ul>
                </div>
            </div>
        </template>
    </div>
</template>

<script>
    import {mapState} from 'vuex'

    export default {
        name: "App",
        computed: mapState(['enclosures']),
    }
</script>

<style scoped>

</style>