function changeRole(id, username, role) {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_change_role');
  floatingWindow.classList.add('shown_floating_window');
  const inputId = document.getElementById('floating_window_change_role_id');
  inputId.value = id;
  const textUsername = document.getElementById('floating_window_change_role_username');
  textUsername.innerText = username;
  if (role == 'admin') {
    const inputRole = document.getElementById('floating_window_change_role_admin');
    inputRole.checked = true;
    textUsername.className = '';
    textUsername.classList.add('role_admin');
  } else if (role == 'vip') {
    const inputRole = document.getElementById('floating_window_change_role_vip');
    inputRole.checked = true;
    textUsername.className = '';
    textUsername.classList.add('role_vip');
  } else if (role == 'normal') {
    const inputRole = document.getElementById('floating_window_change_role_normal');
    inputRole.checked = true;
    textUsername.className = '';
    textUsername.classList.add('role_normal');
  }
}