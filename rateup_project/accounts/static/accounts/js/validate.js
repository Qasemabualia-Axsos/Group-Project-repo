document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    if (!form) return;
    form.addEventListener("submit", (e) => {
        const pwd1 = form.querySelector("#id_password1");
        const pwd2 = form.querySelector("#id_password2");
        if (pwd1 && pwd2 && pwd1.value !== pwd2.value) {
            e.preventDefault();
            alert("Passwords do not match");
        }
    });
});
