var dilosi = [];
$("#submit-button").ready(function(){
    $("#submit-button").on("click",function(){
        var length = $("#table-dilosi tbody tr").length;
        rows = $("#table-dilosi").children("tbody").children("tr");
        for(i=0 ; i< length; i++){
            dilosi.push(rows.eq(i).find("td:eq(0)").text());
        }
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
            data: {"dilosi[]" : dilosi},
            success: function(data){
                dilosi = [];
                alert("Δήλωση Επιτυχής");
            },
            error: function(data){
                alert("Δήλωση Ανεπιτυχής");
            }
        });
    });
});
$("#clear-button").ready(function(){
    $("#clear-button").on("click",function(){
        sessionStorage.clear();
        $("#table-dilosi tbody").empty();
        dilosi = [];
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
            data: {"dilosi[]" : dilosi},
            success: function(data){
                alert("Καθαρισμός Επιτυχής");
            },
            error: function(data){
                alert("Καθαρισμός Ανεπιτυχής");
            }
        });
    });
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}