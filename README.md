# 📊 TOTALE INDICADORES

## Sistema de Gestão de Produção, Indicadores e Performance Operacional

O **Totale Indicadores** é uma plataforma desenvolvida em Python e Streamlit para monitoramento em tempo real da produção, acompanhamento de indicadores operacionais (KPIs), gestão de desempenho de equipes e gamificação através de rankings e pontuações.

O sistema transforma dados operacionais em informações estratégicas, permitindo que gestores e supervisores acompanhem resultados, identifiquem gargalos e tomem decisões baseadas em dados.

---

## 🎯 Objetivos

* Monitorar a produção em tempo real
* Acompanhar indicadores de desempenho
* Avaliar produtividade individual e por equipe
* Controlar metas operacionais
* Medir eficiência operacional
* Gerenciar SLA e qualidade
* Estimular engajamento através de ranking
* Apoiar decisões gerenciais e estratégicas

---

# 🏗️ Arquitetura da Solução

```text
Google Sheets / Excel / Banco de Dados
                    │
                    ▼
            Tratamento dos Dados
               (Pandas)
                    │
                    ▼
          Cálculo dos Indicadores
                    │
                    ▼
              Visualizações
                (Plotly)
                    │
                    ▼
             Aplicação Streamlit
                    │
                    ▼
                  Usuário
```

A aplicação utiliza componentes de dashboard modernos, KPIs em destaque e gráficos interativos para acompanhamento da operação. O Streamlit fornece suporte nativo para exibição de métricas, painéis e indicadores executivos.

---

# 📈 Painel de Produção

## Objetivo

Apresentar o desempenho operacional da produção em tempo real.

---

## Indicadores Principais

### Produção Realizada

Quantidade total produzida no período selecionado.

```python
Produção Realizada = Total de OS Concluídas
```

---

### Meta de Produção

Quantidade planejada para o período.

```python
Meta = Produção Planejada
```

---

### Atingimento da Meta

Percentual atingido em relação à meta definida.

```python
Atingimento (%) =
(Produção Realizada / Meta) * 100
```

---

### Produção por Equipe

Permite identificar quais equipes possuem maior volume produtivo.

---

### Produção por Técnico

Permite analisar a produtividade individual.

---

## Visualizações

* Produção diária
* Produção semanal
* Produção mensal
* Produção acumulada
* Produção por região
* Produção por equipe
* Produção por técnico

---

# ⚡ Painel de Eficiência

## Objetivo

Avaliar a utilização dos recursos disponíveis.

---

## Indicadores

### Eficiência Operacional

```python
Eficiência =
(Horas Produtivas / Horas Disponíveis) * 100
```

---

### Produtividade

```python
Produtividade =
Produção / Horas Trabalhadas
```

---

### Tempo Médio de Execução

```python
Tempo Médio =
Tempo Total / Quantidade de Serviços
```

---

## Classificação

| Faixa         | Status    |
| ------------- | --------- |
| Acima de 90%  | Excelente |
| 80% a 89%     | Muito Bom |
| 70% a 79%     | Atenção   |
| Abaixo de 70% | Crítico   |

---

# 🎯 Painel de Metas

## Objetivo

Acompanhar o desempenho das equipes em relação aos objetivos definidos.

---

## Indicadores

### Meta Planejada

Meta definida para o período.

### Realizado

Produção efetivamente executada.

### Desvio

```python
Desvio = Realizado - Meta
```

### Percentual de Entrega

```python
Entrega (%) =
(Realizado / Meta) * 100
```

---

## Recursos

* Comparativo Meta x Realizado
* Evolução diária
* Evolução mensal
* Histórico de metas

---

# ⭐ Painel de Qualidade

## Objetivo

Monitorar falhas operacionais e garantir excelência na execução.

---

## Indicadores

### Retrabalho

```python
Retrabalho (%) =
(Retrabalhos / Produção Total) * 100
```

---

### Refugo

```python
Refugo (%) =
(Refugos / Produção Total) * 100
```

---

### Índice de Qualidade

```python
Qualidade (%) =
(Serviços Aprovados / Produção Total) * 100
```

---

## Visualizações

* Pareto de ocorrências
* Ranking de falhas
* Evolução mensal
* Comparativo por equipe

---

# ⏰ Painel de SLA

## Objetivo

Monitorar o cumprimento dos prazos operacionais.

---

## Indicadores

### SLA Cumprido

```python
SLA (%) =
(OS no Prazo / Total de OS) * 100
```

---

### SLA Atrasado

```python
Atraso (%) =
(OS Atrasadas / Total de OS) * 100
```

---

### Tempo Médio de Atendimento

```python
TMA =
Tempo Total / Quantidade de OS
```

---

# 🏆 Painel de Ranking

## Objetivo

Promover reconhecimento e engajamento através de gamificação.

---

## Sistema de Pontuação

### Meta Entregue

```python
+100 Pontos
```

### Eficiência Superior a 90%

```python
+50 Pontos
```

### Qualidade Superior

```python
+30 Pontos
```

### SLA Cumprido

```python
+20 Pontos
```

### Atrasos

```python
-20 Pontos
```

### Retrabalho

```python
-10 Pontos
```

---

## Pódio

🥇 Primeiro Lugar

🥈 Segundo Lugar

🥉 Terceiro Lugar

---

## Indicadores do Ranking

* Pontuação Total
* Evolução no Ranking
* Ranking Mensal
* Ranking Anual
* Destaque do Mês

---

# 👨‍🔧 Painel de Técnicos

## Objetivo

Analisar desempenho individual.

---

## Indicadores

* Produção Individual
* Eficiência
* Qualidade
* SLA
* Retrabalho
* Pontuação
* Ranking

---

## Visualizações

* Histórico de Produção
* Evolução de Performance
* Comparativo entre Técnicos
* Ranking Individual

---

# 📊 Painel Executivo

## Objetivo

Fornecer uma visão consolidada para supervisores, coordenadores e diretoria.

---

## KPIs Estratégicos

* Produção Total
* Meta Global
* Eficiência Média
* SLA Geral
* Qualidade
* Ranking das Equipes
* Técnicos Destaque
* Tendência de Produção

---

## Recursos

* Filtros Dinâmicos
* Drill Down
* Exportação Excel
* Exportação CSV
* Atualização Automática
* Responsividade

---

# 📂 Estrutura do Projeto

```text
totale-indicadores/
│
├── streamlit_app.py
├── pages/
│   ├── producao.py
│   ├── indicadores.py
│   ├── ranking.py
│   ├── qualidade.py
│   ├── sla.py
│   └── tecnicos.py
│
├── data/
├── images/
├── utils/
├── requirements.txt
└── README.md
```

---

# 🛠️ Tecnologias Utilizadas

* Python 3.10+
* Streamlit
* Pandas
* NumPy
* Plotly
* OpenPyXL
* Google Sheets API

---

# 🚀 Funcionalidades Futuras

* Integração com Power BI
* Banco de Dados SQL Server
* PostgreSQL
* Alertas Automáticos
* Envio de Relatórios por E-mail
* Inteligência Artificial para Previsões
* Dashboard Mobile
* Aplicativo Android/iOS

---

# 📌 Benefícios

✅ Gestão baseada em indicadores

✅ Monitoramento em tempo real

✅ Aumento da produtividade

✅ Controle operacional

✅ Transparência dos resultados

✅ Engajamento das equipes

✅ Melhoria contínua

---

**Desenvolvido por Denis Vick**
**Totale Indicadores © 2026**
Sistema de Gestão de Produção, Indicadores e Performance Operacional.