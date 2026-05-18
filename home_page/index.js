const engines = {
    google: {
        label: "Google",
        url: "https://www.google.com/search?q="
    },
    duckduckgo: {
        label: "DuckDuckGo",
        url: "https://duckduckgo.com/?q="
    },
    brave: {
        label: "Brave Search",
        url: "https://search.brave.com/search?q="
    },
    bing: {
        label: "Bing",
        url: "https://www.bing.com/search?q="
    },
    yandex: {
        label: "Yandex",
        url: "https://yandex.com/search/?text="
    }
};

const form = document.querySelector(".search");
const input = document.querySelector(".search__input");
const glass = document.querySelector(".search__glass");
const enginePicker = document.querySelector("#enginePicker");
const engineButton = document.querySelector("#engineButton");
const engineLabel = document.querySelector("#engineLabel");
const engineLogo = document.querySelector("#engineLogo");
const engineOptions = Array.from(document.querySelectorAll(".engine__option"));

function syncViewportWidth() {
    const outerWidth = window.outerWidth || window.innerWidth;
    const appWidth = Math.max(320, Math.min(window.innerWidth, outerWidth));
    document.documentElement.style.setProperty("--app-width", `${appWidth}px`);
    document.documentElement.classList.toggle("is-compact", appWidth <= 520);
}

function readSavedEngine() {
    try {
        return localStorage.getItem("robust-search-engine");
    } catch (error) {
        return null;
    }
}

function saveEngine(engineKey) {
    try {
        localStorage.setItem("robust-search-engine", engineKey);
    } catch (error) {
        return;
    }
}

let currentEngine = readSavedEngine() || "google";

function setEngine(engineKey) {
    const engine = engines[engineKey] || engines.google;
    currentEngine = engineKey in engines ? engineKey : "google";
    engineLabel.textContent = engine.label;

    engineOptions.forEach((option) => {
        const isSelected = option.dataset.engine === currentEngine;
        option.classList.toggle("is-selected", isSelected);
        option.setAttribute("aria-selected", String(isSelected));
    });

    const selectedLogo = document.querySelector(`.engine__option[data-engine="${currentEngine}"] .engine__logo`);
    if (selectedLogo) {
        engineLogo.className = selectedLogo.className;
        engineLogo.innerHTML = selectedLogo.innerHTML;
    }

    saveEngine(currentEngine);
}

function openEngineMenu() {
    enginePicker.classList.add("is-open");
    engineButton.setAttribute("aria-expanded", "true");
}

function closeEngineMenu() {
    enginePicker.classList.remove("is-open");
    engineButton.setAttribute("aria-expanded", "false");
}

function toggleEngineMenu() {
    if (enginePicker.classList.contains("is-open")) {
        closeEngineMenu();
    } else {
        openEngineMenu();
    }
}

