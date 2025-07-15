export class DashboardView {
  static getInputText() {
    return document.getElementById("input-text").value;
  }

  static displayResult(message) {
    //SÓ COPIEI, VOU PRECISAR ADAPTAR PRA IMAGEM
    const resultDiv = document.getElementById("result");
    resultDiv.textContent = message;
  }

  static bindPredictButton(handler) {
    const predictButton = document.getElementById("predict-btn");
    predictButton.addEventListener("click", handler);
  }
}
