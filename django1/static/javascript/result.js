// ログイン状態を切り替える変数
const isLoggedIn = true; // ログイン状態（true/falseで管理）

document.addEventListener('DOMContentLoaded', () => {
    const UserScore = document.querySelector('.score-value');
    let score = parseFloat(UserScore.textContent);
    console.log(score)
    if (score >= 100){
        UserScore.classList.add('score-100');
    } else if (score >= 90) { 
        UserScore.classList.add('score-90');
    } else if (score >= 60) {
        UserScore.classList.add('score-60');
    } else if (score >= 30) {
        UserScore.classList.add('score-30');
    } else if (score > 0) {
        UserScore.classList.add('score-1');
    } else {
        UserScore.classList.add('score-0');
    }

    const loggedInContent = document.querySelector('.ranking-content.logged-in');
    const loggedOutContent = document.querySelector('.ranking-content.logged-out');

    // ログイン状態に応じて表示を切り替える
    if (isLoggedIn) {
        loggedInContent.style.display = 'block';
        loggedOutContent.style.display = 'none';
    } else {
        loggedInContent.style.display = 'none';
        loggedOutContent.style.display = 'block';
    }
});