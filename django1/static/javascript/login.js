window.addEventListener('beforeunload', () => {
    localStorage.setItem('last_page', window.location.pathname);    
});

let TabCoolDown = false;
let CurrentTab = 'sign_in';

document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.submit_button');
    const isPlaying = localStorage.getItem('musicPlaying');
    if (isPlaying === 'true') {
        const audio = new Audio("/static/media/login.mp3");
        audio.loop = true;
        audio.play();
    }
    document.querySelector('.main_box').className = "main_box main_active";

    const toggleElement = document.getElementById('form');
    if (toggleElement.getAttribute('data-signup') === 'True'){
        sign_up()
        button.disabled = false;
    } else {
        button.disabled = true;
    }

    
    const usernameInput = document.querySelector("input[name='name']");
    const emailInput = document.querySelector("input[name='email']");
    const passwordInput = document.querySelector("input[name='password']");
    const confirmInput = document.querySelector("input[name='confirm']");

    const usernameError = document.getElementById('name_error');
    const emailError = document.getElementById('email_error');
    const passwordError = document.getElementById('password_error');
    
    const emailRegex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;

    usernameInput.addEventListener('input', function() {
        const value = usernameInput.value;
        if (value.includes('@') || value.includes('＠')) {
            usernameError.style.display = 'block';
            usernameError.textContent = '@は使用できません';
            usernameInput.value = value.replace(/[＠@]/g, '');
        }
    });
    usernameInput.addEventListener('blur', function() {
        usernameError.style.display = 'none';
        usernameError.textContent = '';
    });

    emailInput.addEventListener('input', function() {
        if (CurrentTab == 'sign_up') {
            if (!(emailRegex.test(emailInput.value))) {
                emailError.style.display = 'block';
                emailError.textContent = '適切なメールアドレスを入力してください';
                button.disabled = true;
            } else {
                emailError.style.display = 'none';
                emailError.textContent = '';
                button.disabled = false;
            }
        }
    })
    usernameInput.addEventListener('blur', function() {
        emailError.style.display = 'none';
        emailError.textContent = '';
    });


    confirmInput.addEventListener('input', function() {
        if (confirmInput.value != document.querySelector("input[name='password']").value){
            passwordError.style.display = 'block';
            passwordError.textContent = 'パスワードが一致しません';
        } else {
            passwordError.style.display = 'none';
            passwordError.textContent = '';
        }
    });
    passwordInput.addEventListener('input', function() {
        if (confirmInput.value != '') {
            if (confirmInput.value != document.querySelector("input[name='password']").value){
                passwordError.style.display = 'block';
                passwordError.textContent = 'パスワードが一致しません';
            } else {
                passwordError.style.display = 'none';
                passwordError.textContent = '';
            }
        }

    });

    function validateForm() {
        const isUsernameValid = ((usernameInput.value !== "") && !(/[＠@]/.test(usernameInput.value)));
        const isEmailValid = (emailInput.value !== "");
        const isPasswordValid = (passwordInput.value !== "");
        const isPasswordMatch = (passwordInput.value === confirmInput.value);
        let state = null;
        if (CurrentTab == 'sign_in') {
            state = !(isEmailValid && isPasswordValid);
        } else {
            state = !(isUsernameValid && isEmailValid && isPasswordValid && isPasswordMatch && (emailRegex.test(emailInput.value)));
        };
        button.disabled = state;
    }

    usernameInput.addEventListener('input', validateForm);
    emailInput.addEventListener('input', validateForm);
    passwordInput.addEventListener('input', validateForm);
    confirmInput.addEventListener('input', validateForm);

    /* 保留
    // パスワードの表示/非表示切り替え
    const passwordInput = document.querySelector('.password_input');
    const passwordIcon = document.querySelector('.password-icon');

    passwordIcon.addEventListener('click', () => {
        if (passwordInput.type == 'password') {
            passwordInput.type = 'text';
            passwordIcon.src = 'static/media/password_on.png';
        } else {
            passwordInput.type = 'password';
            passwordIcon.src = 'static/media/password_off.png';
        };
    });
    */
})

