$(document).ready(function () {
    $('#formLogin').submit(function (event) {
        event.preventDefault();

        var email = $('#email').val();
        var senha = $('#senha').val();
        meuip = sessionStorage.getItem('meuip');

        $.ajax({
            type: 'POST',
            url: `http://${meuip}:5000/login_json`,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'email': email,
                'senha': senha
            }),
            success: function (data) {
                console.log(data);
                if (data.email) {
                    sessionStorage.setItem('email', data.email);
                    sessionStorage.setItem('nome', data.nome);
                    localStorage.getItem('email');
                    localStorage.getItem('nome');

                    
                    alert('Login bem-sucedido! ' + data.nome);
                    window.location.assign('/main');
                } else {
                    alert('Usuário não encontrado.');
                }
            },
            error: function (error) {
                console.error(error);
                alert('Erro ao realizar o login.');
            }
        });
    });
});