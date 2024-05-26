document.addEventListener('DOMContentLoaded', function () {

    // Функция инициализации для всех страниц
    function initializeOnAllPages() {
        handleMenu();
        accountMenu();
        handleInput();
    }

    initializeOnAllPages();
});


// HEADER:
// 1. Navbar (scrolling)
function handleMenu() {
    var prevPos = window.pageYOffset;
    var menu = document.getElementById("menu");
    var isUpdating = false;

    window.onscroll = function() {
        var currentScrollPos = window.pageYOffset;

        if (!isUpdating && Math.abs(prevPos - currentScrollPos) > 200) {
            isUpdating = true;
            event.stopPropagation();

            requestAnimationFrame(function updateMenuPosition() {
                if (prevPos > currentScrollPos) {
                    menu.style.top = "0";
                } else {
                    menu.style.top = "-200px";
                }
                prevPos = currentScrollPos;
                isUpdating = false;
            });
        }
    }
};

// 2. Модальное окно аккаунта
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

// 3. htmx login 
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
