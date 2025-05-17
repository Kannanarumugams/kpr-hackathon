// Toggle between sign-in and sign-up forms
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});

// Handle form submissions
document.querySelector('.sign-up-container form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const user = {
        name: this.querySelector('input[type="text"]').value,
        email: this.querySelector('input[type="email"]').value,
        password: this.querySelector('input[type="password"]').value
    };
    
    // Store user data in localStorage
    localStorage.setItem('user', JSON.stringify(user));
    alert('Registration successful! Please sign in.');
    container.classList.remove("right-panel-active");
});

document.querySelector('.sign-in-container form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = this.querySelector('input[type="email"]').value;
    const password = this.querySelector('input[type="password"]').value;
    
    // Retrieve user data from localStorage
    const storedUser = JSON.parse(localStorage.getItem('user'));
    
    if (storedUser && email === storedUser.email && password === storedUser.password) {
        alert('Login successful! Redirecting...');
        // Redirect to the next page (e.g., home.html)
        window.location.href = 'location_form.html'; // Change this to your desired page
    } else {
        alert('Invalid email or password!');
    }
});