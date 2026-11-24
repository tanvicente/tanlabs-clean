# Casos de aceitação da revisão de estilo

Estes casos servem para revisão manual do comportamento de um assistente usando a skill. Não são testes automatizados de equivalência semântica nem de detectores. A redação exata da saída pode variar.

## Condição, negação e grau de certeza

Pedido: reduzir sinais de IA sem alterar sentido ou contexto.

> É importante ressaltar que o plano Tanlabs Pro custa R$ 149,90 por mês. Além disso, não inclui suporte aos domingos. O prazo pode chegar a 5 dias úteis se o cliente não enviar os documentos até 12/12/2026.

Aceitar apenas revisões que mantenham nome, preço, frequência, ausência de suporte aos domingos, possibilidade (não certeza) do prazo de 5 dias úteis e sua condição exata. Não converter o prazo em garantia nem mudar quem deve enviar os documentos.

## Voz e intenção

> Eu não gostei da proposta. Talvez a gente consiga conversar amanhã, mas não prometo fechar o contrato.

Preservar primeira pessoa, discordância, incerteza e ausência de compromisso. Se já estiver natural, manter. Não acrescentar agradecimentos, entusiasmo ou promessa de negociação.

## Citação e limites de escopo

> Segundo o relatório, houve melhora em 18% dos casos analisados. A frase publicada foi: “Não há evidência suficiente para generalizar o resultado”.

Preservar percentual, restrição aos casos analisados, atribuição e citação literal. Não afirmar melhora de 18% na intensidade do resultado nem ampliar a conclusão para todos os casos.

## Limpeza técnica solicitada isoladamente

Pedido: somente limpar caracteres, sem reescrever.

Entrada representada com escapes: `Ação\u00a0com\u200b café.\n👩🏽‍💻 preservada.`

Saída esperada: `Ação com café.\n👩🏽‍💻 preservada.` Sem troca de palavras. Este comportamento também é coberto pelos testes Python.

## Texto ambíguo

> Entregaremos apenas os relatórios aprovados na sexta.

Manter a ambiguidade original ou pedir esclarecimento. Não decidir por conta própria se a aprovação ou a entrega acontece na sexta.
