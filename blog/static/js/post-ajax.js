// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function () {
  $('#create_comment').click(function(event){
    event.preventDefault();
    var response = grecaptcha.getResponse();

    if(response.length == 0){
        console.log('empty recaptcha');}

    else{
        console.log('validated');
        create_comment();
        grecaptcha.reset();
      }

  });
});


// $('#create_comment').on('click', function(event){
//   event.preventDefault();
//   console.log("comment added")  // sanity check
//   // create_comment();
//   alert('it just press it');
// });


function create_comment() {
    // alert($('#pk').val());
    console.log("create post is working!"); // sanity check
    $.ajax({
        url : "/post/comment/", // the endpoint
        type : "POST", // http method
        data : { author : $('#author').val(), text : $('#text').val(), pk : $('#pk').val()}, // data sent with the post request

        // handle a successful response
        success : function(data) {
            $('#author').val(''); // remove the value from the input
            $('#text').val('');
            // console.log(data); // log the returned json to the console
            console.log("success"); // another sanity check
            // $("#comments").load("/post/load_comment/");
            $('#comments').html(data);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
