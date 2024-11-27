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

function performSearch() {
    const query = $('#searchBar').val().trim(); // Get the search query

    if (query.length === 0) {
        $('#searchDropdown').hide(); // Hide dropdown if query is empty
        return;
    }

    $.ajax({
        url: '/search',
        method: 'GET',
        data: { query: query },
        success: function(data) {
            const dropdown = $('#searchDropdown');
            dropdown.empty(); // Clear previous results
            if (data.length === 0) {
                dropdown.append('<div>No matching items found.</div>');
            } else {
                data.forEach(item => {
                    dropdown.append(`
                        <div onclick="selectItem('${item.uid}', '${item.name}', '${item.size}', '${item.quantity}')">
                            ${item.name} (UID: ${item.uid})
                        </div>
                    `);
                });
            }
            dropdown.show(); // Show dropdown
        },
        error: function() {
            alert('An error occurred while searching. Please try again.');
        }
    });
}

function selectItem(uid, name, size, quantity) {
    // Hide the dropdown
    $('#searchDropdown').hide();

    // Populate the inventory table with the selected item
    $('#inventoryBody').html(`
        <tr>
            <td>${uid}</td>
            <td>${name}</td>
            <td>${size}</td>
            <td>${quantity}</td>
        </tr>
    `);

    // Optionally, clear the search bar
    $('#searchBar').val('');
}

// Hide dropdown if clicked outside
$(document).click(function(e) {
    if (!$(e.target).closest('#searchBar, #searchDropdown').length) {
        $('#searchDropdown').hide();
    }
});

function changeQuantity(button, change) {
    const quantitySpan = button.parentElement.querySelector('.quantity-value');
    let currentQuantity = parseInt(quantitySpan.textContent, 10);
    currentQuantity = Math.max(0, currentQuantity + change); // Prevent negative values
    quantitySpan.textContent = currentQuantity;
}


// Open the modal
function openModal(entryId) {
    document.getElementById(entryId).style.display = "block";
}

// Close the modal
function closeModal(entryId) {
    document.getElementById(entryId).style.display = "none";
}

// NOT WORKING FRO SOME REASONDSDEIFHE
window.onclick = function (event) {
    // List of modal IDs
    const modalIds = ["userModal", "filterModal", "editModal", "addEntryModal"];

    modalIds.forEach(id => {
        const modal = document.getElementById(id);
        if (modal && event.target === modal) {
            modal.style.display = "none";
        }
    });
};

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

// Remove a specific drink entry
function removeDrink(entryId) {
    // Find the specific entry by its ID and remove it from the DOM
    const entry = document.getElementById(entryId);
    if (entry) {
        entry.remove();
    }
}

// Remove all entries when submit is clicked
function submitDecrement() {
    // Get all the entries inside the 'entry-list' container
    const entries = document.querySelectorAll('.inventory-entry');

    // Remove each entry
    entries.forEach(entry => {
        entry.remove();
    });
}

function submitIncrement() {
    // Get all the entries inside the 'entry-list' container
    const entries = document.querySelectorAll('.inventory-entry');

    // Remove each entry
    entries.forEach(entry => {
        entry.remove();
    });
}

function saveNewEntry() {
    const newName = document.getElementById("addName").value;
    const newSize = document.getElementById("addSize").value;
    const newSupplier = document.getElementById("addSupplier").value;
    const newMin = document.getElementById("addMin").value;
    const newCategory = document.getElementById("addCategory").value;
    const newPicture = document.getElementById("addPicture").value;

    const newEntry = document.createElement('div');
    newEntry.classList.add('inventory-entry');

    newEntry.innerHTML = `
        <img src="${newPicture}" alt="${newName}" class="entry-image">
        <div class="entry-details">
            <span class="entry-info">
                <span class="entry-text">
                    <strong class="entry-name">${newName}</strong> ${newSize} | SUPPLIER: ${newSupplier} | MIN: ${newMin} | CATEGORY: ${newCategory}
                </span>
                <span class="entry-quantity">
                    <button class="quantity-btn" onclick="changeQuantity(this, -1)">-</button>
                    <span class="quantity-value">0</span>
                    <button class="quantity-btn" onclick="changeQuantity(this, 1)">+</button>
                </span>
            </span>
        </div>
        <img src="https://www.svgrepo.com/show/304506/edit-pen.svg" alt="EDIT" class="edit-button" onclick="openEditSidebar()">
    `;

    // Add the new entry to the inventory
    document.querySelector(".entry-list").appendChild(newEntry);

    // Close the modal
    closeAddEntryModal();
}

