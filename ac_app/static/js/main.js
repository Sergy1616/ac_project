document.addEventListener('DOMContentLoaded', function () {

    // Функция инициализации для всех страниц
    function initializeOnAllPages() {
        accountMenu();
        handleInput();
    }

    initializeOnAllPages();
});


// HEADER:
// 1. Дополнительное меню аккаунта
function accountMenu() {
    const accountMenu = document.getElementById('account-menu');

    document.getElementById('open-account-menu').onclick = function() {
        accountMenu.classList.add('account-menu-open');
        localStorage.setItem('accountMenuState', 'open');
        event.stopPropagation();
    };

    document.addEventListener('click', function(event) {
        if (!accountMenu.contains(event.target) || event.target.id === 'close-menu') {
            accountMenu.classList.remove('account-menu-open');
            localStorage.setItem('accountMenuState', 'closed');
            event.stopPropagation();
        }
    });

    if (localStorage.getItem('accountMenuState') === 'open') {
        accountMenu.classList.add('account-menu-open');
    }
};

// 2. Обработка поля ввода htmx "Username or Email")
function handleInput() {
    var userOrEmailInput = document.getElementById('id_username_or_email');
    var usernameInput = document.getElementById('id_username');

    if (userOrEmailInput) {
        userOrEmailInput.addEventListener('input', function (event) {
            usernameInput.value = event.target.value;
        });
    }

    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('htmx:afterSwap', function(event) {

            if (event.detail.xhr.getResponseHeader('HX-Trigger') === 'loginSuccess') {
                document.getElementById('account-menu').classList.remove('account-menu-open');
                location.reload();
            }
        });
    });
};
