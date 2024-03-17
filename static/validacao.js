function validarTexto(campoId) {
  var campoTexto = document.getElementById(campoId);
  var mensagemErro = document.getElementById("mensagemErro" + campoId.charAt(campoId.length - 1));

  // Expressão regular para permitir apenas letras e espaços
  //var regex = /^[a-zA-Z\s]+$/;
  //var regex = /^[a-zA-Z0-9]*$/;
  var regex = /[\w-]/m;

  if (!regex.test(campoTexto.value)) {
    mensagemErro.textContent = "Use apenas letras, números, traços e subtraços.";
    campoTexto.setCustomValidity("Use apenas letras, números, traços e subtraços.");
  } else {
    mensagemErro.textContent = "";
    campoTexto.setCustomValidity("");
  }
}

document.getElementById("meuFormulario").addEventListener("submit", function (event) {
  // Impede o envio do formulário se houver erros de validação
  if (!this.checkValidity()) {
    event.preventDefault();
  }
});