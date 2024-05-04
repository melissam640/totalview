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

// Routine repeat options show/hide
document.querySelector('#edit-routine-repeat-day').addEventListener('click', () => {
    document.querySelector('#edit-routine-repeat-days').classList.add('d-none');
    });
    
document.querySelector('#edit-routine-repeat-week').addEventListener('click', () => {
    document.querySelector('#edit-routine-repeat-days').classList.remove('d-none');
    });
