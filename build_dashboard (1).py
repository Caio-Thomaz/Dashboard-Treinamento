
import pandas as pd
import plotly.express as px
from datetime import date

INPUT_XLSX = 'base_treinamentos_limpa.xlsx'  # coloque este arquivo na raiz do repositório
OUTPUT_HTML = 'index.html'                   # GitHub Pages usa index.html como página inicial

# Carrega dados
try:
    df = pd.read_excel(INPUT_XLSX, engine='openpyxl')
except Exception as e:
    raise SystemExit(f'Erro ao ler {INPUT_XLSX}: {e}\nCertifique-se de que o arquivo existe na raiz do repo.')

# Normalizações
if 'Data' in df.columns:
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
if 'Dias_para_vencer' in df.columns:
    df['Dias_para_vencer'] = pd.to_numeric(df['Dias_para_vencer'], errors='coerce')

# Calcula Data de Vencimento e Dias Restantes (dinâmico no dia do build)
if 'Data' in df.columns and 'Dias_para_vencer' in df.columns:
    df['Data Vencimento'] = df['Data'] + pd.to_timedelta(df['Dias_para_vencer'], unit='D')
    today = pd.to_datetime(date.today())
    df['Dias Restantes'] = (df['Data Vencimento'] - today).dt.days
else:
    raise SystemExit('Colunas necessárias ausentes: Data e Dias_para_vencer')

# Status

def status(d):
    if pd.isna(d):
        return 'Indefinido'
    if d < 0:
        return 'Vencido'
    if d <= 30:
        return 'A vencer'
    return 'Dentro do prazo'


df['Status'] = df['Dias Restantes'].apply(status)

# KPIs
total_vencidos = int((df['Dias Restantes'] < 0).sum())
prox_30 = int(((df['Dias Restantes'] >= 0) & (df['Dias Restantes'] <= 30)).sum())
no_prazo = int((df['Dias Restantes'] > 30).sum())

# Gráfico principal
fig = px.bar(
    df,
    x='Colaborador', y='Dias Restantes', color='Treinamento',
    title='Dias Restantes por Colaborador e Treinamento',
    hover_data=['Data', 'Data Vencimento', 'Status']
)
fig.update_layout(barmode='group', xaxis_title='Colaborador', yaxis_title='Dias Restantes')

# HTML com KPIs + gráfico + tabela
kpi_html = f"""
<div class=\"kpis\">
  <div class=\"kpi kpi-red\">Vencidos<br><span>{total_vencidos}</span></div>
  <div class=\"kpi kpi-amber\">A vencer (&le;30d)<br><span>{prox_30}</span></div>
  <div class=\"kpi kpi-green\">Dentro do prazo<br><span>{no_prazo}</span></div>
</div>
"""

table_cols = ['Colaborador','Treinamento','Data','Data Vencimento','Dias Restantes','Status']
html_table = df[table_cols].sort_values(['Status','Dias Restantes']).to_html(index=False, classes='data-table')

full_html = f"""<!DOCTYPE html>
<html lang=\"pt-BR\">
<head>
  <meta charset=\"utf-8\"/>
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"/>
  <title>Dashboard de Treinamentos</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 20px; }}
    h1 {{ margin-bottom: 0; }}
    .subtitle {{ color: #555; margin-top: 4px; }}
    .kpis {{ display: flex; gap: 12px; margin: 16px 0; flex-wrap: wrap; }}
    .kpi {{ padding: 12px 16px; border-radius: 8px; color: #fff; font-weight: bold; min-width: 180px; }}
    .kpi span {{ font-size: 24px; display: block; margin-top: 4px; }}
    .kpi-red {{ background: #d84a4a; }}
    .kpi-amber {{ background: #e0a800; }}
    .kpi-green {{ background: #2e7d32; }}
    .data-table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
    .data-table th, .data-table td {{ border: 1px solid #ddd; padding: 8px; }}
    .data-table th {{ background: #f5f5f5; }}
  </style>
</head>
<body>
  <h1>Dashboard de Treinamentos</h1>
  <div class=\"subtitle\">Atualizado em {date.today().isoformat()}</div>
  {kpi_html}
  {fig.to_html(full_html=False, include_plotlyjs='cdn')}
  <h2>Detalhamento</h2>
  {html_table}
</body>
</html>
"""

with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(full_html)

print('Gerado:', OUTPUT_HTML)
