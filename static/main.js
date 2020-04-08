var video = document.getElementById('video');
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
    });

    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var video = document.getElementById('video');
    document.getElementById("snap").addEventListener("click", function() {
            context.drawImage(video, 0, 0, 640, 480);
    });
}