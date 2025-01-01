
function changeIcon() {
    // アイコン変更処理も今後追加予定
    alert("アイコン変更機能が未実装です。");
}


document.addEventListener('DOMContentLoaded', () => {
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