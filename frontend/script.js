document.getElementById('predictForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const data = {
        age: parseFloat(document.getElementById('age').value),
        turn_cur_cr_avg_v2: parseFloat(document.getElementById('turn_cur_cr_avg_v2').value),
        mob_cnt_days: parseFloat(document.getElementById('mob_cnt_days').value),
        device_iphone_avg: parseFloat(document.getElementById('device_iphone_avg').value),
        vert_has_app_ru_tinkoff_investing: parseFloat(document.getElementById('vert_has_app_ru_tinkoff_investing').value)
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        document.getElementById('predicted_income').innerText = `Прогноз дохода: ${result.predicted_income.toFixed(2)}₽`;
        document.getElementById('archetype').innerText = `Архетип: ${result.archetype}`;
        document.getElementById('story').innerText = `История: ${result.story}`;
        document.getElementById('insights').innerText = `Инсайты: Сильные стороны - ${result.insights.strength}, Возможности - ${result.insights.opportunity}, Рекомендации - ${result.insights.recommendation}`;
    } catch (err) {
        console.error('Ошибка при запросе к серверу:', err);
    }
});
