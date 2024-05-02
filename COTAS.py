import streamlit as st

def calcular_rendimento_investimento(valor_para_investir, valores_preco, valores_rendimento):
    resultados = []
    for valor_preco, valor_rendimento in zip(valores_preco, valores_rendimento):
        numero_de_cotas = valor_para_investir / valor_preco
        rendimento_total = numero_de_cotas * valor_rendimento
        retorno_anual = rendimento_total * 12
        retorno_semestral = rendimento_total * 6
        retorno_trimestral = rendimento_total * 3
        retorno_mensal = rendimento_total * 1
        resultados.append((numero_de_cotas, rendimento_total, retorno_mensal, retorno_trimestral, retorno_semestral, retorno_anual))
    return resultados

def calcular_investimento_necessario(valores_desejados_dividendos, valores_rendimento, valores_preco):
    resultados = []
    for valor_desejado_dividendos, valor_rendimento, valor_preco in zip(valores_desejados_dividendos, valores_rendimento, valores_preco):
        quantidade_cotas_necessarias = valor_desejado_dividendos / valor_rendimento
        investimento_necessario = quantidade_cotas_necessarias * valor_preco
        retorno_anual = quantidade_cotas_necessarias * valor_rendimento * 12
        retorno_semestral = quantidade_cotas_necessarias * valor_rendimento * 6
        retorno_trimestral = quantidade_cotas_necessarias * valor_rendimento * 3
        retorno_mensal = quantidade_cotas_necessarias * valor_rendimento * 1
        resultados.append((quantidade_cotas_necessarias, investimento_necessario, retorno_mensal, retorno_trimestral, retorno_semestral, retorno_anual))
    return resultados

def calcular_tempo(salario_mensal, rendimento_por_ano):
    tempo_necessario = salario_mensal / rendimento_por_ano
    return tempo_necessario

def calcular_investimento_total(numero_cotas, preco_cota, dividendos_por_cota):
    investimento_total = (numero_cotas * preco_cota) + (numero_cotas * dividendos_por_cota)
    return investimento_total

def calcular_investimento_compra(numero_cotas, preco_cota):
    investimento_compra = numero_cotas * preco_cota
    return investimento_compra

def calcular_valor_acumulado(numero_cotas, preco_cota, dividendos_por_cota, meses):
    investimento_total = calcular_investimento_total(numero_cotas, preco_cota, dividendos_por_cota)
    valor_acumulado = 0

    for mes in range(meses):
        # Calcula os dividendos mensais e reinveste no mesmo fundo
        dividendos_mensais = numero_cotas * dividendos_por_cota
        investimento_total += dividendos_mensais
        numero_cotas += (dividendos_mensais / preco_cota)
        valor_acumulado = investimento_total

    return valor_acumulado

def calcular_rendimento(cota_price, dividendos, investimento_mensal, periodo_meses, reinvestir=True):
    cotas_adquiridas = 0
    rendimento_acumulado = 0
    cotas_totais = 0
    cotas_acumuladas = 0
    cotas_retiradas = 0

    for mes in range(1, periodo_meses + 1):
        # Calcular rendimento mensal
        rendimento_mensal = cotas_adquiridas * dividendos

        # Adicionar investimento mensal
        cotas_adquiridas += investimento_mensal / cota_price

        # Calcular rendimento acumulado
        rendimento_acumulado += rendimento_mensal

        if reinvestir:
            # Reinvestir rendimentos em novas cotas
            cotas_adquiridas += rendimento_mensal / cota_price

        # Calcular total de cotas
        cotas_totais = cotas_adquiridas

        # Opção 3: Retirar rendimento todo mês
        rendimento_mensal_retirado = rendimento_mensal if mes < periodo_meses else 0
        rendimento_acumulado -= rendimento_mensal_retirado

        # Atualizar cotas acumuladas e retiradas em reais
        cotas_acumuladas += rendimento_mensal_retirado / cota_price
        cotas_retiradas += rendimento_mensal_retirado

    return rendimento_acumulado, cotas_totais, cotas_acumuladas, cotas_retiradas

# Estilo CSS para personalizar o front-end
estilo = """
    <style>
        body {
            color: #000000; /* Preto */
            background-color: #ffd700; /* Dourado */
        }

        h1 {
            color: #ffd700; /* Dourado */
            font-size: 36px;
        }

        .stTextInput, .stNumberInput {
            color: #000000; /* Preto */
            background-color: #ffd700; /* Dourado */
            font-size: 24px;
            border: 2px solid #000000; /* Preto */
        }

        .stButton {
            color: #000000; /* Preto */
            background-color: #ffd700; /* Dourado */
            font-size: 28px;
            border: 2px solid #000000; /* Preto */
        }

        .stMarkdown {
            color: #000000; /* Preto */
            font-size: 20px;
        }
    </style>
"""

# Adiciona o estilo ao início do app
st.markdown(estilo, unsafe_allow_html=True)

st.title('Calculadora de Rendimento em Fundos Imobiliários')

# Adiciona dinamicamente os preços e rendimentos
num_cotas = st.number_input("Número de cotas para simulação:", value=1, min_value=1, step=1)
valores_preco = [st.number_input(f"Preço da cota {i+1}:", min_value=0.01, value=10.46, step=0.01) for i in range(num_cotas)]
valores_rendimento = [st.number_input(f"Rendimento por cota {i+1}:", min_value=0.01, value=0.11, step=0.01) for i in range(num_cotas)]

# Mostra os preços e rendimentos
for i, (valor_preco, valor_rendimento) in enumerate(zip(valores_preco, valores_rendimento), start=1):
    st.markdown(f"### Cota {i}")
    st.markdown(f"Preço da cota: **{valor_preco:.2f}**")
    st.markdown(f"Rendimento por cota: **{valor_rendimento:.2%}**")

