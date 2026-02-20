function escondeInput(){
    const select = document.getElementById("tipo").value
    const link_input = document.querySelector(".inputlink")
    const texto_input = document.querySelector(".inputtexto")

    // escondendo inputs condicionais
    link_input.style.display = 'none'
    texto_input.style.display = 'none'

    if (select === 'interna'){
        texto_input.style.display = 'flex'
    } else if(select === 'externa'){
        link_input.style.display = 'flex'
    }
}