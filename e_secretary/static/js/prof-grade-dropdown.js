$("#course-filter").ready(function(){
    var text = $("#course-filter option:selected").text();
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        method: "POST",
        url: "",
        data: {"text" : text},
        success: function(response){
            $("#grades-table").html(response);
        },
        error: function(data){}
    });
    $("#course-filter").on('change',function(){
        var text = $("#course-filter option:selected").text();
        $.ajax({
            method: "POST",
            url: "",
            data: {"text" : text},
            success: function(response){
                $("#grades-table").html(response);
            },
            error: function(data){}
        });
    });
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}