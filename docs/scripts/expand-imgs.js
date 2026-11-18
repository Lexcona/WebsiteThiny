document.querySelectorAll(".blog-post img").forEach(elem => {
    elem.addEventListener("click", () => {
        openOverlay(elem.src);
    });
});

document.addEventListener("keydown", function (event) {
    console.log(event.code);
    if (event.code === "Escape" && overlay.style.display !== "none") {
        closeOverlay();
    }
});



function openOverlay(src) {
    const overlay = document.querySelector("#overlay");
    const img = document.querySelector("#overlay-img");

    img.src = src;
    overlay.classList.add("open");
}


function closeOverlay() {
    document.querySelector("#overlay").classList.remove("open");
}