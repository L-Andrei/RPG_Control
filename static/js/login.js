$(document).ready(function () {
    $('#formLogin').submit(function (event) {
        event.preventDefault();

        var email = $('#email').val();
        var senha = $('#senha').val();

        $.ajax({
            type: 'POST',
            url: '/login_json',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'email': email,
                'senha': senha
            }),
            success: function (data) {
                console.log(data);
                if (data.email) {
                    sessionStorage.setItem('userEmail', data.email);
                    sessionStorage.setItem('userEmail', data.nome);
                    
                    alert('Login bem-sucedido! Email: ' + data.email + ', Nome: ' + data.nome);
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