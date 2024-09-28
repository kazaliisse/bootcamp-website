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
document
  .getElementById("contact-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const submitButton = document.getElementById("contact-submit");
    submitButton.textContent = "Sending your message...";

    setTimeout(function () {
      submitButton.textContent = "Contact Us";
      document.getElementById("success-message").style.display = "block";

      // Hide the message after 3 seconds
      setTimeout(function () {
        document.getElementById("success-message").style.display = "none";
      }, 3000);
      // Reset the form after submission
      document.getElementById("contact-form").reset();
    }, 2000);
  });
