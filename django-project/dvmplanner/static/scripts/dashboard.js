function updateClock() {
  const currentTime = new Date();
  const currentDayName = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'][currentTime.getDay() - 1];
  const currentDay = currentTime.getDate();
  const currentMonth = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'][currentTime.getMonth()];
  const currentYear = currentTime.getFullYear();
  const currentHours = String(currentTime.getHours()).padStart(2, '0');
  const currentMinutes = String(currentTime.getMinutes()).padStart(2, '0');
  const currentSeconds = String(currentTime.getSeconds()).padStart(2, '0');
  document.getElementById('live_date').innerText = `${ currentDayName }, der ${ currentDay }. ${ currentMonth } ${ currentYear }`;
  document.getElementById('live_time').innerText = `${ currentHours }.${ currentMinutes }:${ currentSeconds } Uhr`;
}

updateClock();
setInterval(updateClock, 1000);

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