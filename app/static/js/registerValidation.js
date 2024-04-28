document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");

  form.addEventListener("submit", function (event) {
    const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    let isValid = true;

    if (usernameInput.value.trim() === "") {
      isValid = false;
      usernameInput.classList.add("invalid");
    } else {
      usernameInput.classList.remove("invalid");
    }

    if (emailInput.value.trim() === "" || !isValidEmail(emailInput.value)) {
      isValid = false;
      emailInput.classList.add("invalid");
    } else {
      emailInput.classList.remove("invalid");
    }

    if (passwordInput.value.trim() === "") {
      isValid = false;
      passwordInput.classList.add("invalid");
    } else {
      passwordInput.classList.remove("invalid");
    }

    if (!isValid) {
      event.preventDefault();
    }
  });

  function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  }
});
