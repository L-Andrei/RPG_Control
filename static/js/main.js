$(document).ready(function() {
    const meuip = sessionStorage.getItem('meuip');

    function obterPartidasDisponiveis() {
        $.ajax({
            type: 'GET',
            url: `http://${meuip}:5000/partidas_disponiveis`,
            success: function(data) {
                exibirPartidas(data.partidas_disponiveis);
            },
            error: function(error) {
                console.error('Erro ao obter partidas disponíveis:', error);
            }
        });
    }

    function entrarNaPartida(idPartida) {
        $.ajax({
            type: 'POST',
            url: `http://${meuip}:5000/entrar_partida`,
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({ partida_id: idPartida }),
            success: function(data) {
                alert(data.mensagem);
                // Atualize a lista de partidas após entrar
                obterPartidasDisponiveis();
            },
            error: function(error) {
                console.error('Erro ao entrar na partida:', error);
            }
        });
    }

    function exibirPartidas(partidas) {
        const listaPartidas = $('#listaPartidas');
        listaPartidas.empty();

        partidas.forEach(function(partida) {
            const li = $('<li>');
            li.addClass('partida-item');

            const infoPartida = $(`
                <div class="partida-info">
                    <span>ID: ${partida.id}</span>
                    <span>Mestre: ${partida.mestre_id}</span>
                    <span>Limite: ${partida.limite_jogadores}</span>
                    <span>Jogadores Atuais: ${partida.jogadores_atuais}</span>
                </div>
            `);

            const btnEntrar = $('<button>');
            btnEntrar.text('Entrar na Partida');
            btnEntrar.addClass('btn-entrar');
            btnEntrar.val(partida.id); // Adiciona o ID da partida ao valor do botão
            btnEntrar.click(function() {
                entrarNaPartida(btnEntrar.val()); // Captura o valor do botão (ID da partida)
            });

            li.append(infoPartida);
            li.append(btnEntrar);
            listaPartidas.append(li);
        });
    }

    obterPartidasDisponiveis();
});