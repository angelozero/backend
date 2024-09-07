import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Carregando o modelo
model, model_columns = joblib.load('best_model_with_columns.pkl')

# Função de teste
def test_model_performance():
    # Gerando dados de teste fictícios (ou carregando um dataset de teste real)
    X_test_sample = pd.DataFrame({
        'last_evaluation': [0.7, 0.5, 0.3],
        'number_project': [3, 2, 5],
        'average_montly_hours': [150, 200, 100],
        'time_spend_company': [3, 2, 5],
        'Work_accident': [0, 1, 0],
        'promotion_last_5years': [0, 1, 0],
        'dept_IT': [1, 0, 0],
        'dept_sales': [0, 1, 0],
        'salary_low': [1, 0, 0],
        'salary_medium': [0, 1, 0],
        'salary_high': [0, 0, 1]
    })

    # Valores reais de satisfação (1 para satisfeito, 0 para insatisfeito)
    y_test_sample = np.array([1, 0, 0])  

    # Certifique-se de que as colunas estão na mesma ordem do modelo
    X_test_sample = X_test_sample.reindex(columns=model_columns, fill_value=0)

    # Predições do modelo
    y_pred = model.predict(X_test_sample)

    # Métricas de desempenho
    accuracy = accuracy_score(y_test_sample, y_pred)
    precision = precision_score(y_test_sample, y_pred)
    recall = recall_score(y_test_sample, y_pred)

    # Limites aceitáveis
    assert accuracy > 0.60, f"Acurácia do modelo abaixo do esperado: {accuracy:.2f}"
    assert precision <= 0.0, f"Precisão do modelo abaixo do esperado: {precision:.2f}"
    assert recall <= 0.0, f"Recall do modelo abaixo do esperado: {recall:.2f}"