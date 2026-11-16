function catFaceSpawner(amount) {
    let background = document.getElementById("background")

    for (let i = 0; i < amount; i++) {
        let thingy = ((100/amount)*i);
        console.log(thingy)
        background.innerHTML += `\n<span style="left: ${thingy}%; animation-delay: -${Math.random() * amount*2}s">:3</span>`;
    }
}

catFaceSpawner(100);