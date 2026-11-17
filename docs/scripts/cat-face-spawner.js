const amount = 100;
const fallDuration = 15;

const laneWidth = 64;

const catWidth = 32;
const catHeight = 30;
const minGapX = 8;
const minGapY = 12;

// found the base somewhere online but forgor where
// the og version was too weird on the thingy 

function catFaceSpawner() {
    const background = document.getElementById("background");
    if (!background) {
        return;
    }

    const width = window.innerWidth;
    const height = window.innerHeight;
    const laneCount = Math.max(1, Math.min(amount, Math.floor(width / laneWidth)));


    const maxCatsPerLane = Math.max(1, Math.floor((height + catHeight) / (catHeight + minGapY)));
    const catCount = Math.min(amount, laneCount * maxCatsPerLane);

    const lanes = Array.from({ length: laneCount }, () => []);
    for (let i = 0; i < catCount; i++) {
        lanes[i % laneCount].push(i);
    }

    const fragment = document.createDocumentFragment();
    const laneSize = width / laneCount;
    const maxFunnyX = Math.max(0, (laneSize - catWidth) / 2 - minGapX);
    const requiredPhaseGap = (catHeight + minGapY) / (height + catHeight);

    lanes.forEach((lane, laneIndex) => {
        if (lane.length === 0) {
            return;
        }

        const laneCenter = laneIndex * laneSize + (laneSize - catWidth) / 2;

        const laneDuration = fallDuration * (0.85 + Math.random() * 0.3);
        const phaseSlot = 1 / lane.length;
        const funnyPhase = Math.max(0, Math.min(0.4, 1 - requiredPhaseGap / phaseSlot));
        const laneOffset = Math.random();

        lane.forEach((_, slot) => {
            const thingy = document.createElement("span");
            const x = laneCenter + (Math.random() * 2 - 1) * maxFunnyX;
            const phaser = ((slot + laneOffset + Math.random() * funnyPhase) * phaseSlot) % 1;

            thingy.textContent = ":3";
            thingy.style.left = `${x}px`;
            thingy.style.animationDuration = `${laneDuration}s`;
            thingy.style.animationDelay = `-${phaser * laneDuration}s`;

            fragment.appendChild(thingy);
        });
    });

    background.replaceChildren(fragment);
}

let resizeTimer;

window.addEventListener("resize", () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(catFaceSpawner, 150);
});

catFaceSpawner();
