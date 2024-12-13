window.addEventListener('load', () => {
    // スペクトラム用
    const audio = new Audio("/static/media/top.mp3");
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
            const blockCount = Math.floor(barHeight / 255 * maxBlocks);

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

    document.getElementById('mute-btn').addEventListener('click', function () {
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
    });
    

    // 初期はミュート状態
    audio.pause();
    document.getElementById('mute-btn').textContent = '音楽を再生する';
});
