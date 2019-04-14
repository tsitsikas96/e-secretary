// Submit post on submit
$('#student_grade_form').on('submit', function(event) {
  event.preventDefault()
  if (checkGrade()) {
    submit_grade()
  } else {
    $('#error_message').html(
      "<span class='alert alert-warning' role='alert'> Oops! " +
        'Please enter a correct number' +
        '</span>'
    )
    $('#error_message').show()
  }
})

// checking for correct number
function checkGrade(grade) {
  var grade = parseFloat($('#grade').val())
  if (!isNaN(grade)) {
    if (grade > 10 || grade < 0) {
      return false
    }
    return true
  }
  return false
}

// AJAX for submitting grade
function submit_grade() {
  $.ajax({
    url: window.location, // the endpoint
    type: 'POST', // http method
    data: {
      grade: $('#grade').val(),
      student_id: $('#student_id').val(),
      didaskalia_id: $('#didaskalia_id').val(),
      ergasia_id: $('#ergasia_id').val(),
    }, // data sent with the post request

    // handle a successful response
    success: function(json) {
      var grade = parseFloat($('#grade').val()).toFixed(1)
      $('#submited_grade').html(grade)
      $('#grade').val('')
      $('#error_message').val('')
      $('#error_message').hide()
    },

    // handle a non-successful response
    error: function(xhr, errmsg, err) {
      // console.log(
      //   xhr.status + ': ' +
      //   xhr.responseText);
    },
  })
}

$(function() {
  // This function gets cookie with a given name
  function getCookie(name) {
    var cookieValue = null
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';')
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i])
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }
  var csrftoken = getCookie('csrftoken')

  /*
  The functions below will create a header with csrftoken
  */

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
  }

  function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host // host + port
    var protocol = document.location.protocol
    var sr_origin = '//' + host
    var origin = protocol + sr_origin
    // Allow absolute or scheme relative URLs to same origin
    return (
      url == origin ||
      url.slice(0, origin.length + 1) == origin + '/' ||
      (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
      // or any other URL that isn't scheme relative or absolute i.e relative.
      !/^(\/\/|http:|https:).*/.test(url)
    )
  }

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader('X-CSRFToken', csrftoken)
      }
    },
  })
})