function createDestination(rawValue) {
    const value = rawValue.trim();

    if (!value) {
        return "";
    }

    const hasProtocol = /^[a-z][a-z0-9+.-]*:\/\//i.test(value);
    const isLocalhost = /^localhost(?::\d+)?(?:\/|$)/i.test(value);
    const isIp = /^(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?(?:\/|$)/.test(value);
    const looksLikeDomain = /^[^\s/@]+\.[^\s]{2,}(?:\/.*)?$/i.test(value);

    if (hasProtocol) {
        return value;
    }

    if (isLocalhost || isIp || looksLikeDomain) {
        return "https://" + value;
    }

    return engines[currentEngine].url + encodeURIComponent(value);
}

engineButton.addEventListener("click", toggleEngineMenu);

engineOptions.forEach((option) => {
    option.addEventListener("click", () => {
        setEngine(option.dataset.engine);
        closeEngineMenu();
        input.focus();
    });
});

document.addEventListener("click", (event) => {
    if (!enginePicker.contains(event.target)) {
        closeEngineMenu();
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeEngineMenu();
        input.focus();
    }

    if ((event.key === "ArrowDown" || event.key === "ArrowUp") && enginePicker.classList.contains("is-open")) {
        event.preventDefault();
        const activeElement = document.activeElement;
        const currentIndex = engineOptions.indexOf(activeElement);
        const direction = event.key === "ArrowDown" ? 1 : -1;
        const nextIndex = currentIndex === -1
            ? 0
            : (currentIndex + direction + engineOptions.length) % engineOptions.length;

        engineOptions[nextIndex].focus();
    }
});

form.addEventListener("submit", (event) => {
    event.preventDefault();
    const destination = createDestination(input.value);

    if (destination) {
        window.location.href = destination;
    }
});

function handlePointerMove(event) {
    const x = event.clientX / window.innerWidth - 0.5;
    const y = event.clientY / window.innerHeight - 0.5;

    document.documentElement.style.setProperty("--parallax-x", `${x * -10}px`);
    document.documentElement.style.setProperty("--parallax-y", `${y * -7}px`);

    if (glass) {
        const rect = glass.getBoundingClientRect();
        const reflectX = ((event.clientX - rect.left) / rect.width) * 100;
        const reflectY = ((event.clientY - rect.top) / rect.height) * 100;
        glass.style.setProperty("--reflect-x", `${reflectX}%`);
        glass.style.setProperty("--reflect-y", `${reflectY}%`);
    }
}

document.addEventListener("pointermove", handlePointerMove, { passive: true });
document.addEventListener("mousemove", handlePointerMove, { passive: true });

syncViewportWidth();
setEngine(currentEngine);
window.setTimeout(() => input.focus(), 250);

const canvas = document.querySelector("#orbCanvas");
const ctx = canvas.getContext("2d", { alpha: true });
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const scene = {
    width: 0,
    height: 0,
    dpr: 1,
    mouseX: 0,
    mouseY: 0,
    targetMouseX: 0,
    targetMouseY: 0
};

const objects = [
    { type: "glow", x: 0.09, y: 0.14, radius: 0.1, depth: 0.18, phase: 0.8, speed: 0.04, alpha: 0.42 },
    { type: "sphere", x: 0.16, y: 0.48, radius: 0.16, depth: 0.34, phase: 2.2, speed: 0.035, alpha: 0.42, hue: 212 },
    { type: "sphere", x: 0.75, y: 0.24, radius: 0.115, depth: 0.5, phase: 0.4, speed: 0.044, alpha: 0.58, hue: 202 },
    { type: "sphere", x: 0.43, y: 0.82, radius: 0.13, depth: 0.66, phase: 3.1, speed: 0.03, alpha: 0.56, hue: 207 },
    { type: "sphere", x: 0.67, y: 0.72, radius: 0.08, depth: 0.72, phase: 5.1, speed: 0.047, alpha: 0.38, hue: 209 },
    { type: "darkSphere", x: 0.84, y: 0.57, radius: 0.092, depth: 0.88, phase: 1.2, speed: 0.038, alpha: 0.74 },
    { type: "glow", x: 0.88, y: 0.8, radius: 0.1, depth: 0.32, phase: 4.5, speed: 0.033, alpha: 0.3 },
    { type: "bowl", x: 0.63, y: 0.32, radius: 0.12, depth: 0.42, phase: 2.9, speed: 0.026, alpha: 0.2 }
];

const dust = Array.from({ length: 36 }, () => ({
    x: Math.random(),
    y: Math.random(),
    size: Math.random() * 0.9 + 0.28,
    speed: Math.random() * 0.05 + 0.018,
    drift: Math.random() * 0.35 + 0.12,
    phase: Math.random() * Math.PI * 2,
    alpha: Math.random() * 0.14 + 0.05
}));

function resizeCanvas() {
    scene.width = window.innerWidth;
    scene.height = window.innerHeight;
    scene.dpr = Math.min(window.devicePixelRatio || 1, 1.6);

    canvas.width = Math.floor(scene.width * scene.dpr);
    canvas.height = Math.floor(scene.height * scene.dpr);
    canvas.style.width = scene.width + "px";
    canvas.style.height = scene.height + "px";

    ctx.setTransform(scene.dpr, 0, 0, scene.dpr, 0, 0);
}

function drawBackground(time) {
    const gradient = ctx.createLinearGradient(0, 0, scene.width, scene.height);
    gradient.addColorStop(0, "#031a55");
    gradient.addColorStop(0.36, "#020d2b");
    gradient.addColorStop(0.72, "#000612");
    gradient.addColorStop(1, "#000207");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, scene.width, scene.height);

    ctx.save();
    ctx.globalCompositeOperation = "screen";
    const wash = ctx.createRadialGradient(
        scene.width * (0.35 + Math.sin(time * 0.035) * 0.02),
        scene.height * 0.55,
        0,
        scene.width * 0.35,
        scene.height * 0.55,
        Math.max(scene.width, scene.height) * 0.68
    );
    wash.addColorStop(0, "rgba(20, 75, 190, 0.14)");
    wash.addColorStop(0.46, "rgba(7, 34, 98, 0.07)");
    wash.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = wash;
    ctx.fillRect(0, 0, scene.width, scene.height);
    ctx.restore();
}

