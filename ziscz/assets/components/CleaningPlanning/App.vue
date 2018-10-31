<template>

    <div class="card">
        <div class="card-header">
            Planning
        </div>
        <div class="card-body">
            <div class="form-group">
                <div class="row">
                    <div class="col text-center">
                        <div class="btn-group">
                            <button
                                v-for="mode in modes"
                                @click="actual = mode"
                                :class="{active: mode === actual}"
                                class="btn btn-outline-primary"
                                type="button"
                            >
                                {{ mode }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState} from 'vuex'

    export default {
        name: "App",
        data: () => ({
            modes: [
                'One time',
                'Daily',
                'Weekly',
                'Monthly',
                'Custom',
            ],
            actual: 'One time',
        }),
        computed: {
            ...mapState([]),
        },
        methods: {},
        mounted() {
        }
    }
</script>

<style scoped>

</style>