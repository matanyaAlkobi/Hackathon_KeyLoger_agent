function toggleForms() {
    document.getElementById('login-box').classList.toggle('hidden');
    document.getElementById('register-box').classList.toggle('hidden');
}

const form = document.querySelector('#register-box form');
const full_name = document.getElementById('full_name');
const email = document.getElementById('email');
const password = document.getElementById('password');

const errorElement = document.createElement('p');
errorElement.style.color = 'red';
document.querySelector('#register-box').appendChild(errorElement);

function isVaildEmail(email){
    const re =  /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email)
}




form.addEventListener('submit', (e) => {
    let messages = [];

    if (full_name.value.trim() === '') {
        messages.push('Name is required');
    }

    if(email.value.trim() === ''){
        messages.push('Email is required');
    }
    else if (!isVaildEmail (email.value)){
        messages.push('Invaild email format')
    }

    if (password.value.trim() === '') {
        messages.push('Password is required');
    }
    else if (password.value.length < 8) {
        messages.push('Password must be longer than 8 characters');
    }
    if (password.value.length > 30) {
        messages.push('Password must be less than 30 characters');
    }

    if (messages.length > 0) {
        e.preventDefault();
        errorElement.innerText = messages.join(', ');
    } else {
        e.preventDefault();
        setTimeout(() => {
            toggleForms();
        }, 500);
    }
});