# Escolha do modo de cálculo
opcao = st.sidebar.radio("Escolha a opção:", ("Rendimento Mensal", "Investimento Necessário para Dividendos Anuais", "Calcular Tempo Necessário", "Calcular Valor Acumulado", "Simular Investimento"))

if opcao == "Rendimento Mensal":
    valor_para_investir = st.number_input("Digite o valor que deseja investir: ")
    if st.button('Calcular'):
        resultados = calcular_rendimento_investimento(valor_para_investir, valores_preco, valores_rendimento)
        for i, resultado in enumerate(resultados, start=1):
            st.markdown(f"### Resultados para Cota {i}")
            st.markdown(f"O retorno em 1 mês é de **R$ {resultado[2]:.2f}**")
            st.markdown(f"O retorno em 3 meses é de **R$ {resultado[3]:.2f}**")
            st.markdown(f"O retorno em 6 meses é de **R$ {resultado[4]:.2f}**")
            st.markdown(f"O retorno em 12 meses é de **R$ {resultado[5]:.2f}**")
            st.markdown(f"Com R$ {valor_para_investir:.2f}, você pode comprar **{resultado[0]:.2f} cotas**.")
            st.markdown(f"O rendimento total estimado é de **R$ {resultado[1]:.2f}**")

elif opcao == "Investimento Necessário para Dividendos Anuais":
    valores_desejados_dividendos = st.number_input("Digite o valor que deseja receber em dividendos anuais: ")
    if st.button('Calcular'):
        resultados = calcular_investimento_necessario([valores_desejados_dividendos] * num_cotas, valores_rendimento, valores_preco)
        for i, resultado in enumerate(resultados, start=1):
            st.markdown(f"### Resultados para Cota {i}")
            st.markdown(f"Quantidade de cotas necessárias para receber R${valores_desejados_dividendos:.2f} em dividendos anuais: **{resultado[0]:.2f}**")
            st.markdown(f"Valor de Investimento Necessário: **R$ {resultado[1]:.2f}**")
            st.markdown(f"Retorno em 1 ano: **R$ {resultado[5]:.2f}**")
            st.markdown(f"Retorno em 6 meses: **R$ {resultado[4]:.2f}**")
            st.markdown(f"Retorno em 3 meses: **R$ {resultado[3]:.2f}**")
            st.markdown(f"Retorno em 1 mês: **R$ {resultado[2]:.2f}**")

elif opcao == "Calcular Tempo Necessário":
    salario_mensal = st.number_input("Digite o valor que deseja receber de salário em dividendos:")
    retorno_anual = st.number_input("Digite o valor que recebe anualmente em dividendos:")
    rendimento_por_ano = retorno_anual / 12

    if st.button('Calcular'):
        tempo_necessario = calcular_tempo(salario_mensal, rendimento_por_ano)
        st.markdown(f"Para receber um salário de R$ {salario_mensal:.2f}, são necessários aproximadamente {tempo_necessario:.2f} meses.")

elif opcao == "Calcular Valor Acumulado":
    numero_cotas_acumulado = st.number_input("Digite o número de cotas iniciais:")
    preco_cota_acumulado = st.number_input("Digite o preço da cota:")
    dividendos_por_cota_acumulado = st.number_input("Digite os dividendos por cota:")
    meses_acumulado = st.number_input("Digite o número de meses para calcular o valor acumulado:")

    # Converta meses_acumulado para um número inteiro
    meses_acumulado = int(meses_acumulado)

    if st.button('Calcular'):
        valor_acumulado = calcular_valor_acumulado(numero_cotas_acumulado, preco_cota_acumulado, dividendos_por_cota_acumulado, meses_acumulado)
        st.markdown(f"O valor acumulado após {meses_acumulado} meses é de R$ {valor_acumulado:.2f}.")

elif opcao == "Simular Investimento":
    cota_price = st.number_input("Digite o preço da cota: ")
    dividendos = st.number_input("Digite o valor dos dividendos por cota: ")
    investimento_mensal = st.number_input("Digite o valor que você deseja investir por mês: ")
    periodo_meses = st.number_input("Digite o período de tempo desejado em meses: ", min_value=1, step=1)

    if st.button('Simular'):
        rendimento_acumulado, cotas_totais, cotas_retiradas, cotas_mensais = calcular_rendimento(cota_price, dividendos, investimento_mensal, periodo_meses, reinvestir=False)
        rendimento_reinvestido, cotas_reinvestidas, _, _ = calcular_rendimento(cota_price, dividendos, investimento_mensal, periodo_meses, reinvestir=True)
        rendimento_mensal, _, _, _ = calcular_rendimento(cota_price, dividendos, investimento_mensal, periodo_meses, reinvestir=False)

        st.markdown("\n**1ª Opção: Rendimento acumulado ao longo do tempo:** R$ {:.2f}".format(rendimento_acumulado))
        st.markdown("2ª Opção: **Rendimento reinvestido comprando novas cotas:** R$ {:.2f}".format(rendimento_reinvestido))
        st.markdown("3ª Opção: **Rendimento mensal retirando todo mês:** R$ {:.2f}".format(rendimento_mensal))
        st.markdown("\n**Total de cotas acumuladas (Opção 1):** {:.2f} cotas".format(cotas_totais))
        st.markdown("Total de cotas reinvestidas (Opção 2): {:.2f} cotas".format(cotas_reinvestidas))
        st.markdown("Total de cotas retiradas (Opção 3): {:.2f} reais".format(cotas_retiradas))
