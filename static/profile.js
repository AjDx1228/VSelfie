(async () => {
    const userString = localStorage.getItem('user');
    const user = JSON.parse(userString);
    if (!user) {
        return;
    }

    const photos = await fetch(`/my_photos`).then((resp) => resp.json());
    const parentNode = document.querySelector('.photos');
    for (photo of photos) {
        const el = document.createElement('img');
        el.src = photo;
        el.classList.add('photo');
        parentNode.append(el);
    }
})()