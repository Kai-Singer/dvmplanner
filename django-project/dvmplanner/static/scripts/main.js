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
    usermenu.classList.add('hidden_usermenu');
  }
}

function toggleLongNote(button, notes, longNotes) {
  const parent = button.parentElement;
  const textElement = parent.querySelector('div');
  if (button.classList.contains('toggled_note')) {
    button.classList.remove('toggled_note');
    button.innerText = 'Ausklappen';
    textElement.innerText = notes;
  } else {
    button.classList.add('toggled_note');
    button.innerText = 'Einklappen';
    textElement.innerText = longNotes;
  }
}