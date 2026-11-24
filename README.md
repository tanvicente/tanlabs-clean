# Tanlabs Clean

Skill própria da **Tanlabs** para limpar caracteres invisíveis e espaços especiais em textos, preservando acentos, parágrafos e emojis. Inclui um utilitário Python local e instruções para revisão editorial opcional no assistente.

**[Usar o editor web](https://tanlabs.com.br/clean/)** · **[Ler a skill](skills/tanlabs-clean/SKILL.md)** · **[Baixar a skill](https://github.com/tanvicente/tanlabs-clean/releases/latest/download/tanlabs-clean.zip)**

## Usar em um assistente

Baixe `tanlabs-clean.zip` na seção Releases. O pacote contém a pasta `tanlabs-clean/`, com `SKILL.md`, metadados, licença e script. Importe-o pela função de skills do seu assistente, quando disponível. Para ambientes que usam uma pasta local de skills, copie a pasta extraída para o diretório de skills desse ambiente.

Em instalações locais do Codex, a pasta pode ser colocada em `~/.agents/skills/tanlabs-clean/`. Em Claude Code, em `~/.claude/skills/tanlabs-clean/`. O ambiente precisa conseguir ler a skill e executar Python. O suporte a instalação, importação e execução varia por produto e conta; colar um link por si só não instala uma skill.

Após a instalação, solicite:

```text
Use a skill tanlabs-clean para limpar os caracteres invisíveis do texto abaixo.
Preserve o conteúdo e informe as alterações verificadas.

[COLE SEU TEXTO]
```

No Codex, você também pode invocar `$tanlabs-clean`. Para melhorar a redação, peça explicitamente uma revisão editorial, preservando fatos e sentido.

## Usar diretamente no terminal

Requer **Python 3.9+**. Não precisa de `pip`, API, modelo, serviço HTTP ou conexão de rede durante a limpeza.

```sh
git clone https://github.com/tanvicente/tanlabs-clean.git
cd tanlabs-clean
python3 skills/tanlabs-clean/scripts/clean_text.py entrada.txt --inspect
python3 skills/tanlabs-clean/scripts/clean_text.py entrada.txt -o texto-limpo.txt --report relatorio.json
```

O utilitário aceita TXT/Markdown em UTF-8 ou `-` para stdin. Nunca sobrescreve arquivos existentes. A saída padrão contém o texto limpo; o resumo vai para stderr. `--inspect` exibe apenas JSON. O relatório inclui códigos, quantidades e ações, sem o conteúdo da prosa.

| Opção | Efeito |
|---|---|
| `--keep-invisible` | Preserva os invisíveis inspecionados |
| `--keep-spaces` | Preserva espaços especiais |
| `--remove-bidi` | Remove controles direcionais; pode afetar árabe/hebraico |
| `--plain-punctuation` | Converte aspas curvas, traços e reticências |
| `--report arquivo.json` | Grava um novo relatório JSON |

Por padrão, preserva ZWJ/ZWNJ, seletores de variação, sequências emoji, quebras de linha e grafemas combinados. Não aplica NFC/NFKC. Limite de 2 MB e 500 mil unidades UTF-16. Arquivos binários, PDF, DOCX e codificações inválidas são recusados. A ferramenta destina-se a prosa; alguns invisíveis são legítimos em fórmulas e idiomas, então revise as opções antes de usá-la.

## Limites e privacidade

A limpeza não identifica autoria por IA e não verifica nem garante a remoção de marcas estatísticas como textGrain ou SynthID. A revisão editorial é feita pelo assistente que você escolher, quando solicitada; não é uma função do utilitário Python. Não há serviço de detecção embutido.

O script não faz requisições de rede ou telemetria e lê apenas a entrada indicada. Quando usado dentro de um assistente, o conteúdo continua sujeito às regras e condições daquele ambiente.

## Testes

```sh
python3 -m unittest discover -s tests -v
```

Código e instruções sob licença MIT. © 2026 Tanlabs.
