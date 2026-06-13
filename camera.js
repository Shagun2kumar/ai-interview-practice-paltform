async function startCamera(){
    let video = document.getElementById("video");

    let stream = await navigator.mediaDevices.getUserMedia({
        video: true
    });

    video.srcObject = stream;
}









