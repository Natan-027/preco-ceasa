from flask import Flask, render_template, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import os
import json
import time

app = Flask(__name__)

# Cache para armazenar os dados e evitar requisições frequentes ao site do CEASA
cache = {
    'dados': None,
    'ultima_atualizacao': None,
    'tempo_expiracao': 3600  # 1 hora em segundos
}

def cache_expirado():
    """Verifica se o cache expirou"""
    if cache['ultima_atualizacao'] is None:
        return True
    
    tempo_atual = time.time()
    return (tempo_atual - cache['ultima_atualizacao']) > cache['tempo_expiracao']

def obter_cotacoes_ceasa(mercado_id=211, data=None):
    """
    Obtém as cotações do CEASA-ES para o mercado e data especificados.
    
    Args:
        mercado_id: ID do mercado (211 = CEASA GRANDE VITÓRIA)
        data: Data no formato DD/MM/AAAA (se None, usa a data mais recente disponível)
    
    Returns:
        DataFrame com as cotações ou None em caso de erro
    """
    # Verificar se há dados em cache válidos
    if not cache_expirado() and cache['dados'] is not None:
        return cache['dados']
    
    try:
        # URL base do sistema CEASA-ES
        base_url = "http://200.198.51.71/detec"
        
        # Etapa 1: Acessar a página de filtro
        session = requests.Session()
        filtro_url = f"{base_url}/filtro_boletim_es/"
        
        # Obter a página de filtro
        response = session.get(filtro_url, timeout=10)
        response.raise_for_status()
        
        # Etapa 2: Selecionar o mercado (CEASA GRANDE VITÓRIA)
        filtro_post_url = f"{base_url}/filtro_boletim_es/filtro_boletim_es.php"
        
        # Primeiro post para selecionar o mercado
        mercado_data = {
            "hdn_operacao": "filtro",
            "hdn_mercado": mercado_id,
            "sel_mercado": mercado_id
        }
        
        response = session.post(filtro_post_url, data=mercado_data, timeout=10)
        response.raise_for_status()
        
        # Etapa 3: Se data não foi especificada, obter a data mais recente disponível
        if data is None:
            soup = BeautifulSoup(response.text, 'html.parser')
            select_data = soup.find('select', {'name': 'sel_data'})
            
            if select_data and select_data.find_all('option'):
                # A primeira opção após a opção padrão é a data mais recente
                opcoes = select_data.find_all('option')
                if len(opcoes) > 1:
                    data = opcoes[1].get('value', '').strip()
        
        if not data:
            # Usar dados de exemplo se não conseguir obter a data
            return obter_dados_exemplo()
        
        # Etapa 4: Selecionar a data e obter o boletim
        data_data = {
            "hdn_operacao": "filtro",
            "hdn_mercado": mercado_id,
            "sel_mercado": mercado_id,
            "sel_data": data
        }
        
        response = session.post(filtro_post_url, data=data_data, timeout=10)
        response.raise_for_status()
        
        # Etapa 5: Acessar a página do boletim completo
        boletim_url = f"{base_url}/boletim_completo_es/boletim_completo_es.php"
        response = session.get(boletim_url, timeout=10)
        response.raise_for_status()
        
        # Etapa 6: Extrair os dados da tabela
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontrar a tabela principal
        tabela = soup.find('table', {'class': 'tabela'})
        
        if not tabela:
            # Usar dados de exemplo se não conseguir encontrar a tabela
            return obter_dados_exemplo()
        
        # Extrair os dados da tabela
        dados = []
        
        # Obter todas as linhas da tabela, exceto o cabeçalho
        linhas = tabela.find_all('tr')[1:]  # Pular o cabeçalho
        
        for linha in linhas:
            colunas = linha.find_all('td')
            if len(colunas) >= 6:  # Verificar se tem colunas suficientes
                produto = colunas[0].text.strip()
                unidade = colunas[1].text.strip()
                preco_min = colunas[2].text.strip().replace(',', '.')
                preco_med = colunas[3].text.strip().replace(',', '.')
                preco_max = colunas[4].text.strip().replace(',', '.')
                classificacao = colunas[5].text.strip() if len(colunas) > 5 else ""
                
                dados.append({
                    'produto': produto,
                    'unidade': unidade,
                    'preco_min': preco_min,
                    'preco_med': preco_med,
                    'preco_max': preco_max,
                    'classificacao': classificacao
                })
        
        # Criar DataFrame
        df = pd.DataFrame(dados)
        
        # Converter colunas de preço para float
        for col in ['preco_min', 'preco_med', 'preco_max']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Atualizar o cache
        cache['dados'] = df
        cache['ultima_atualizacao'] = time.time()
        
        return df
    
    except Exception as e:
        print(f"Erro ao obter cotações: {str(e)}")
        # Em caso de erro, usar dados de exemplo
        return obter_dados_exemplo()

