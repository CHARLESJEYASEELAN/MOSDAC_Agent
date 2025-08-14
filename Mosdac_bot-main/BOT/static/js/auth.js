// Authentication JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const alertMessage = document.getElementById('alertMessage');

    // Handle login form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        
        if (!username || !password) {
            showAlert('Please fill in all fields', 'error');
            return;
        }
        
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert(data.message, 'success');
                // Redirect to chatbot page after a short delay
                setTimeout(() => {
                    window.location.href = '/chatbot';
                }, 1000);
            } else {
                showAlert(data.message, 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            showAlert('An error occurred during login. Please try again.', 'error');
        }
    });

    // Handle register form submission
    registerForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        // Validation
        if (!username || !email || !password || !confirmPassword) {
            showAlert('Please fill in all fields', 'error');
            return;
        }
        
        if (username.length < 3) {
            showAlert('Username must be at least 3 characters long', 'error');
            return;
        }
        
        if (password.length < 6) {
            showAlert('Password must be at least 6 characters long', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            showAlert('Passwords do not match', 'error');
            return;
        }
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showAlert('Please enter a valid email address', 'error');
            return;
        }
        
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert(data.message, 'success');
                // Redirect to chatbot page after a short delay
                setTimeout(() => {
                    window.location.href = '/chatbot';
                }, 1000);
            } else {
                showAlert(data.message, 'error');
            }
        } catch (error) {
            console.error('Registration error:', error);
            showAlert('An error occurred during registration. Please try again.', 'error');
        }
    });
});

// Switch between login and register forms
function switchForm(formType) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const alertMessage = document.getElementById('alertMessage');
    
    // Hide alert message
    alertMessage.style.display = 'none';
    
    if (formType === 'register') {
        loginForm.classList.remove('active');
        registerForm.classList.add('active');
    } else {
        registerForm.classList.remove('active');
        loginForm.classList.add('active');
    }
    
    // Clear form fields
    clearFormFields();
}

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.nextElementSibling.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Show alert message
function showAlert(message, type) {
    const alertMessage = document.getElementById('alertMessage');
    alertMessage.textContent = message;
    alertMessage.className = `alert ${type}`;
    alertMessage.style.display = 'block';
    
    // Auto-hide success messages after 3 seconds
    if (type === 'success') {
        setTimeout(() => {
            alertMessage.style.display = 'none';
        }, 3000);
    }
}

// Clear form fields
function clearFormFields() {
    document.getElementById('loginUsername').value = '';
    document.getElementById('loginPassword').value = '';
    document.getElementById('registerUsername').value = '';
    document.getElementById('registerEmail').value = '';
    document.getElementById('registerPassword').value = '';
    document.getElementById('confirmPassword').value = '';
}

// Add input event listeners for real-time validation feedback
document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('input');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove error styling on input
            this.style.borderColor = '';
        });
        
        input.addEventListener('focus', function() {
            // Hide alert on focus
            const alertMessage = document.getElementById('alertMessage');
            if (alertMessage.classList.contains('error')) {
                alertMessage.style.display = 'none';
            }
        });
    });
    
    // Password strength indicator for register form
    const registerPassword = document.getElementById('registerPassword');
    if (registerPassword) {
        registerPassword.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            if (password.length >= 6) strength++;
            if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
            if (password.match(/\d/)) strength++;
            if (password.match(/[^a-zA-Z\d]/)) strength++;
            
            // Visual feedback could be added here
            if (strength < 2 && password.length > 0) {
                this.style.borderColor = '#e74c3c';
            } else if (strength >= 2) {
                this.style.borderColor = '#27ae60';
            }
        });
    }
    
    // Confirm password validation
    const confirmPassword = document.getElementById('confirmPassword');
    if (confirmPassword) {
        confirmPassword.addEventListener('input', function() {
            const password = document.getElementById('registerPassword').value;
            const confirm = this.value;
            
            if (confirm.length > 0) {
                if (password === confirm) {
                    this.style.borderColor = '#27ae60';
                } else {
                    this.style.borderColor = '#e74c3c';
                }
            }
        });
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Alt + R to switch to register
    if (e.altKey && e.key === 'r') {
        e.preventDefault();
        switchForm('register');
    }
    
    // Alt + L to switch to login
    if (e.altKey && e.key === 'l') {
        e.preventDefault();
        switchForm('login');
    }
});

// Form animation on load
window.addEventListener('load', function() {
    const loginCard = document.querySelector('.login-card');
    loginCard.style.opacity = '0';
    loginCard.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        loginCard.style.transition = 'all 0.6s ease';
        loginCard.style.opacity = '1';
        loginCard.style.transform = 'translateY(0)';
    }, 100);
});
