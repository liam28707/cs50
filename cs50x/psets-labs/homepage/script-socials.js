document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.button-box a');

    buttons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const url = this.getAttribute('href');
            window.open(url, '_blank');
        })
    })
})