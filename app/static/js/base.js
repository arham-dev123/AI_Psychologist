
$(window).on('load', function () {
    $('#loading').hide();
})
function toggleModals() {
    // Hide signup modal
    $('#signupModal').modal('hide');
    // Show login modal
    $('#loginModal').modal('show');
}

function toggleModals2() {
    // Hide signup modal
    $('#loginModal').modal('hide');
    // Show login modal
    $('#signupModal').modal('show');
}

function openNav() {
  document.getElementById("navbarMobile").style.width = "250px";
  document.getElementById("main").style.marginRight = "250px";
}

function closeNav() {
  document.getElementById("navbarMobile").style.width = "0";
  document.getElementById("main").style.marginRight= "0";
}