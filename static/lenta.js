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

if (query.scrollToEnd) {
    window.scrollTo(0, document.body.clientHeight);
}

document.getElementById("prev_photos").addEventListener("click", async function() {
    offset += OFFSET_STEP;
    window.location.href = `http://${window.location.host}/?offset=${offset}&scrollToEnd=true`;
})