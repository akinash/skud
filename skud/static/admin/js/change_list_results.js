/**
* Created by artem-pc on 23.10.2017.
*/
(function($) {
$(document).ready(function($) {

    function float_avarage(field, field_text) {
        body = $("body");
        var average = 0;
        var count = 0;
        field.each(function(){
            text = $(this).text();
            if(text !== '-' && text !== '0,0') {
                average += parseFloat(text.replace(',', '.'));
                count += 1;
            }
        });
        average = (average/count).toFixed(2);
        if(isNaN(average))
            average = '0.0';
        var replaced = body.html().replace('#' + field_text + '#', average);
        body.html(replaced);
    }

    float_avarage($('.field-hours_delay'), 'field-hours_delay_average');
    float_avarage($('.field-hours_way_out'), 'field-hours_way_out_average');
    float_avarage($('.field-hours_duration'), 'field-hours_duration_average');

});
})(django.jQuery);