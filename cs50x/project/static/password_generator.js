document.addEventListener("DOMContentLoaded", function() {
    const generateButton = document.getElementById("generate-password-btn");
    const generatedPasswordInput = document.getElementById("generated-password");  // Fix the ID here
    const passwordLengthInput = document.getElementById("password-length");

    generateButton.addEventListener("click", function() {
        fetch("/generate_password", {
            method: "POST",
            body: JSON.stringify({ length: parseInt(passwordLengthInput.value) }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.text())
        .then(password => {
            generatedPasswordInput.value = password;  // Fix the variable name here
        });
    });
});
