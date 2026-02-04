let currentPWM = window.__INITIAL_PWM__ ?? 1000;

let pwmCanvas, pwmCtx;
let pulseCanvas, pulseCtx;
let scroll = 0;

function sendPWM(value) {
    document.getElementById('val').textContent = value;
    currentPWM = parseInt(value, 10);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/set_live', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send('pwm=' + encodeURIComponent(value));
}

function drawPWM() {
    const w = pwmCanvas.width;
    const h = pwmCanvas.height;

    const period_us = 20000;
    const pwm_us = currentPWM;
    const us_per_pixel = 50;
    const pixels_per_period = period_us / us_per_pixel;
    const high_pixels = pwm_us / us_per_pixel;

    scroll = (scroll + 2) % pixels_per_period;

    pwmCtx.fillStyle = '#0b0f1a';
    pwmCtx.fillRect(0, 0, w, h);

    pwmCtx.strokeStyle = '#00c27a';
    pwmCtx.lineWidth = 2;

    pwmCtx.beginPath();
    for (let x = 0; x < w; x++) {
        const phase = (x + scroll) % pixels_per_period;
        const y = (phase < high_pixels) ? h * 0.25 : h * 0.75;
        if (x === 0) pwmCtx.moveTo(x, y);
        else pwmCtx.lineTo(x, y);
    }
    pwmCtx.stroke();

    requestAnimationFrame(drawPWM);
}

function drawPulseSignal(points) {
    const w = pulseCanvas.width;
    const h = pulseCanvas.height;

    pulseCtx.fillStyle = '#0b0f1a';
    pulseCtx.fillRect(0, 0, w, h);

    pulseCtx.strokeStyle = '#0f8bff';
    pulseCtx.lineWidth = 2;

    const now = Date.now() / 1000;
    const window_s = 5.0;

    pulseCtx.beginPath();
    pulseCtx.moveTo(0, h * 0.75);
    pulseCtx.lineTo(w, h * 0.75);
    pulseCtx.stroke();

    pulseCtx.strokeStyle = '#0f8bff';
    for (let i = 0; i < points.length; i++) {
        const t = points[i].t;
        const age = now - t;
        if (age < 0 || age > window_s) continue;
        const x = w - (age / window_s) * w;
        pulseCtx.beginPath();
        pulseCtx.moveTo(x, h * 0.75);
        pulseCtx.lineTo(x, h * 0.25);
        pulseCtx.stroke();
    }
}

async function refreshHall() {
    const r = await fetch('/api/hall', { cache: 'no-store' });
    const data = await r.json();
    document.getElementById('hall-count').textContent = data.count;
    document.getElementById('rpm').textContent = data.rpm;
    document.getElementById('magnets').textContent = data.magnets_per_rev;
}

async function refreshPulse() {
    const r = await fetch('/api/pulse', { cache: 'no-store' });
    const data = await r.json();
    drawPulseSignal(data);
}

async function refreshAll() {
    try {
        await Promise.all([refreshHall(), refreshPulse()]);
    } catch (e) {
        // ignore transient fetch errors
    }
}

function resizeCanvases() {
    pwmCanvas.width = pwmCanvas.clientWidth;
    pwmCanvas.height = pwmCanvas.clientHeight;
    pulseCanvas.width = pulseCanvas.clientWidth;
    pulseCanvas.height = pulseCanvas.clientHeight;
}

window.addEventListener('load', () => {
    pwmCanvas = document.getElementById('pwmCanvas');
    pwmCtx = pwmCanvas.getContext('2d');
    pulseCanvas = document.getElementById('pulseCanvas');
    pulseCtx = pulseCanvas.getContext('2d');

    const range = document.getElementById('pwmRange');
    range.addEventListener('input', (e) => sendPWM(e.target.value));

    resizeCanvases();
    window.addEventListener('resize', resizeCanvases);

    drawPWM();
    refreshAll();
    setInterval(refreshAll, 300);
});
