// Renders the calendar
document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    themeSystem: 'bootstrap5',
    headerToolbar: {
      start: 'prev next today',
      center: 'title',
      end: 'dayGridMonth dayGridWeek dayGridDay'
    }
    })
    // Add user events to calendar
    fetch('/api/add-event')
      .then((response) => response.json())
      .then((responseData) => {
        for (const data of responseData) {
            calendar.addEvent(data);
        }
      })
    calendar.render();
});

// Adds additional text boxes to enter the title of actions for a new routine
// within the new routine modal
document.querySelector('#add-action').addEventListener('click', () => {
  document.querySelector('#add-action-section').insertAdjacentHTML('afterend',
    `<div class="form-floating mb-3">
      <input type="text" class="form-control" id="action-title" name="action-title" placeholder="New Action">
      <label for="action-title">Action Title</label>
    </div>`
  );
});

for (const uncheckedAction of document.querySelectorAll('.action-unchecked')) {
  uncheckedAction.addEventListener('change', (evt) => {
    
    console.log('event was triggered');
    
    const checkbox = evt.target
    console.log('checkbox:', checkbox);
    
    const data = {
      'actionId': checkbox.value
    };
    console.log('data: ', data);
    
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
    } )
  })
}

// Adds additional text boxes to enter the title of tasks for a new tasklist
// within the new tasklist modal
document.querySelector('#add-task').addEventListener('click', () => {
  document.querySelector('#add-task-section').insertAdjacentHTML('afterend',
    `<div class="form-floating mb-3">
      <input type="text" class="form-control" id="task-title" name="task-title" placeholder="New Task">
      <label for="task-title">Task Title</label>
    </div>`
  );
});
