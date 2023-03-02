$(document).ready(function () {
    count = 1;
    $("div").on('click', ".removeselected", function () {

        if (count == 1) {
            valueincookie = []
            var selectedvalue = [$(this).attr("id")];
            valueincookie = $.cookie('valueincookie')
            if (typeof valueincookie != 'undefined') {
                valueincookie = JSON.parse($.cookie('valueincookie'))
                console.log('defined', valueincookie)
            } else {
                valueincookie = []
            }
            valueincookie = valueincookie.filter((el) => !selectedvalue.includes(el));
            $.cookie('valueincookie', JSON.stringify(valueincookie), { path: '/' })
            console.log($.cookie('valueincookie'))
            location.reload();
        }
        count++;
    });
});