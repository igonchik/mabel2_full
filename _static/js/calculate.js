$(function () {
    var calc_id = $('#calc_id').val();
    var timerId = setInterval(function () {
        $.ajax ({
            type: "GET",
            url: "/get_calc_result/"+ calc_id+ "/",
            dataType: "html",
            success: function(data) {
                data = $.parseJSON(data);
                if (data.ready)
                {
                    clearInterval(timerId);
                    $.ajax ({
                        type: "GET",
                        url: "/getstat_tempalte/"+ calc_id+ "/",
                        success: function(data) {
                            $('.column-2').html(data);
                            $('#ordersaw').click(function() {
                                order_saw();
                            });
                        },
                        failure: function(error) {
                            $('.column-2').html(error_div);
                            return 1;
                        },
                        error: function(error) {
                            $('.column-2').html(error_div);
                            return 1;
                        }
                    });
                }
            },
            failure: function(error) {
                $('.column-2').html(error_div);
                return 1;
            },
            error: function(error) {
                $('.column-2').html(error_div);
                return 1;
            }
        });
    }, 3000);
});