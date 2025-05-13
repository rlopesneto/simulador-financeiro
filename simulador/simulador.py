import streamlit as st
import numpy_financial as npf
from math import log

# === Funções ===

def calcular_valor_futuro(c0, r, t):
    return c0 * (1 + r)**t

def calcular_valor_atual(vf, r, t):
    return vf / (1 + r)**t

def calcular_val(v_inicial, fluxos, r):
    return sum(cf / (1 + r)**i for i, cf in enumerate(fluxos)) - v_inicial

def calcular_tir(fluxos):
    return npf.irr(fluxos)

def calcular_perpetuidade(c, r):
    return c / r

def calcular_perpetuidade_crescente(c1, r, g):
    return c1 / (r - g)

def calcular_anuidade_constante(c, r, t):
    return c * (1 - 1 / (1 + r)**t) / r

def calcular_anuidade_crescente(c1, r, g, t):
    return (c1 / (r - g)) * (1 - ((1 + g) / (1 + r))**t)

def calcular_payback_descontado(investimento, fluxos, r):
    acumulado = 0
    for i, cf in enumerate(fluxos):
        acumulado += cf / (1 + r)**i
        if acumulado >= investimento:
            anterior = sum(fluxos[j] / (1 + r)**j for j in range(i))
            restante = investimento - anterior
            fracao = restante / (fluxos[i] / (1 + r)**i)
            return i + fracao
    return float('inf')

def calcular_break_even_fluxo(investimento, r, t):
    return investimento * r / (1 - 1 / (1 + r)**t)

def calcular_break_even_quantidade(custo_fixo, preco_unit, custo_unit, r, t):
    fator = (1 - 1 / (1 + r)**t) / r
    return custo_fixo / ((preco_unit - custo_unit) * fator)

def calcular_tae(r, m):
    return (1 + r / m)**m - 1

def calcular_taxa_implicita(vf, c0, t):
    return (vf / c0)**(1 / t) - 1

def calcular_periodos(vf, c0, r):
    return log(vf / c0) / log(1 + r)

def calcular_racio_bc_fluxos(fluxos, investimento, r):
    valor_atual_beneficios = sum(cf / (1 + r)**i for i, cf in enumerate(fluxos))
    return valor_atual_beneficios / abs(investimento)

def calcular_racio_bc_final(va_beneficio_final, investimento):
    return va_beneficio_final / abs(investimento)

# === Interface Streamlit ===
st.title("Ferramenta de avaliação financeira")

with st.expander("Guia de Utilização"):
    st.markdown("""
    ### Parâmetros de Entrada

    | Campo | Descrição | Relacionado com |
    |-------|-------------|-------------------|
    | Investimento Inicial (€) | Valor aplicado no início do projeto (C0) | VAL, TIR, Payback, Break-even, Valor Futuro |
    | Taxa de Juro (%) | Taxa de desconto anual (r) | Valor Atual, VAL, Anuidades, TIR, TAE, Períodos, Break-even |
    | Nº Períodos (anos) | Tempo de duração do projeto (t) | Valor Futuro, VAL, Payback, Anuidades, Valor Atual, Break-even |
    | Valor Futuro Esperado (€) | Valor que se espera obter no futuro (VF) | Valor Atual, Taxa Implícita, Períodos |
    | Fluxo de Caixa Anual (€) | Receita constante anual prevista | VAL, TIR, Anuidades, Perpetuidades, Payback, Rácio B/C |
    | Taxa de Crescimento (%) | Taxa de crescimento anual dos fluxos | Anuidade/Perpetuidade crescente |
    | Capitalizações por ano | Usado para calcular a TAE | TAE (Taxa Anual Efetiva) |
    | Custos Fixos (€) | Valor fixo a cobrir com vendas | Break-even (quantidade) |
    | Preço por Unidade (€) | Preço de venda unitário | Break-even (quantidade) |
    | Custo por Unidade (€) | Custo de produção unitário | Break-even (quantidade) |

    ### Como obter cada resultado

    | Resultado | Depende de |
    |-----------|------------|
    | Valor Futuro (VF) | Investimento Inicial, Taxa de Juro, Períodos |
    | Valor Atual (VA) | Valor Futuro, Taxa de Juro, Períodos |
    | VAL | Investimento Inicial, Fluxos, Taxa de Juro |
    | TIR | Investimento Inicial, Fluxos |
    | Payback Descontado | Investimento Inicial, Fluxos, Taxa de Juro |
    | Anuidade | Fluxo, Taxa de Juro, Períodos |
    | Perpetuidade | Fluxo, Taxa de Juro |
    | Break-even (fluxo) | Investimento, Taxa, Períodos |
    | Break-even (quantidade) | Custos fixos, Preço unitário, Custo unitário, Taxa, Períodos |
    | TAE | Taxa nominal, nº de capitalizações |
    | Taxa Implícita | Valor Futuro, Investimento, Períodos |
    | Períodos necessários | Valor Futuro, Investimento, Taxa |
    | Rácio B/C | Valor Atual dos Benefícios, Investimento |
    """)

