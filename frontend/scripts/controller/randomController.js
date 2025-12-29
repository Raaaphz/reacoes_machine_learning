import { DashboardModel } from "../model/dashboardModel.js";
import { DashboardView } from "../view/dashboardView.js";

const guessdiv = document.querySelector("#label_random");
const scoreSpan = document.querySelector("#score_value");

// reação sorteada atual (estado global)
let resultado = "";
let score = 0;

// FUNÇÃO DE SORTEIO
function sortearReacao() {
  function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min);
  }

  const random = getRandomInt(0, 1000);

  if (random < 135) {
    resultado = "angry";
  } else if (random > 135 && random < 200) {
    resultado = "disgust";
  } else if (random > 200 && random < 286) {
    resultado = "fear";
  } else if (random > 286 && random < 681) {
    resultado = "happy";
  } else if (random > 681 && random < 962) {
    resultado = "sad";
  } else if (random > 962 && random < 999) {
    resultado = "surprise";
  } else {
    resultado = "neutral";
  }

  console.log("Reação sorteada:", resultado);
  guessdiv.textContent = resultado;
}

// AO CARREGAR A PÁGINA
document.addEventListener("DOMContentLoaded", () => {
  sortearReacao();
  scoreSpan.textContent = score;
});

// PREDIÇÃO
const handlePrediction = async () => {
  const texto = DashboardView.getInputText();

  if (!texto) {
    DashboardView.displayResult("Neutral");
    score = 0;
    scoreSpan.textContent = score;
    return;
  }

  try {
    const prediction = await DashboardModel.makePrediction(texto);
    const predictionLower = prediction.toLowerCase();

    DashboardView.displayResult(`The reaction is: ${prediction}`);

    // COMPARAÇÃO
    if (predictionLower === resultado) {
      score++;
      scoreSpan.textContent = score;
      console.log("reação acertada");

      // sorteia nova reação
      sortearReacao();
    } else {
      score = 0;
      scoreSpan.textContent = score;
      console.log("reação errada");

      sortearReacao();
    }
  } catch (error) {
    DashboardView.displayResult(error.message);
    score = 0;
    scoreSpan.textContent = score;
  }
};

DashboardView.bindPredictButton(handlePrediction);
