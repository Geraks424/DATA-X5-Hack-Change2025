import pandas as pd
import numpy as np


def create_client_archetypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Создает архетипы клиентов на основе признаков.
    """
    df = df.copy()

    # 1. ZOOMERS (молодые, tech-savvy)
    df['zoomers_score'] = (
            df.get('mob_cnt_days', 0).fillna(0) +
            df.get('device_iphone_avg', 0).fillna(0) * 10 +
            df.get('vert_has_app_ru_tinkoff_investing', 0).fillna(0) * 20 +
            df.get('vert_has_app_ru_vtb_invest', 0).fillna(0) * 15
    )

    # 2. MILLENNIALS (25-40 лет, профессионалы)
    df['millennials_score'] = (
            df.get('turn_cur_cr_avg_v2', 0).fillna(0) / (df.get('age', 1).fillna(1) + 1) +
            df.get('dp_ils_total_seniority', 0).fillna(0) * 0.1 +
            (df.get('hdb_bki_total_products', 0).fillna(0) > 0) * 10
    )

    # 3. SMART SAVERS (финансовые оптимизаторы)
    df['smart_savers_score'] = (
            df.get('hdb_bki_total_products', 0).fillna(0) * 5 +
            df.get('hdb_bki_total_max_limit', 0).fillna(0) / (df.get('hdb_outstand_sum', 1).fillna(1) + 1) +
            (df.get('hdb_ovrd_sum', 0).fillna(0) == 0) * 20
    )

    # 4. ADVENTURER (активные путешественники)
    df['adventurer_score'] = (
            df.get('avg_6m_travel', 0).fillna(0) * 0.01 +
            df.get('avg_6m_hotels', 0).fillna(0) * 0.01 +
            df.get('cntRegionTripsWavg1m', 0).fillna(0) * 2
    )

    # 5. PROFESSIONALS (финансовые эксперты)
    df['professionals_score'] = (
            (df.get('turn_cur_cr_avg_v2', 0).fillna(0) - df.get('turn_cur_db_avg_v2', 0).fillna(0)) /
            (df.get('turn_cur_cr_avg_v2', 1).fillna(1) + 1) * 100 +
            df.get('curr_rur_amt_cm_avg', 0).fillna(0) * 0.001 +
            df.get('turn_save_db_min_v2', 0).fillna(0) * 0.1
    )

    # Определяем доминирующий архетип с помощью numpy
    archetype_cols = ['zoomers_score', 'millennials_score', 'smart_savers_score', 'adventurer_score',
                      'professionals_score']
    df['dominant_archetype'] = np.array(archetype_cols)[np.argmax(df[archetype_cols].values, axis=1)]
    df['dominant_archetype'] = df['dominant_archetype'].str.replace('_score', '')

    return df


# 🎯 Генерация креативной истории по доходу и архетипу
def generate_financial_story(income: float, archetype: str, age: int) -> str:
    stories = {
        'zoomers': [
            f"🎮 Поколение Z! В {age} лет ваш цифровой образ жизни = доход {income:,.0f}₽",
            f"📱 Цифровой абориген! Ваша tech-грамотность создает доход {income:,.0f}₽"
        ],
        'millennials': [
            f"💼 Золотой миллениал! Стабильная карьера = доход {income:,.0f}₽ в {age} лет",
            f"🏢 Профессионал экстра-класса! Ваш опыт создает доход {income:,.0f}₽"
        ],
        'smart_savers': [
            f"🎯 Финансовый стратег! Умные решения = доход {income:,.0f}₽",
            f"💡 Гений оптимизации! Вы создаете доход {income:,.0f}₽ через smart-подход"
        ],
        'adventurer': [
            f"✈️ Искатель приключений! Активная жизнь = доход {income:,.0f}₽",
            f"🌍 Гражданин мира! Путешествия + доход {income:,.0f}₽ = идеальная формула"
        ],
        'professionals': [
            f"👔 Финансовый эксперт! Консервативный подход = стабильный доход {income:,.0f}₽",
            f"🏛️ Профессионал высшей лиги! Ваш опыт = доход {income:,.0f}₽"
        ]
    }

    archetype_stories = stories.get(archetype, [f"Прогноз дохода: {income:,.0f}₽"])
    story_idx = min(int(income / 50000), len(archetype_stories) - 1)
    return archetype_stories[story_idx]


# 📊 Получение инсайтов по архетипу
def get_archetype_insights(archetype: str, income: float) -> dict:
    insights = {
        'zoomers': {
            'strength': 'Цифровая грамотность - ваша суперсила',
            'opportunity': 'Финтех и цифровые инвестиции для ускорения роста',
            'recommendation': 'Крипто-портфель и робо-эдвайзинг'
        },
        'millennials': {
            'strength': 'Идеальный баланс цифровых навыков и профессионального опыта',
            'opportunity': 'Карьерный рост и инвестиции в недвижимость',
            'recommendation': 'Ипотека с эксклюзивной ставкой'
        },
        'smart_savers': {
            'strength': 'Умение заставлять деньги работать на себя',
            'opportunity': 'Оптимизация кредитного портфеля',
            'recommendation': 'Кредитные карты с бонусами'
        }
    }

    return insights.get(archetype, {
        'strength': 'Уникальный финансовый профиль',
        'opportunity': 'Индивидуальные финансовые решения',
        'recommendation': 'Персональный финансовый план'
    })
