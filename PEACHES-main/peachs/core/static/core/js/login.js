document.addEventListener("DOMContentLoaded", function () {
  var togglePasswordBtn = document.getElementById("togglePasswordBtn");
  var passwordInput = document.getElementById("passwordInput");

  togglePasswordBtn.addEventListener("click", function () {
    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      togglePasswordBtn.innerHTML = '<i class="bi bi-eye-slash-fill"></i>';
    } else {
      passwordInput.type = "password";
      togglePasswordBtn.innerHTML = '<i class="bi bi-eye-fill"></i>';
    }
  });
});

setTimeout(function () {
  var errorMessage = document.getElementById("error-message");
  errorMessage.style.display = "none";
}, 5000);

