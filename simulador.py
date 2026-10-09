import streamlit as st
import pandas as pd
import os
from datetime import datetime
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="Ascani Digital", page_icon="💻", layout="wide")

st.title("💻 Simulador de Orçamentos - Ascani Digital")
st.write("Ferramenta de precificação e geração de propostas comerciais.")

# --- 1. DADOS DO CLIENTE ---
st.subheader("1. Dados do Cliente")
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Nome da Empresa/Cliente:")
    cpf_cnpj = st.text_input("CPF / CNPJ:")
with col2:
    telefone = st.text_input("Telefone / WhatsApp:")
    email = st.text_input("E-mail:")

# --- 2. ÂMBITO DO PROJETO ---
st.subheader("2. Âmbito do Projeto")
col3, col4 = st.columns(2)
with col3:
    servico = st.selectbox("Serviço Principal:", ["Desenvolvimento Web", "Automação de Processos", "Dashboard Power BI"])
    descricao = st.text_area("Descrição detalhada do que será criado (aparecerá no PDF):", height=130)
with col4:
    horas_estimadas = st.number_input("Horas Estimadas de Trabalho:", min_value=1, value=20)
    valor_hora = st.number_input("Valor da Hora (R$):", min_value=10.0, value=80.0)
    # NOVO CAMPO: Valor Mensal
    valor_mensal = st.number_input("Valor Mensal (Hospedagem/Manutenção) R$:", min_value=0.0, value=0.0)

# --- 3. CUSTOS E MARGENS (USO INTERNO) ---
st.subheader("3. Custos e Margens (Uso Interno)")
col5, col6 = st.columns(2)
with col5:
    custos_extras = st.number_input("Custos Adicionais Únicos (Domínio, Servidor, APIs) R$:", min_value=0.0, value=0.0)
with col6:
    imposto = st.slider("Imposto/Taxa (%):", 0, 30, 6)
    margem_desejada = st.slider("Margem de Lucro Desejada (%):", 0, 100, 30)

st.divider()

# Lógica de Cálculo
custo_hora = horas_estimadas * valor_hora
custo_total = custo_hora + custos_extras
valor_com_imposto = custo_total / (1 - (imposto / 100))
preco_final = valor_com_imposto / (1 - (margem_desejada / 100))
lucro_estimado = preco_final - custo_total - (preco_final * (imposto / 100))

# Resumo Financeiro (Apenas para si)
st.subheader("📊 Resumo Financeiro (Visão Interna)")
col_res1, col_res2, col_res3 = st.columns(3)
col_res1.metric("Custo Total", f"R$ {custo_total:,.2f}")
col_res2.metric("Preço Final Sugerido", f"R$ {preco_final:,.2f}")
col_res3.metric("Lucro Estimado", f"R$ {lucro_estimado:,.2f}")

st.divider()

# --- FUNÇÕES DE EXPORTAÇÃO E HISTÓRICO ---

