let slides = document.querySelectorAll(".slide");
let currentSlide = 0;

function showNextSlide() {
  slides[currentSlide].classList.remove("active");
  currentSlide = (currentSlide + 1) % slides.length;
  slides[currentSlide].classList.add("active");
}

// Automatically change slides every 5 seconds
setInterval(showNextSlide, 5000);

// contact javascript
document.addEventListener("DOMContentLoaded", function () {
  // Your form submission handling code
  const contactForm = document.getElementById("contact-form");

  if (contactForm) {
    contactForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevents default form submission behavior

      const submitButton = document.getElementById("contact-submit");
      submitButton.textContent = "Sending your message..."; // Change button text

      // Simulate form submission delay (2 seconds)
      setTimeout(function () {
        submitButton.textContent = "Contact Us"; // Reset button text
        document.getElementById("success-message").style.display = "block"; // Show success message

        // Hide the message after 3 seconds
        setTimeout(function () {
          document.getElementById("success-message").style.display = "none";
        }, 3000);

        // Reset the form after submission
        document.getElementById("contact-form").reset();
      }, 2000);
    });
  }
});
