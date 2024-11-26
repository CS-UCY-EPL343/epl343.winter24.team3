document.getElementById('register-form-element').addEventListener('submit', function (event) {
    event.preventDefault(); 

    const username = document.getElementById('new-username').value.trim();
    const password = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const passwordError = document.getElementById('password-error');

    // check if username !=null
    if (!username) {
        alert('Please enter a valid username.');
        return;
    }

    // if password and confirmPassword are not equal
    if (password !== confirmPassword) {
        passwordError.style.display = 'block'; // error message
        return; 
    } else {
        passwordError.style.display = 'none'; 
    }

    //if valid then submit
    alert('Registration successful!');
    this.submit();
});

//elegxos gia Login Form
function validateLogin(event) {
    event.preventDefault(); 

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value;
    const loginError = document.getElementById('login-error');

    // error message
    if (!username || !password) {
        loginError.style.display = 'block';
        return false;
    }

    loginError.style.display = 'none';
    alert('Login successful!');
    return true;
}
