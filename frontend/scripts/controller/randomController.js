const guessdiv = document.querySelector("#label_random");

document.addEventListener("DOMContentLoaded", () => {
  const guessdiv = document.querySelector("#label_random");

  function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min);
  }

  random = getRandomInt(0, 6);

  if (random == 0) {
    resultado = "angry";
  } else if (random == 1) {
    resultado = "disgust";
  } else if (random == 2) {
    resultado = "fear";
  } else if (random == 3) {
    resultado = "happy";
  } else if (random == 4) {
    resultado == "sad";
  } else if (random == 5) {
    resultado == "surprise";
  } else {
    resultado = "neutro";
  }

  console.log(resultado);

  guessdiv.textContent = resultado;
});
