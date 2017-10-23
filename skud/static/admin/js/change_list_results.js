/**
* Created by artem-pc on 23.10.2017.
*/
(function($) {
$(document).ready(function($) {

    function avarage(field, field_text) {
        body = $("body");
        var hours_delay_average = 0;
        var hours_delay_average_count = 0;
        field.each(function(){
            text = $(this).text();
            if(text !== '-' && text !== '0,0') {
                hours_delay_average += parseFloat(text.replace(',', '.'));
                hours_delay_average_count += 1;
            }
        });
        hours_delay_average = (hours_delay_average/hours_delay_average_count).toFixed(2);
        if(isNaN(hours_delay_average))
            hours_delay_average = '0.0';
        var replaced = body.html().replace('#' + field_text + '#', hours_delay_average);
        body.html(replaced);
    }

    avarage($('.field-hours_delay'), 'field-hours_delay_average');
    avarage($('.field-hours_way_out'), 'field-hours_way_out_average');
    avarage($('.field-hours_duration'), 'field-hours_duration_average');

});
})(django.jQuery);