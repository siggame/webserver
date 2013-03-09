$(function() {
  // If we're not using the sidebar, expand the main content
  if ($("#no-sidebar").length > 0) {
    $("#content").toggleClass('span9');
  }

  // If we're not using the breadcrumb, add 20px of margin to the body
  // to keep spacing the same from page to page
  if ($("#no-breadcrumb").length > 0) {
    $("#content").parent().css('margin-top', '20px');
  }

  // If the URL starts with "/weblog/" or "/about", gray out the
  // siggame tab
  if (window.location.pathname.match(/^\/weblog\//) != null ||
      window.location.pathname.match(/^\/about/) != null) {
    $("#siggame-tab").toggleClass("active");
  }

  // If the URL starts with "/profile/", gray out the profile tab
  if (window.location.pathname.match(/^\/profile/) != null) {
    $("#profile-tab").toggleClass("active");
  }

  // If the URL starts with "/competition", gray out the profile tab
  if ((window.location.pathname.match(/^\/competition/) != null) ||
      (window.location.pathname.match(/^\/repo/) != null)) {
    $("#competition-tab").toggleClass("active");
  }

  $('#your-competitions').tooltip({placement: "left", delay: 1000});

  // If the URL starts with "/invitation", gray out the profile tab
  if (window.location.pathname.match(/^\/invitation/) != null) {
    $("#invitation-tab").toggleClass("active");
  }

  // If the URL starts with "/docs" gray out the documentation tab
  if (window.location.pathname.match(/^\/docs/) != null) {
    $("#documentation-tab").toggleClass("active");
  }
});
