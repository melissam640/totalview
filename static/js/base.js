// Adds additional text boxes to enter the title of actions for a new routine
// within the new routine modal
document.querySelector('#add-action').addEventListener('click', () => {
    console.log('event was triggered');
    document.querySelector('#routine-create-button').insertAdjacentHTML('beforebegin',
      `<div class="mb-3">
      <input type="text" class="form-control" name="action-title" id="action-title" placeholder="New Action">
      </div>`
    );
  });
  
  // Adds additional text boxes to enter the title of tasks for a new tasklist
  // within the new tasklist modal
  document.querySelector('#add-task').addEventListener('click', () => {
    document.querySelector('#tasklist-create-button').insertAdjacentHTML('beforebegin',
      `<div class="mb-3">
      <input type="text" class="form-control" name="task-title" id="task-title" placeholder="New Task">
      </div>`
    );
  });
  
  // Event repeat options show/hide
  document.querySelector('#event-repeat-none').addEventListener('click', () => {
    document.querySelector('#event-repeat-date-range').classList.add('d-none');
    document.querySelector('#event-repeat-days').classList.add('d-none');
  });
  
  document.querySelector('#event-repeat-day').addEventListener('click', () => {
    document.querySelector('#event-repeat-date-range').classList.remove('d-none');
    document.querySelector('#event-repeat-days').classList.add('d-none');
  });
  
  document.querySelector('#event-repeat-week').addEventListener('click', () => {
    document.querySelector('#event-repeat-date-range').classList.remove('d-none');
    document.querySelector('#event-repeat-days').classList.remove('d-none');
  });
  
  // Routine repeat options show/hide
  document.querySelector('#rou-repeat-day').addEventListener('click', () => {
    document.querySelector('#routine-repeat-date-range').classList.remove('d-none');
    document.querySelector('#routine-repeat-days').classList.add('d-none');
  });
  
  document.querySelector('#rou-repeat-week').addEventListener('click', () => {
    document.querySelector('#routine-repeat-date-range').classList.remove('d-none');
    document.querySelector('#routine-repeat-days').classList.remove('d-none');
  });
  
  // Tasklist repeat options show/hide
  document.querySelector('#tasklist-none').addEventListener('click', () => {
    document.querySelector('#tasklist-repeat-date-range').classList.add('d-none');
    document.querySelector('#tasklist-repeat-days').classList.add('d-none');
  });
  
  document.querySelector('#tasklist-day').addEventListener('click', () => {
    document.querySelector('#tasklist-repeat-date-range').classList.remove('d-none');
    document.querySelector('#tasklist-repeat-days').classList.add('d-none');
  });
  
  document.querySelector('#tasklist-week').addEventListener('click', () => {
    document.querySelector('#tasklist-repeat-date-range').classList.remove('d-none');
    document.querySelector('#tasklist-repeat-days').classList.remove('d-none');
  });