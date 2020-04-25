const btnAuthorize = document.getElementById("authorize");
const btnUnauthorize = document.getElementById("unauthorize");
const userString = localStorage.getItem('user');
if (userString) {
    btnAuthorize.style.display = 'none';
    btnUnauthorize.style.display = 'block';

    const user = JSON.parse(userString);

    renderUser(user);
}

btnAuthorize.addEventListener("click", async function() {
    if (!localStorage.getItem('user')) {
        window.open(
            `https://oauth.vk.com/authorize?client_id=7413978&display=popup&redirect_uri=${window.location.origin}/callback/vk/code&scope=photos`,
            "JSSite",
            "width=800,height=800,resizable=yes,scrollbars=yes,status=yes"
        );
        const code = localStorage.getItem('code');
        const user = await fetch(`/authorize/vk?code=${code}`).then((resp) => resp.json());

        if (user.error) {
            return;
        }

        localStorage.setItem('user', JSON.stringify(user));

        btnAuthorize.style.display = 'none';
        btnUnauthorize.style.display = 'block';

        renderUser(user);
    }
})

btnUnauthorize.addEventListener("click", async function() {
    localStorage.removeItem('user');
    btnAuthorize.style.display = 'block';
    btnUnauthorize.style.display = 'none';
    document.querySelector('.user-info').style.display = 'none';

    await fetch(`/logout`);
})

function renderUser(user) {
    document.querySelector('.user-info').style.display = 'flex';
    const userName = document.getElementById('user-name');
    userName.innerHTML = '';
    userName.append(user['first_name'])
}