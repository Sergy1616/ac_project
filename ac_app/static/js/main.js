document.addEventListener('DOMContentLoaded', function () {

    // Функция инициализации для всех страниц
    function initializeOnAllPages() {
        accountMenu();
    }

    initializeOnAllPages();
});


// HEADER:
// 1. Дополнительное меню аккаунта
function accountMenu() {
    document.getElementById('open-account-menu').onclick = function() {
        document.getElementById('account-menu').style.right = '0px';
    };

    document.getElementById('close-menu').onclick = function() {
        document.getElementById('account-menu').style.right = '-400px';
    };
};