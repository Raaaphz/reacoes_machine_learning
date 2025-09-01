export class DashboardView {
  static getInputText() {
    return document.getElementById("input-text").value;
  }

  static displayResult(message) {
    const resultDiv = document.getElementById("result");
    resultDiv.textContent = `${message}`;

    this.updateImage(message.toLowerCase());
  }

  static updateImage(reaction) {
    const imagens = document.querySelectorAll(".imagemReacao .imagem");
    imagens.forEach((img) => img.classList.remove("ativo"));

    reaction = reaction.toLowerCase();

    // mapeando os nomes
    const mapa = {
      angry: "emogi_angry",
      disgust: "emogi_disgust",
      fear: "emogi_fear",
      happy: "emogi_happy",
      sad: "emogi_sad",
      surprise: "emogi_surprise",
      neutral: "emogi_neutro",
      neutro: "emogi_neutro",
    };

    // 🔑 tenta encontrar se alguma key do mapa está dentro da frase
    let chaveEncontrada = Object.keys(mapa).find((key) =>
      reaction.includes(key)
    );

    const alvo = mapa[chaveEncontrada];
    let imgAtiva = null;

    if (alvo) {
      imgAtiva = document.querySelector(
        `.imagemReacao .imagem img[alt="${alvo}"]`
      );
      if (imgAtiva) {
        imgAtiva.parentElement.classList.add("ativo");
      }
    }

    console.log("Reaction recebido:", reaction);
    console.log("Chave encontrada:", chaveEncontrada);
    console.log("Alvo mapeado:", alvo);
    console.log("Elemento encontrado:", imgAtiva);
  }

  static bindPredictButton(handler) {
    const predictButton = document.getElementById("predict-btn");
    predictButton.addEventListener("click", handler);
  }
}
