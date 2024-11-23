function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('close');
}

function toggleDropdown(event) {
    const target = event.target;
    const parent = target.closest('.sidebar-dropdown');

    // Check if the clicked link is the INVENTORY link
    if (target.textContent.trim() === 'INVENTORY') {
        // Redirect to the inventory page
        window.location.href = "/inventory";
        return;
    }

    if (target.textContent.trim() === 'TRANSACTIONS') {
        // Redirect to the inventory page
        window.location.href = "/transactions";
        return;
    }

    // Otherwise, toggle the dropdown if it exists
    if (parent) {
        event.preventDefault();
        parent.classList.toggle('open');
    }
}


function toggleUserDropdown(event) {
    event.preventDefault();
    const parent = event.target.closest('.user-dropdown');
    parent.classList.toggle('open');
}



document.querySelectorAll('.dropdown a').forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault();
        const targetId = link.getAttribute('href').slice(1); // Remove '#' from href
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

function changeQuantity(button, change) {
    const quantitySpan = button.parentElement.querySelector('.quantity-value');
    let currentQuantity = parseInt(quantitySpan.textContent, 10);
    currentQuantity = Math.max(0, currentQuantity + change); // Prevent negative values
    quantitySpan.textContent = currentQuantity;
}

function openFilterModal() {
    document.getElementById('filterModal').style.display = 'block';
}

function closeFilterModal() {
    document.getElementById('filterModal').style.display = 'none';
}