$(document).ready( function(){
  $('#floatingPassword, #floatingConfirmPassword').on('keyup', function () {
    if ($('#floatingPassword').val() == $('#floatingConfirmPassword').val()) {
      $('#submitButton').prop('disabled', false);
      $('#message').hide();
    } else 
      $('#submitButton').prop('disabled', true);
      $('#message').html('Passwords Do Not Match').css('color', 'red');
  });
})

