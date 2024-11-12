// Switch between forms
function switchTab(formType) {
  const forms = ["login", "signup", "reset"];
  forms.forEach((form) => {
    const formElement = document.getElementById(`${form}-form`);
    formElement.classList.remove("active");
  });

  const activeForm = document.getElementById(`${formType}-form`);
  activeForm.classList.add("active");
}

// Validate Login Form
function validateLogin() {
  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;

  if (!email || !password) {
    alert("Please fill in all fields.");
    return false;
  }
  return true;
}

// Validate Sign Up Form
function validateSignup() {
  const name = document.getElementById("signupName").value;
  const email = document.getElementById("signupEmail").value;
  const password = document.getElementById("signupPassword").value;
  const confirmPassword = document.getElementById(
    "signupConfirmPassword"
  ).value;

  if (!name || !email || !password || !confirmPassword) {
    alert("Please fill in all fields.");
    return false;
  }

  if (password !== confirmPassword) {
    alert("Passwords do not match.");
    return false;
  }

  return true;
}

// Validate Reset Password Form
function validateReset() {
  const email = document.getElementById("resetEmail").value;

  if (!email) {
    alert("Please enter your email.");
    return false;
  }

  return true;
}
