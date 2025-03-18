document.addEventListener("DOMContentLoaded", function () {
    let container = document.querySelector(".container");
    let loginForm = document.querySelector("#loginForm");
    let signInForm = document.querySelector("#signInForm");
    let loginToggle = document.querySelector("#loginToggle");
    let signInToggle = document.querySelector("#signInToggle");
    let passwordInput = document.querySelector("#password");
    let confirmPasswordInput = document.querySelector("#confirm_password");
    let passwordError = document.querySelector("#password-error");
    let registerButton = document.querySelector("#register-btn");
    let signInFormElement = document.querySelector("#signInForm");

    // Toggle between Login and Sign In forms
    loginToggle.addEventListener("click", function () {
        container.classList.remove("slide");
        loginForm.classList.add("active");
        signInForm.classList.remove("active");
    });

    signInToggle.addEventListener("click", function () {
        container.classList.add("slide");
        signInForm.classList.add("active");
        loginForm.classList.remove("active");
    });

    // Show login form by default
    loginForm.classList.add("active");

    // Function to validate password
    function validatePassword() {
        let password = passwordInput.value;
        let confirmPassword = confirmPasswordInput.value;
        let passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

        if (!passwordPattern.test(password)) {
            passwordError.style.display = "block";
            passwordError.innerHTML = "⚠ Password must be at least 8 characters long, contain one uppercase, one lowercase, one digit, and one special character.";
            registerButton.disabled = true;
        } else if (password !== confirmPassword) {
            passwordError.style.display = "block";
            passwordError.innerHTML = "⚠ Passwords do not match!";
            registerButton.disabled = true;
        } else {
            passwordError.style.display = "none";
            registerButton.disabled = false;
        }
    }

    // Prevent form submission if password is invalid
    signInFormElement.addEventListener("submit", function (event) {
        if (registerButton.disabled) {
            event.preventDefault(); // Stop form submission
            passwordError.style.display = "block";
            passwordError.innerHTML = "⚠ Fix the errors before submitting!";
        }
    });

    // Event listeners for password validation
    passwordInput.addEventListener("keyup", validatePassword);
    confirmPasswordInput.addEventListener("keyup", validatePassword);
});


// Password pop-up (error message) appears on the same page instead of switching to Login
// Prevents form submission if the password is invalid
// Keeps user on the registration (Sign In) page until a valid password is entered

