# CLAUDE.md — Regras do Projeto AVM (ALLEN)

Este ficheiro contém instruções permanentes para o Claude Code neste repositório.
Deves segui-las em **todas** as sessões, independentemente do que for pedido numa mensagem individual.

## Contexto do projeto

AVM (Assistente Virtual Multimodal / ALLEN) é um projeto de final de curso (Licenciatura em
Engenharia Informática, UCAN), desenvolvido individualmente. O código faz parte de um trabalho
académico que terá de ser explicado e defendido em arguição. Por isso, **clareza e capacidade de
explicação têm prioridade sobre elegância ou "cleverness" técnica**.

Arquitetura já validada — não alterar sem discutir primeiro:
- LangGraph `StateGraph` como motor de orquestração.
- Modalidades (voz, gesto, câmara) são **tools**, não nodes. Só ativam por comando explícito do
  utilizador.
- Saída de voz (Kokoro TTS) é tratada por um node determinístico `falar_resposta` antes do
  `__end__` — nunca é uma tool call decidida pelo LLM.
- Estrutura de implementação em quatro ficheiros: `state.py`, `tools.py`, `graph.py`, `main.py`.
- Princípio "efficiency-first": nada deve consumir recursos (CPU, memória, chamadas de modelo)
  desnecessariamente. Nenhum componente fica ativo por defeito.

## Regras obrigatórias de trabalho

1. **Explica antes de assumir.** Se uma implementação exigir uma decisão que não foi pedida
   explicitamente (nova dependência, padrão de design, abstração extra, tratamento de erros não
   solicitado, mudança de arquitetura), explica a razão e as alternativas **antes** de escrever o
   código, não depois.

2. **Prefere sempre a solução mais simples** que resolve o problema. Evita over-engineering,
   camadas de abstração desnecessárias, ou "flexibilidade para o futuro" que não foi pedida.

3. **Mudanças grandes precisam de plano primeiro.** Para qualquer alteração que toque mais do
   que uma função ou ficheiro, apresenta um plano curto (o que vai mudar e porquê) antes de
   aplicar. Não avances sem confirmação nesses casos.

4. **Diffs pequenos e explicáveis.** Prefere entregar funcionalidades em incrementos pequenos e
   testáveis em vez de grandes blocos de código de uma só vez. Cada incremento deve poder ser
   totalmente explicado numa frase ou duas.

5. **Após cada implementação, resume em português:**
   - O que foi feito.
   - Porque foi feito assim (especialmente se houve alguma decisão não-óbvia).
   - Qualquer desvio da arquitetura combinada (e porquê foi necessário, se foi).

6. **Não introduzir novas dependências, bibliotecas ou serviços externos** sem perguntar primeiro
   e justificar a necessidade face ao stack já definido (Python 3.11, Ollama/llama3.2, Whisper,
   MediaPipe Hands, DeepFace/FER, SQLite, APScheduler, Electron, Docker, Redis).

7. **Se algo não puder ser explicado de forma simples, é sinal de que está demasiado complexo.**
   Nesse caso, procura a alternativa mais direta antes de propor a solução.

## Como devo pedir esclarecimentos

Sempre que eu colar um trecho de código já implementado e pedir "explica isto", trata-o como se
eu fosse ter de defender essa parte numa arguição: explica o objetivo, o porquê da abordagem
escolhida, e quaisquer trade-offs relevantes — em português, de forma direta e sem jargão
desnecessário.