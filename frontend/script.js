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
    // Используем относительный путь — работает и при локальной разработке и при деплое за одним доменом
    const response = await fetch('/predict', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });

    const result = await response.json();
    if (response.ok && result.predicted_income !== undefined) {
      resultDiv.textContent = `Прогнозируемый доход: ${result.predicted_income.toFixed(2)}₽`;
      resultDiv.style.color = 'green';
    } else {
      resultDiv.textContent = `Ошибка: ${result.error || 'Неизвестная ошибка'}`;
      resultDiv.style.color = 'red';
    }
  } catch (err) {
    resultDiv.textContent = 'Ошибка подключения к серверу';
    resultDiv.style.color = 'red';
  }
});