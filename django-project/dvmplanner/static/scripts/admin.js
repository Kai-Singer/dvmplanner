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

function editModule(index, name, semester) {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_edit_module');
  floatingWindow.classList.add('shown_floating_window');
  const inputIndex = document.getElementById('floating_window_edit_module_index');
  inputIndex.value = index;
  const containerSemester = document.getElementById('floating_window_edit_module_semester_container');
  const inputSemester = document.getElementById('floating_window_edit_module_semester');
  const inputSemesterHidden = document.getElementById('floating_window_edit_module_semester_hidden');
  if (semester == null) {
    containerSemester.classList.add('hidden_form_item');
    inputSemesterHidden.value = '';
  } else {
    containerSemester.classList.remove('hidden_form_item');
    inputSemester.innerText = semester + '. Semester';
    inputSemesterHidden.value = semester;
  }
  const textIndex = document.getElementById('floating_window_edit_module_index_text');
  textIndex.innerText = index;
  const inputName = document.getElementById('floating_window_edit_module_name');
  inputName.value = name;
}

function deleteModule(index, name) {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_delete_module');
  floatingWindow.classList.add('shown_floating_window');
  const inputIndex = document.getElementById('floating_window_delete_module_index');
  inputIndex.value = index;
  const textName = document.getElementById('floating_window_delete_module_name_text');
  textName.innerText = index + ' ' + name;
}

function addModule() {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_add_module');
  floatingWindow.classList.add('shown_floating_window');
}

function restoreDefault() {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_restore_default');
  floatingWindow.classList.add('shown_floating_window');
}