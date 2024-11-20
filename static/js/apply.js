document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("application-form");
  const successMessage = document.getElementById("application-success-message");
  const loadingMessage = document.getElementById("application-loading-message");
  const clearBtn = document.getElementById("clear-resume-btn");
  const resumeInput = document.getElementById("resume-apply");

  // Handle file input change and show/hide "Clear File" button
  resumeInput.addEventListener("change", function () {
    if (this.files.length > 0) {
      clearBtn.style.display = "inline-block";
    } else {
      clearBtn.style.display = "none";
    }
  });

  // Clear file input
  function clearFileInput() {
    resumeInput.value = ""; // Clears the selected file
    clearBtn.style.display = "none"; // Hide the 'Clear File' button
  }

  // Handle form submission
  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default form submission

    // Show loading message
    loadingMessage.style.display = "block";

    // Gather form data (including file)
    const formData = new FormData(form);

    try {
      // Send the data to the server
      const response = await fetch("/apply", {
        method: "POST",
        body: formData, // Send FormData including file as a multipart request
      });

      // Hide loading message
      loadingMessage.style.display = "none";

      if (response.ok) {
        // Show success message
        successMessage.style.display = "block";
        form.reset(); // Reset the form

        // Hide the success message after 3 seconds
        setTimeout(() => {
          successMessage.style.display = "none";
        }, 3000);

        // Clear the file input and reset button visibility
        clearFileInput();
      } else {
        console.error("Error submitting application:", response.statusText);
      }
    } catch (error) {
      console.error("Error submitting application:", error);
      loadingMessage.style.display = "none"; // Hide loading message in case of error
    }
  });

  // Attach the clear button action
  clearBtn.addEventListener("click", clearFileInput);
});
