// When unchecked recurring task checkbox is checked, task is marked completed
for (const uncheckedTask of document.querySelectorAll('.recur-task-unchecked')) {
    uncheckedTask.addEventListener('change', (evt) => {
      
      const checkbox = evt.target;
      
      const data = {
        'taskId': checkbox.value
      };
      
      fetch('/complete-recur-task', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      })
  
      .then((response) => response.json())
      .then((message) => {
        console.log(message);
        checkbox.classList.remove('recur-task-unchecked');
        checkbox.classList.add('recur-task-checked');
      });
    });
  }
  
  // When checked task checkbox is unchecked, task is marked incompleted
  for (const checkedTask of document.querySelectorAll('.recur-task-checked')) {
    checkedTask.addEventListener('change', (evt) => {
      
      const checkbox = evt.target;
      
      const data = {
        'taskId': checkbox.value
      };
      
      fetch('/undo-complete-recur-task', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      })
  
      .then((response) => response.json())
      .then((message) => {
        console.log(message);
        checkbox.classList.remove('recur-task-checked');
        checkbox.classList.add('recur-task-unchecked');
      });
    });
  }

  // Routine repeat options show/hide
document.querySelector('#edit-tasklist-repeat-day').addEventListener('click', () => {
    document.querySelector('#edit-tasklist-repeat-days').classList.add('d-none');
    });
    
document.querySelector('#edit-tasklist-repeat-week').addEventListener('click', () => {
    document.querySelector('#edit-tasklist-repeat-days').classList.remove('d-none');
    });