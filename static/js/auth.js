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

// Handle form submission for Sign-up
document.addEventListener("DOMContentLoaded", function () {
  // Switch to Sign-up form when the Sign-up button is clicked
  const signupButton = document.getElementById("signupButton");
  if (signupButton) {
    signupButton.addEventListener("click", function () {
      switchTab("signup");
    });
  }

  // Handle form submission for Sign-up
  const signupForm = document.getElementById("signupForm");
  if (signupForm) {
    signupForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent default form submission
      const name = document.getElementById("signupName").value;
      const email = document.getElementById("signupEmail").value;
      const password = document.getElementById("signupPassword").value;
      const confirmPassword = document.getElementById(
        "signupConfirmPassword"
      ).value;

      // Validation
      if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
      }

      // Make an AJAX request to the Flask backend for Sign-up
      fetch("/auth/signup", {
        // Updated API endpoint
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
          email: email,
          password: password,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert("Sign up successful! Please log in.");
            switchTab("login"); // Switch to the login form after sign-up
          } else {
            alert("Sign up failed: " + data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  }

  // Handle form submission for Login
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent default form submission
      const email = document.getElementById("loginEmail").value;
      const password = document.getElementById("loginPassword").value;

      // Make an AJAX request to the Flask backend for Login
      fetch("/auth/login", {
        // Updated API endpoint
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            window.location.href = "/home"; // Redirect to dashboard or homepage
          } else {
            alert("Login failed: " + data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  }
});

// Function to handle the password reset form submission
async function validateReset() {
  // Prevent default form submission
  event.preventDefault();

  // Get the email from the form input
  const email = document.getElementById("resetEmail").value;

  try {
    const response = await fetch("/password_reset", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email: email }),
    });

    const result = await response.json();

    if (result.success) {
      alert(result.message); // Notify user of success
    } else {
      alert(result.message); // Notify user of failure
    }
  } catch (error) {
    alert("An error occurred. Please try again later.");
  }
}

let isProfileFetched = false; // Flag to ensure the profile is fetched only once

function toggleProfileMenu() {
  const dropdown = document.getElementById("profileDropdown");
  const isVisible = !dropdown.classList.contains("hidden");

  // Toggle the dropdown visibility
  dropdown.classList.toggle("hidden");

  // Only fetch user profile data when the dropdown is shown and data hasn't been fetched yet
  if (!isVisible && !isProfileFetched) {
    fetchUserProfile();
    isProfileFetched = true; // Mark profile data as fetched
  }
}

function fetchUserProfile() {
  fetch("/auth/profile")
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        document.getElementById("userName").textContent = `Name: ${data.name}`;
        document.getElementById(
          "userEmail"
        ).textContent = `Email: ${data.email}`;
      } else {
        console.error(data.message);
      }
    })
    .catch((error) => {
      console.error("Error fetching user profile:", error);
    });
}
