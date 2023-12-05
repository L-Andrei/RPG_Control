$(document).ready(function () {
    $('#formCadastro').submit(function (event) {
        event.preventDefault();

        var nome = $('#nome').val();
        var senha = $('#senha').val();
        var email = $('#email').val();

        $.ajax({
            type: 'POST',
            url: '/cadastrar_usuario_json',
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                'nome': nome,
                'senha': parseInt(senha),
                'email': email
            }),
            success: function (data) {
                console.log(data);
                if (data.email) {
                    // Salvar informações na sessão local
                    localStorage.setItem('email', data.email);
                    localStorage.setItem('nome', data.nome);

                    alert('Usuário cadastrado com sucesso!');
                    // Redirecionar para a página de login ou fazer outra ação
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