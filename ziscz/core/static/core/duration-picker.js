(function (jQuery) {
    jQuery(function ($) {
        $('[data-duration-picker-widget]').each(function (i, el) {
            $(el).durationPicker({
                translations: {
                    day: 'den',
                    hour: 'hodina',
                    minute: 'minuty',
                    second: 'sekunda',
                    days: 'dny',
                    hours: 'hodiny',
                    minutes: 'minuty',
                    seconds: 'sekundy',
                },
                showSeconds: true,
                showDays: false,
            });
        });
    });
})(window.jQuery);