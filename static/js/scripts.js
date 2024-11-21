function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('close');
}

function toggleDropdown(event) {
    event.preventDefault();
    const parent = event.target.closest('.sidebar-dropdown');
    parent.classList.toggle('open');
}

function toggleUserDropdown(event) {
    event.preventDefault();
    const parent = event.target.closest('.user-dropdown');
    parent.classList.toggle('open');
}