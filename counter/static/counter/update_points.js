// Wait for page to load
document.addEventListener("DOMContentLoaded", function () {
  // Select the submit button and input to be used later
  const submit = document.querySelector("#submit");
  const input = document.querySelector("#input");

  // Disable submit button by default:
  submit.disabled = true;

  // Listen for input to be typed into the input field
  input.onkeyup = () => {
    if (input.value.length > 0) {
      submit.disabled = false;
    } else {
      submit.disabled = true;
    }
  };
});
