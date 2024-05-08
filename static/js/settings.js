// Change from light to dark mode
document.querySelector('#theme-mode-toggle').addEventListener('change', () => {
  
    fetch('/change-theme')
      .then((response) => response.json())
      .then((theme) => {
        document.documentElement.setAttribute('data-bs-theme', theme);
        document.querySelector('#logo').setAttribute('src', `/static/background-pic/logo-${theme}.png`);
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
          el.setAttribute('border-color', accent);
        }
        for ( el of document.querySelectorAll('.nav-link')) {
            el.setAttribute('color', accent);
          }
      });
  });