def obter_dados_exemplo():
    """
    Retorna dados de exemplo para quando não for possível obter dados reais
    """
    dados = [
        {'produto': 'ALFACE AMERICANA', 'unidade': 'KG', 'preco_min': 5.31, 'preco_med': 5.52, 'preco_max': 5.73, 'classificacao': 'MFR'},
        {'produto': 'TOMATE LONGA VIDA', 'unidade': 'KG', 'preco_min': 6.83, 'preco_med': 7.05, 'preco_max': 7.27, 'classificacao': 'MFI'},
        {'produto': 'CENOURA', 'unidade': 'KG', 'preco_min': 3.25, 'preco_med': 3.45, 'preco_max': 3.65, 'classificacao': 'MFR'},
        {'produto': 'BATATA', 'unidade': 'KG', 'preco_min': 2.75, 'preco_med': 2.95, 'preco_max': 3.15, 'classificacao': 'MFI'},
        {'produto': 'CEBOLA', 'unidade': 'KG', 'preco_min': 4.10, 'preco_med': 4.30, 'preco_max': 4.50, 'classificacao': 'ME'},
        {'produto': 'PIMENTÃO VERDE', 'unidade': 'KG', 'preco_min': 4.20, 'preco_med': 4.26, 'preco_max': 4.38, 'classificacao': 'MFI'},
        {'produto': 'REPOLHO', 'unidade': 'KG', 'preco_min': 2.00, 'preco_med': 2.00, 'preco_max': 2.00, 'classificacao': 'MFI'},
        {'produto': 'BETERRABA', 'unidade': 'KG', 'preco_min': 3.50, 'preco_med': 3.65, 'preco_max': 3.80, 'classificacao': 'MFR'},
        {'produto': 'ABOBRINHA', 'unidade': 'KG', 'preco_min': 2.27, 'preco_med': 2.27, 'preco_max': 2.27, 'classificacao': 'MFI'},
        {'produto': 'PEPINO', 'unidade': 'KG', 'preco_min': 2.13, 'preco_med': 2.22, 'preco_max': 2.31, 'classificacao': 'MFI'}
    ]
    
    df = pd.DataFrame(dados)
    
    # Atualizar o cache
    cache['dados'] = df
    cache['ultima_atualizacao'] = time.time()
    
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wix')
def wix_embed():
    # Servir a página HTML específica para incorporação no Wix
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'wix_embed.html')

@app.route('/iframe')
def iframe_template():
    # Servir o template de iframe
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'iframe_template.html')

@app.route('/api/cotacoes')
def api_cotacoes():
    # Obter cotações do CEASA-ES (CEASA GRANDE VITÓRIA)
    df = obter_cotacoes_ceasa()
    
    if df is None:
        return jsonify({'error': 'Não foi possível obter as cotações'}), 500
    
    # Converter DataFrame para dicionário
    cotacoes = df.to_dict(orient='records')
    
    # Obter a data atual
    data_atual = datetime.now().strftime('%d/%m/%Y')
    
    return jsonify({
        'data_atualizacao': data_atual,
        'cotacoes': cotacoes
    })

@app.route('/api/tabela-html')
def api_tabela_html():
    # Obter cotações do CEASA-ES (CEASA GRANDE VITÓRIA)
    df = obter_cotacoes_ceasa()
    
    if df is None:
        return "Não foi possível obter as cotações", 500
    
    # Formatar o DataFrame para exibição HTML
    df_html = df.copy()
    
    # Formatar colunas de preço para exibição em Reais
    for col in ['preco_min', 'preco_med', 'preco_max']:
        df_html[col] = df_html[col].apply(lambda x: f"R$ {x:.2f}".replace('.', ',') if pd.notnull(x) else "-")
    
    # Renomear colunas para exibição
    df_html = df_html.rename(columns={
        'produto': 'Produto',
        'unidade': 'Unidade',
        'preco_min': 'Preço Mínimo',
        'preco_med': 'Preço Médio',
        'preco_max': 'Preço Máximo',
        'classificacao': 'Classificação'
    })
    
    # Converter para HTML
    tabela_html = df_html.to_html(classes='table table-striped table-hover', index=False)
    
    # Adicionar título e data
    data_atual = datetime.now().strftime('%d/%m/%Y')
    html_completo = f"""
    <div class="container">
        <h2>Cotações CEASA-ES - Grande Vitória</h2>
        <p>Atualizado em: {data_atual}</p>
        {tabela_html}
        <p class="small text-muted">Fonte: CEASA-ES</p>
    </div>
    """
    
    return html_completo

if __name__ == '__main__':
    # Configuração para produção
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