# === Interface de Entrada ===
st.sidebar.header("Parâmetros de Entrada")
c0 = st.sidebar.number_input("Investimento Inicial (€)", value=10000.0)
r = st.sidebar.number_input("Taxa de Juro (%)", value=5.0) / 100
vf = st.sidebar.number_input("Valor Futuro Esperado (€)", value=11576.25)
t = st.sidebar.number_input("Número de Períodos (anos)", value=3, step=1)
fluxo = st.sidebar.number_input("Fluxo de Caixa Anual (€)", value=3000.0)
g = st.sidebar.number_input("Taxa de Crescimento (%)", value=3.0) / 100
m = st.sidebar.number_input("Nº Capitalizações por ano (para TAE)", value=12, step=1)

# Break-even por unidade
st.sidebar.subheader("Break-even Quantitativo")
custo_fixo = st.sidebar.number_input("Custos Fixos (€)", value=10000.0)
preco_unit = st.sidebar.number_input("Preço por Unidade (€)", value=50.0)
custo_unit = st.sidebar.number_input("Custo por Unidade (€)", value=30.0)

fluxos = [fluxo] * int(t)

if st.sidebar.button("Calcular"):
    st.subheader("Resultados")
    st.write("**Valor Futuro:** €{:.2f}".format(calcular_valor_futuro(c0, r, t)))
    st.write("**Valor Atual:** €{:.2f}".format(calcular_valor_atual(vf, r, t)))
    st.write("**VAL:** €{:.2f}".format(calcular_val(c0, fluxos, r)))
    st.write("**TIR:** {:.2f}%".format(calcular_tir([-c0] + fluxos) * 100))
    st.write("**Perpetuidade:** €{:.2f}".format(calcular_perpetuidade(fluxo, r)))
    st.write("**Perpetuidade Crescente:** €{:.2f}".format(calcular_perpetuidade_crescente(fluxo, r, g)))
    st.write("**Anuidade Constante (VA):** €{:.2f}".format(calcular_anuidade_constante(fluxo, r, t)))
    st.write("**Anuidade Crescente (VA):** €{:.2f}".format(calcular_anuidade_crescente(fluxo, r, g, t)))
    st.write("**Payback Descontado:** {:.2f} anos".format(calcular_payback_descontado(c0, fluxos, r)))
    st.write("**Break-even (Fluxo Anual):** €{:.2f}".format(calcular_break_even_fluxo(c0, r, t)))
    st.write("**Break-even (Unidades a Vender):** {:.2f} unidades".format(calcular_break_even_quantidade(custo_fixo, preco_unit, custo_unit, r, t)))
    st.write("**Taxa Anual Efetiva (TAE):** {:.2f}%".format(calcular_tae(r, m) * 100))
    st.write("**Taxa Implícita (de C0 para VF):** {:.2f}%".format(calcular_taxa_implicita(vf, c0, t) * 100))
    st.write("**Número de Períodos necessário:** {:.2f} anos".format(calcular_periodos(vf, c0, r)))
    st.write("**Rácio Benefício/Custo (fluxos descontados):** {:.2f}".format(calcular_racio_bc_fluxos(fluxos, c0, r)))
    st.write("**Rácio Benefício/Custo (VA de benefício final):** {:.2f}".format(calcular_racio_bc_final(calcular_valor_atual(vf, r, t), c0)))

