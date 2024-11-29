function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('close');
}

function toggleDropdown(event) {
    const target = event.target;
    const parent = target.closest('.sidebar-dropdown');

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

// Search bar
function performSearch() {
    const query = document.getElementById('searchBar').value.trim(); // Get the search query
    
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
                        <div onclick="selectItem('${item.entry_id}')">
                            | ${item.name.toUpperCase()} ${item.size}mL ${item.supplier}
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

function selectItem(entry_id) {
    $.ajax({
        url: '/selectedItem',
        method: 'GET',
        data: { EntryID: entry_id },
        success: function(response) {
            if (response.html) {
                // Replace the entire <body> content with the new HTML
                document.open();
                document.write(response.html);
                document.close();
            } else if (response.error) {
            }
        },
        error: function() {
            alert('An error occurred while selecting the item.');
        }
    });
}

// Hide dropdown if clicked outside
$(document).click(function(e) {
    if (!$(e.target).closest('#searchBar, #searchDropdown').length) {
        $('#searchDropdown').hide();
    }
});

let quantityUpdateTimeout;
function changeQuantity(button, change) {
    const quantitySpan = button.parentElement.querySelector('.quantity-value');
    let currentQuantity = parseInt(quantitySpan.textContent, 10);
    currentQuantity = Math.max(0, currentQuantity + change); // Prevent negative values
    quantitySpan.textContent = currentQuantity;

    // Get necessary data to send to Flask
    const entryID = button.closest('.inventory-entry').getAttribute('data-entry-id'); // Assuming each entry has a data attribute for its ID
    const newQuantity = currentQuantity;

    // Clear any existing timeout to debounce
    clearTimeout(quantityUpdateTimeout);

    // Set a timeout to delay sending the update request
    quantityUpdateTimeout = setTimeout(() => {
        updateQuantityOnServer(entryID, newQuantity);
    }, 500); // 0.5-second delay
}

function updateQuantityOnServer(entryID, quantity) {
    // Send data to Flask
    fetch('/updateQuantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ entryID, quantity }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Quantity updated successfully:', data);
    })
    .catch(error => {
        console.error('Error updating quantity:', error);
    });
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

function openEditModal(uid, photo, name, size, category, supplier, minRequirement) {
    document.querySelector('[name="u_item_uid"]').value = uid;
    document.querySelector('[name="u_item_photo"]').value = photo;
    document.querySelector('[name="u_item_name"]').value = name;
    document.querySelector('[name="u_item_category"]').value = category;
    document.querySelector('[name="u_item_size"]').value = size;
    document.querySelector('[name="u_item_supplier"]').value = supplier;
    document.querySelector('[name="u_item_min_requirement"]').value = minRequirement;

    // Open the modal
    document.getElementById('editModal').style.display = 'block';
}

function saveEdit() {
    const formData = new FormData(document.getElementById('updateEntry'));
    const data = {
        u_item_uid: formData.get('u_item_uid'),
        u_item_photo: formData.get('u_item_photo'),
        u_item_name: formData.get('u_item_name'),
        u_item_category: formData.get('u_item_category'),
        u_item_size: formData.get('u_item_size'),
        u_item_supplier: formData.get('u_item_supplier'),
        u_item_min_requirement: formData.get('u_item_min_requirement'),
    };

    fetch('/updateEntry', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(result => {
        console.log('Update successful:', result);
        location.reload(); // Reload the page to reflect the changes
    })
    .catch(error => {
        console.error('Error updating item:', error);
    });
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

function performSearchBulk() {
    const query = document.getElementById('searchBar').value.trim(); // Get the search query
    
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
                        <div onclick="selectItemBulk('${item.entry_id}')">
                            | ${item.name.toUpperCase()} ${item.size}mL ${item.supplier}
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

function selectItemBulk(entry_id) {
    // Populate and open the modal for quantity input
    document.getElementById('selectedEntryID').value = entry_id; // Set hidden input for entry_id
    document.getElementById('quantityModal').style.display = 'block';
}

function removeDrinkD(entry_id) {
    // Make the POST request to remove the item
    $.ajax({
        url: '/removeDecrease', // Backend endpoint for removing the item
        method: 'POST',
        data: { entry_id: entry_id }, // Send the entry ID
        success: function (response) {
            if (response.html) {
                // Replace the entire page content with the updated HTML
                document.body.innerHTML = response.html;
            }
        },
        error: function (xhr, status, error) {
            console.error('Error:', xhr.responseText);
        }
    });
}

function removeDrinkI(entry_id) {
    // Make the POST request to remove the item
    $.ajax({
        url: '/removeIncrease', // Backend endpoint for removing the item
        method: 'POST',
        data: { entry_id: entry_id }, // Send the entry ID
        success: function (response) {
            if (response.html) {
                // Replace the entire page content with the updated HTML
                document.body.innerHTML = response.html;
            }
        },
        error: function (xhr, status, error) {
            console.error('Error:', xhr.responseText);
        }
    });
}

function changeQuantityTemp(button, change) {
    const quantitySpan = button.parentElement.querySelector('.quantity-value');
    let currentQuantity = parseInt(quantitySpan.textContent, 10);
    currentQuantity = Math.max(0, currentQuantity + change); // Prevent negative values
    quantitySpan.textContent = currentQuantity;
    document.getElementById('quantity').value = currentQuantity;
}

function performSearchTra() {
    const query = document.getElementById('searchBar').value.trim(); // Get the search query
    
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
                    size = item.size;
                    size_str = size >= 1000 ? (size/1000)+'L' : size+'mL'; // Format size for display
                    dropdown.append(`
                        <div onclick="selectItemTra('${item.entry_id}', '${item.name}', '${item.size}', '${item.supplier}')">
                            | ${item.name.toUpperCase()} ${size_str} ${item.supplier}
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

function empty(){
    document.getElementById('searchBar').value = ''; // Clear the search bar
    $('#searchDropdown').hide(); // Hide the dropdown
}

function selectItemTra(entry_id, name, size, supplier) {
    size_str = size >= 1000 ? (size/1000)+'L' : size+'mL';
    // Populate and open the modal for quantity input
    document.getElementById('item_uid').value = entry_id; // Set hidden input for entry_id
    $('#searchDropdown').hide();
    document.getElementById('searchBar').value = name.toUpperCase() + ' ' + size_str + ' | Supplier: ' + supplier;
}