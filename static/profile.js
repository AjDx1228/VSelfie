(async () => {
    const userString = localStorage.getItem('user');
    const user = JSON.parse(userString);
    const vk_id = user['id'];
    const photos = await fetch(`/my_photos/${vk_id}`).then((resp) => resp.json());
    const parentNode = document.querySelector('.photos');
    for (photo of photos) {
        const el = document.createElement('img');
        el.src = photo;
        el.classList.add('photo');
        parentNode.append(el);
    }
})()