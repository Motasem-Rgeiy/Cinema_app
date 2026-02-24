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


function cartRemove(button) {
    const url = button.getAttribute('data-url');

    fetch(url)
    .then(response => response.json())
    .then(data => {
        // 1. Create and show the message
        const msg = document.createElement('div');
        msg.innerText = data.message;
        msg.style.cssText = "position:fixed; top:20px; right:20px; background:#ff4b2b; color:white; padding:15px; border-radius:5px; z-index:10000;";
        document.body.appendChild(msg);

        // 2. Wait 1 second so the user can see the message, then reload
        setTimeout(() => {
            window.location.reload();
        }, 1); 
    })
    .catch(err => {
        console.log("Error:", err);
        // If there is an error, you might still want to reload to be safe
        // window.location.reload();
    });
}

