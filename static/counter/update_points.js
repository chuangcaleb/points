// Wait for page to load
document.addEventListener("DOMContentLoaded", function () {
  // Select the submit button and input to be used later
  const submit = document.querySelector("#submit");
  const input = document.querySelector("#input");

  // Disable submit button by default:
  submit.disabled = true;

  function disable_empty_input() {
    if (input.value.length > 0) {
      submit.disabled = false;
    } else {
      submit.disabled = true;
    }
  }

  // Listen for input to be typed into the input field
  input.onkeyup = () => disable_empty_input();

  document.querySelectorAll(".fixed-values").forEach((button) => {
    button.onclick = () => {
      const input_value = document.getElementById("input");
      if (input_value.value == "") {
        input_value.value = 0;
      }
      input_value.value =
        parseInt(input_value.value) + parseInt(button.innerHTML);
      disable_empty_input();
    };
  });
});
