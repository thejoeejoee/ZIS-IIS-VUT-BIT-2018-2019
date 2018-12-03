<template>
    <div class="row">
        <template
            v-for="(enclosure, i) in enclosures"
        >
            <div class="col-3">
                <div
                    :style="{backgroundColor: enclosure.enclosure_color}"
                    class="card"
                >
                    <span class="card-header text-light small d-flex justify-content-between align-items-center">
                        <a :href="url(enclosure)" class="flex-fill">
                            {{ enclosure.name }}
                        </a>
                        
                        <a
                            v-if="can_delete_enclosure && !enclosure.animals.length"
                            :href="urlDelete(enclosure)" class="btn btn-outline-danger btn-sm">
                                <img src="../../../web/static/img/icons/trash.svg" alt="" width="20">
                        </a>

                    </span>

                    <animal-list :enclosure="enclosure"/>
                    <div class="card-footer small" v-if="enclosure.last_cleaning_date" :title="trans.last_cleaning">
                        <img src="../../../web/static/img/icons/duster.svg" alt="" width="20" class="mr-1">
                        {{ enclosure.last_cleaning_date | moment("HH:mm DD.MM.YYYY") }}
                    </div>
                </div>
            </div>
            <div class="clearfix w-100" v-if="i % 4 === 3">&nbsp;</div>
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
            ...mapState(['enclosures', 'can_change_enclosure', 'can_delete_enclosure', 'trans']),
        },
        methods: {
            url(enclosure) {
                return this.can_change_enclosure ? reverse('enclosure_detail', enclosure.id) : undefined;
            },
            urlDelete(enclosure) {
                return this.can_delete_enclosure ? reverse('enclosure_delete', enclosure.id) : undefined;
            },
        }
    }
</script>

