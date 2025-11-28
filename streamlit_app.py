"""
Streamlit web application for Alfa-Bank Income Prediction Dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from typing import Dict, List, Optional
import yaml

# Page configuration
st.set_page_config(
    page_title="Alfa-Bank Income Prediction Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load configuration
try:
    with open("config.yaml", 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    API_URL = f"http://{config['api']['host']}:{config['api']['port']}"
except:
    API_URL = "http://localhost:8000"
    config = {"api": {"host": "localhost", "port": 8000}}


# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #EF3124;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #EF3124;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


def check_api_health() -> bool:
    """Check if API is available"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200 and response.json().get("model_loaded", False)
    except:
        return False


def predict_income(client_data: Dict) -> Optional[Dict]:
    """Call prediction API"""
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"data": client_data},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}. Make sure the API is running.")
        return None


def get_shap_explanation(client_data: Dict) -> Optional[Dict]:
    """Get SHAP explanation from API"""
    try:
        response = requests.post(
            f"{API_URL}/shap_explain",
            json={"data": client_data},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def get_feature_importance() -> Optional[List[Dict]]:
    """Get feature importance from API"""
    try:
        response = requests.get(f"{API_URL}/feature_importance?top_n=20")
        if response.status_code == 200:
            return response.json().get("features", [])
        return None
    except:
        return None


def load_sample_clients() -> pd.DataFrame:
    """Load sample client data"""
    # Generate sample data structure
    sample_data = {
        'id': [1, 2, 3, 4, 5],
        'age': [35, 42, 28, 55, 31],
        'employment_years': [5, 12, 3, 25, 6],
        'education': ['higher', 'higher', 'secondary', 'higher', 'higher'],
        'city': ['Moscow', 'St. Petersburg', 'Moscow', 'Novosibirsk', 'Moscow'],
    }
    return pd.DataFrame(sample_data)


def main():
    # Header
    st.markdown('<h1 class="main-header">💰 Alfa-Bank Income Prediction Dashboard</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Настройки")
        
        # API status
        api_status = check_api_health()
        if api_status:
            st.success("✅ API подключен")
        else:
            st.error("❌ API недоступен")
            st.info("Запустите API: `python -m uvicorn src.api:app --reload`")
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Выберите раздел",
            ["🔮 Предсказание дохода", "👥 Клиентская база", "📊 Аналитика модели", "📈 Мониторинг"]
        )
    
    # Main content
    if page == "🔮 Предсказание дохода":
        prediction_page()
    elif page == "👥 Клиентская база":
        client_database_page()
    elif page == "📊 Аналитика модели":
        analytics_page()
    elif page == "📈 Мониторинг":
        monitoring_page()


def prediction_page():
    """Income prediction page"""
    st.header("🔮 Предсказание дохода клиента")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Данные клиента")
        
        # Client input form
        with st.form("client_form"):
            age = st.number_input("Возраст", min_value=18, max_value=100, value=35)
            employment_years = st.number_input("Стаж работы (лет)", min_value=0, max_value=50, value=5)
            education = st.selectbox("Образование", ["secondary", "higher", "postgraduate"])
            city = st.selectbox("Город", ["Moscow", "St. Petersburg", "Novosibirsk", "Kazan", "Yekaterinburg"])
            
            # Additional fields (can be expanded based on actual data structure)
            col_a, col_b = st.columns(2)
            with col_a:
                family_status = st.selectbox("Семейное положение", ["single", "married", "divorced"])
            with col_b:
                has_children = st.checkbox("Есть дети")
            
            submitted = st.form_submit_button("🔍 Предсказать доход", type="primary")
        
        if submitted and api_status:
            client_data = {
                "age": age,
                "employment_years": employment_years,
                "education": education,
                "city": city,
                "family_status": family_status,
                "has_children": 1 if has_children else 0
            }
            
            # Show loading
            with st.spinner("Выполняется предсказание..."):
                result = predict_income(client_data)
            
            if result:
                st.session_state['prediction_result'] = result
                st.session_state['client_data'] = client_data
                st.rerun()
    
    with col2:
        st.subheader("Результаты предсказания")
        
        if 'prediction_result' in st.session_state:
            result = st.session_state['prediction_result']
            client_data = st.session_state.get('client_data', {})
            
            # Display prediction
            predicted_income = result['predicted_income']
            
            st.markdown(f"""
                <div class="prediction-box">
                    <h2 style="color: #EF3124; margin-bottom: 1rem;">Прогнозируемый доход</h2>
                    <h1 style="font-size: 3rem; margin: 1rem 0;">{predicted_income:,.0f} ₽</h1>
                    <p style="color: #666;">в месяц</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Recommendations
            st.subheader("💼 Рекомендуемые продукты")
            recommendations = result.get('recommendations', [])
            
            for rec in recommendations:
                with st.expander(f"✅ {rec['product_name']} (Приоритет: {rec['priority']:.1f}x)"):
                    st.write(rec['description'])
                    st.metric("Минимальный доход", f"{rec['min_income_required']:,.0f} ₽")
                    if rec.get('max_rate'):
                        st.metric("Максимальная ставка", f"{rec['max_rate']:.1f}%")
                    st.progress(min(1.0, rec.get('confidence', 0.5)))
            
            # SHAP explanation button
            if st.button("📊 Показать объяснение предсказания"):
                with st.spinner("Генерируется объяснение..."):
                    shap_result = get_shap_explanation(client_data)
                
                if shap_result:
                    display_shap_explanation(shap_result)
        else:
            st.info("👈 Заполните форму слева и нажмите 'Предсказать доход'")


def display_shap_explanation(shap_result: Dict):
    """Display SHAP explanation"""
    st.subheader("🔍 Объяснение предсказания (SHAP)")
    
    top_features = shap_result.get('top_features', [])
    
    if top_features:
        # Create waterfall plot
        fig = go.Figure(go.Waterfall(
            orientation="v",
            measure=["relative"] * (len(top_features) - 1) + ["total"],
            x=[f["feature"] for f in top_features],
            textposition="outside",
            text=[f"{f['contribution']:+.2f}" for f in top_features],
            y=[f["contribution"] for f in top_features],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="Вклад факторов в предсказание",
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature contributions table
        st.subheader("Детальный вклад факторов")
        contrib_df = pd.DataFrame(top_features)
        contrib_df['contribution'] = contrib_df['contribution'].apply(lambda x: f"{x:+.2f}")
        st.dataframe(contrib_df, use_container_width=True, hide_index=True)


def client_database_page():
    """Client database page with batch predictions"""
    st.header("👥 Клиентская база")
    
    # Load sample clients
    clients_df = load_sample_clients()
    
    st.subheader("Выберите клиентов для анализа")
    
    # Client selector
    selected_ids = st.multiselect(
        "Клиенты",
        options=clients_df['id'].tolist(),
        default=clients_df['id'].tolist()[:3]
    )
    
    if selected_ids:
        selected_clients = clients_df[clients_df['id'].isin(selected_ids)]
        st.dataframe(selected_clients, use_container_width=True)
        
        if st.button("📊 Предсказать доходы для выбранных клиентов") and api_status:
            with st.spinner("Выполняется пакетное предсказание..."):
                # Convert to API format
                clients_data = selected_clients.drop(columns=['id']).to_dict('records')
                
                try:
                    response = requests.post(
                        f"{API_URL}/batch_predict",
                        json={"clients": clients_data},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        predictions = response.json()['predictions']
                        
                        # Display results
                        results_df = pd.DataFrame(predictions)
                        results_df['predicted_income'] = results_df['predicted_income'].round(2)
                        
                        # Merge with client data
                        results_df = selected_clients.merge(
                            results_df, 
                            left_on='id', 
                            right_on='client_id'
                        )
                        
                        st.subheader("📈 Результаты предсказаний")
                        st.dataframe(results_df[['id', 'age', 'education', 'city', 'predicted_income']], 
                                   use_container_width=True)
                        
                        # Visualization
                        fig = px.bar(
                            results_df,
                            x='id',
                            y='predicted_income',
                            title="Прогнозируемый доход по клиентам",
                            labels={'predicted_income': 'Доход (₽)', 'id': 'ID клиента'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Ошибка при предсказании: {str(e)}")


def analytics_page():
    """Model analytics page"""
    st.header("📊 Аналитика модели")
    
    if not api_status:
        st.warning("API недоступен. Невозможно загрузить данные о модели.")
        return
    
    # Feature importance
    st.subheader("🔝 Важность признаков")
    
    importance_data = get_feature_importance()
    if importance_data:
        importance_df = pd.DataFrame(importance_data)
        
        # Bar chart
        fig = px.bar(
            importance_df,
            x='importance',
            y='feature',
            orientation='h',
            title="Топ-20 важнейших признаков",
            labels={'importance': 'Важность', 'feature': 'Признак'}
        )
        fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Table
        st.dataframe(importance_df, use_container_width=True, hide_index=True)
    else:
        st.info("Не удалось загрузить данные о важности признаков")


def monitoring_page():
    """Model monitoring page"""
    st.header("📈 Мониторинг качества модели")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Статус модели", "✅ Активна")
        st.metric("Запросов сегодня", "1,234", "↑ 12%")
    
    with col2:
        st.metric("Средняя точность", "87.5%", "↑ 2.3%")
        st.metric("Время ответа", "0.15s", "↓ 0.02s")
    
    with col3:
        st.metric("Успешных рекомендаций", "89%", "↑ 5%")
        st.metric("Клиентов обслужено", "5,678", "↑ 234")
    
    st.markdown("---")
    
    # Mock monitoring charts
    st.subheader("Метрики за последний месяц")
    
    dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    mock_data = pd.DataFrame({
        'date': dates,
        'predictions': np.random.randint(50, 200, 30),
        'accuracy': np.random.uniform(0.85, 0.95, 30),
        'response_time': np.random.uniform(0.1, 0.2, 30)
    })
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Количество предсказаний', 'Точность модели', 
                       'Время ответа (мс)', 'Распределение ошибок'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"type": "histogram"}]]
    )
    
    # Predictions over time
    fig.add_trace(
        go.Scatter(x=mock_data['date'], y=mock_data['predictions'], 
                  name='Предсказания', line=dict(color='#EF3124')),
        row=1, col=1
    )
    
    # Accuracy over time
    fig.add_trace(
        go.Scatter(x=mock_data['date'], y=mock_data['accuracy'], 
                  name='Точность', line=dict(color='green'), fill='tonexty'),
        row=1, col=2
    )
    
    # Response time
    fig.add_trace(
        go.Scatter(x=mock_data['date'], y=mock_data['response_time']*1000, 
                  name='Время ответа', line=dict(color='orange')),
        row=2, col=1
    )
    
    # Error distribution
    errors = np.random.normal(0, 5000, 1000)
    fig.add_trace(
        go.Histogram(x=errors, name='Ошибки', nbinsx=30),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    # Initialize session state
    if 'prediction_result' not in st.session_state:
        st.session_state['prediction_result'] = None
    if 'client_data' not in st.session_state:
        st.session_state['client_data'] = None
    
    # Check API status
    api_status = check_api_health()
    
    main()

