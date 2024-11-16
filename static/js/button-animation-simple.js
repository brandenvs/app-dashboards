// The button element
const contactButton = document.getElementById('contactButton');

// Hover
contactButton.addEventListener('mouseenter', () => {
    contactButton.classList.add('pop-animation');
});

// remove pop
contactButton.addEventListener('mouseleave', () => {
    contactButton.classList.remove('pop-animation');
});

// add pop, short delay added
contactButton.addEventListener('click', () => {
    contactButton.classList.add('pop-animation');
    setTimeout(() => {
        contactButton.classList.remove('pop-animation');
    }, 150); // Delay to remove class
});
