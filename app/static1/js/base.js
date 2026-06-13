
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

function mobileNavigation() {
    var x = document.getElementById("navbarSupportedContent");
    if (x.className === "mobileicon") {
      x.className += " responsive";
    } else {
      x.className = "mobileicon";
    }
  }