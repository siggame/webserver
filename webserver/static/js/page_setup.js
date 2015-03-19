$(function() {

  $('[data-toggle="tooltip"]').tooltip();

  $('.navbar-toggle').click(function() {
    $('#sidebar-wrapper').toggleClass('toggled');
  });

  resize_home_iframes = function() {
    var boxes = $('.embed-responsive.home-content');
    var content_height = $(window).outerHeight() - $(".footer").outerHeight() - boxes.offset().top;
    $('.embed-responsive.home-content').css('padding-bottom', content_height);
  }

  $(window).resize(resize_home_iframes);
  resize_home_iframes();

});
