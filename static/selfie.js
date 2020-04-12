var video = document.getElementById('video');
var videoContent = document.getElementById('video-content');
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.srcObject = stream;
        video.play();
    }).catch(() => {
        console.log('Camera is not found')
        videoContent.style.display = 'none';
    });

    var result = document.getElementById('result');
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    document.getElementById("snap").addEventListener("click", function() {
        context.drawImage(video, 0, 0, 480, 320);
        result.style.display = 'flex';
    });

    document.getElementById("publish").addEventListener("click", async function() {
        const data = {
            photo: canvas.toDataURL()
        }

        await fetch('/publish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(data)
        });

        window.location.href = `http://${window.location.host}/`;
    });
} else {
    console.log('Browser does not support getUserMedia');
}
