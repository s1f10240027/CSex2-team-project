//音楽再生stateの引継ぎ
window.addEventListener('beforeunload', () => {
    localStorage.setItem('last_page', window.location.pathname);    
});

//注意事項の表示、スペクトラムの呼び出し
document.addEventListener('DOMContentLoaded', () => {
    //if (window.location.pathname == localStorage.getItem('last_page')){
    //    localStorage.clear('musicPlaying'); 
    //}

    const isPlaying = localStorage.getItem('musicPlaying');
    if (isPlaying === 'true') {
        document.getElementById('overlay').style.display = 'none'; // 注意事項画面を非表示
        document.getElementById('main-content').style.display = 'block'; // メインコンテンツを表示
        StartSuomiSpectrum()
    }else {
        document.getElementById('overlay').style.display = 'block'; // 注意事項画面を表示
    }
    
    document.getElementById('touch-start').addEventListener('click', () => {
        document.getElementById('overlay').style.display = 'none'; // 注意事項画面を非表示
        document.getElementById('main-content').style.display = 'block'; // メインコンテンツを表示
        localStorage.setItem('musicPlaying', 'true');
        StartSuomiSpectrum()
    });
});

//スペクトラムの描画
function StartSuomiSpectrum() {
    const audio = new Audio("/static/media/bgm_top.mp3");
    console.log(audio)
    audio.loop = true;

    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const audioSource = audioContext.createMediaElementSource(audio);
    const analyser = audioContext.createAnalyser();

    const canvas = document.getElementById('audio-spectrum');
    const canvasContext = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = 200;

    analyser.fftSize = 256;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    audioSource.connect(analyser);
    analyser.connect(audioContext.destination);

    function drawSpectrum() {
        requestAnimationFrame(drawSpectrum);
        analyser.getByteFrequencyData(dataArray);

        canvasContext.fillStyle = '#fffacd';
        canvasContext.fillRect(0, 0, canvas.width, canvas.height);

        const barWidth = (canvas.width / bufferLength) * 1.5;
        const blockSize = 1;
        const blockGap = 1;
        const maxBlocks = 20;
        const centerY = canvas.height / 2;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            const barHeight = dataArray[i];
            const threshold = 20; 
            const blockCount = barHeight > threshold ? Math.floor((barHeight - threshold) / (255 - threshold) * maxBlocks) : 0;

            

            const gradient = canvasContext.createLinearGradient(0, 0, canvas.width, 0);
            gradient.addColorStop(0, 'rgba(0, 255, 255, 1)');
            gradient.addColorStop(1, 'rgba(255, 0, 255, 1)');

            canvasContext.fillStyle = gradient;

            for (let j = 0; j < blockCount; j++) {
                const y = centerY - (blockSize + blockGap) * (j + 1);
                canvasContext.fillRect(x, y, barWidth, blockSize);
            }

            for (let j = 0; j < blockCount; j++) {
                const y = centerY + (blockSize + blockGap) * j;
                canvasContext.fillRect(x, y, barWidth, blockSize);
            }

            x += barWidth + blockGap;
        }
    }

    audio.play().catch((error) => {
        document.getElementById('overlay').style.display = 'block';
        console.error('音楽の再生に失敗しました:', error);
    });
    drawSpectrum();

    // ミュートボタンの処理
   /* document.getElementById('mute-btn').addEventListener('click', function () {
        const button = this;
    
        if (audioContext.state === 'suspended') {
            audioContext.resume(); 
        }
    
        if (audio.paused) {
            button.textContent = '音楽をミュートする';
            audio.play();
            drawSpectrum();
        } else {
            button.textContent = '音楽を再生する';
            audio.pause();
        }
    });*/
}

//右上と左下のスライドショー
document.addEventListener('DOMContentLoaded', () => {
    function slideImages(containerSelector, imageSelector, rotateDeg) {
        const container = document.querySelector(containerSelector);
        const images = document.querySelectorAll(imageSelector);
        const slideWidth = images[0].offsetWidth;
        let currentPosition = 0; 
        
        function slide() {
            currentPosition -= 0.5;
            container.style.transform = `rotate(${rotateDeg}deg) translateX(${currentPosition}px)`;

            if (Math.abs(currentPosition) >= slideWidth) {
                const firstImage = container.firstElementChild;

                container.style.transition = "none"; 
                currentPosition += slideWidth; 
                container.style.transform = `rotate(${rotateDeg}deg) translateX(${currentPosition}px)`;

                container.appendChild(firstImage);
                requestAnimationFrame(() => {
                    container.style.transition = ""; 
                });
            }

            requestAnimationFrame(slide);
        }

        slide();
    }

    slideImages(".slide-container1", ".slide-image1",45);
    slideImages(".slide-container2", ".slide-image2",-135);
});
