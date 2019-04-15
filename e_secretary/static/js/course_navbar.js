function setCourseNavigation() {
    let path = $(location).attr('pathname');
    // path = path.replace(/\/$/, '');
    path = decodeURIComponent(path);

    $('#course_navbar li a').each(function () {
        let href = $(this).attr('href');
        // href = href.replace(/\/$ (url)''/, '')
        // if (path.substring(1, href.length + 1) === href) {
        if (path === href) {
            $(this).closest("li").addClass('active');
        }
    });
}

window.onload = function () {
    setCourseNavigation();
};