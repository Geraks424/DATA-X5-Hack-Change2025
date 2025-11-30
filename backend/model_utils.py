import pandas as pd
import numpy as np

def create_client_archetypes(df):
    df = df.copy()
    df['zoomers_score'] = df.get('mob_cnt_days', 0) + df.get('device_iphone_avg', 0)*10
    df['millennials_score'] = df.get('turn_cur_cr_avg_v2', 0) / (df.get('age', 1) + 1)
    df['smart_savers_score'] = df.get('hdb_bki_total_products', 0) * 5
    df['adventurer_score'] = df.get('avg_6m_travel', 0) * 0.01
    df['professionals_score'] = (df.get('turn_cur_cr_avg_v2', 0) - df.get('turn_cur_db_avg_v2', 0)) / (df.get('turn_cur_cr_avg_v2', 1)+1)*100
    archetype_scores = df[['zoomers_score','millennials_score','smart_savers_score','adventurer_score','professionals_score']]
    df['dominant_archetype'] = archetype_scores.idxmax(axis=1).str.replace('_score','')
    return df

def generate_financial_story(income, archetype, age):
    stories = {
        'zoomers': [f"🎮 Поколение Z! В {age} лет доход {income:,.0f}₽"],
        'millennials': [f"💼 Миллениал! Доход {income:,.0f}₽"],
        'smart_savers': [f"🎯 Финансовый стратег! Доход {income:,.0f}₽"],
        'adventurer': [f"✈️ Путешественник! Доход {income:,.0f}₽"],
        'professionals': [f"👔 Профи! Доход {income:,.0f}₽"]
    }
    return stories.get(archetype, [f"Прогноз дохода: {income:,.0f}₽"])

def get_archetype_insights(archetype, income):
    insights = {
        'zoomers': {'strength':'Цифровая грамотность','opportunity':'Финтех','recommendation':'Робо-эдвайзинг'},
        'millennials': {'strength':'Баланс навыков','opportunity':'Карьерный рост','recommendation':'Ипотека'},
        'smart_savers': {'strength':'Умение копить','opportunity':'Оптимизация кредитов','recommendation':'Бонусные карты'}
    }
    return insights.get(archetype, {'strength':'Уникальный профиль','opportunity':'Индивидуальные решения','recommendation':'План'})
