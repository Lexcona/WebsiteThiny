async function randomCat() {
    const response = await fetch("/imgs/cats.json");
    const cats = await response.json();

    const randomIndex = Math.floor(Math.random() * cats.length);
    const cat = cats[randomIndex];

    return cat;
}

async function cat404() {
    const imgThingy = document.getElementById("img-404");

    if (!imgThingy) {
        return;
    }

    try {
        imgThingy.src = await randomCat();
    } catch (error){
        console.error("cat went boom :(\n", error)
        return
    }
}

cat404();