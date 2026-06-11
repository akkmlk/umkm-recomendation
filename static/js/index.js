// 1. Tangkap semua elemen yang dibutuhkan
const triggerBtn = document.getElementById('btn-input');
const searchModal = document.getElementById('search-modal');
const closeModalBtn = document.getElementById('close-modal');
const realInput = document.getElementById('real-search-input');
const overlay = document.getElementById('overlay-body');

// 2. Fungsi untuk Membuka Modal
triggerBtn.addEventListener('click', () => {
    // Hapus class 'hidden' agar modal muncul
    searchModal.classList.remove('hidden');
    overlay.classList.remove('hidden');

    // (Opsional/UX Bagus) Langsung arahkan kursor (fokus) ke input asli di dalam modal
    setTimeout(() => {
        realInput.focus();
    }, 100);
});

// 3. Fungsi untuk Menutup Modal (via tombol X)
closeModalBtn.addEventListener('click', () => {
    searchModal.classList.add('hidden');
    overlay.classList.add('hidden');
});

// 4. (Bonus UX) Tutup modal jika user mengklik area gelap di luar kotak modal
window.addEventListener('click', (event) => {
    if (event.target === searchModal) {
        searchModal.classList.add('hidden');
        overlay.classList.add('hidden');
    }
});


// product-slider di halaman produk detail
const slider = document.getElementById('product-slider');
let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener("mousedown", (e) => {
    isDown = true;
    slider.classList.add('cursor-grabbing');
    slider.classList.remove('cursor-grab');
    slider.classList.remove('snap-x', 'snap-mandatory');

    startX = e.pageX - slider.offsetLeft;
    scrollLeft = slider.scrollLeft;
});

slider.addEventListener('mouseup', () => {
    isDown = false;
    slider.classList.remove('cursor-grabbing');
    slider.classList.add('cursor-grab');
    slider.classList.add('snap-x', 'snap-mandotory');
});
slider.addEventListener('mouseleave', () => {
    isDown = false;
    slider.classList.remove('cursor-grabbing');
    slider.classList.add('cursor-grab');
    slider.classList.add('snap-x', 'snap-mandotory');
});

slider.addEventListener('mousemove', (e) => {
    if (!isDown) return;
    e.preventDefault()

    const x = e.pageX - slider.offsetLeft;
    const walk = (x - startX) * 15;

    slider.scrollLeft = scrollLeft - walk;
});