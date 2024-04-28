document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
  
    form.addEventListener('submit', function(event) {
      const usernameInput = document.getElementById('username');
      const passwordInput = document.getElementById('password');
  
      let isValid = true;
  
      if (usernameInput.value.trim() === '') {
        isValid = false;
        usernameInput.classList.add('invalid');
      } else {
        usernameInput.classList.remove('invalid');
      }
  
      if (passwordInput.value.trim() === '') {
        isValid = false;
        passwordInput.classList.add('invalid');
      } else {
        passwordInput.classList.remove('invalid');
      }
  
      if (!isValid) {
        event.preventDefault(); // Empêche l'envoi du formulaire si la validation échoue
      }
    });
  });
  