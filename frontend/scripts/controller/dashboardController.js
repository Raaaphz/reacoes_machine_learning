import { DashboardModel } from "../model/dashboardModel.js";
import { DashboardView } from "../view/dashboardView.js";

const handlePrediction = async () => {
  const texto = DashboardView.getInputText();

  if (!texto) {
    DashboardView.displayResult("Neutral");
    return;
  }

  try {
    const prediction = await DashboardModel.makePrediction(texto);
    DashboardView.displayResult(`The reaction is: ${prediction}`);
  } catch (error) {
    DashboardView.displayResult(error.message);
  }
};

DashboardView.bindPredictButton(handlePrediction);
