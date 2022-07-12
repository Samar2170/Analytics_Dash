
var base_link = "/get-all-installs/";   

var currentPage="1";
var nextPage;

var search = "";


$(document).ready(function() {
    console.log("ready");
    getInstalls(currentPage);
});


function changePage() {
    $(document).ready(function() {
        currentPage=nextPage;
        getInstalls();
    })
    
}

function getInstalls(page=currentPage) {
    $(document).ready(function() {
        if (search == "") {
            searchQ = ""
        } else {
            searchQ = "&query=" + search;
        }
        $.ajax({
            url: base_link +"?page="+ page + searchQ,
            type: "GET",
            success: function(data) {
                renderTable(data);
            }
        });
    })
}

function renderTable(resp, append=true) {
    $(document).ready(function() {

        console.log(resp.data.data);
        $.each(resp.data.data, function(i,item) {
            trHtml = "";


            trHtml += '<tr><td>'+item.package_name+'</td><td>' +item.carrier+ '</td><td>' +item.daily_device_installs +
                    '</td><td>' + item.active_daily_installs+'</td></tr>'
        
        $('#installs').append(trHtml);
        $('.pagination').show();
        })

    })
    nextPage=resp.next_page;
}