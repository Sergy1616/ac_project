document.addEventListener('DOMContentLoaded', function () {
    // star detail page
    if (document.body.getAttribute('data-page') === 'star_detail') {
        favoriteAndWishlist();
    }

    // product detail page
    if (document.body.getAttribute('data-page') === 'product_detail') {
        addProductCart();
        favoriteAndWishlist();
    }

    // user wishlist page
    if (window.location.pathname === '/account/wish_list/') {
        removeFromWishlist();
    }
});


async function handleFormSubmit(form, onSuccess) {
    const formData = new FormData(form);
    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

    try {
        const response = await fetch(form.action, {
            method: form.method,
            headers: {'X-CSRFToken': csrfToken},
            body: formData
        });

        if (response.status === 401) {
            window.location.replace(`/account/login/?next=${encodeURIComponent(window.location.href)}`);
            throw new Error('Unauthorized');
        }

        const data = await response.json();
        onSuccess(data);
    } catch (error) {
        console.error('Error:', error);
    }
};

// favorite/wishlist
function favoriteAndWishlist() {
    const form = document.getElementById('ajax-form-submit');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(form, (data) => {
                const button = form.querySelector('button');
                button.querySelector('span').innerText = data.action;
                button.querySelector('img').src = data.image_src;
            });
        });
    }
};

// remove product (user wishlist page)
function removeFromWishlist() {
    document.querySelectorAll('form[id^="ajax-form-submit"]').forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            handleFormSubmit(form, (data) => {
                if (data.result === 'removed') {
                    location.reload();
                }
            });
        });
    });
};

// product detail page
function addProductCart() {
    const form = document.getElementById('add-product-form');
    if (form) {
        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(form);
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

            try {
                const response = await fetch(form.action, {
                    method: form.method,
                    headers: {'X-CSRFToken': csrfToken},
                    body: formData
                });

                const data = await response.json();
                if (data.result === 'success') {
                    document.getElementById('total-unique-items').textContent = data.total_unique;
                    updateTotalUniqueItems(data.total_unique);
                    showModal(data.message);
                } else {
                    showModal('Failed to add the product to the cart. Please try again.');
                }
            } catch (error) {
                showModal('An error occurred. Please try again later.');
                console.error('Error:', error);
            }
        });
    }
};

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
};
