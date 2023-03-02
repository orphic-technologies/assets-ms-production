$.ajax({
    url: $("#container").attr("data-url"),
    dataType: 'json',
    success: function (data) {
        Highcharts.chart("container", data);
    }
});