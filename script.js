/* ============================================
   SCRIPT.JS — AMAS AI shared utilities
   - Aurora canvas background    (only runs if #bg-canvas exists)
   - GSAP reveal animations      (only runs if matching elements exist)
   - Hover-button orb effect     (only runs on .hover-btn)
   ============================================
   Safe to drop on any page — each block has its own existence guard.
*/

// ─── THREE.JS AURORA BACKGROUND ─────────────────────
const canvas = document.getElementById('bg-canvas');

if (canvas) {
    const scene    = new THREE.Scene();
    const camera   = new THREE.PerspectiveCamera(35, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 60;

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Mouse tracking
    const mouse = new THREE.Vector2(0, 0);
    window.addEventListener('mousemove', (e) => {
        mouse.x = (e.clientX / window.innerWidth)  * 2 - 1;
        mouse.y = (e.clientY / window.innerHeight) * 2 - 1;
    });

    // ── Liquid Background Shader ──
    const bgUniforms = {
        uTime:  { value: 0 },
        uMouse: { value: new THREE.Vector2(0, 0) }
    };

    const bgGeo = new THREE.PlaneGeometry(1, 1);
    const bgMat = new THREE.ShaderMaterial({
        transparent: true,
        uniforms: bgUniforms,
        vertexShader: `
            varying vec2 vUv;
            void main() {
                vUv = uv;
                gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
            }
        `,
        fragmentShader: `
            uniform float uTime;
            uniform vec2  uMouse;
            varying vec2  vUv;

            void main() {
                vec2  uv = vUv;
                float t  = uTime * 0.15;
                vec2  m  = uMouse * 0.1;

                float wave = (
                    sin(uv.x * 8.0 + t + m.x * 12.0) +
                    sin(uv.y * 6.0 - t + m.y * 12.0)
                ) * 0.5 + 0.5;

                float c = smoothstep(0.0, 1.0, wave);
                gl_FragColor = vec4(mix(vec3(0.004), vec3(0.04, 0.06, 0.08), c), 1.0);
            }
        `
    });

    const bgMesh = new THREE.Mesh(bgGeo, bgMat);
    scene.add(bgMesh);

    // Scale bg to fill screen
    function scaleBg() {
        const vFov   = THREE.MathUtils.degToRad(camera.fov);
        const height = 2 * Math.tan(vFov / 2) * camera.position.z;
        const width  = height * camera.aspect;
        bgMesh.scale.set(width, height, 1);
    }
    scaleBg();

    // ── Rotating Icosahedron (Monolith) ──
    const icoGeo = new THREE.IcosahedronGeometry(13, 1);
    const icoMat = new THREE.MeshStandardMaterial({
        color:     0x0a0a0a,
        roughness: 0.05,
        metalness: 1.0,
    });
    const icoMesh = new THREE.Mesh(icoGeo, icoMat);
    icoMesh.position.set(18, 0, -10);
    scene.add(icoMesh);

    // Lights for icosahedron
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const spotLight = new THREE.SpotLight(0x00C2FF, 3);
    spotLight.position.set(50, 50, 50);
    scene.add(spotLight);

    // ── Animation Loop ──
    const clock = new THREE.Clock();
    let floatOffset = 0;

    function animate() {
        requestAnimationFrame(animate);

        const elapsed = clock.getElapsedTime();
        floatOffset   = Math.sin(elapsed * 0.6) * 1.5;

        // Update shader uniforms
        bgUniforms.uTime.value = elapsed;
        bgUniforms.uMouse.value.lerp(mouse, 0.05);

        // Rotate icosahedron
        icoMesh.rotation.y  = elapsed * 0.25;
        icoMesh.rotation.x  = elapsed * 0.1;
        icoMesh.position.y  = floatOffset;

        renderer.render(scene, camera);
    }
    animate();

    // ── Resize Handler ──
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
        scaleBg();
    });
}


// ─── GSAP ANIMATIONS ─────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    if (typeof gsap === 'undefined') return;

    // Reveal hero on load (landing page)
    const reveal = document.getElementById('reveal');
    if (reveal) {
        gsap.fromTo(reveal,
            { filter: 'blur(30px)', opacity: 0, scale: 1.02 },
            { filter: 'blur(0px)',  opacity: 1, scale: 1,
              duration: 2.2, ease: 'expo.out' }
        );
    }

    // Stagger cards in from right (landing page)
    const cards = document.querySelectorAll('.command-cell');
    if (cards.length) {
        gsap.from(cards, {
            x: 60, opacity: 0,
            stagger: 0.12,
            duration: 1.5,
            ease: 'power4.out',
            delay: 0.8,
            clearProps: 'all'
        });
    }

    // CTA button magnetic effect (landing page)
    const ctaBtn = document.getElementById('cta-btn');
    if (ctaBtn) {
        window.addEventListener('mousemove', (e) => {
            const rect = ctaBtn.getBoundingClientRect();
            const cx   = rect.left + rect.width  / 2;
            const cy   = rect.top  + rect.height / 2;
            const dist = Math.hypot(e.clientX - cx, e.clientY - cy);

            if (dist < 160) {
                gsap.to(ctaBtn, {
                    x: (e.clientX - cx) * 0.35,
                    y: (e.clientY - cy) * 0.35,
                    duration: 0.5,
                    ease: 'power2.out'
                });
            } else {
                gsap.to(ctaBtn, {
                    x: 0, y: 0,
                    duration: 0.8,
                    ease: 'elastic.out(1, 0.3)'
                });
            }
        });
    }
});


// ─── BUTTON ORB EFFECT ───────────────────────
document.querySelectorAll('.hover-btn').forEach((btn) => {
    let lastTime  = 0;
    let listening = false;

    btn.addEventListener('pointerenter', () => listening = true);
    btn.addEventListener('pointerleave', () => listening = false);

    btn.addEventListener('pointermove', (e) => {
        if (!listening) return;

        const now = Date.now();
        if (now - lastTime < 100) return;
        lastTime = now;

        const rect = btn.getBoundingClientRect();
        const x    = e.clientX - rect.left;
        const y    = e.clientY - rect.top;

        const orb = document.createElement('div');
        orb.classList.add('btn-orb');
        orb.style.left = x + 'px';
        orb.style.top  = y + 'px';
        btn.appendChild(orb);

        // Fade in
        requestAnimationFrame(() => orb.classList.add('visible'));

        // Fade out + remove
        setTimeout(() => orb.classList.replace('visible', 'fading'), 1000);
        setTimeout(() => orb.remove(), 2200);
    });
});