$(document).ready(function() {
    
    $('#btnCriarPartida').on('click', function() {
        criarPartida();
    });

    function criarPartida() {

        var mestre = sessionStorage.getItem('email');
        var limiteJogadores = $('#limite_jogadores').val();
        var meuip = sessionStorage.getItem('meuip');

        $.ajax({
            type: 'POST',
            url: `http://${meuip}:5000/cadastrar_partida`,  // Rota para cadastrar uma nova partida
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                mestre_id: mestre,
                limite_jogadores: limiteJogadores
            }),
            success: function(data) {
                alert('Partida criada com sucesso!');
                window.location.assign('/main');
            },
            error: function(error) {
                console.error('Erro ao criar a partida:', error.responseText);
            }
        });
    }

});