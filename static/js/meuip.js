$(function () {

    var url = document.URL;
    var protocolo = "http://";
    var http = protocolo.length; 
    var comeco = url.substring(http); 
    var partes = comeco.split("/"); 
    var primeiro = partes[0];

    posicao_doispontos = primeiro.indexOf(":");
    if (posicao_doispontos >= 0) { 
        meuip = primeiro.substring(0, posicao_doispontos);
    } else {
        meuip = primeiro;
    }
    var mensagem = "URL = " + url + "<br/>Endereço do servidor: "+meuip;
    $("#mostrar").html(mensagem);

    sessionStorage.setItem("meuip",meuip);
});