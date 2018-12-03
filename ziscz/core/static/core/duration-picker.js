(function (jQuery) {
    jQuery(function ($) {
        $('[data-duration-picker-widget]').each(function (i, el) {
            $(el).durationPicker({
                translations: JSON.parse(el.dataset.trans),
                showSeconds: true,
                showDays: false,
            });
        });
    });
})(window.jQuery);