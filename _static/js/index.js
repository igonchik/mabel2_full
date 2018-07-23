var progressbar = '<td colspan="6" class="progress_gif"></td>';
var errorbar = '<td colspan="6" class="errorbar">Ошибка обработки данных, попробуйте выполнить операцию позже!</td>';
var progress_div = '<div class="progress_div"></div>';
var error_div = '<div class="error_div">Ошибка обработки данных, попробуйте выполнить операцию позже!</div>';

$(window).scroll(function() {
    if ($(this).scrollTop())
    {
        $('#scroll_top:hidden').stop(true, true).fadeIn();
    } else
    {
        $('#scroll_top').stop(true, true).fadeOut();
    }
});

function send_delete(e) {
    var elem = e.target;
    elem = $(elem);
    elem.parent().parent().remove();
    update_raw();
}

function edit_go(e) {
    var elem = e.target;
    var temp_el = $(elem).parent().parent().find('.len_input').parent().parent();
    $(elem).parent().parent().find('.len_input').removeClass('has-error');
    $(elem).parent().parent().find('.width_input').removeClass('has-error');
    $(elem).parent().parent().find('.count_input').removeClass('has-error');
    $(elem).parent().parent().find('.right-part').removeClass('has-error');
    $(elem).parent().parent().find('.top-part').removeClass('has-error');
    $(elem).parent().parent().find('.bottom-part').removeClass('has-error');
    $(elem).parent().parent().find('.left-part').removeClass('has-error');
    var test1 = $.isNumeric($(elem).parent().parent().find('.len_input').val());
    var test2 = $.isNumeric($(elem).parent().parent().find('.width_input').val());
    var test3 = $.isNumeric($(elem).parent().parent().find('.count_input').val());
    var test4 = $(elem).parent().parent().find('[name="border-right"]').val();
    var test5 = $(elem).parent().parent().find('[name="border-top"]').val();
    var test6 = $(elem).parent().parent().find('[name="border-bottom"]').val();
    var test7 = $(elem).parent().parent().find('[name="border-left"]').val();
    if (!test1)
        $(elem).parent().parent().find('.len_input').addClass('has-error');
    if (!test2)
        $(elem).parent().parent().find('.width_input').addClass('has-error');
    if (!test3)
        $(elem).parent().parent().find('.count_input').addClass('has-error');
    if (!(parseFloat(test4) > 0))
        $(elem).parent().parent().find('.right-part').addClass('has-error');
    if (!(parseFloat(test5) > 0))
        $(elem).parent().parent().find('.top-part').addClass('has-error');
    if (!(parseFloat(test6) > 0))
        $(elem).parent().parent().find('.bottom-part').addClass('has-error');
    if (!(parseFloat(test7) > 0))
        $(elem).parent().parent().find('.left-part').addClass('has-error');
    if (test1 && test2 && test3 && parseFloat(test4) > 0 && parseFloat(test5) > 0
        && parseFloat(test6) > 0 && parseFloat(test7) > 0) {
        if ($(elem).parent().parent().find('.btn-add-go').length > 0) {
            var html = '<button title="Изменить" type="button" class="btn btn-success btn-edit-go">' +
                '<span class="glyphicon glyphicon-pencil"></span></button> ' +
                '<button title="Изменить" type="button" class="btn btn-danger btn-rmv-go">' +
                '<span class="glyphicon glyphicon-remove"></span></button> ';
            $(elem).parent().parent().find('.btn-add-go').parent().html(html);
            temp_el.find('.btn-rmv-go').click(function(e) {
                send_delete(e);
            });
            temp_el.find('.btn-edit-go').click(function(e) {
                edit_go(e);
            });
        }
        update_raw();
        return 0;
    } else
    {
        show_error_tooltip($(elem).parent().parent().find('.action_td'));
    }
    return 1;
}

function save_saw()
{
    var elem = $.parseHTML('<tr class="saw control saw0"></tr>');
    $('#saws_rows:last-child').append(elem);
    $(elem).html(progressbar);
    $.ajax ({
        type: "GET",
        url: "/update/",
        dataType: "html",
        success: function(data) {
            $(elem).html(data);
            elem = $(elem);
            elem.find('.border-right').click(function(e){
                $(this).parent().find('.border-right').removeClass('checked');
                $(this).addClass('checked');
                $(this).parent().find('[name="border-right"]').val($(this).attr('data-value'));
            });
            elem.find('.border-top').click(function(e){
                $(this).parent().find('.border-top').removeClass('checked');
                $(this).addClass('checked');
                $(this).parent().find('[name="border-top"]').val($(this).attr('data-value'));
            });
            elem.find('.border-bottom').click(function(e){
                $(this).parent().find('.border-bottom').removeClass('checked');
                $(this).addClass('checked');
                $(this).parent().find('[name="border-bottom"]').val($(this).attr('data-value'));
            });
            elem.find('.border-left').click(function(e){
                $(this).parent().find('.border-left').removeClass('checked');
                $(this).addClass('checked');
                $(this).parent().find('[name="border-left"]').val($(this).attr('data-value'));
            });
            elem.find('.btn-add-go').click(function(e) {
                if (edit_go(e) == 0)
                    save_saw();
            });
            elem.find('.btn-rmv-go').click(function(e) {
                send_delete(e);
            });
            elem.find('.btn-edit-go').click(function(e) {
                edit_go(e);
            });
            elem.find('.color-part').tooltip();
            return 0;
        },
        failure: function(error) {
            $(elem).html(errorbar);
            return 1;
        },
        error: function(error) {
            $(elem).html(errorbar);
            return 1;
        }
    });
}


