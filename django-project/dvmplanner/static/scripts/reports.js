function editReport(id, beginn_day, beginn_time, end_day, end_time, module_index, module_name, notes, long_notes) {
  if (long_notes != '') notes = long_notes;
  if (end_day == '') end_day = beginn_day;
  beginn_day = beginn_day.split('.');
  beginn_day = beginn_day[2] + '-' + beginn_day[1] + '-' + beginn_day[0];
  beginn_time = beginn_time.split(':');
  beginn_time = beginn_time[0].split('.');
  beginn_time = beginn_time[0] + ':' + beginn_time[1];
  beginn = beginn_day + 'T' + beginn_time;
  end_day = end_day.split('.');
  end_day = end_day[2] + '-' + end_day[1] + '-' + end_day[0];
  end_time = end_time.split(':');
  end_time = end_time[0].split('.');
  end_time = end_time[0] + ':' + end_time[1];
  end = end_day + 'T' + end_time;
  module_name = module_index + ' ' + module_name;

  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_edit_report');
  floatingWindow.classList.add('shown_floating_window');
  const inputBeginn = document.getElementById('floating_window_edit_report_beginn');
  inputBeginn.value = beginn;
  const inputEnd = document.getElementById('floating_window_edit_report_end');
  inputEnd.value = end;
  const inputModule = document.getElementById('floating_window_edit_report_module');
  inputModule.innerText = module_name;
  const inputModuleHidden = document.getElementById('floating_window_edit_report_module_hidden');
  inputModuleHidden.value = module_index;
  const inputNotes = document.getElementById('floating_window_edit_report_notes');
  inputNotes.innerText = notes;
  const inputId = document.getElementById('floating_window_edit_report_id');
  inputId.value = id;
}

function deleteReport(id) {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_delete_report');
  floatingWindow.classList.add('shown_floating_window');
  const inputId = document.getElementById('floating_window_delete_report_id');
  inputId.value = id;
}

function uploadData() {
  const floatingBackground = document.getElementById('floating_background');
  floatingBackground.classList.add('shown_floating_window');
  const floatingWindow = document.getElementById('floating_window_upload_data');
  floatingWindow.classList.add('shown_floating_window');
}