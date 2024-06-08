document.addEventListener('DOMContentLoaded', function () {
    if (window.location.pathname === '/cart/') {
        cartProductUpdate();
        cartProductRemove();
    }
});


function handleCartForm(form) {
    var formData = new FormData(form);
    var csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

    fetch(form.action, {
        method: form.method,
        headers: {'X-CSRFToken': csrfToken},
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'success') {
            window.location.reload();
        } else {
            alert('An error occurred. Please try again.');
            window.location.reload();
        }
    })
    .catch(error => {
        alert('An error occurred. Please try again.');
        window.location.reload();
        console.error('Error:', error);
    });
};

function cartProductUpdate() {
    document.querySelectorAll('.cart-update').forEach(function (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            handleCartForm(form);
        });
    });
};

function cartProductRemove() {
    document.querySelectorAll('.cart-remove').forEach(function (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            handleCartForm(form);
        });
    });
};
