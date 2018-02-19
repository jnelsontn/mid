function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    headers: {
        "X-CSRFToken": getCookie("csrftoken")
    }
});

function call_url(url, form, success_callback, error_handler, query_string, method) {
    var post_data = (typeof query_string !== 'undefined') ? query_string : $(form).serialize();

    var error_handler = (typeof error_handler !== 'undefined') ? error_handler : error_function;
    var success_callback = (typeof success_callback !== 'undefined') ? success_callback : success_function;
    var type_method = (typeof method !== "undefined") ? method : "POST";

    $.ajax({
        url: url,
        type: type_method,
        data: post_data,
        cache: false,
        error: function (error) {
            console.log("error calling: " + url, error);
            error_handler(error);
        },
        success: function (response) {
            if (response.type === "error") {
                error_handler(response);
            }
            success_callback(response);
        }
    });
}

function success_function(response) {
    console.log(response);
}

function error_function(response) {
    console.log(response);
}
