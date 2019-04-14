$(document).ready(function() {

    sessionStorage.clear(); 
    temp_save_diloseis();

    $("#table-didask tbody").on("click","tr", function() {
        var tr = $(this).closest("tr").clone();
        tr.find("td:eq(4)").remove();
        tr.find("td:last").remove();
        id = tr.find("td:eq(0)").text();
        if(check_duplicates(id)){
            alert("To μάθημα έχει προστεθεί ήδη στη δήλωση");
            return;
        }
        $("#table-dilosi tbody").append(tr);
        sessionStorage.setItem("id_" + id,id);
    });

    $("#table-dilosi tbody").on("click","tr",function() {
        var tr = $(this).closest("tr").remove().clone();
        id = tr.find("td:eq(0)").text();
        sessionStorage.removeItem("id_" + id);
    });
});

function temp_save_diloseis(){
    var length = $("#table-dilosi tbody tr").length;
    rows = $("#table-dilosi").children("tbody").children("tr");
    for(i=0 ; i< length; i++){
        id = rows.eq(i).find("td:eq(0)").text();
        sessionStorage.setItem("id_" + id,id);
    }
}

function check_duplicates(id){
    if(id === sessionStorage.getItem("id_" + id)){
        return true;
    }
    return false;
}