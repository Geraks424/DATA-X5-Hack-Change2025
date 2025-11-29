const form = document.getElementById('income-form');
const resultDiv = document.getElementById('result');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const data = {};
  formData.forEach((value, key) => {
    data[key] = Number(value);
  });

  try {
    const response = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
    const result = await response.json();
    if (result.predicted_income !== undefined) {
      resultDiv.textContent = `Прогнозируемый доход: ${result.predicted_income.toFixed(2)}₽`;
    } else {
      resultDiv.textContent = `Ошибка: ${result.error}`;
    }
  } catch (err) {
    resultDiv.textContent = 'Ошибка подключения к серверу';
  }
});