window.addEventListener('beforeunload', () => {
    localStorage.setItem('last_page', window.location.pathname);    
});

document.addEventListener('DOMContentLoaded', () => {
    const isPlaying = localStorage.getItem('musicPlaying');
    if (isPlaying === 'true') {
        const audio = new Audio("/static/media/bgm_genre.mp3");
        audio.loop = true;
        audio.play();
    };
})