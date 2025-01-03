function editProfile(username, first_name, last_name, email) {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_edit_profile');
  floatingWindow.classList.add('shown_floating_window');
  const inputUsername = document.getElementById('floating_window_edit_profile_username');
  inputUsername.value = username;
  const inputFirstName = document.getElementById('floating_window_edit_profile_first_name');
  inputFirstName.value = first_name;
  const inputLastName = document.getElementById('floating_window_edit_profile_last_name');
  inputLastName.value = last_name;
  const inputEmail = document.getElementById('floating_window_edit_profile_email');
  inputEmail.value = email;
}

function editPassword() {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_edit_password');
  floatingWindow.classList.add('shown_floating_window');
}

function removePicture() {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_remove_picture');
  floatingWindow.classList.add('shown_floating_window');
}

function deleteProfile() {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_delete_profile');
  floatingWindow.classList.add('shown_floating_window');
}

function editPicture(addingPicture) {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_edit_picture');
  floatingWindow.classList.add('shown_floating_window');
  const textContext = document.getElementById('floating_window_edit_picture_context');
  if (addingPicture) {
    textContext.innerText = 'Profilbild hinzufügen';
  } else {
    textContext.innerText = 'Profilbild ändern';
  }
}