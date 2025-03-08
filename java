import * as THREE from 'https://cdn.jsdelivr.net/npm/three@latest/build/three.module.js';

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Create hexagonal geometry
const hexShape = new THREE.Shape();
const radius = 2;
for (let i = 0; i < 6; i++) {
    const angle = (i * Math.PI) / 3;
    hexShape.lineTo(Math.cos(angle) * radius, Math.sin(angle) * radius);
}
hexShape.closePath();

const extrudeSettings = { depth: 0.5, bevelEnabled: false };
const hexGeometry = new THREE.ExtrudeGeometry(hexShape, extrudeSettings);
const hexMaterial = new THREE.MeshStandardMaterial({ color: 0xff5733, metalness: 0.5, roughness: 0.3 });
const hexMesh = new THREE.Mesh(hexGeometry, hexMaterial);
scene.add(hexMesh);

// Hexagonal Sphere (Wireframe)
const sphereGeometry = new THREE.SphereGeometry(3.5, 6, 6);
const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
const sphereMesh = new THREE.Mesh(sphereGeometry, sphereMaterial);
scene.add(sphereMesh);

// Lighting
const light = new THREE.PointLight(0xffffff, 1, 100);
light.position.set(5, 5, 5);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040));

// Camera position
camera.position.z = 8;

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    hexMesh.rotation.x += 0.02;
    hexMesh.rotation.y += 0.02;
    renderer.render(scene, camera);
}
animate();

// Resize handling
window.addEventListener('resize', () => {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
});
