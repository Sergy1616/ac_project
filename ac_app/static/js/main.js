document.addEventListener('DOMContentLoaded', function () {
    // initializing the comment handler with data-page="comment-edit"
    if (document.body.getAttribute('data-page') === 'comment-edit') {
        window.commentsHandler = new CommentsHandler();
    }

    // news pagination
    if (window.location.pathname === '/space/news/') {
        new Pagination('space_news', 'space_news');
    }
    // stars pagination
    if (window.location.pathname === '/space/stars/') {
        new Pagination('stars', 'stars');
    }
    //  constellations pagination
    if (window.location.pathname === '/space/constellations/') {
        new Pagination('constellation', 'constellation');
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
        const cancelButton = document.getElementById('cancelCommentDeletion');
        if (cancelButton) {
            cancelButton.onclick = function() {
                document.getElementById('confirmModal').style.display = 'none';
            };
        }
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
class Pagination {
    constructor(modelType, containerId) {
        this.modelType = modelType;
        this.containerId = containerId;
        this.page = 1;
        this.emptyPage = false;
        this.blockRequest = false;
        this.spectralFilter = this.modelType === 'stars' ? new URLSearchParams(window.location.search).get('spectral') : null;
        this.init();
    }

    init() {
        window.addEventListener('scroll', this.handleScroll.bind(this));
        window.dispatchEvent(new Event('scroll'));
    }

    handleScroll() {
        let margin = document.documentElement.scrollHeight - window.innerHeight - 200;
        if(window.pageYOffset > margin && !this.emptyPage && !this.blockRequest) {
            this.loadMore();
        }
    }

    loadMore() {
        this.blockRequest = true;
        this.page += 1;
        let fetchUrl = `?ajax=true&page=${this.page}`;
        if (this.modelType === 'stars') {
            fetchUrl += this.spectralFilter ? '&spectral=' + this.spectralFilter : '';
        }
        fetch(fetchUrl)
            .then(response => response.text())
            .then(html => this.processResponse(html));
    }

    processResponse(html) {
        if(html === '') {
            this.emptyPage = true;
        } else {
            let containerList = document.getElementById(this.containerId);
            if (containerList) {
                containerList.insertAdjacentHTML('beforeEnd', html);
                this.blockRequest = false;
            }
        }
    }
}