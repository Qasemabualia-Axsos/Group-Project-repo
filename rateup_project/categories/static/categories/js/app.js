document.addEventListener("DOMContentLoaded", () => {
    console.log("Categories JS Loaded ✅");

    // Example: confirm before delete
    const deleteBtns = document.querySelectorAll(".btn-danger");
    deleteBtns.forEach(btn => {
        btn.addEventListener("click", e => {
            if(!confirm("Are you sure you want to delete this category?")) {
                e.preventDefault();
            }
        });
    });
});
