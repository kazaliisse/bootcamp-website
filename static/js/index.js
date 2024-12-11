// Wait for the DOM to fully load before executing the script
document.addEventListener("DOMContentLoaded", function () {
  // Slide management
  let slides = document.querySelectorAll(".slide");
  let currentSlide = 0;

  function showNextSlide() {
    // Check if slides exist
    if (slides.length === 0) {
      console.error("No slides available.");
      return; // Exit the function
    }

    // Remove the 'active' class from the current slide
    slides[currentSlide].classList.remove("active");

    // Update currentSlide index
    currentSlide = (currentSlide + 1) % slides.length;

    // Add the 'active' class to the next slide
    slides[currentSlide].classList.add("active");

    // Log current slide index for debugging
    console.log("Current slide index:", currentSlide);
  }

  // Automatically change slides every 5 seconds
  setInterval(showNextSlide, 5000);

  // Contact form submission handling
  const contactForm = document.getElementById("contact-form");
  if (contactForm) {
    contactForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevents default form submission behavior

      const submitButton = document.getElementById("contact-submit");
      submitButton.textContent = "Sending your message..."; // Change button text

      // Gather form data
      const formData = new FormData(contactForm);
      const data = {
        "first-name": formData.get("first-name"),
        "last-name": formData.get("last-name"),
        email: formData.get("email"),
        phone: formData.get("phone"),
        reason: formData.get("reason"),
      };

      // Send the data to the server
      fetch("/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams(data),
      })
        .then((response) => {
          if (response.ok) {
            // Show success message
            document.getElementById("success-message").style.display = "block";
            return contactForm.reset(); // Reset the form
          } else {
            throw new Error("Network response was not ok.");
          }
        })
        .catch((error) => {
          console.error("There was a problem with the fetch operation:", error);
        })
        .finally(() => {
          // Reset button text after submission
          submitButton.textContent = "Contact Us";
          // Hide the success message after 3 seconds
          setTimeout(() => {
            document.getElementById("success-message").style.display = "none";
          }, 3000);
        });
    });
  }
});

window.onload = function () {
  const counters = [
    { elementId: "counter1", maxCount: 1000, speed: 5 },
    { elementId: "counter2", maxCount: 500, speed: 10 },
    { elementId: "counter3", maxCount: 300, speed: 15 },
  ];

  counters.forEach((counter) => {
    let count = 0;
    let counterElement = document.getElementById(counter.elementId);

    function updateCounter() {
      if (count <= counter.maxCount) {
        counterElement.textContent = count;
        count++;
      }
    }

    setInterval(updateCounter, counter.speed);
  });
};

// let currentIndex = 0;
// const slider = document.querySelector(".slider");
// const slides = document.querySelectorAll(".slider img");
// const totalSlides = slides.length;

// // Show next slide
// function nextSlide() {
//   currentIndex = (currentIndex + 1) % totalSlides;
//   updateSliderPosition();
// }

// // Show previous slide
// function prevSlide() {
//   currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
//   updateSliderPosition();
// }

// // Update slider position
// function updateSliderPosition() {
//   slider.style.transform = `translateX(-${currentIndex * 100}%)`;
// }

// // Auto-slide every 3 seconds
// setInterval(nextSlide, 3000);

document.addEventListener("DOMContentLoaded", () => {
  const imageInput = document.getElementById("imageInput");
  const profileImage = document.getElementById("profileImage");
  const customFileLabel = document.querySelector(".custom-file-label");

  // Load the saved image from localStorage on page load
  const savedImage = localStorage.getItem("profileImage");
  if (savedImage) {
    profileImage.src = savedImage;
    profileImage.classList.remove("hidden");
  }

  // Show the file picker when label is clicked
  customFileLabel.addEventListener("click", () => {
    imageInput.click();
  });

  // Handle the file input change event
  imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];

    if (file) {
      const reader = new FileReader();

      // Load the file and display it
      reader.onload = (e) => {
        const imageData = e.target.result;
        profileImage.src = imageData;
        profileImage.classList.remove("hidden");

        // Save the image data URL in localStorage
        localStorage.setItem("profileImage", imageData);
      };

      reader.readAsDataURL(file); // Read the file as a data URL
    }
  });
});
