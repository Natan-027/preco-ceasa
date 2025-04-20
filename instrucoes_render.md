# Instruções para Implantação no Render.com

Este guia explica como implantar a aplicação de cotações do CEASA-ES no Render.com, um serviço de hospedagem gratuito que permite que a aplicação seja acessada online sem necessidade de instalação local.

## Passos para Implantação

1. Crie uma conta no [Render.com](https://render.com/) (é gratuito)

2. Após fazer login, clique em "New +" e selecione "Web Service"

3. Conecte sua conta do GitHub ou faça upload do código diretamente:
   - Se usar GitHub, primeiro crie um repositório e faça upload dos arquivos
   - Ou use a opção "Upload Files" para fazer upload direto

4. Configure o serviço:
   - **Nome**: ceasa-es-cotacoes (ou outro nome de sua preferência)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plano**: Free

5. Clique em "Create Web Service"

6. Aguarde a implantação (pode levar alguns minutos)

7. Após a implantação, o Render fornecerá uma URL (algo como https://ceasa-es-cotacoes.onrender.com)

## Incorporando no Wix

1. No editor do Wix, adicione um elemento "HTML Embed" ou "iframe"

2. Cole o seguinte código, substituindo `SUA_URL_DO_RENDER` pela URL fornecida pelo Render:
   ```html
   <iframe src="https://SUA_URL_DO_RENDER/wix" width="100%" height="500" frameborder="0"></iframe>
   ```

3. Ajuste a largura e altura conforme necessário para seu site

4. Salve e publique seu site Wix

## Observações Importantes

- O plano gratuito do Render coloca a aplicação em modo de espera após 15 minutos de inatividade
- Quando alguém acessa o site, a aplicação é reativada automaticamente (pode levar alguns segundos)
- Os dados são atualizados automaticamente sempre que o iframe é carregado
- O sistema inclui um cache para evitar requisições frequentes ao site do CEASA-ES
- Se o site do CEASA-ES estiver indisponível, a aplicação exibirá dados de exemplo

## Solução de Problemas

- Se o iframe não carregar, verifique se a URL do Render está correta
- Se os dados não aparecerem, pode ser que o serviço esteja iniciando após um período de inatividade (aguarde alguns segundos e recarregue a página)
- Para qualquer outro problema, verifique os logs no painel de controle do Render
