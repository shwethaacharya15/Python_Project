document.addEventListener("DOMContentLoaded", function () {
    let container = document.querySelector(".container");
    let loginForm = document.querySelector("#loginForm");
    let signInForm = document.querySelector("#signInForm");
    let loginToggle = document.querySelector("#loginToggle");
    let signInToggle = document.querySelector("#signInToggle");

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
});
