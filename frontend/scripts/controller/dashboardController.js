import { dashboardModel } from "../model/dashboardModel.js";
import { DashboardView } from "../view/dashboardView";

const handlePrediction = async () => {
  const texto = DashboardView.getInputText();

  if (!texto) {
    DashboardView.displayResult("Por favor, insira um texto.");
    return;
  }

  try {
    const prediction = await dashboardModel.makePrediction(texto);
    DashboardView.displayResult(`A reação foi de: ${prediction}`); //TAMBÉM ADAPTAR PARA EXIBIR IMAGEM
  } catch (error) {
    DashboardView.displayResult(error.message);
  }
};

DashboardView.bindPredictButton(handlePrediction);
