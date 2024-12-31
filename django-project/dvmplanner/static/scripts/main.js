const profile_button = document.getElementById('profile_button');
const usermenu = document.getElementById('usermenu');

profile_button.addEventListener('click', () => {
  usermenu.classList.toggle('hidden_usermenu');
});

document.addEventListener('click', element => {
  if (!(usermenu.contains(element.target) || profile_button == element.target || profile_button.contains(element.target))) {
    usermenu.classList.add('hidden_usermenu');
  }
});

function toggleNavbar() {
  const navbar = document.getElementById('navbar');
  const content = document.getElementById('content');
  const img = document.getElementById('navbar_hide_button_img');

  if (navbar.classList.contains('shown_navbar')) {
    navbar.classList.remove('shown_navbar');
    content.classList.remove('hidden_content');
    img.src = staticMenuIcon;
    img.alt = 'Open menu';

  } else {
    navbar.classList.add('shown_navbar');
    content.classList.add('hidden_content');
    img.src = staticCloseIcon;
    img.alt = 'Close menu';
  }
}

function closeFloatingWindows() {
  const bg = document.getElementById('floating_background')
  bg.classList.remove('shown_floating_window');
  
  document.querySelectorAll('.floating_container').forEach(floatingWindow => {
    floatingWindow.classList.remove('shown_floating_window');
  });
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

function formDropdownSelect(item, key) {
  const dropdown = item.parentElement.parentElement;
  const parent = dropdown.parentElement;
  const button = dropdown.querySelector('.dropdown_button > div');
  const input = parent.querySelector('.dropdown_input');
  button.innerText = item.innerText;
  dropdown.classList.remove('dropdown_expanded');
  input.value = key;
}