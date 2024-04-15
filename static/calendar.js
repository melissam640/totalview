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

document.querySelector('#addtask0').addEventListener('click', () => {
    document.querySelector('#task1').style.display = 'block';
    document.querySelector('#addtask1').style.display = 'block';
});

document.querySelector('#addtask1').addEventListener('click', () => {
    document.querySelector('#task2').style.display = 'block';
    document.querySelector('#addtask2').style.display = 'block';
});

document.querySelector('#addtask2').addEventListener('click', () => {
    document.querySelector('#task3').style.display = 'block';
    document.querySelector('#addtask3').style.display = 'block';
});

document.querySelector('#addtask3').addEventListener('click', () => {
    document.querySelector('#task4').style.display = 'block';
    document.querySelector('#addtask4').style.display = 'block';
});