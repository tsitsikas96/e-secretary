function setNavigation() {
  let path = $(location).attr('pathname');
  // path = path.replace(/\/$/, '');
  path = decodeURIComponent(path);

  $('#menu-content a').each(function () {
    let href = $(this).attr('href');
    // href = href.replace(/\/$ (url)''/, '')
    // if (path.substring(1, href.length + 1) === href) {
    if (path === href) {
      $(this).children("li").addClass('active');
    }
  });
}

window.onload = function () {
  setNavigation();

};
