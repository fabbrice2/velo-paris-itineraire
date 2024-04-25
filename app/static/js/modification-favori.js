document.addEventListener('DOMContentLoaded', function() {
    const input = document.querySelector('.change-name');
    const validerBtn = document.querySelector('.valider');

    input.addEventListener('input', function() {
      if (input.value.trim() !== '') {
        validerBtn.style.opacity = '1';
      } else {
        validerBtn.style.opacity = '0.5';
      }
    });
  });
  
