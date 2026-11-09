# Mega Repositório / Fonte Unificada para Hydra Launcher

Este repositório consolida 36 fontes públicas do Hydra Launcher em uma única fonte mestre com **555.280 downloads desduplicados**.

---

## 📊 Estatísticas da Compilação

- **Total de fontes consultadas:** 36
- **Fontes obtidas com sucesso:** 33
- **Downloads brutos encontrados:** 570.770
- **Downloads únicos consolidados:** 555.280
- **Arquivos gerados:**
  - `mega_source.json` (~364 MB, formatado com indentação)
  - `mega_source.min.json` (~318 MB, minificado para carregamento mais leve)
  - `summary.json` (relatório de status de cada fonte)

---

## 🚀 Como Usar no Hydra Launcher

### Opção 1: Servidor Local (Uso imediato no seu PC)

Como o arquivo consolidado tem ~318 MB, você pode rodá-lo localmente na sua máquina:

1. Abra o terminal nesta pasta:
   ```powershell
   cd C:\Users\marce\.gemini\antigravity\scratch\hydra-mega-source
   python -m http.server 8080
   ```
2. No Hydra Launcher:
   - Vá em **Configurações** > **Fontes de Download** (Sources).
   - Adicione a URL:
     ```
     http://localhost:8080/mega_source.min.json
     ```

---

### Opção 2: Hospedar na Web (GitHub Releases / Cloudflare Pages)

Devido ao limite de 100 MB para arquivos normais em commits do GitHub:
- **GitHub Releases:** Crie um repositório no GitHub, crie uma "Release" (ex: `v1.0.0`) e faça o upload do `mega_source.min.json` como asset anexado. A URL direta da release poderá ser inserida no Hydra Launcher.
- **Cloudflare Pages / R2 / Pastebin grande:** Você pode hospedar o arquivo em um bucket R2 gratuito com link público.

---

## 🔄 Como Atualizar a Mega Fonte

Para baixar novamente todas as fontes e gerar uma nova versão atualizada:

```powershell
python build_mega_repo.py
```
