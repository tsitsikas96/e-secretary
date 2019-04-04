$(function () {
  $("#avatar_box").hover(
    function () {
      $('#change_avatar_button').stop().animate({
        "opacity": "1"
      }, 50);
    },
    function () {
      $('#change_avatar_button').stop().animate({
        "opacity": "0"
      }, 50);
    });
});
