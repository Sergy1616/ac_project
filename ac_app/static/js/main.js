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
    
    // sort products
    if (document.body.getAttribute('data-page') === 'products') {
        sortProducts();
    }

    // product detail slider
    if (document.body.getAttribute('data-page') === 'product_detail') {
        productDetailSlider();
    }

    // main slider
    if (window.location.pathname === '/' || document.body.getAttribute('data-page') === 'products') {
        mainSlider();
    }

    // home page content sliders
    if (window.location.pathname === '/') {
        homeContentSlider();
    }

    function initializeOnAllPages() {
        handleMenu();
        accountMenu();
        handleInput();
    }

    initializeOnAllPages();
});

// Browser
function handlePageShow(event) {
    if (event.persisted) {
        window.location.reload();
    }
}
window.addEventListener('pageshow', handlePageShow);


// HEADER:
// 1. Navbar (scrolling)
function handleMenu() {
    var prevPos = window.pageYOffset;
    var menu = document.getElementById("menu");
    var isUpdating = false;

    window.onscroll = function(event) {
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

    document.getElementById('open-account-menu').onclick = function(event) {
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
                var response = JSON.parse(event.detail.xhr.responseText);
                showModal(response.message, true);
            }
        });
    });
};

// 4. Modal message
function showModal(message, reload=false) {
    const modal = document.getElementById('notification-modal');
    const modalMessage = document.getElementById('modal-message');
    const modalBackground = document.getElementById('modal-background');

    modalMessage.textContent = message;
    modal.classList.add('modal-message-open');
    modalBackground.classList.add('modal-background-open')
    setTimeout(() => {
        modal.classList.remove('modal-message-open');
        modalBackground.classList.remove('modal-background-open');
        if (reload) {
            window.location.reload();
        }
    }, 1500);
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

// SHOP:
// 1. Slider Product Detail
function productDetailSlider() {
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.querySelector('.product-images img');

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', () => {
            mainImage.src = thumbnail.src;
        });
    });
};

// 2. Sort Products
function sortProducts() {
    var sortSelect = document.getElementById('id_sort');
        sortSelect.addEventListener('change', function() {
            document.getElementById('sortForm').submit();
        });
};

// SLIDER:
function mainSlider() {
    const slider = document.querySelector('.slider-wrapper');
    const ImageAndLink = slider.querySelectorAll('img, a');
    const cardBounding = slider.getBoundingClientRect();
    let clicked = false;
    let initialPos = 0;
    let currentScroll = 0;
    let autoscroll;
    let isDragging = false;

    function setGrabState(state) {
        if(state){
            slider.classList.add('grab');
        } else{
            slider.classList.remove('grab');
        }
        clicked = state;
    };

    slider.onmousedown = (event) => {
        initialPos = event.clientX - cardBounding.left;
        currentScroll = slider.scrollLeft;
        setGrabState(true);
    };

    slider.onmousemove = (event) => {
        if (clicked) {
            isDragging = true;
            const xPos = event.clientX - cardBounding.left;
            const scrollPos = currentScroll + -(xPos - initialPos);
            slider.scrollLeft = scrollPos;
        }
    };

    slider.onmouseup = slider.onmouseleave = () => {
        setGrabState(false);
        if (!isDragging) {
            isDragging = false;
        }
    };

    ImageAndLink.forEach(item=> {
        item.setAttribute('draggable', false);
        item.addEventListener('click', (e) => {
            if (isDragging) {
                e.preventDefault();
            }
            isDragging = false;
        });
    });

    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    let widthToScroll = slider.children[0].offsetWidth;

    window.onresize = function() {
        widthToScroll = slider.children[0].offsetWidth;
    };

    prevButton.onclick = function() { slider.scrollLeft -= widthToScroll; };
    nextButton.onclick = function() { slider.scrollLeft += widthToScroll; };

    const slides = Array.from(slider.children);
    slides.slice(-1).reverse().forEach(item=> {
        slider.insertAdjacentHTML('afterbegin', item.outerHTML);
    });
    slides.slice(0, 1).forEach(item=> {
        slider.insertAdjacentHTML('beforeend', item.outerHTML);
    });

    slider.onscroll = function() {
        if(slider.scrollLeft === 0) {
            slider.classList.add('no-smooth');
            slider.scrollLeft = slider.scrollWidth - (2 * slider.offsetWidth);
            slider.classList.remove('no-smooth');
        }
        else if(slider.scrollLeft === slider.scrollWidth - slider.offsetWidth) {
            slider.classList.add('no-smooth');
            slider.scrollLeft = slider.offsetWidth;
            slider.classList.remove('no-smooth');
        }
        if(autoscroll) {
            clearTimeout(autoscroll);
        }
        autoscroll = setTimeout(()=> {
            slider.scrollLeft += widthToScroll;
        }, 5000);
    };

    autoscroll = setTimeout(() => {
        slider.scrollLeft += slider.children[0].offsetWidth;
    }, 5000);
};

// Home page sliders
function homeContentSlider() {
    const sliders = document.querySelectorAll('.slider-container');

    sliders.forEach(slider => {
        const contentSlider = slider.querySelector('.content-slider');
        const linksAndImages = contentSlider.querySelectorAll('a, img');
        const cardBounding = contentSlider.getBoundingClientRect();
        let clicked = false, initialPos = 0, currentScroll = 0, isDragging = false;

        function setGrabState(state) {
            if (state) {
                contentSlider.classList.add('grab');
            } else {
                contentSlider.classList.remove('grab');
            }
            clicked = state;
        }

        const handleMouseDown = (event) => {
            initialPos = event.clientX - cardBounding.left;
            currentScroll = contentSlider.scrollLeft;
            setGrabState(true);
        };

        const handleMouseMove = (event) => {
            if (clicked) {
                isDragging = true;
                const xPos = event.clientX - cardBounding.left;
                const scrollPos = currentScroll + -(xPos - initialPos);
                contentSlider.scrollLeft = scrollPos;
            }
        };

        const handleMouseUp = () => {
            setGrabState(false);
            if (!isDragging) {
                isDragging = false;
            }
        };

        contentSlider.addEventListener('mousedown', handleMouseDown);
        contentSlider.addEventListener('mousemove', handleMouseMove);
        contentSlider.addEventListener('mouseup', handleMouseUp);
        contentSlider.addEventListener('mouseleave', handleMouseUp);

        linksAndImages.forEach(item => {
            item.setAttribute('draggable', false);
            item.addEventListener('click', (e) => {
                if (isDragging) {
                    e.preventDefault();
                }
                isDragging = false;
            });
        });

        const widthToScroll = contentSlider.children[0].offsetWidth;
        const prevButton = slider.querySelector('.left-arrow');
        const nextButton = slider.querySelector('.right-arrow');
        prevButton.addEventListener('click', () => { contentSlider.scrollLeft -= widthToScroll });
        nextButton.addEventListener('click', () => { contentSlider.scrollLeft += widthToScroll });
    });
};
