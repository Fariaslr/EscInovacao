
# 📊 Data Analyzer App

Aplicativo web interativo para análise exploratória de dados desenvolvido com **Streamlit**, **Pandas**, **Seaborn** e **Matplotlib**. Ideal para visualizar, filtrar e entender rapidamente conjuntos de dados em formato `.csv` ou `.xlsx`.

---

## ✅ Funcionalidades

- 📁 Upload de arquivos CSV e Excel (.xlsx)
- 📋 Visualização dos dados em tabela
- 📈 Estatísticas descritivas (média, mediana, desvio padrão)
- 🔍 Filtro interativo por colunas numéricas
- 📊 Gráficos gerados automaticamente:
  - Histograma
  - Gráfico de Dispersão (Scatter Plot)
  - Gráfico de Barras
- Interface intuitiva com instruções para o usuário

---

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/data-analyzer-app.git
cd data-analyzer-app
```

### 2. Crie e ative um ambiente virtual (recomendado)

No **Windows**:

```bash
python -m venv venv
.env\Scriptsctivate
```

No **Linux/Mac**:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

Com o `requirements.txt`:

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install streamlit pandas seaborn matplotlib openpyxl scikit-learn
```

### 4. Execute o aplicativo

```bash
streamlit run app.py
```

> O navegador será aberto automaticamente em `http://localhost:8501`.

---

## 📁 Estrutura do Projeto

```
📦 data-analyzer-app
├── app.py                # Código principal do aplicativo
├── iris.csv              # Exemplo de dataset gerado automaticamente
├── .gitignore            # Arquivos/pastas ignoradas pelo Git
├── requirements.txt      # Lista de dependências
└── README.md             # Este arquivo
```

---

## 📌 Observações

- O dataset **Iris** da biblioteca `scikit-learn` é salvo automaticamente como `iris.csv` ao iniciar o app.
- Para adicionar novos tipos de gráficos ou funcionalidades, edite o arquivo `app.py`.
- Certifique-se de ativar o ambiente virtual sempre que for usar o projeto localmente.

---

💡 Desenvolvido para fins educacionais e de análise de dados. Sinta-se à vontade para contribuir ou personalizar!
