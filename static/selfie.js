var video = document.getElementById('video');
var videoContent = document.getElementById('video-content');
var errorContainer = document.getElementById('error-wrapper');
var pageContainer = document.getElementById('page');
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.srcObject = stream;
        video.play();


        var snapBtn = document.getElementById("snap");
        snapBtn.style.display = 'block';

        var result = document.getElementById('result');
        var canvas = document.getElementById('canvas');
        var context = canvas.getContext('2d');
        snapBtn.addEventListener("click", function() {
            context.save();
            context.scale(-1, 1);
            context.drawImage(video, 0, 0, -420, 320);
            context.restore();

            result.style.display = 'flex';
        });

        document.getElementById("publish").addEventListener("click", async function() {
            const data = {
                photo: canvas.toDataURL()
            }
            
            const userString = localStorage.getItem('user');
            const user = JSON.parse(userString);
            const vk_id = user['id'];

            await fetch(`/publish/${vk_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=utf-8'
                },
                body: JSON.stringify(data)
            });

            window.location.href = `http://${window.location.host}/`;
        });
    }).catch(() => {
        errorContainer.style.display = 'flex';
        pageContainer.style.display = 'none';
    });
} else {
    errorContainer.style.display = 'flex';
    pageContainer.style.display = 'none';
}
