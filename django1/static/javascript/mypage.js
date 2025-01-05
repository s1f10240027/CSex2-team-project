// 音楽再生処理
const audio = new Audio("/static/media/bgm_mypage.mp3");
window.addEventListener('beforeunload', () => {
    localStorage.setItem('last_page', window.location.pathname);
    if (!(audio.paused)) {
        localStorage.setItem('mypage_currentTime', audio.currentTime);
    };
})

document.addEventListener('DOMContentLoaded', () => {
    const isOnMypage = `${localStorage.getItem('last_page')}`.includes("Mypage");
    const savedTime = parseFloat(localStorage.getItem('mypage_currentTime'));

    audio.addEventListener('loadedmetadata', () => {
        audio.currentTime = 0;
        if (isOnMypage && !isNaN(savedTime)) {
            audio.currentTime = savedTime + 0.1;
        } else {
            localStorage.removeItem('mypage_currentTime');
        }
        const isPlaying = localStorage.getItem('musicPlaying');
        if (isPlaying === 'true') {
            console.log("audio started")
            audio.loop = true;
            audio.play();
        };
    })
})


// アイコン変更処理
function ClickFileInput() {
    document.querySelector(".imageInput").click();
}

function changeIcon(event) {
    const file = event.target.files[0];
    if (file) {
        const form = event.target.closest('form');
        form.submit();
    }
}

// renameの制限処理
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname != '/Mypage/rename') {
        return;
    };
    const usernameInput = document.querySelector("input[name='name']");
    const usernameError = document.getElementById('name_error');
    const button = document.querySelector(".change");
    button.disabled = true;
    
    usernameInput.addEventListener('input', function() {
        const value = usernameInput.value;
        if (value.includes('@') || value.includes('＠')) {
            usernameError.style.display = 'block';
            usernameError.textContent = '@は使用できません';
            usernameInput.value = value.replace(/[＠@]/g, '');
        }
        if (value.length > 10) {
            usernameInput.value = value.slice(0, 10);
            usernameError.style.display = 'block';
            usernameError.textContent = '設定可能な文字数は最大10文字です';
        }
        
        if (value == ""){
            button.disabled = true;
        } else {
            button.disabled = false;
        }
    });

    usernameInput.addEventListener('blur', function() {
        usernameError.style.display = 'none';
        usernameError.textContent = '';
    });

})