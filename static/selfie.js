var video = document.getElementById('video');
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.srcObject = stream;
        video.play();
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
    });
} else {
    video.style.display = 'none';
}
