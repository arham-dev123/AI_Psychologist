
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
  const drawer = document.getElementById("navbarMobile");
  const overlay = document.querySelector(".mobile-nav-overlay");
  const menuButton = document.querySelector(".mobile-menu-btn");

  if (!drawer) {
    return;
  }

  drawer.classList.add("is-open");
  drawer.setAttribute("aria-hidden", "false");
  document.body.classList.add("mobile-nav-open");

  if (overlay) {
    overlay.classList.add("is-open");
  }

  if (menuButton) {
    menuButton.setAttribute("aria-expanded", "true");
  }
}

function closeNav() {
  const drawer = document.getElementById("navbarMobile");
  const overlay = document.querySelector(".mobile-nav-overlay");
  const menuButton = document.querySelector(".mobile-menu-btn");

  if (!drawer) {
    return;
  }

  drawer.classList.remove("is-open");
  drawer.setAttribute("aria-hidden", "true");
  document.body.classList.remove("mobile-nav-open");

  if (overlay) {
    overlay.classList.remove("is-open");
  }

  if (menuButton) {
    menuButton.setAttribute("aria-expanded", "false");
  }
}

document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeNav();
  }
});

window.addEventListener("resize", function () {
  if (window.innerWidth > 768) {
    closeNav();
  }
});
