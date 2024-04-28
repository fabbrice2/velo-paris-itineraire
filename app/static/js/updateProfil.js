document.addEventListener("DOMContentLoaded", function () {
  const saveButton = document.querySelector('button[type="submit"]');
  const successMessage = document.createElement("p");
  successMessage.textContent = "Element changé avec succès";

  saveButton.addEventListener("click", function (event) {
    event.preventDefault();

    saveButton.parentNode.insertBefore(successMessage, saveButton.nextSibling);

    // Disparition du message après 5 secondes
    setTimeout(function () {
      successMessage.remove();
    }, 5000);
  });
});
