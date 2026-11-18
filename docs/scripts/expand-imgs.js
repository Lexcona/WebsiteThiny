document.querySelectorAll(".blog-post img").forEach(elem => {
    elem.addEventListener("click", () => {
        openOverlay(elem.src);
    });
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