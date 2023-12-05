$(document).ready(function () {
    $('#formCadastro').submit(function (event) {
        event.preventDefault();

        var nome = $('#nome').val();
        var senha = $('#senha').val();
        var email = $('#email').val();
        meuip = sessionStorage.getItem('meuip');

        $.ajax({
            type: 'POST',
            url: `http://${meuip}:5000/cadastrar_usuario_json`,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'nome': nome,
                'senha': senha,
                'email': email
            }),
            success: function (data) {
                console.log(data);
                if (data.email) {
                    // Salvar informações na sessão local
                    localStorage.setItem('email', data.email);
                    localStorage.setItem('nome', data.nome);
                    localStorage.getItem('email');
                    localStorage.getItem('nome');

                    alert('Usuário cadastrado com sucesso!');
                    window.location.assign("main");
                } else {
                    alert('Erro ao cadastrar usuário.');
                }
            },
            error: function (error) {
                console.error(error);
                alert('Erro ao cadastrar usuário.');
            }
        });
    });
});