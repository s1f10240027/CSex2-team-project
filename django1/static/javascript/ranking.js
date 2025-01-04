// 音楽再生処理
const audio = new Audio("/static/media/ranking.mp3");
window.addEventListener('beforeunload', () => {
    localStorage.setItem('last_page', window.location.pathname);
    if (!(audio.paused)) {
        localStorage.setItem('ranking_currentTime', audio.currentTime);
    };
})

document.addEventListener('DOMContentLoaded', () => {
    const isOnRanking = `${localStorage.getItem('last_page')}`.includes("Ranking");
    const savedTime = parseFloat(localStorage.getItem('ranking_currentTime'));

    audio.addEventListener('loadedmetadata', () => {
        audio.currentTime = 0;
        if (isOnRanking && !isNaN(savedTime)) {
            audio.currentTime = savedTime + 0.1;
        } else {
            localStorage.removeItem('ranking_currentTime');
        }
        const isPlaying = localStorage.getItem('musicPlaying');
        if (isPlaying === 'true') {
            console.log("audio started")
            audio.loop = true;
            audio.play();
        };
    })
})
