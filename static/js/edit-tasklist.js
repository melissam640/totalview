// When unchecked task checkbox is checked, task is marked completed
for (const uncheckedTask of document.querySelectorAll('.task-unchecked')) {
    uncheckedTask.addEventListener('change', (evt) => {
      
      const checkbox = evt.target;
      
      const data = {
        'taskId': checkbox.value
      };
      
      fetch('/complete-task', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      })
  
      .then((response) => response.json())
      .then((message) => {
        console.log(message);
        checkbox.classList.remove('task-unchecked');
        checkbox.classList.add('task-checked');
      });
    });
  }
  
  // When checked task checkbox is unchecked, task is marked incompleted
  for (const checkedTask of document.querySelectorAll('.task-checked')) {
    checkedTask.addEventListener('change', (evt) => {
      
      const checkbox = evt.target;
      
      const data = {
        'taskId': checkbox.value
      };
      
      fetch('/undo-complete-task', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      })
  
      .then((response) => response.json())
      .then((message) => {
        console.log(message);
        checkbox.classList.remove('task-checked');
        checkbox.classList.add('task-unchecked');
      });
    });
  }