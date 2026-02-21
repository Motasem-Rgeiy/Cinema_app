// Main JavaScript for Cinema Booking System

document.addEventListener('DOMContentLoaded', function() {
    console.log('Cinema Booking System Loaded');
    
    // Add any global interactivity here
    
    // Example: Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
