// Mock-данные (реалистичные, на основе твоего CSV)
const mockData = {
  "0": {
    age: 34,
    gender: "Мужской",
    income: 85200,
    shap: [
      { feature: "per_capita_income_rur_amt", effect: 21000 },
      { feature: "dda_rur_amt_cm_avg", effect: 15000 },
      { feature: "blacklist_flag", effect: -12000 },
      { feature: "loan_cnt", effect: -8000 },
      { feature: "age", effect: 5000 }
    ],
    recommendations: [
      "Автокредит до 1.5 млн",
      "Премиальная дебетовая карта"
    ]
  },
  "1": {
    age: 45,
    gender: "Женский",
    income: 120500,
    shap: [
      { feature: "per_capita_income_rur_amt", effect: 30000 },
      { feature: "dda_rur_amt_cm_avg", effect: 25000 },
      { feature: "blacklist_flag", effect: -5000 }
    ],
    recommendations: [
      "Вклад «Выгодный» под 12%",
      "Ипотека на льготных условиях"
    ]
  },
  "3": {
    age: 72,
    gender: "Женский",
    income: 223000,
    shap: [
      { feature: "per_capita_income_rur_amt", effect: 80000 },
      { feature: "device_iphone_avg", effect: 8000 }
    ],
    recommendations: [
      "Инвестиционный счет ИИС",
      "Карта All Airlines"
    ]
  },
  "12": {
    age: 54,
    gender: "Женский",
    income: 1780817,
    shap: [
      { feature: "dda_rur_amt_3m_avg", effect: 106511 },
      { feature: "loan_cnt", effect: -13562 }
    ],
    recommendations: [
      "Бизнес-кредит",
      "Кассовое обслуживание"
    ]
  },
  "63": {
    age: 48,
    gender: "Мужской",
    income: 12485081,
    shap: [
      { feature: "per_capita_income_rur_amt", effect: 175885 },
      { feature: "bki_total_products", effect: -10000 }
    ],
    recommendations: [
      "Корпоративный счёт",
      "Зарплатный проект"
    ]
  }
};

// DOM-элементы
const clientIdInput = document.getElementById('clientIdInput');
const searchBtn = document.getElementById('searchBtn');
const errorEl = document.getElementById('error');
const loadingEl = document.getElementById('loading');
const resultEl = document.getElementById('result');
const resultIdEl = document.getElementById('resultId');
const incomeEl = document.getElementById('income');
const shapListEl = document.getElementById('shapList');
const recommendationsEl = document.getElementById('recommendations');

// Обработчик поиска
searchBtn.addEventListener('click', handleSearch);
clientIdInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') handleSearch();
});

// В функции handleSearch замените:
function handleSearch() {
  const id = clientIdInput.value.trim();

  // Валидация
  if (!id) return showError('Введите ID клиента');
  if (!/^\d+$/.test(id)) return showError('ID должен содержать только цифры');

  // Показ загрузки
  hideError();
  loadingEl.classList.remove('hidden');
  resultEl.classList.add('hidden');

  // Имитация задержки сети
  setTimeout(() => {
    const client = mockData[id];

    if (client) {
      showResult(id, client);
    } else {
      showError('Клиент не найден. Доступны ID: 0, 1, 3, 12, 63');
    }

    loadingEl.classList.add('hidden');
  }, 600);
}

// В функции showResult замените:
function showResult(id, client) {
  resultIdEl.textContent = id;
  incomeEl.textContent = client.income.toLocaleString('ru-RU') + ' ₽/мес';

  // SHAP
  shapListEl.innerHTML = '';
  client.shap.forEach(item => {
    const isPositive = item.effect > 0;
    const sign = isPositive ? '+' : '';
    const color = isPositive ? '#52c41a' : '#ff4d4f';
    shapListEl.innerHTML += `
      <div style="padding: 6px 0; display: flex; justify-content: space-between; font-size: 14px;">
        <span>${item.feature}</span>
        <span style="color: ${color}">${sign}${item.effect.toLocaleString('ru-RU')} ₽</span>
      </div>
    `;
  });

  // Рекомендации
  recommendationsEl.innerHTML = '';
  client.recommendations.forEach(rec => {
    recommendationsEl.innerHTML += `
      <div style="padding: 6px 0; font-size: 15px;">• ${rec}</div>
    `;
  });

  resultEl.classList.remove('hidden');
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.style.display = 'block';
}

function hideError() {
  errorEl.style.display = 'none';
}