document.addEventListener( 'DOMContentLoaded', _ => {
        loadBookmarks();
        loadToggleBookmarkButton();
        document.querySelector('#filter-title').addEventListener('click', toggleFilter);
        document.querySelector('#filter-bookmark-icon').addEventListener('click', toggleFilterByBookmarks);
        var bookmarks = document.querySelectorAll('.bookmark-icon');
        bookmarks.forEach(function(bookmark) {
            bookmark.addEventListener('click', bookmarkItem);
        });
    }
);

function loadBookmarks() {
    items = window.localStorage.getItem('bookmarks');

    if (items == null) {
        window.localStorage.setItem("bookmarks", "");
        return;
    }

    items = items.split(',');
    items.forEach(function(item) {
        m_item = document.getElementById(item)
        if (m_item === null) {
            return;
        }
        img = document.getElementById(item).firstElementChild.getElementsByTagName('img')[1];
        img.src = '../static/icons/heartfull.png';
    });
}

function loadToggleBookmarkButton() {
    if (window.localStorage.getItem('toggleBookmarks') === null) {
        window.localStorage.setItem('toggleBookmarks', JSON.stringify(false));
    }

    else if (JSON.parse(window.localStorage.getItem('toggleBookmarks'))) {
        console.log('Set Bookmark button active on load')
        document.getElementById('filter-bookmark-icon').src = "../static/icons/heartfull.png";
        document.getElementById('filter-bookmark-input').setAttribute('value', window.localStorage.getItem('bookmarks'));
    }
}

function toggleFilter() {
    style = getStyle('filter-form', 'display');

    if (style === 'none') {
        document.querySelector('#filter-form').style.display = 'block';
        document.querySelector('#filter-title').innerHTML = 'Hide Filter'
    }

    else if (style === 'block') {
        document.querySelector('#filter-form').style.display = 'none';
        document.querySelector('#filter-title').innerHTML = 'Show Filter'
    }
}

function getStyle(id, name) {
    var element = document.getElementById(id);
    return element.currentStyle ? element.currentStyle[name] : window.getComputedStyle ? window.getComputedStyle(element, null).getPropertyValue(name) : null;
}

function bookmarkItem() {
    storage = window.localStorage;

    if (storage.getItem('bookmarks') === null) {
        this.src = "../static/icons/heartfull.png"
        window.localStorage.setItem("bookmarks", this.parentElement.parentElement.id.toString());
        return;
    }

    else {
        bookmarks = storage.getItem('bookmarks');
        items = bookmarks.split(',');
        id = this.parentElement.parentElement.id.toString()

        if (!arrayContains(id, items)) {
            this.src = "../static/icons/heartfull.png";
            items.push(id);
            storage.setItem('bookmarks', items.join(','));
        }

        else {
            this.src = "../static/icons/heartempty.png";
            items.splice(items.indexOf(id), 1);
            storage.setItem('bookmarks', items.join(','));
        }
    }
}

function arrayContains(needle, haystack) {
    return (haystack.indexOf(needle) > -1);
}

function toggleFilterByBookmarks() {
    
    bookmarks = window.localStorage.getItem('bookmarks');
    
    if (bookmarks === null) {
        return;
    }

    input = document.getElementById('filter-bookmark-input');
    icon = document.getElementById('filter-bookmark-icon');

    if (!JSON.parse(window.localStorage.getItem('toggleBookmarks'))) {
        window.localStorage.setItem('toggleBookmarks', JSON.stringify(true));
        icon.src = "../static/icons/heartfull.png";
        input.setAttribute('value', bookmarks);
    }

    else {
        window.localStorage.setItem('toggleBookmarks', JSON.stringify(false));
        icon.src = "../static/icons/heartempty.png";
        input.setAttribute('value', '');
    }
}