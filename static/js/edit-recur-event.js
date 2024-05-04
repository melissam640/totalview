  // Routine repeat options show/hide
  document.querySelector('#edit-recur-event-repeat-day').addEventListener('click', () => {
    document.querySelector('#edit-recur-event-repeat-days').classList.add('d-none');
  });
  
  document.querySelector('#edit-recur-event-repeat-week').addEventListener('click', () => {
    document.querySelector('#edit-recur-event-repeat-days').classList.remove('d-none');
  });