# Mega Repositório / Fonte Unificada para Hydra Launcher

Mega repositório consolidado e sanitizado de acordo com o esquema oficial do **Hydra Launcher**.

---

## 🔗 URL Oficial (Testada e Aprovada)

Copie e cole a seguinte URL em **Configurações > Fontes de Download** no Hydra Launcher:

```text
https://raw.githubusercontent.com/marcelotavs1/hydra-mega-source/main/mega_source.json
```

---

## ⚙️ Por que a versão anterior falhou?

1. **Esquema Estrito do Servidor do Hydra:** Cada download precisa ter exatamente os campos `title`, `uris` (mínimo 1 link válido), `uploadDate` e `fileSize`. Metadados extras pesados (requisitos de sistema, trailers, sinopses) que vinham em certas fontes eram rejeitados pelo validador da API.
2. **Timeout por Tamanho:** Arquivos acima de 100 MB causam timeout no servidor central do Hydra durante o download para validação.
3. **Redirecionamento temporário de Releases:** Links de GitHub Releases geram links temporários assinados da Azure Storage com expiração de minutos, enquanto links do `raw.githubusercontent.com` são diretos e permanentes.
