# Mega Repositório / Fonte Unificada para Hydra Launcher

Repositório oficial gerado com **555.280 downloads únicos consolidados** a partir de 33 fontes públicas do Hydra Launcher.

---

## 🔗 URL para Adicionar no Hydra Launcher

Copie e cole a seguinte URL nas **Configurações > Fontes de Download** do seu Hydra Launcher:

```text
https://github.com/marcelotavs1/hydra-mega-source/releases/download/v1.0.0/mega_source.min.json
```

---

## 📊 Estatísticas da Compilação

- **Fontes analisadas:** 36
- **Fontes ativas com sucesso:** 33
- **Downloads brutos:** 570.770
- **Downloads únicos após deduplicação:** 555.280
- **Tamanho do arquivo:** ~318 MB (`mega_source.min.json`)

---

## 🔄 Como Atualizar a Base

Para sincronizar novas versões das fontes e gerar uma nova release:

1. Execute o script de compilação:
   ```powershell
   python build_mega_repo.py
   ```
2. Crie uma nova tag/release no GitHub:
   ```powershell
   gh release create v1.0.1 mega_source.min.json --title "Mega Hydra Source v1.0.1"
   ```
