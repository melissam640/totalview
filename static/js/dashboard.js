// When unchecked action checkbox is checked, action is marked completed
for (const uncheckedAction of document.querySelectorAll('.action-unchecked')) {
    uncheckedAction.addEventListener('change', (evt) => {
      
      const checkbox = evt.target;
      
      const data = {
        'actionId': checkbox.value
      };
      
      fetch('/complete-action', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      })
  
      .then((response) => response.json())
      .then((message) => {
        console.log(message);
        checkbox.classList.remove('action-unchecked');
        checkbox.classList.add('action-checked');
      });
    });
  }
  
  // When checked action checkbox is unchecked, action is marked incompleted
  for (const checkedAction of document.querySelectorAll('.action-checked')) {
    checkedAction.addEventListener('change', (evt) => {
      
      const checkbox = evt.target;
      
      const data = {
        'actionId': checkbox.value
      };
      
      fetch('/undo-complete-action', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          'Content-Type': 'application/json',
        },
      })
  
      .then((response) => response.json())
      .then((message) => {
        console.log(message);
        checkbox.classList.remove('action-checked');
        checkbox.classList.add('action-unchecked');
      });
    });
  }
  
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