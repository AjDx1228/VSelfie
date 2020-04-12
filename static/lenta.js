function parseQuery(queryString) {
    var query = {};
    var pairs = (queryString[0] === '?' ? queryString.substr(1) : queryString).split('&');
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i].split('=');
        query[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1] || '');
    }
    return query;
}

const OFFSET_STEP = 5;

const query = parseQuery(window.location.search);
let offset = Number(query.offset) || 0;

document.getElementById("prev_photos").addEventListener("click", async function() {
    offset += OFFSET_STEP;

    const prevPhotos = await fetch(`/photos?offset=${offset}`).then((resp) => resp.json());
    const parentNode = document.querySelector('.photos');
    for (photo of prevPhotos) {
        const el = document.createElement('img');
        el.src = photo;
        el.classList.add('photo');
        parentNode.append(el);
    }
})