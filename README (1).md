
# Dashboard de Treinamentos (GitHub Pages)

Este repositório publica um dashboard estático (HTML) com Plotly no **GitHub Pages**, atualizado automaticamente por **GitHub Actions**.

## Como usar
1. Faça upload do arquivo **base_treinamentos_limpa.xlsx** na **raiz** do repositório (colunas: `Colaborador`, `Treinamento`, `Data`, `Dias_para_vencer`).
2. Confirme o workflow em `.github/workflows/build.yml`.
3. Vá em **Settings → Pages → Build and deployment → Source = GitHub Actions**.
4. Acesse a aba **Actions**, aguarde finalizar. A URL pública será `https://SEU-USUARIO.github.io/NOME-DO-REPO/`.

## Atualização automática
- Roda **diariamente** e **a cada push**.
- Recalcula **Dias Restantes** com base no dia do build.
