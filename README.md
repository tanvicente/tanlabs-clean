# Tanlabs Clean

Skill própria da **Tanlabs** para reduzir padrões de escrita associados à IA, preservando sentido, contexto, fatos e intenção. Combina revisão conservadora no assistente com limpeza técnica de caracteres e espaços. Não garante eliminar todos os sinais de IA nem aprovação em detectores.

**[Usar o editor web](https://tanlabs.com.br/clean/)** · **[Ler a skill](skills/tanlabs-clean/SKILL.md)** · **[Baixar a skill](https://github.com/tanvicente/tanlabs-clean/releases/latest/download/tanlabs-clean.zip)**

## Usar em um assistente

Baixe `tanlabs-clean.zip` na seção Releases. O pacote contém a pasta `tanlabs-clean/`, com `SKILL.md`, metadados, licença e script. Importe-o pela função de skills do seu assistente, quando disponível. Para ambientes que usam uma pasta local de skills, copie a pasta extraída para o diretório de skills desse ambiente.

Em instalações locais do Codex, a pasta pode ser colocada em `~/.agents/skills/tanlabs-clean/`. Em Claude Code, em `~/.claude/skills/tanlabs-clean/`. A revisão de estilo acontece no assistente. Para a limpeza técnica automática, o ambiente também precisa executar Python 3.9+. O suporte a instalação, importação e execução varia por produto e conta; colar um link por si só não instala uma skill.

Após a instalação, solicite:

```text
Use a skill tanlabs-clean para reduzir os sinais de escrita por IA no texto abaixo.
Preserve o sentido, o contexto, a intenção, os fatos, os nomes, os números e as ressalvas.
Faça apenas mudanças necessárias e não acrescente informações.

[COLE SEU TEXTO]
```

No Codex, você também pode invocar `$tanlabs-clean`. Se quiser manter todas as palavras, peça **somente limpeza técnica, sem reescrever**. O script de terminal faz apenas essa limpeza; a revisão de estilo é feita pelo assistente.

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

A skill não identifica autoria por IA, não verifica marcas estatísticas e não garante aprovação em detectores. A revisão busca reduzir repetições e fórmulas de escrita quando presentes. Não usa sinônimos de forma mecânica, não cria experiências pessoais e não modifica fatos, negações, condições ou compromissos. Se uma mudança puder afetar o sentido, a orientação é preservar o trecho. Não há verificador automático de equivalência semântica nem serviço de detecção embutido.

O script não faz requisições de rede ou telemetria e lê apenas a entrada indicada. Quando usado dentro de um assistente, o conteúdo continua sujeito às regras e condições daquele ambiente.

## Testes

```sh
python3 -m unittest discover -s tests -v
```

Os [casos de aceitação da revisão](tests/review-cases.md) orientam a avaliação manual de preservação de sentido. Eles não comprovam equivalência semântica automática.

Código e instruções sob licença MIT. © 2026 Tanlabs.
