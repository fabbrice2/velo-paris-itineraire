document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", function (event) {
    const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");

    let isValid = true;

    if (usernameInput.value.trim() === "") {
      isValid = false;
      usernameInput.classList.add("invalid");
    } else {
      usernameInput.classList.remove("invalid");
    }

    if (emailInput.value.trim() === "") {
      isValid = false;
      emailInput.classList.add("invalid");
    } else {
      emailInput.classList.remove("invalid");
    }

    if (!isValid) {
      event.preventDefault();
    }
  });
});
