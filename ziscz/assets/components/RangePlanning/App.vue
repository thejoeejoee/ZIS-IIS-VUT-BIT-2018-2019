<template>

    <div class="card">
        <div class="card-header">
            Planning
        </div>
        <div class="card-body">
            <input type="hidden" name="date_range" v-model="serialized">

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
            <div class="form-group">
                <div class="row justify-content-center" v-if="actual === 'One time'">
                    <div class="col-4 text-center">
                        datetime
                        <datetime v-model="date" :auto="true" type="datetime" input-class="form-control text-center"></datetime>
                    </div>
                </div>
                <div class="row justify-content-center" v-if="rangeUnit">
                    <div class="col-3 text-right">
                        first
                        <datetime
                            v-model="dateFrom"
                            :auto="true"
                            :minDatetime="minDatetime"
                            :maxDatetime="dateTo"
                            type="datetime"
                            input-class="form-control text-right"
                        ></datetime>
                    </div>
                    <div class="col-1 text-center">-</div>
                    <div class="col-3">
                        end of plan
                        <datetime
                            v-model="dateTo"
                            :auto="true"
                            :minDatetime="dateFrom"
                            input-class="form-control"
                        ></datetime>
                    </div>
                </div>
                <hr v-if="rangeUnit">

                <div class="row">
                    <div class="col" :class="rangeUnit === 'day' ? 'text-left' : 'text-center'">
                        <template v-for="(item, i) in range">
                            <span class="badge badge-primary">
                                {{ item | moment("HH:mm | dd DD.MM.YYYY") }}
                            </span>
                            <br v-if="rangeUnit === 'day' && i % 7 === 6">
                            <br v-if="rangeUnit === 'week' && i % 4 === 3">
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState} from 'vuex'
    import {Datetime} from 'vue-datetime'
    import 'vue-datetime/dist/vue-datetime.css'
    import PR from 'power-range'


    export default {
        name: "App",
        components: {
            datetime: Datetime
        },
        data: () => {
            let date = new Date();
            date.setHours(date.getHours() + 1);
            date.setMinutes(0);
            return ({
                modes: [
                    'One time',
                    'Daily',
                    'Weekly',
                    'Monthly',
                    // 'Custom',
                ],
                actual: 'One time',
                dateFrom: date.toISOString(),
                dateTo: null,
                date: date.toISOString(),
            })
        },
        computed: {
            ...mapState([]),
            range() {
                if (!(this.dateFrom && this.dateTo && this.rangeUnit)) return [];
                return PR.create(
                    new Date(this.dateFrom),
                    new Date(this.dateTo),
                    {unit: this.rangeUnit}
                )
            },
            rangeUnit() {
                return {
                    'Daily': 'day',
                    'Weekly': 'week',
                    'Monthly': 'month',
                }[this.actual]
            },
            serialized() {
                return JSON.stringify({
                    mode: this.actual,
                    range: (
                        this.actual === 'One time' ?
                            [new Date(this.date),] :
                            this.range
                    ).map((date) => date.getTime() / 1000),
                })
            },
            minDatetime() {
                return new Date().toISOString();
            }
        },
        methods: {},
        mounted() {
        }
    }
</script>

<style scoped>

</style>