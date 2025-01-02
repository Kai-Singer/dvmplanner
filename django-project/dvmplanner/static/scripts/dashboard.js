function deleteEntry(index) {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_delete_entry');
  floatingWindow.classList.add('shown_floating_window');
  const inputId = document.getElementById('floating_window_delete_entry_index');
  inputId.value = index;
}

function deleteEntries() {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_delete_entries');
  floatingWindow.classList.add('shown_floating_window');
}