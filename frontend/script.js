// Mock-данные в формате API
const mockData = [
  {
    "id": "0",
    "age": 34,
    "gender": "Мужской",
    "predicted_income": 85200,
    "shap_values": {
      "per_capita_income_rur_amt": 21000,
      "dda_rur_amt_cm_avg": 15000,
      "blacklist_flag": -12000,
      "loan_cnt": -8000,
      "age": 5000
    },
    "recommendations": [
      "Автокредит до 1.5 млн",
      "Премиальная дебетовая карта"
    ]
  },
  {
    "id": "1",
    "age": 45,
    "gender": "Женский",
    "predicted_income": 120500,
    "shap_values": {
      "per_capita_income_rur_amt": 30000,
      "dda_rur_amt_cm_avg": 25000,
      "blacklist_flag": -5000
    },
    "recommendations": [
      "Вклад «Выгодный» под 12%",
      "Ипотека на льготных условиях"
    ]
  },
  {
    "id": "3",
    "age": 72,
    "gender": "Женский",
    "predicted_income": 223000,
    "shap_values": {
      "per_capita_income_rur_amt": 80000,
      "device_iphone_avg": 8000
    },
    "recommendations": [
      "Инвестиционный счет ИИС",
      "Карта All Airlines"
    ]
  },
  {
    "id": "12",
    "age": 54,
    "gender": "Женский",
    "predicted_income": 1780817,
    "shap_values": {
      "dda_rur_amt_3m_avg": 106511,
      "loan_cnt": -13562
    },
    "recommendations": [
      "Бизнес-кредит",
      "Кассовое обслуживание"
    ]
  },
  {
    "id": "63",
    "age": 48,
    "gender": "Мужской",
    "predicted_income": 12485081,
    "shap_values": {
      "per_capita_income_rur_amt": 175885,
      "bki_total_products": -10000
    },
    "recommendations": [
      "Корпоративный счёт",
      "Зарплатный проект"
    ]
  }
];

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

// Функция для имитации API запроса
async function fetchClientData(clientId) {
  // Имитация задержки сети
  await new Promise(resolve => setTimeout(resolve, 600));
  
  // Ищем клиента в mock данных
  const client = mockData.find(client => client.id === clientId);
  
  if (!client) {
    throw new Error('Клиент не найден');
  }
  
  return client;
}

async function handleSearch() {
  const id = clientIdInput.value.trim();

  // Валидация
  if (!id) return showError('Введите ID клиента');
  
  // ID может быть строкой (как в вашем формате "12")
  if (!/^\d+$/.test(id)) return showError('ID должен содержать только цифры');

  // Показ загрузки
  hideError();
  loadingEl.classList.remove('hidden');
  resultEl.classList.add('hidden');

  try {
    const client = await fetchClientData(id);
    showResult(client);
  } catch (error) {
    const availableIds = mockData.map(client => client.id).join(', ');
    showError(`Клиент не найден. Доступны ID: ${availableIds}`);
  } finally {
    loadingEl.classList.add('hidden');
  }
}

function showResult(client) {
  // Обновляем информацию о клиенте
  resultIdEl.textContent = client.id;
  incomeEl.textContent = client.predicted_income.toLocaleString('ru-RU') + ' ₽/мес';

  // Дополнительная информация о клиенте (если есть элементы в HTML)
  const iconPath = getIconPath(client.gender, client.age);
  const iconEl = document.getElementById('clientIcon');
  if (iconEl) iconEl.src = iconPath;
  const genderEl = document.getElementById('clientGender');
  const ageEl = document.getElementById('clientAge');
  
  if (genderEl) genderEl.textContent = client.gender;
  if (ageEl) ageEl.textContent = `${client.age} лет`;

  // SHAP значения (теперь это объект, а не массив)
  shapListEl.innerHTML = '';
  for (const [feature, effect] of Object.entries(client.shap_values)) {
    const isPositive = effect > 0;
    const sign = isPositive ? '+' : '-';
    const color = isPositive ? '#52c41a' : '#ff4d4f';
    
    // Форматируем название фичи для читаемости
    const featureName = formatFeatureName(feature);
    
    shapListEl.innerHTML += `
      <div style="padding: 6px 0; display: flex; justify-content: space-between; font-size: 14px;">
        <span>${featureName}</span>
        <span style="color: ${color}">${sign}${Math.abs(effect).toLocaleString('ru-RU')} ₽</span>
      </div>
    `;
  }

  // Рекомендации
  recommendationsEl.innerHTML = '';
  client.recommendations.forEach(rec => {
    recommendationsEl.innerHTML += `
      <div style="padding: 6px 0; font-size: 15px;">• ${rec}</div>
    `;
  });

  resultEl.classList.remove('hidden');
}

// Функция для форматирования названий фич
function formatFeatureName(feature) {
  const featureNames = {
    "per_capita_income_rur_amt": "Доход на душу населения",
    "dda_rur_amt_cm_avg": "Средний остаток на счетах",
    "dda_rur_amt_3m_avg": "Остаток на счетах (3 месяца)",
    "blacklist_flag": "Наличие в черном списке",
    "loan_cnt": "Количество кредитов",
    "age": "Возраст",
    "device_iphone_avg": "Использование iPhone",
    "bki_total_products": "Количество продуктов БКИ"
  };
  
  return featureNames[feature] || feature;
}

function getIconPath(gender, age) {
  if (age == null || isNaN(age)) {
    return gender === 'Мужской' 
      ? './icons/man_26-45.png' 
      : './icons/woman_26-45.png';
  }

  let group;
  if (age < 25) group = 'under25';
  else if (age <= 45) group = '26-45';
  else if (age <= 65) group = '46-65';
  else group = '65plus';

  const prefix = gender === 'Мужской' ? 'man' : 'woman';
  return `./icons/${prefix}_${group}.png`;
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.style.display = 'block';
}

function hideError() {
  errorEl.style.display = 'none';
}