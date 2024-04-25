


  window.addEventListener('DOMContentLoaded', () => {
    const adresse = document.querySelector('.adresse-item');
    const ellipsis = '....';

    if (adresse.scrollWidth > adresse.clientWidth) {
        while (adresse.scrollWidth > adresse.clientWidth) {
            adresse.textContent = adresse.textContent.slice(0, -1);
        }
        adresse.textContent += ellipsis;
    }
});


