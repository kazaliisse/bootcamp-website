document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("application-form");
  const successMessage = document.getElementById("application-success-message");
  const loadingMessage = document.getElementById("application-loading-message");

  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent default form submission

    // Show loading message
    loadingMessage.style.display = "block";

    // Gather form data
    const formData = new FormData(form);
    const data = {
      firstName: formData.get("first-name"),
      lastName: formData.get("last-name"),
      email: formData.get("email"),
      phone: formData.get("phone"),
      gender: formData.get("gender"),
      county: formData.get("county"),
      course: formData.get("course"),
    };

    try {
      // Send the data to the server
      const response = await fetch("/apply", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
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
      } else {
        console.error("Error submitting application:", response.statusText);
      }
    } catch (error) {
      console.error("Error submitting application:", error);
      loadingMessage.style.display = "none"; // Hide loading message in case of error
    }
  });
});
