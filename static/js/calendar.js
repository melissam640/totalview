// Renders the calendar
document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    themeSystem: 'bootstrap5',
    headerToolbar: {
      start: 'prev,next today',
      center: 'title',
      end: 'dayGridMonth dayGridWeek dayGridDay'
    },
    navLinks: true,
    dayMaxEvents: true
    });
    // Add user events to calendar
    fetch('/api/add-event')
      .then((response) => response.json())
      .then((responseData) => {
        for (const data of responseData) {
            calendar.addEvent(data);
        }
      });
    calendar.render();
});

// Change from light to dark mode
document.querySelector('#theme-mode-toggle').addEventListener('change', () => {
  
  fetch('/change-theme')
    .then((response) => response.json())
    .then((theme) => {
      document.documentElement.setAttribute('data-bs-theme', theme);
    });
});

// Change accent color
document.querySelector('#accent-color').addEventListener('input', (evt) => {
  
  console.log("listener was trigger")
  
  const data = {
    'accent': evt.target.value
    };

  fetch('/change-accent-color', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
    },
  })

    .then((response) => response.json())
    .then((accent) => {
      for ( el of document.querySelectorAll('.btn-primary')) {
        el.setAttribute('background-color', accent);
      }
    });
});

// Adds additional text boxes to enter the title of actions for a new routine
// within the new routine modal
document.querySelector('#add-action').addEventListener('click', () => {
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
document.querySelector('#repeat-none').addEventListener('click', () => {
  document.querySelector('#event-repeat-date-range').classList.add('d-none');
  document.querySelector('#event-repeat-days').classList.add('d-none');
});

document.querySelector('#repeat-day').addEventListener('click', () => {
  document.querySelector('#event-repeat-date-range').classList.remove('d-none');
  document.querySelector('#event-repeat-days').classList.add('d-none');
});

document.querySelector('#repeat-week').addEventListener('click', () => {
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