<template>
    <div>
        <full-calendar
            ref="calendar"
            :config="config"
            :editable="editable"
        ></full-calendar>
    </div>
</template>

<script>
    import {FullCalendar} from 'vue-full-calendar'
    import 'fullcalendar/dist/fullcalendar.css'
    import {mapState} from 'vuex'
    import Axios from 'axios'
    import reverse from 'django-reverse'
    import moment from 'moment'
    import toastr from 'toastr'

    /**
     * @param start Date
     * @param end Date
     * @param timezone String
     * @returns {{}} object
     */
    const toParams = (start, end, timezone) => ({
        start: start.toISOString(),
        end: end.toISOString(),
        timezone,
    });

    export default {
        name: "App",
        components: {
            FullCalendar
        },
        computed: mapState(['editable', 'trans', 'locale']),
        mounted() {
            this.$refs.calendar.fireMethod('option', {
                buttonText: {
                    agendaWeek: this.trans.week,
                    listDay: this.trans.day_detail,
                    month: this.trans.month,
                },
            });
            this.$refs.calendar.fireMethod('option', {locale: this.locale});
        },
        data() {
            return {
                config: {
                    themeSystem: 'bootstrap4',
                    locale: 'cs',
                    timezone: 'Europe/Prague',
                    // editable: this.editable,
                    selectable: false,
                    height: 'auto',
                    businessHours: {
                        // days of week. an array of zero-based day of week integers (0=Sunday)
                        dow: [0, 1, 2, 3, 4, 5, 6], // Monday - Thursday

                        start: '08:00', // a start time (10am in this example)
                        end: '20:00', // an end time (6pm in this example)
                    },
                    minTime: '06:00:00',
                    maxTime: '22:00:00',
                    timeFormat: 'H(:mm)', // uppercase H for 24-hour clock
                    slotLabelFormat: 'HH(:mm)',
                    columnHeaderFormat: 'ddd D.M.',
                    nowIndicator: true,
                    eventLimit: 3, // for all non-agenda views
                    themeButtonIcons: {
                        prev: '',
                        next: '',
                        prevYear: 'left-double-arrow',
                        nextYear: 'right-double-arrow'
                    },
                    // buttonText in created()
                    buttonText: {
                        prev: '<',
                        next: '>',
                    },
                    defaultView: 'agendaWeek',
                    header: {
                        center: 'title',
                        right: 'listDay,agendaWeek,month',
                        left: 'prev,next'
                    },
                    views: {
                        week: {
                            allDaySlot: false,
                            slotEventOverlap: true,
                        },
                        agendaWeek: {
                            allDaySlot: false,
                            slotEventOverlap: true,
                        },
                    },
                    eventRender(event, element, view) {
                        var title = element.find('.fc-title');
                        element.popover({
                            title: moment(event.start).format("HH:mm - DD.MM.YYYY"),
                            content: event.description || title.text(),
                            delay: 400,
                            placement: 'auto',
                            trigger: 'hover',
                            container: false,
                        });
                        if (event.done) {
                            element.find('.fc-time').append('<span class="float-right font-weight-bold">&check;</span>');
                            element.css({color: '#d7d7d7'});
                        } else if (event.its_too_late_to_apologize) {
                            element.find('.fc-time').append('<span class="float-right font-weight-bold">&cross;</span>');
                            element.css({color: '#721c24', backgroundColor: '#f5c6cb', borderColor: '#721c24'});
                        }
                    },
                    eventDrop(event, delta, revertFunc, jsEvent, ui, view) {
                        Axios.post(reverse('api:calendar_event_start_change'), {
                            id: event.id,
                            start: moment(event.start).local().format(),
                        }).then(({data}) => {
                            if (!data.success) {
                                revertFunc();
                                toastr.warning(data.message);
                            } else data.message && toastr.success(data.message);
                        }).catch(revertFunc.bind(this))
                    },
                    eventResize(event, delta, revertFunc, jsEvent, ui, view) {
                        Axios.post(reverse('api:calendar_event_end_change'), {
                            id: event.id,
                            end: moment(event.end).local().format(),
                        }).then(({data}) => {
                            if (!data.success) {
                                revertFunc();
                                toastr.warning(data.message);
                            } else data.message && toastr.success(data.message);
                        }).catch(revertFunc.bind(this))
                    },
                    navLinks: true,
                    eventSources: [
                        {
                            /**
                             *
                             * @param start Date
                             * @param end Date
                             * @param timezone
                             * @param callback
                             */
                            events(start, end, timezone, callback) {
                                Axios.get(reverse('api:calendar_cleaning'), {params: toParams(start, end, timezone)}).then(response => {
                                    callback(response.data)
                                })
                            },
                            textColor: 'white',
                        },
                        {
                            events(start, end, timezone, callback) {
                                Axios.get(reverse('api:calendar_feeding'), {params: toParams(start, end, timezone)}).then(response => {
                                    callback(response.data)
                                })
                            },
                        },
                    ]
                }
            }
        },

    }
</script>

<style scoped>

</style>