document
  .getElementById("application-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const submitButton = document.getElementById("apply-submit-button");
    submitButton.textContent = "Submitting your application...";

    setTimeout(function () {
      submitButton.textContent = "Submit Application";
      document.getElementById("application-success-message").style.display =
        "block";

      // Hide the message after 3 seconds
      setTimeout(function () {
        document.getElementById("application-success-message").style.display =
          "none";
      }, 3000);

      // Reset the form after submission
      document.getElementById("application-form").reset();
    }, 2000);
  });
