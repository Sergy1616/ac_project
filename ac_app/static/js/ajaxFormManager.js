document.addEventListener('DOMContentLoaded', function () {
    // cart page
    if (window.location.pathname === '/cart/') {
        cartProductUpdate();
        cartProductRemove();
    }

    // product detail page
    if (document.body.getAttribute('data-page') === 'product_detail') {
        addProductCart();
        favoriteAndWishlist();
    }

    // star detail page
    if (document.body.getAttribute('data-page') === 'star_detail') {
        favoriteAndWishlist();
    }

});

// favorite/wishlist ajax
function favoriteAndWishlist() {
    document.getElementById('favourite-wishlist-form-ajax').addEventListener('submit', function (e) {
        e.preventDefault();
    
        const form = this;
        const xhr = new XMLHttpRequest();
        xhr.open(form.method, form.action);
    
        xhr.onload = function () {
            if (xhr.status >= 200 && xhr.status < 300) {
                const response = JSON.parse(xhr.responseText);
                form.querySelector('button span').innerText = response.action;
                form.querySelector('button img').src = response.image_src;
            } else {
                if (xhr.status === 401) {
                    window.location.replace(`/account/login/?next=${encodeURIComponent(window.location.href)}`);
                }
            }
        };
        xhr.send(new FormData(form));
    });
}

// Cart form (ajax cartProductUpdate, cartProductRemove)
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
}

function cartProductUpdate() {
    document.querySelectorAll('.cart-update').forEach(function (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            handleCartForm(form);
        });
    });
}

function cartProductRemove() {
    document.querySelectorAll('.cart-remove').forEach(function (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            handleCartForm(form);
        });
    });
}

// product detail page
function addProductCart() {
    var form = document.getElementById('add-product-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

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
                document.getElementById('total-unique-items').textContent = data.total_unique;
                updateTotalUniqueItems(data.total_unique);
                showModal(data.message);
            } else {
                showModal('Failed to add the product to the cart. Please try again.');
            }
        })
        .catch(error => {
            showModal('An error occurred. Please try again later.');
            console.error('Error:', error);
        });
    });
}

// display (total_unique) "addProductCart"
function updateTotalUniqueItems(total_unique) {
    var totalUniqueItemsElement = document.getElementById('total-unique-items');

    if (totalUniqueItemsElement) {
        if (total_unique > 0) {
            totalUniqueItemsElement.parentElement.style.display = 'flex';
            totalUniqueItemsElement.textContent = total_unique;
        } else {
            totalUniqueItemsElement.parentElement.style.display = 'none';
        }
    }
}

// modal "addProductCart"
function showModal(message) {
    const modal = document.getElementById('notification-modal');
    const modalMessage = document.getElementById('modal-message');
    modalMessage.textContent = message;
    modal.style.display = 'block';
    setTimeout(() => {
        modal.style.display = 'none';
    }, 2000);
}