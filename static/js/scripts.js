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

// Open the modal
function openModal() {
    document.getElementById("userModal").style.display = "block";
}

// Close the modal
function closeModal() {
    document.getElementById("userModal").style.display = "none";
}

window.onclick = function (event) {
    // Close User Modal if clicked outside
    const userModal = document.getElementById("userModal");
    if (event.target === userModal) {
        userModal.style.display = "none";
    }

    // Close Filter Modal if clicked outside
    const filterModal = document.getElementById("filterModal");
    if (event.target === filterModal) {
        filterModal.style.display = "none";
    }
};

function openEditSidebar() {
    const editModal = document.getElementById("editModal");
    editModal.style.display = "block";
}

function closeEditSidebar() {
    const editModal = document.getElementById("editModal");
    editModal.style.display = "none";
}

function saveEdit() {
    const newName = document.getElementById("editName").value;
    const newSize = document.getElementById("editSize").value;
    const newSupplier = document.getElementById("editSupplier").value;
    const newMin = document.getElementById("editMin").value;

    // Update the entry in the main inventory
    const entryDetails = document.querySelector(".entry-name").closest(".inventory-entry");
    entryDetails.querySelector(".entry-text").innerHTML = `
        <strong class="entry-name">${newName}</strong> ${newSize} | SUPPLIER: ${newSupplier} | MIN: ${newMin}
    `;

    // Close the modal
    closeEditSidebar();
}
