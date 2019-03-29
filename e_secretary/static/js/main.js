window.onload = function () {

  $.getScript('static/js/sidebar.js', function () {
    setNavigation();
  });

  // $.getScript('static/js/events_feed.js', function () {
  //   generate_events();
  // });

};
