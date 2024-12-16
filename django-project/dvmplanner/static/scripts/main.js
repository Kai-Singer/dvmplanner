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
    img.src = staticCloseIcon;
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
  const img = button.querySelector('img');
  const tooltip = button.querySelector('div');
  if (button.classList.contains('toggled_note')) {
    button.classList.remove('toggled_note');
    img.src = staticArrowRightIcon;
    img.alt = 'Expand';
    textElement.innerText = notes;
    tooltip.innerText = 'Ausklappen';
  } else {
    button.classList.add('toggled_note');
    img.src = staticArrowLeftIcon;
    img.alt = 'Shrink';
    textElement.innerText = longNotes;
    tooltip.innerText = 'Einklappen';
  }
}

document.querySelectorAll('.dropdown').forEach(dropdown => {
  const button = dropdown.querySelector('.dropdown_button');
  const content = dropdown.querySelector('.dropdown_content');

  button.addEventListener('click', () => {
    dropdown.classList.toggle('dropdown_expanded');
  });

  content.querySelectorAll('.dropdown_item').forEach(item => {
    item.addEventListener('click', () => {
      dropdown.classList.remove('dropdown_expanded');
    });
  });

  document.addEventListener('click', element => {
    if (!dropdown.contains(element.target)) {
      dropdown.classList.remove('dropdown_expanded');
    }
  });
});