let idParaExcluir = null;

function abrirModal(id, nome) {
    idParaExcluir = id;
    document.getElementById("mensagemModal").innerText = `Tem certeza que deseja excluir "${nome}"?`;
    document.getElementById("modalExclusao").style.display = "flex";
}

function fecharModal() {
    idParaExcluir = null;
    document.getElementById("modalExclusao").style.display = "none";
}

function excluirItem() {
    if (idParaExcluir !== null) {
        window.location.href = `/excluir/bebida/${idParaExcluir}`;
    }
}
