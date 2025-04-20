# Documentação: Sistema de Cotações CEASA-ES para Wix

## Visão Geral

Este sistema foi desenvolvido para automatizar a obtenção de cotações do CEASA-ES (Centrais de Abastecimento do Espírito Santo) e disponibilizá-las em um formato que possa ser facilmente incorporado em um site Wix. O sistema consiste em um aplicativo web desenvolvido com Flask que acessa o site do CEASA-ES, extrai os dados de cotações e os disponibiliza em diferentes formatos (JSON e HTML).

## Componentes do Sistema

O sistema é composto pelos seguintes componentes:

1. **Aplicativo Flask (`app.py`)**: Servidor web que gerencia as requisições e fornece as cotações em diferentes formatos.
2. **Página Principal (`index.html`)**: Interface para visualização das cotações em um navegador.
3. **Página para Wix (`wix_embed.html`)**: Versão otimizada para incorporação em sites Wix.
4. **Template de iframe (`iframe_template.html`)**: Modelo para incorporação via iframe.

## Funcionalidades

O sistema oferece as seguintes funcionalidades:

1. **Obtenção automática de cotações**: Acessa o site do CEASA-ES, seleciona o mercado (CEASA GRANDE VITÓRIA) e a data mais recente disponível, e extrai os dados da tabela de cotações.
2. **API JSON**: Fornece os dados em formato JSON através da rota `/api/cotacoes`.
3. **Tabela HTML**: Fornece uma tabela HTML formatada através da rota `/api/tabela-html`.
4. **Página para Wix**: Fornece uma página HTML otimizada para incorporação em sites Wix através da rota `/wix`.
5. **Template de iframe**: Fornece um modelo de iframe para incorporação em sites através da rota `/iframe`.

## Limitações Conhecidas

Durante os testes, foram identificadas as seguintes limitações:

1. **Acesso ao site do CEASA-ES**: O aplicativo pode enfrentar dificuldades para acessar o site do CEASA-ES em determinados ambientes devido a restrições de rede ou políticas de segurança. Nestes casos, o sistema exibirá uma mensagem de erro.
2. **Dados de exemplo**: A página para Wix (`/wix`) atualmente exibe dados de exemplo para demonstração. Em um ambiente de produção, estes dados seriam substituídos pelos dados reais obtidos do CEASA-ES.
3. **Template de iframe**: O template de iframe (`/iframe`) requer que a URL do serviço seja substituída pela URL real do serviço hospedado.

## Instalação e Execução

Para instalar e executar o sistema, siga os passos abaixo:

1. Certifique-se de ter Python 3.6 ou superior instalado.
2. Instale as dependências necessárias:
   ```
   pip install flask requests beautifulsoup4 pandas
   ```
3. Execute o aplicativo Flask:
   ```
   python app.py
   ```
4. O aplicativo estará disponível em `http://localhost:5000`.

## Incorporação no Wix

Para incorporar as cotações do CEASA-ES em um site Wix, siga os passos abaixo:

1. **Usando HTML Embed**:
   - No editor do Wix, adicione um elemento "HTML Embed".
   - Cole o código HTML abaixo, substituindo `URL_DO_SERVICO` pela URL real do serviço hospedado:
     ```html
     <iframe src="URL_DO_SERVICO/wix" width="100%" height="500" frameborder="0"></iframe>
     ```

2. **Usando iframe**:
   - No editor do Wix, adicione um elemento "iframe".
   - Configure o iframe com a URL do serviço hospedado seguida de `/wix`.
   - Ajuste a largura e altura conforme necessário.

## Personalização

O sistema pode ser personalizado de várias formas:

1. **Estilo da tabela**: O estilo da tabela pode ser modificado editando o CSS nas páginas HTML.
2. **Dados exibidos**: Os campos exibidos na tabela podem ser modificados editando o código JavaScript nas páginas HTML.
3. **Mercado**: Por padrão, o sistema obtém cotações do CEASA GRANDE VITÓRIA (ID 211). Para mudar o mercado, modifique o parâmetro `mercado_id` na função `obter_cotacoes_ceasa` no arquivo `app.py`.

## Solução de Problemas

Se você encontrar problemas ao usar o sistema, verifique os seguintes pontos:

1. **Erro ao carregar cotações**: Verifique se o serviço está sendo executado e se tem acesso à internet. O site do CEASA-ES pode estar temporariamente indisponível ou ter mudado sua estrutura.
2. **Iframe não carrega**: Verifique se a URL do serviço está correta e se o serviço está em execução. Certifique-se de que o site Wix permite a incorporação de iframes externos.
3. **Dados desatualizados**: O sistema obtém os dados mais recentes disponíveis no site do CEASA-ES. Se os dados parecerem desatualizados, verifique se o site do CEASA-ES foi atualizado recentemente.

## Considerações para Produção

Para usar este sistema em um ambiente de produção, considere os seguintes pontos:

1. **Hospedagem**: O aplicativo Flask deve ser hospedado em um servidor web com suporte a Python. Opções incluem Heroku, PythonAnywhere, AWS, Google Cloud, etc.
2. **HTTPS**: O Wix requer que todos os recursos externos usem HTTPS. Certifique-se de que o serviço hospedado suporte HTTPS.
3. **Agendamento**: Para garantir que os dados estejam sempre atualizados, considere implementar um sistema de agendamento que atualize os dados periodicamente.
4. **Cache**: Para melhorar o desempenho e reduzir a carga no site do CEASA-ES, considere implementar um sistema de cache que armazene os dados por um período determinado.

## Próximos Passos

Para melhorar o sistema, considere as seguintes melhorias:

1. **Implementar cache**: Armazenar os dados obtidos por um período determinado para reduzir a carga no site do CEASA-ES.
2. **Adicionar autenticação**: Proteger o acesso à API com autenticação para evitar uso não autorizado.
3. **Melhorar tratamento de erros**: Implementar um sistema mais robusto de tratamento de erros para lidar com diferentes cenários de falha.
4. **Adicionar filtros**: Permitir que o usuário filtre os dados por produto, preço, etc.
5. **Implementar histórico**: Armazenar dados históricos para permitir a visualização de tendências de preços ao longo do tempo.
