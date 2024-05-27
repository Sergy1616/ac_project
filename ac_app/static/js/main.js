document.addEventListener('DOMContentLoaded', function () {
    // initializing the comment handler with data-page="comment-edit"
    if (document.body.getAttribute('data-page') === 'comment-edit') {
        window.commentsHandler = new CommentsHandler();
    }

    // news pagination
    if (window.location.pathname === '/space/news/') {
        initializeScrollNewsListener();
    }   

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

// 2. Modal account
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

// COMMENTS:
class CommentsHandler {
    constructor() {
        this.initCancelCommentDeletion();
    }
    // 1. Cancel Delete Button
    initCancelCommentDeletion() {
        document.getElementById('cancelCommentDeletion').onclick = function() {
            document.getElementById('confirmModal').style.display = 'none';
        };
    }
    // 2. Form Text Edit
    loadEditForm(commentId, commentText) {
        document.querySelector('textarea[name="text"]').value = commentText;
        document.getElementById('commentId').value = commentId;
    }
    // 3. Modal
    showConfirmModal(commentId) {
        document.getElementById('modalCommentId').value = commentId;
        document.getElementById('confirmModal').style.display = 'block';
    }
};

// PAGINATION:
function initializeScrollNewsListener() {
    var page = 1;
    var emptyPage = false;
    var blockRequest = false;

    window.addEventListener('scroll', function(e) {
        var margin = document.documentElement.scrollHeight - window.innerHeight - 200;
        if(window.pageYOffset > margin && !emptyPage && !blockRequest) {
            blockRequest = true;
            page += 1;
            fetch('?news_object_list=1&page=' + page)
            .then(response => response.text())
            .then(html => {
                if (html === '') {
                    emptyPage = true;
                }
                else {
                    var newsList = document.getElementById('space_news');
                    if (newsList) {
                        newsList.insertAdjacentHTML('beforeEnd', html);
                        blockRequest = false;
                    }
                }
            });
        }
    });
    const scrollEvent = new Event('scroll');
    window.dispatchEvent(scrollEvent);
}