function getObjectPosition(object, time) {
    const motion = reducedMotion ? 0 : 1;
    const floatX = Math.sin(time * object.speed + object.phase) * 36 * object.depth * motion;
    const floatY = Math.cos(time * object.speed * 0.85 + object.phase) * 30 * object.depth * motion;
    const parallaxX = scene.mouseX * 78 * object.depth;
    const parallaxY = scene.mouseY * 54 * object.depth;

    return {
        x: scene.width * object.x + floatX + parallaxX,
        y: scene.height * object.y + floatY + parallaxY,
        radius: Math.max(scene.width, scene.height) * object.radius
    };
}

function drawShadow(x, y, radius, alpha) {
    ctx.save();
    ctx.globalAlpha = alpha;
    ctx.filter = `blur(${Math.max(18, radius * 0.18)}px)`;
    ctx.fillStyle = "rgba(0, 0, 0, 0.72)";
    ctx.beginPath();
    ctx.ellipse(x + radius * 0.24, y + radius * 1.08, radius * 0.92, radius * 0.2, -0.08, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
}

function drawGlow(object, time) {
    const { x, y, radius } = getObjectPosition(object, time);
    ctx.save();
    ctx.globalCompositeOperation = "screen";
    ctx.filter = `blur(${radius * 0.16}px)`;
    const glow = ctx.createRadialGradient(x, y, 0, x, y, radius);
    glow.addColorStop(0, `rgba(67, 169, 255, ${0.5 * object.alpha})`);
    glow.addColorStop(0.44, `rgba(21, 103, 230, ${0.2 * object.alpha})`);
    glow.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
}

function drawSphere(object, time) {
    const { x, y, radius } = getObjectPosition(object, time);
    drawShadow(x, y, radius, 0.34 * object.alpha);

    ctx.save();
    ctx.globalCompositeOperation = "screen";
    const outerGlow = ctx.createRadialGradient(x - radius * 0.2, y - radius * 0.18, radius * 0.1, x, y, radius * 1.45);
    outerGlow.addColorStop(0, `rgba(66, 178, 255, ${0.18 * object.alpha})`);
    outerGlow.addColorStop(0.55, `rgba(30, 100, 238, ${0.08 * object.alpha})`);
    outerGlow.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = outerGlow;
    ctx.beginPath();
    ctx.arc(x, y, radius * 1.45, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    ctx.save();
    const body = ctx.createRadialGradient(
        x - radius * 0.36,
        y - radius * 0.43,
        radius * 0.06,
        x + radius * 0.18,
        y + radius * 0.24,
        radius * 1.05
    );
    body.addColorStop(0, `rgba(175, 224, 255, ${0.62 * object.alpha})`);
    body.addColorStop(0.18, `rgba(42, 167, 255, ${0.88 * object.alpha})`);
    body.addColorStop(0.52, `rgba(24, 94, 221, ${0.92 * object.alpha})`);
    body.addColorStop(0.82, `rgba(3, 24, 82, ${0.96 * object.alpha})`);
    body.addColorStop(1, `rgba(0, 7, 28, ${object.alpha})`);
    ctx.fillStyle = body;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();

    const highlight = ctx.createRadialGradient(
        x - radius * 0.43,
        y - radius * 0.45,
        0,
        x - radius * 0.43,
        y - radius * 0.45,
        radius * 0.55
    );
    highlight.addColorStop(0, `rgba(255, 255, 255, ${0.34 * object.alpha})`);
    highlight.addColorStop(0.34, `rgba(119, 205, 255, ${0.18 * object.alpha})`);
    highlight.addColorStop(1, "rgba(255, 255, 255, 0)");
    ctx.globalCompositeOperation = "screen";
    ctx.fillStyle = highlight;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
}

function drawDarkSphere(object, time) {
    const { x, y, radius } = getObjectPosition(object, time);
    drawShadow(x, y, radius, 0.52);

    ctx.save();
    const body = ctx.createRadialGradient(
        x - radius * 0.46,
        y - radius * 0.44,
        radius * 0.02,
        x + radius * 0.22,
        y + radius * 0.22,
        radius
    );
    body.addColorStop(0, "rgba(28, 105, 232, 0.48)");
    body.addColorStop(0.2, "rgba(7, 26, 82, 0.62)");
    body.addColorStop(0.62, "rgba(0, 4, 14, 0.98)");
    body.addColorStop(1, "rgba(0, 0, 0, 1)");
    ctx.fillStyle = body;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.globalCompositeOperation = "screen";
    const rim = ctx.createRadialGradient(
        x - radius * 0.62,
        y - radius * 0.38,
        radius * 0.28,
        x,
        y,
        radius * 1.02
    );
    rim.addColorStop(0, "rgba(43, 150, 255, 0.34)");
    rim.addColorStop(0.42, "rgba(23, 102, 255, 0.12)");
    rim.addColorStop(0.78, "rgba(0, 0, 0, 0)");
    rim.addColorStop(1, "rgba(80, 174, 255, 0.16)");
    ctx.fillStyle = rim;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
}

function drawBowl(object, time) {
    const { x, y, radius } = getObjectPosition(object, time);
    drawShadow(x, y, radius, 0.26);

    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(-0.18);
    ctx.scale(1.25, 0.54);

    const body = ctx.createRadialGradient(-radius * 0.28, -radius * 0.25, radius * 0.1, 0, 0, radius);
    body.addColorStop(0, `rgba(92, 176, 255, ${0.42 * object.alpha})`);
    body.addColorStop(0.45, `rgba(15, 80, 198, ${0.7 * object.alpha})`);
    body.addColorStop(1, `rgba(1, 10, 32, ${0.82 * object.alpha})`);
    ctx.fillStyle = body;
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI, true);
    ctx.lineTo(radius, 0);
    ctx.arc(0, 0, radius, 0, Math.PI, false);
    ctx.closePath();
    ctx.fill();

    ctx.globalCompositeOperation = "screen";
    ctx.strokeStyle = `rgba(121, 202, 255, ${0.18 * object.alpha})`;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.ellipse(0, 0, radius, radius * 0.22, 0, Math.PI, 0);
    ctx.stroke();
    ctx.restore();
}

function drawDust(time) {
    ctx.save();
    ctx.globalCompositeOperation = "screen";

    dust.forEach((particle) => {
        const x = particle.x * scene.width
            + Math.sin(time * particle.drift + particle.phase) * 14
            + scene.mouseX * 16;
        const rawY = particle.y * scene.height + time * particle.speed * 12;
        const y = rawY % (scene.height + 40) - 20 + scene.mouseY * 12;
        const alpha = particle.alpha * (0.6 + Math.sin(time * 0.5 + particle.phase) * 0.22);

        ctx.fillStyle = `rgba(178, 218, 255, ${alpha})`;
        ctx.beginPath();
        ctx.arc(x, y, particle.size, 0, Math.PI * 2);
        ctx.fill();
    });

    ctx.restore();
}

function animate(timeStamp) {
    const time = timeStamp * 0.001;
    scene.mouseX += (scene.targetMouseX - scene.mouseX) * 0.05;
    scene.mouseY += (scene.targetMouseY - scene.mouseY) * 0.05;

    drawBackground(time);
    objects.forEach((object) => {
        if (object.type === "glow") {
            drawGlow(object, time);
        } else if (object.type === "sphere") {
            drawSphere(object, time);
        } else if (object.type === "darkSphere") {
            drawDarkSphere(object, time);
        } else if (object.type === "bowl") {
            drawBowl(object, time);
        }
    });

    drawDust(time);
    requestAnimationFrame(animate);
}

function updateScenePointer(event) {
    scene.targetMouseX = event.clientX / window.innerWidth - 0.5;
    scene.targetMouseY = event.clientY / window.innerHeight - 0.5;
}

window.addEventListener("resize", resizeCanvas);
window.addEventListener("resize", syncViewportWidth);
document.addEventListener("pointermove", updateScenePointer, { passive: true });
document.addEventListener("mousemove", updateScenePointer, { passive: true });

resizeCanvas();
requestAnimationFrame(animate);
