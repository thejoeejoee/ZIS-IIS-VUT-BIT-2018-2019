<template>
    <div>
        <full-calendar
            ref="calendar"
            :config="config"
        ></full-calendar>
    </div>
</template>

<script>
    import {FullCalendar} from 'vue-full-calendar'
    import 'fullcalendar/dist/fullcalendar.css'
    import Axios from 'axios'
    import reverse from 'django-reverse'

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
        data() {
            return {
                config: {
                    themeSystem: 'bootstrap4',
                    locale: 'cs',
                    // defaultView: 'day',
                    timezone: 'Europe/Prague',
                    editable: false,
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
                    nowIndicator: true,
                    eventLimit: 3, // for all non-agenda views
                    themeButtonIcons: {
                        prev: '',
                        next: '',
                        prevYear: 'left-double-arrow',
                        nextYear: 'right-double-arrow'
                    },
                    buttonText: {
                        prev: '<',
                        next: '>',
                        agendaWeek: 'týden',
                        listDay: 'detail dne',
                        month: 'měsíc'
                    },
                    defaultView: 'listDay',
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
                            color: '#17a2b8',
                            textColor: 'white',
                        },
                        {
                            events(start, end, timezone, callback) {
                                Axios.get(reverse('api:calendar_feeding'), {params: toParams(start, end, timezone)}).then(response => {
                                    callback(response.data)
                                })
                            },
                            color: '#ffc107',
                        },
                    ]
                }
            }
        },

    }
</script>

<style scoped>

</style>