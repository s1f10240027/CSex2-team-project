document.addEventListener('DOMContentLoaded', () => {
    const AnswerButton = document.querySelectorAll('.option');
    AnswerButton.forEach(button => {
        button.disabled = true;
        button.style.cursor = 'not-allowed'; 
        button.style.opacity = '0.5'; 
    });

    let musicVolumeDown;
    const mainImage = document.getElementById('jacket');
    document.addEventListener('click', (event) => {
        if (event.target.classList.contains('option')) {

            const newImageUrl = event.target.getAttribute('data-image');
            mainImage.src = newImageUrl;
            
            AnswerButton.forEach(button => {
                button.style.cursor = 'default'; 
                button.disabled = true;
                if (button.textContent == event.target.getAttribute('data-correct')){
                    button.classList.add('correct');  
                } else {
                    button.classList.add('incorrect');  
                }
            });

            const CorrectAudio = new Audio('static/media/correct.mp3');
            const IncorrectAudio = new Audio('static/media/incorrect.mp3');
            musicVolumeDown = true;
            if (event.target.textContent == event.target.getAttribute('data-correct')){
                CorrectAudio.play();
            } else {
                IncorrectAudio.play();
            }
        }
    });

    const audio = document.getElementById("audio");
    const playButton = document.getElementById("playmusic");
    const currentTimeDisplay = document.getElementById("current-time");
    const progressBar = document.getElementById("progress-bar");
    const message = document.getElementById("playmessage");


    let saveTime = 0; 
    let fadein, fadeout;
    let firstclick = true;
    let fadeoutState = false;
    
    audio.addEventListener('loadedmetadata', () => {
        audio.currentTime = saveTime;
    });

    playButton.addEventListener('click', () => {
        if (audio.paused) {
            audio.play().then(() => {
                if (firstclick == true) {
                    AnswerButton.forEach(button => {
                        button.disabled = false;
                        button.style.cursor = 'pointer'; 
                        button.style.opacity = '1'; 
                        button.style.color = 'black';
                    });
                };
                firstclick = false;
                let fadeinNow; 
                message.textContent = "再生中";
                playButton.classList.add('playing');
                playButton.classList.remove('paused');
                console.log(audio.currentTime, audio.volume)
                if (audio.currentTime == 0){ 
                    audio.volume = 0;
                };
                if (audio.volume != 1) { 
                    if (fadeoutState == false) {
                        fadein = setInterval(() => {
                            if (audio.volume < 1) {
                                audio.volume = parseFloat((audio.volume + 0.01).toFixed(2));
                            } else {
                                audio.volume = 1;
                                clearInterval(fadein);
                                fadeinNow = false;
                            }
                        }, 15);
                    };
                };

                let fadeOutStart = audio.duration - 1.5;
                fadeout = setInterval(() => {
                    if (audio.currentTime >= fadeOutStart) {
                        if (fadeoutState == false){
                            fadeoutState = true;
                        };
                        if (audio.volume > 0) {
                            audio.volume = parseFloat((audio.volume - 0.01).toFixed(2));
                        } else {
                            audio.pause();
                            clearInterval(fadein);
                            clearInterval(fadeout);
                            fadeoutState = false;
                            saveTime = 0;
                            currentTimeDisplay.textContent = "0:10 / 0:10";
                            message.textContent = "クリックで再生";
                            playButton.classList.add('paused');
                            playButton.classList.remove('playing');
                        }
                    }
                }, 15);
            }).catch(error => {
                console.error("再生エラー: ", error);
            });

            audio.addEventListener('timeupdate', () => {
                let minutes = Math.floor(audio.currentTime / 60);
                let seconds = Math.floor(audio.currentTime % 60);
                currentTimeDisplay.textContent = `${minutes}:${seconds < 10 ? '0' + seconds : seconds} / 0:10`;
                progressBar.value = (audio.currentTime / audio.duration) * 100;
            });

        } else {
            saveTime = audio.currentTime;
            audio.pause();
            message.textContent = "クリックで再生";
            playButton.classList.add('paused');
            playButton.classList.remove('playing');
            clearInterval(fadein);
            clearInterval(fadeout);
        }
    });
});

