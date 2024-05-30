// favorite/wishlist ajax
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