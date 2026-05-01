document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
    }

    const toggleButtons = document.querySelectorAll(".theme-toggle-btn");

    function updateButtonText() {
        const isDark = document.body.classList.contains("dark-theme");
        toggleButtons.forEach((btn) => {
            btn.textContent = isDark ? "Switch to Light Mode" : "Switch to Dark Mode";
        });
    }

    toggleButtons.forEach((button) => {
        button.addEventListener("click", function () {
            document.body.classList.toggle("dark-theme");

            const isDark = document.body.classList.contains("dark-theme");
            localStorage.setItem("theme", isDark ? "dark" : "light");

            updateButtonText();
        });
    });

    updateButtonText();
});