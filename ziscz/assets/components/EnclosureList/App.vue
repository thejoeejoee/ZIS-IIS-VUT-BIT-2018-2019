<template>
    <div class="card-deck">
        <template
            v-for="enclosure in enclosures"
        >
            <div
                :style="{backgroundColor: enclosure.enclosure_color}"
                class="card"
            >
                <a class="card-header text-light" :href="url(enclosure)">
                    {{ enclosure.name }}
                    <small class="float-right">{{ enclosure.type_enclosure }}</small>
                </a>
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
    import reverse from 'django-reverse'

    export default {
        name: "App",
        computed: {
            ...mapState(['enclosures']),
        },
        methods: {
            url(enclosure) {
                return reverse('enclosure_detail', enclosure.id);
            }
        }
    }
</script>

<style scoped>

</style>