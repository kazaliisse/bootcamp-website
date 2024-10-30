// Select elements
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");
const resetForm = document.getElementById("reset-form");
const signupBtn = document.getElementById("signup-btn");
const loginBtn = document.getElementById("login-btn");
const resetBtn = document.getElementById("reset-btn");
const backToLoginBtns = document.querySelectorAll(".back-to-login");

// Function to show login form and hide others
function showLoginForm() {
  loginForm.classList.remove("hidden");
  signupForm.classList.add("hidden");
  resetForm.classList.add("hidden");
}

// Function to show signup form and hide others
function showSignupForm() {
  signupForm.classList.remove("hidden");
  loginForm.classList.add("hidden");
  resetForm.classList.add("hidden");
}

// Function to show reset password form and hide others
function showResetForm() {
  resetForm.classList.remove("hidden");
  loginForm.classList.add("hidden");
  signupForm.classList.add("hidden");
}

// Event listeners for buttons
signupBtn.addEventListener("click", showSignupForm);
loginBtn.addEventListener("click", showLoginForm);
resetBtn.addEventListener("click", showResetForm);

// Event listeners for back to login buttons on signup and reset forms
backToLoginBtns.forEach((btn) => {
  btn.addEventListener("click", showLoginForm);
});
