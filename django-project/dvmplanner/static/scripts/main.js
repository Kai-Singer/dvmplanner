function toggleNavbar() {
  const navbar = document.getElementById('navbar');
  const content = document.getElementById('content');
  const img = document.getElementById('navbar_hide_button_img');

  if (navbar.classList.contains('shown_navbar')) {
    navbar.classList.remove('shown_navbar');
    content.classList.remove('hidden_content');
    img.src = staticMenuIcon;
    img.alt = 'Open Menu';

  } else {
    navbar.classList.add('shown_navbar');
    content.classList.add('hidden_content');
    img.src = staticCloseMenuIcon;
    img.alt = 'Close Menu';
  }
}

function toggleUserMenu() {
  const usermenu = document.getElementById('usermenu');
  if (usermenu.classList.contains('hidden_usermenu')) {
    usermenu.classList.remove('hidden_usermenu');
  } else {
    usermenu.classList.add('hidden_usermenu')
  }
}