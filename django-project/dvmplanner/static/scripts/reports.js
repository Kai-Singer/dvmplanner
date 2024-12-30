const floatingBackground = document.getElementById('floating_background');
floatingBackground.classList.add('shown_floating_window');

const floatingWindow = document.getElementById('floating_window_edit_report');
floatingWindow.classList.add('shown_floating_window');

const inputBeginn = floatingWindow.querySelector('#floating_window_edit_report_beginn > input');
inputBeginn.value = '2024-12-31T23:59';

const inputEnd = floatingWindow.querySelector('#floating_window_edit_report_end > input');
inputEnd.value = '2024-12-31T23:59';

const inputModule = floatingWindow.querySelector('#floating_window_edit_report_module');
inputModule.innerText = 'Text';

const inputModuleHidden = inputModule.parentElement.parentElement.querySelector('input');
inputModuleHidden.value = 'Text';

const inputNotes = floatingWindow.querySelector('#floating_window_edit_report_notes > textarea');
inputNotes.innerText = 'Text';