function sign_up(){
    if (TabCoolDown == false && CurrentTab == 'sign_in'){
        const button = document.querySelector('.submit_button');
        button.disabled = true;
        CurrentTab = 'sign_up';
        TabCoolDown = true;
        let Completion = 0;
        let inputs = document.querySelectorAll('.form_input');
        document.querySelectorAll('.ul_tabs > li')[0].className=""; 
        document.querySelectorAll('.ul_tabs > li')[1].className="active"; 
    
        for(let i = 0; i < inputs.length ; i++) {
            if (i != 2 ){
                document.querySelectorAll('.form_input')[i].className = "form_input visible";
            }
            if (inputs[i].placeholder == 'メールアドレス または ユーザー名'){
                inputs[i].placeholder = 'メールアドレス';
            }
        } 

        setTimeout( function(){
            for(let d = 0; d < inputs.length ; d++) {
                document.querySelectorAll('.form_input')[d].className = "form_input visible active_input";  
            }
            Completion += 1;
            if (Completion >= 2){
                TabCoolDown = false;
            }
        },60 );
        
        document.querySelector('.submit_button').textContent = "アカウント作成";

        setTimeout(function(){
            const emailInput = document.querySelector("input[name='email']");
            const emailError = document.getElementById('email_error');
            if (emailInput.value != '') {
                if (!(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(emailInput.value))) {
                    emailError.style.display = 'block';
                    emailError.textContent = '適切なメールアドレスを入力してください';
                };
            };
        },1000);

        setTimeout(function(){
            Completion += 1;
            if (Completion >= 2){
                TabCoolDown = false;
            }
        },1400);
    }
}

function sign_in(){
    if (TabCoolDown == false && CurrentTab == 'sign_up'){
        CurrentTab = 'sign_in';
        TabCoolDown = true;

        const button = document.querySelector('.submit_button')
        button.textContent = "ログイン"; 
        
        const emailInput = document.querySelector("input[name='email']");
        const passwordInput = document.querySelector("input[name='password']");
        button.disabled = !(emailInput.value !== '' && passwordInput.value !== '');

        let errors = [
            document.getElementById('name_error'),
            document.getElementById('email_error'),
            document.getElementById('password_error')
        ]
        for (let i = 0; i < errors.length; i++) {
            errors[i].style.display = 'none';
            errors[i].textContent = '';
        }

        let Completion = 0;
        let inputs = document.querySelectorAll('.form_input');
        document.querySelectorAll('.ul_tabs > li')[0].className = "active"; 
        document.querySelectorAll('.ul_tabs > li')[1].className = "";    
        for(let i = 0; i < inputs.length ; i++) {
            switch(i) {
                case 1:
                    break;
                case 2:
                    break;
                default: 
                    document.querySelectorAll('.form_input')[i].className = "form_input visible";
            }
            if (inputs[i].placeholder == 'メールアドレス'){
                inputs[i].placeholder = 'メールアドレス または ユーザー名';
            }
        }

        setTimeout( function(){
            for(let d = 0; d < inputs.length ; d++) {
                switch(d) {
                    case 1:
                        console.log(d, inputs[d].name);
                        break;
                    case 2:
                        console.log(d, inputs[d].name);
                    default:
                        console.log(d, inputs[d].name);
                        document.querySelectorAll('.form_input')[d].className = "form_input visible";  
                        document.querySelectorAll('.form_input')[2].className = "form_input visible active_input";  
                }
            }
            Completion += 1;
            if (Completion >= 2){
                TabCoolDown = false;
            }
        },60 );

        setTimeout(function(){
            //document.querySelector('.forgot_password').style.opacity = "1";
            //document.querySelector('.forgot_password').style.top = "5px";
        
            for(var d = 0; d < inputs.length ; d++  ) {
                switch(d) {
                    case 1:
                        console.log(inputs[d].name);
                        break;
                    case 2:
                        console.log(inputs[d].name);
                        break;
                    default:
                        document.querySelectorAll('.form_input')[d].className = "form_input";
                        document.querySelectorAll('.form_input')[d].value = "";
                }
            }
            Completion += 1;
            if (Completion >= 2){
                TabCoolDown = false;
            }
        },1400);  
    }
}