def gerar_pdf(nome_cliente, cpf_cnpj, telefone, email, tipo_servico, desc_projeto, valor_investimento, v_mensal):
    pdf = FPDF()
    pdf.add_page()
    
    # Cores
    COR_TEXTO = (40, 40, 40)
    COR_DESTAQUE = (0, 102, 204)
    COR_FUNDO_CAIXA = (245, 247, 250)
    
    # Cabeçalho e Logo
    if os.path.exists("logo.png"):
        pdf.image("logo.png", 10, 10, 45)
    elif os.path.exists("logo.jpg"):
        pdf.image("logo.jpg", 10, 10, 45)
    elif os.path.exists("logo.jpeg"):
        pdf.image("logo.jpeg", 10, 10, 45)
        
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(*COR_TEXTO)
    pdf.cell(0, 10, "PROPOSTA COMERCIAL", ln=True, align="R")
    
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, "Ascani Digital", ln=True, align="R")
    
    pdf.ln(10)
    pdf.set_draw_color(*COR_DESTAQUE)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # Dados do Cliente
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(*COR_TEXTO)
    pdf.cell(0, 8, "1. Dados do Cliente", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(20, 6, "Cliente:", border=0)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, f"{nome_cliente}", border=0, ln=True)
    
    if cpf_cnpj:
        pdf.set_font("Arial", "", 11)
        pdf.cell(25, 6, "CPF/CNPJ:", border=0)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{cpf_cnpj}", border=0, ln=True)
        
    if telefone or email:
        pdf.set_font("Arial", "", 11)
        contatos = f"{telefone}  |  {email}".strip(' |')
        pdf.cell(20, 6, "Contato:", border=0)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{contatos}", border=0, ln=True)
        
    pdf.ln(8)
    
    # Escopo do Projeto
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(*COR_TEXTO)
    pdf.cell(0, 8, "2. Escopo do Projeto", ln=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(20, 6, "Serviço:", border=0)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, f"{tipo_servico}", border=0, ln=True)
    pdf.ln(2)
    
    if desc_projeto:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, "Descrição:", ln=True)
        pdf.set_font("Arial", "", 11)
        desc_tratada = desc_projeto.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, desc_tratada)
        
    pdf.ln(10)
    
    # Caixa de Investimento
    pdf.set_fill_color(*COR_FUNDO_CAIXA)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(100, 100, 100)
    # TÍTULO ALTERADO AQUI
    pdf.cell(0, 10, " 3. Valor Total do Investimento", border=0, ln=True, fill=True) 
    
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(*COR_DESTAQUE)
    pdf.cell(0, 12, f" R$ {valor_investimento:,.2f}", border=0, ln=True, fill=True)
    
    # Adiciona a mensalidade se for maior que zero
    if v_mensal > 0:
        pdf.set_font("Arial", "B", 11)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 8, f" + Pagamento Mensal (Manutenção/Serviços): R$ {v_mensal:,.2f} / mês", border=0, ln=True, fill=True)
        
    pdf.ln(15)

    # ESPAÇO PARA ASSINATURA
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(*COR_TEXTO)
    pdf.cell(100, 8, "____________________________________________________", ln=True)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(100, 6, f"Assinatura do Cliente: {nome_cliente}", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(100, 6, "Data: ____/____/________", ln=True)
    
    # Rodapé
    pdf.set_y(-40) 
    pdf.set_font("Arial", "I", 10)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 5, "Ascani Digital - Transformando a sua presença online.", ln=True, align="C")
    pdf.cell(0, 5, "Validade desta proposta: 15 dias úteis.", ln=True, align="C")
    
    nome_ficheiro = f"Proposta_{nome_cliente.replace(' ', '_')}.pdf"
    pdf.output(nome_ficheiro)
    return nome_ficheiro

def guardar_historico(cliente_nome, doc, tel, mail, servico_nome, desc, custo, preco, lucro, margem, v_mensal):
    ficheiro = 'historico_orcamentos.csv'
    novo_dado = pd.DataFrame({
        'Data': [datetime.now().strftime("%d/%m/%Y %H:%M")],
        'Cliente': [cliente_nome],
        'CPF/CNPJ': [doc],
        'Telefone': [tel],
        'E-mail': [mail],
        'Servico': [servico_nome],
        'Descricao': [desc],
        'Custo Total': [custo],
        'Preco Final': [preco],
        'Lucro': [lucro],
        'Margem (%)': [margem],
        'Valor Mensal': [v_mensal] # Guarda também a mensalidade
    })
    if os.path.exists(ficheiro):
        novo_dado.to_csv(ficheiro, mode='a', header=False, index=False)
    else:
        novo_dado.to_csv(ficheiro, index=False)

# --- BOTÃO DE AÇÃO ---

if st.button("Validar e Gerar Proposta", type="primary"):
    if cliente.strip() == "":
        st.warning("⚠️ Por favor, preencha pelo menos o Nome do Cliente antes de gerar a proposta.")
    else:
        # Passamos a nova variável valor_mensal
        guardar_historico(cliente, cpf_cnpj, telefone, email, servico, descricao, custo_total, preco_final, lucro_estimado, margem_desejada, valor_mensal)
        st.success("✅ Orçamento guardado no seu histórico interno (historico_orcamentos.csv)!")
        
        ficheiro_pdf = gerar_pdf(cliente, cpf_cnpj, telefone, email, servico, descricao, preco_final, valor_mensal)
        
        with open(ficheiro_pdf, "rb") as f:
            st.download_button(
                label="📥 Descarregar Proposta em PDF (Para o Cliente)",
                data=f,
                file_name=ficheiro_pdf,
                mime="application/pdf"
            )
