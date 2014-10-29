$(function() {

  $('[data-toggle="tooltip"]').tooltip();

  $('.navbar-toggle').click(function() {
    $('#sidebar-wrapper').toggleClass('toggled');
  });

});