function order_saw() {

}

function print_saw() {
    $('.column-2').html(progress_div);
    var records = [];
    var csrf = $('[name="csrfmiddlewaretoken"]').val();
    var material_uid = $('#material_uid').val();
    var edge_uid = $('#edge_uid').val();
    $('.saw.control').each(function() {
        var saw = new Object();
        elem = $(this);
        saw.len_input = elem.find('.len_input').val();
        saw.width_input = elem.find('.width_input').val();
        saw.count_input = elem.find('.count_input').val();
        saw.border_right = elem.find('[name="border-right"]').val();
        saw.border_top = elem.find('[name="border-top"]').val();
        saw.border_bottom = elem.find('[name="border-bottom"]').val();
        saw.border_left = elem.find('[name="border-left"]').val();
        saw.struct = elem.find('[name="struct"]').val();
        records.push(saw);
    });
    records.pop();

    var info = new Object();
    info.material_uid = material_uid;
    info.edge_uid = edge_uid;
    records.push(info);

    var string_saw = JSON.stringify(records);
    $.ajax ({
        type: "POST",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        },
        url: "/calculate/",
        data: string_saw,
        contentType: "application/json;charset=utf-8",
        dataType: "html",
        success: function(data) {
            $('.column-2').html(data);
            $('#ordersaw').click(function() {
                order_saw();
            });
        },
        failure: function(error) {
            $('.column-2').html(error_div);
        },
        error: function(error) {
            $('.column-2').html(error_div);
        }
    });
}

function show_error_tooltip (elem) {
    //TODO: TOOLTIP FAIL
    elem.tooltip();
}

function update_raw()
{
    $('.column-2').html(progress_div);
    var records = [];
    var csrf = $('[name="csrfmiddlewaretoken"]').val();
    var material_uid = $('#material_uid').val();
    var edge_uid = $('#edge_uid').val();
    $('.saw.control').each(function() {
        var saw = new Object();
        elem = $(this);
        saw.len_input = elem.find('.len_input').val();
        saw.width_input = elem.find('.width_input').val();
        saw.count_input = elem.find('.count_input').val();
        saw.border_right = elem.find('[name="border-right"]').val();
        saw.border_top = elem.find('[name="border-top"]').val();
        saw.border_bottom = elem.find('[name="border-bottom"]').val();
        saw.border_left = elem.find('[name="border-left"]').val();
        saw.struct = elem.find('[name="struct"]').val();
        records.push(saw);
    });
    records.pop();

    var info = new Object();
    info.material_uid = material_uid;
    info.edge_uid = edge_uid;
    records.push(info);

    var string_saw = JSON.stringify(records);
    $.ajax ({
        type: "POST",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        },
        url: "/update/",
        data: string_saw,
        contentType: "application/json;charset=utf-8",
        dataType: "html",
        success: function(data) {
            $('.column-2').html(data);
            $('#printsaw').click(function() {
                print_saw();
            });
            return 0;
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

$(function () {
    $('.border-right').click(function(e){
        $(this).parent().find('.border-right').removeClass('checked');
        $(this).addClass('checked');
        $(this).parent().find('[name="border-right"]').val($(this).attr('data-value'));
    });
    $('.border-top').click(function(e){
        $(this).parent().find('.border-top').removeClass('checked');
        $(this).addClass('checked');
        $(this).parent().find('[name="border-top"]').val($(this).attr('data-value'));
    });
    $('.border-bottom').click(function(e){
        $(this).parent().find('.border-bottom').removeClass('checked');
        $(this).addClass('checked');
        $(this).parent().find('[name="border-bottom"]').val($(this).attr('data-value'));
    });
    $('.border-left').click(function(e){
        $(this).parent().find('.border-left').removeClass('checked');
        $(this).addClass('checked');
        $(this).parent().find('[name="border-left"]').val($(this).attr('data-value'));
    });
    $('.btn-add-go').click(function(e) {
        if (edit_go(e) == 0)
            save_saw();
    });
    $('.btn-rmv-go').click(function(e) {
        send_delete(e);
    });
    $('.btn-edit-go').click(function(e) {
        edit_go(e);
    });
    $('#printsaw').click(function() {
        print_saw();
    });
    $('.color-part').tooltip();
});