$(document).ready(function() {

    function obterPartidasDisponiveis() {
        $.ajax({
            type: 'GET',
            url: '/partidas_disponiveis', 
            success: function(data) {
                exibirPartidas(data.partidas_disponiveis);
            },
            error: function(error) {
                console.error('Erro ao obter partidas disponíveis:', error);
            }
        });
    }

    function exibirPartidas(partidas) {
        const listaPartidas = $('#listaPartidas');
        listaPartidas.empty();

        partidas.forEach(function(partida) {
            const li = $('<li>');
            li.text(`ID: ${partida.id}, Mestre: ${partida.mestre_id}, Limite: ${partida.limite_jogadores}, Jogadores Atuais: ${partida.jogadores_atuais}`);
            listaPartidas.append(li);
        });
    }

    obterPartidasDisponiveis();
});