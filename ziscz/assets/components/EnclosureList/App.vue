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
                <animal-list :enclosure="enclosure"/>
                <div class="card-footer small" v-if="enclosure.last_cleaning_date" title="Last cleaning">
                    <img src="../../../web/static/img/icons/duster.svg" alt="" width="20" class="mr-1">
                    {{ enclosure.last_cleaning_date | moment("HH:mm DD.MM.YYYY") }}
                </div>
            </div>
        </template>
    </div>
</template>

<script>
    import {mapState} from 'vuex'
    import reverse from 'django-reverse'
    import AnimalList from "./AnimalList";

    export default {
        name: "App",
        components: {AnimalList},
        computed: {
            ...mapState(['enclosures']),
        },
        methods: {
            url(enclosure) {
                return reverse('enclosure_detail', enclosure.id);
            },
        }
    }
</script>

