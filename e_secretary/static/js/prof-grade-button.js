$("#submit-grades").ready(function(){
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $("#submit-grades").on('click',function(){
        $.ajax({
            method: "POST",
            url: "",
            data: {"save" : 1},
            success: function(data){
                alert("Οι βαθμολογίες αποθηκεύτηκαν");
            },
            error: function(){
                alert("Error");
            }
        });
    });
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}