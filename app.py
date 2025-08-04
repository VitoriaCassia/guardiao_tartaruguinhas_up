# app.py - Guardião das Tartaruguinhas 
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


# ***********DEFINIÇÃO DE LAYOUT E TÍTULO DO NAVEGADOR *********************************

st.set_page_config(layout='wide', page_title='Guardião das Tartaruguinhas')


# ***********DEFINIÇÃO DAS VARIÁVEIS GLOBAIS *********************************

# Define o nome do arquivo onde os dados serão salvos
data_path = 'dados_ninhos.csv'


# *******************ESTILOS CSS PERSONALIZADOS ******************************

st.markdown("""
<style>
    /* Estilo para os botões do menu lateral */
    div[data-testid="stSidebar"] .stButton > button {
        background-color: #1b4d28 !important;
        color: white !important;
        font-weight: bold;
        font-size: 1.1em;
        width: 100%;
        padding: 12px 5px;
        margin-bottom: 5px;
        border-radius: 8px;
        border: none !important;
        transition: background-color 0.2s;
        text-align: left !important;
    }
    div[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #28a745 !important;
        color: white !important;
    }
    div[data-testid="stSidebar"] .stButton button:focus,
    div[data-testid="stSidebar"] .stButton button:active {
        background-color: #28a745 !important;
        color: white !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* Padronização dos rótulos de todas as telas */
    label p {
        font-weight: bold !important;
        font-size: 1.2em !important;
    }
    
    /* Padronização dos campos de texto e número em todas as telas */
    div[data-testid="stForm"] div input,
    .st-emotion-cache-1wv932v div input {
        font-size: 1.2em !important;
    }
    
    /* Padronização dos campos de seleção (selectbox) */
    .st-emotion-cache-1y50o7l p {
        font-size: 1.2em !important;
    }
</style>
""", unsafe_allow_html=True)

# ********************** CARREGAR E SALVAR DADOS *******************************

def carregar_dados():
    global ninhos_df
    if os.path.exists(data_path):
        try:
            ninhos_df = pd.read_csv(data_path)
            if 'Número do ninho' in ninhos_df.columns:
                ninhos_df['Número do ninho'] = ninhos_df['Número do ninho'].astype(int)
            return ninhos_df
        except pd.errors.EmptyDataError:
            st.warning("O arquivo de dados está vazio. Criando um novo DataFrame.")
            return inicializar_dataframe()
    else:
        return inicializar_dataframe()

def inicializar_dataframe():
    colunas = ['Número do ninho', 'Região', 'Quantidade de ovos', 'Status dos ovos',
               'Risco de alagamento', 'Dias para eclosão', 'Presença de predadores', 'Data de registro']
    return pd.DataFrame(columns=colunas)

def salvar_dados(df):
    df.to_csv(data_path, index=False)


# ********************** INICIAR VARIÁVEIS DE SESSÃO GLOBAIS *****************

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'Início'
if 'cadastro_salvo' not in st.session_state:
    st.session_state.cadastro_salvo = False
if 'ninhos_df' not in st.session_state:
    st.session_state.ninhos_df = carregar_dados()
if 'mensagem_sucesso' not in st.session_state:
    st.session_state.mensagem_sucesso = ""


# ********************** MENU LATERAL **************************************************

def menu_lateral(pagina_atual):
    #st.markdown("<h2 style='color:#1b4d28; text-align: center;'>MENU</h2>", unsafe_allow_html=True)
    
    if st.button("🏠 **Início**", key="Início", use_container_width=True):
        st.session_state.pagina = "Início"
        st.rerun()
    if st.button("📝 **Cadastrar**", key="Cadastrar", use_container_width=True):
        st.session_state.pagina = "Cadastrar"
        st.session_state.cadastro_salvo = False
        st.rerun()
    if st.button("✏️ **Alterar**", key="Alterar", use_container_width=True):
        st.session_state.pagina = "Alterar"
        st.rerun()
    if st.button("🗑️ **Excluir**", key="Excluir", use_container_width=True):
        st.session_state.pagina = "Excluir"
        st.rerun()
    if st.button("📋 **Relatório**", key="Relatório", use_container_width=True):
        st.session_state.pagina = "Relatório"
        st.rerun()
    if st.button("📈 **Estatísticas**", key="Estatísticas", use_container_width=True):
        st.session_state.pagina = "Estatísticas"
        st.rerun()
    if st.button("❌ **Sair**", key="Sair", use_container_width=True):
        st.session_state.pagina = "Sair"
        st.rerun()


# ********************** MOSTRAR TELA INICIAL ************************************

def mostrar_tela_inicial():
    st.markdown("""
    <div style='background-color: white; padding: 20px; border-radius: 10px; margin-bottom: 10px; text-align: center;'>         
        <h1 style='color: #1b4d28; font-weight: bold; font-size: 2.8em;'>🌟 Bora de Missão! 🌟 </h1>
        <p style='color: #1b4d28; font-weight: bold; font-size: 1.5em;'>Você está prestes a entrar na jornada de proteção dos ninhos das tartaruguinhas da Amazônia.</p>
        <p style='color: #1b4d28; font-weight: bold; font-size: 1.5em;'>Escolha uma opção ao lado e ajude a proteger a vida de cada tartaruguinha.</p>
    </div>
    """, unsafe_allow_html=True)
    if os.path.exists("logo_sgt.png"):
        st.image("logo_sgt.png", use_container_width=True)
    else:
        st.error("Imagem 'logo_sgt.png' não encontrada. Verifique se o arquivo está na mesma pasta do 'app.py'.")

def limpar_formulario():
    st.session_state.pop("regiao", None)
    st.session_state.pop("ovos", None)
    st.session_state.pop("status", None)
    st.session_state.pop("risco", None)
    st.session_state.pop("dias", None)
    st.session_state.pop("predadores", None)
    st.session_state.cadastro_salvo = False

def selectbox_com_default(label, opcoes, key):
    return st.selectbox(label, ["Selecione uma opção"] + opcoes, key=key)


# ********************** CADASTRAR NINHO *******************************

def cadastrar_ninho():
    st.markdown("<h2 style='color:#1b4d28;'>📝 Cadastrar Novo Ninho</h2>", unsafe_allow_html=True)
    if st.session_state.cadastro_salvo:
        st.success("✅ Ninho cadastrado com sucesso!")
        if st.button("Fazer Novo Cadastro"):
            limpar_formulario()
            st.rerun()
    if not st.session_state.cadastro_salvo:
        with st.form("form_cadastro_ninho", clear_on_submit=False):
            novo_numero = len(st.session_state.ninhos_df) + 1
            st.number_input("Número do ninho:", value=novo_numero, disabled=True, key="numero_ninho_cadastro")
            regiao = selectbox_com_default("Região:", ["Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste"], "regiao")
            ovos = st.number_input("Quantidade de ovos:", min_value=0, step=1, key="ovos", format="%d")
            status = selectbox_com_default("Status dos ovos:", ["Intacto", "Ameaçado", "Danificado"], "status")
            risco = selectbox_com_default("Nível de risco:", ["Estável 🟢", "Sob observação 🟡", "Crítico 🔴"], "risco")
            dias = st.number_input("Dias para a eclosão:", min_value=0, step=1, key="dias", format="%d")
            predadores = selectbox_com_default("Presença de predadores?", ["Sim", "Não"], "predadores")
            data_registro = datetime.now().strftime("%d/%m/%Y")
            st.markdown(f"**Data do registro:** {data_registro}")
            salvar_button = st.form_submit_button("Salvar Cadastro")
        if salvar_button:
            if "Selecione uma opção" in [regiao, status, risco, predadores]:
                st.warning("Por favor, selecione todas as opções corretamente antes de salvar.")
            else:
                novo_dado = {
                    'Número do ninho': novo_numero,
                    'Região': regiao,
                    'Quantidade de ovos': ovos,
                    'Status dos ovos': status,
                    'Risco de alagamento': risco,
                    'Dias para eclosão': dias,
                    'Presença de predadores': predadores,
                    'Data de registro': data_registro
                }
                st.session_state.ninhos_df = pd.concat([st.session_state.ninhos_df, pd.DataFrame([novo_dado])], ignore_index=True)
                salvar_dados(st.session_state.ninhos_df)
                st.session_state.cadastro_salvo = True
                st.rerun()


# ********************** ALTERAR NINHO *******************************

def alterar_ninho():
    st.markdown("<h2 style='color:#1b4d28;'>✏️ Alterar Ninho</h2>", unsafe_allow_html=True)
    if st.session_state.mensagem_sucesso:
        st.success(st.session_state.mensagem_sucesso)
        st.session_state.mensagem_sucesso = ""
    df_para_alterar = st.session_state.ninhos_df.sort_values(by='Número do ninho')
    if df_para_alterar.empty:
        st.warning("Nenhum ninho cadastrado para alterar.")
        return
    ids = df_para_alterar['Número do ninho'].astype(str).tolist()
    ids_options = ["Selecione uma opção"] + ids
    id_escolhido = st.selectbox("Escolha o número do ninho para alterar:", ids_options, key="alterar_id")
    if id_escolhido != "Selecione uma opção":
        dado = df_para_alterar[df_para_alterar['Número do ninho'] == int(id_escolhido)].iloc[0]
        regioes_opcoes = ["Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste"]
        status_opcoes = ["Intacto", "Ameaçado", "Danificado"]
        risco_opcoes = ["Estável 🟢", "Sob observação 🟡", "Crítico 🔴"]
        predadores_opcoes = ["Sim", "Não"]
        with st.form("form_alteracao_ninho"):
            regiao = st.selectbox("Região:", regioes_opcoes, index=regioes_opcoes.index(dado['Região']), key="alterar_regiao")
            ovos = st.number_input("Quantidade de ovos:", min_value=0, value=int(dado['Quantidade de ovos']), key="alterar_ovos")
            status = st.selectbox("Status dos ovos:", status_opcoes, index=status_opcoes.index(dado['Status dos ovos']), key="alterar_status")
            risco = st.selectbox("Nível de risco:", risco_opcoes, index=risco_opcoes.index(dado['Risco de alagamento']), key="alterar_risco")
            dias = st.number_input("Dias para a eclosão:", min_value=0, value=int(dado['Dias para eclosão']), key="alterar_dias")
            predadores = st.selectbox("Presença de predadores?", predadores_opcoes, index=predadores_opcoes.index(dado['Presença de predadores']), key="alterar_predadores")
            salvar_alteracao_button = st.form_submit_button("Salvar Alteração")
        if salvar_alteracao_button:
            if "Selecione uma opção" in [regiao, status, risco, predadores]:
                st.warning("Por favor, selecione todas as opções corretamente antes de salvar.")
                return
            st.session_state.ninhos_df.loc[st.session_state.ninhos_df['Número do ninho'] == int(id_escolhido), ['Região', 'Quantidade de ovos', 'Status dos ovos', 'Risco de alagamento', 'Dias para eclosão', 'Presença de predadores']] = [regiao, ovos, status, risco, dias, predadores]
            salvar_dados(st.session_state.ninhos_df)
            st.session_state.mensagem_sucesso = f"✅ Ninho {id_escolhido} alterado com sucesso!"
            st.rerun()

# ********************** EXCLUIR NINHO *******************************************************

def excluir_ninho():
    st.markdown("<h2 style='color:#1b4d28;'>🗑️ Excluir Ninho</h2>", unsafe_allow_html=True)
    if st.session_state.mensagem_sucesso:
        st.success(st.session_state.mensagem_sucesso)
        st.session_state.mensagem_sucesso = ""
    df_para_excluir = st.session_state.ninhos_df.sort_values(by='Número do ninho').drop_duplicates().reset_index(drop=True)
    if df_para_excluir.empty:
        st.warning("Nenhum ninho cadastrado para excluir.")
        return
    ids = df_para_excluir['Número do ninho'].astype(str).tolist()
    ids_options = ["Selecione uma opção"] + ids
    id_escolhido = st.selectbox("Escolha o número do ninho para excluir:", ids_options, key="excluir_id")
    if id_escolhido != "Selecione uma opção":
        st.warning(f"Tem certeza que deseja excluir o ninho {id_escolhido}?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirmar Exclusão", use_container_width=True):
                st.session_state.ninhos_df = st.session_state.ninhos_df[st.session_state.ninhos_df['Número do ninho'] != int(id_escolhido)].reset_index(drop=True)
                st.session_state.ninhos_df['Número do ninho'] = range(1, len(st.session_state.ninhos_df) + 1)
                salvar_dados(st.session_state.ninhos_df)
                st.session_state.mensagem_sucesso = f"✅ Ninho {id_escolhido} excluído com sucesso!"
                st.rerun()
        with col2:
            if st.button("Cancelar", use_container_width=True):
                st.session_state.pagina = "Início"
                st.rerun()


# ********************** RELATÓRIO *******************************

def relatorio():
    st.markdown("<h2 style='color:#1b4d28;'>📋 Relatório de Ninhos</h2>", unsafe_allow_html=True)
    df = st.session_state.ninhos_df
    if df.empty:
        st.info("Nenhum ninho cadastrado ainda.")
    else:
        st.markdown("<h3 style='color:#1b4d28; font-size:1.5em;'>Dados Detalhados dos Ninhos</h3>", unsafe_allow_html=True)
        st.markdown("---")
        for index, row in df.iterrows():
            st.markdown(f"""
            <div style='background-color: #d4edda; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <p style='font-size: 1.5em; color: #1b4d28; font-weight: bold;'>🐢 Ninho {row['Número do ninho']}</p>
                <ul style='font-size: 1.3em; color: #1b4d28;'>
                    <li><b>Região:</b> {row['Região']}</li>
                    <li><b>Ovos:</b> {row['Quantidade de ovos']}</li>
                    <li><b>Status:</b> {row['Status dos ovos']}</li>
                    <li><b>Risco:</b> {row['Risco de alagamento']}</li>
                    <li><b>Eclosão em:</b> {row['Dias para eclosão']} dias</li>
                    <li><b>Predadores:</b> {row['Presença de predadores']}</li>
                    <li><b>Data de Registro:</b> {row['Data de registro']}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ********************** ESTATÍSTICA ********************************************

def estatisticas():
    st.markdown("<h2 style='color:#1b4d28;'>📊 Estatísticas dos Ninhos</h2>", unsafe_allow_html=True)
    df = st.session_state.ninhos_df
    if df.empty:
        st.info("Nenhum dado disponível para estatísticas.")
    else:
        df_limpo = df.drop_duplicates()
        total_ninhos = len(df_limpo)
        media_ovos = df_limpo["Quantidade de ovos"].mean()
        predadores_sim = df_limpo[df_limpo["Presença de predadores"] == "Sim"].shape[0]
        risco_critico = df_limpo[df_limpo["Risco de alagamento"] == "Crítico 🔴"].shape[0]
        ovos_danificados = df_limpo[df_limpo["Status dos ovos"] == "Danificado"].shape[0]
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"<div style='background-color:#d4edda; padding:15px; border-radius:10px; text-align:center;'>"\
                f"<h3 style='color:#155724; font-size:1.4em;'>🐢 Total de Ninhos</h3>"\
                f"<p style='font-size:2.2em; font-weight:bold; color:#155724;'>{total_ninhos}</p>"\
                f"</div>", unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"<div style='background-color:#fff3cd; padding:15px; border-radius:10px; text-align:center;'>"\
                f"<h3 style='color:#856404; font-size:1.4em;'>🥚 Média de Ovos</h3>"\
                f"<p style='font-size:2.2em; font-weight:bold; color:#856404;'>{media_ovos:.2f}</p>"\
                f"</div>", unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f"<div style='background-color:#f8d7da; padding:15px; border-radius:10px; text-align:center;'>"\
                f"<h3 style='color:#721c24; font-size:1.4em;'>⚠️ Ninhos em Risco</h3>"\
                f"<p style='font-size:2.2em; font-weight:bold; color:#721c24;'>{risco_critico}</p>"\
                f"</div>", unsafe_allow_html=True
            )
        st.markdown("<br>", unsafe_allow_html=True)
        col4, col5 = st.columns(2)
        with col4:
            st.markdown(
                f"<div style='background-color:#cce5ff; padding:15px; border-radius:10px; text-align:center;'>"\
                f"<h3 style='color:#004085; font-size:1.4em;'>💥 Ovos Danificados</h3>"\
                f"<p style='font-size:2.2em; font-weight:bold; color:#004085;'>{ovos_danificados}</p>"\
                f"</div>", unsafe_allow_html=True
            )
        with col5:
            st.markdown(
                f"<div style='background-color:#e2e3e5; padding:15px; border-radius:10px; text-align:center;'>"\
                f"<h3 style='color:#495057; font-size:1.4em;'>🦊 Com Predadores</h3>"\
                f"<p style='font-size:2.2em; font-weight:bold; color:#495057;'>{predadores_sim}</p>"\
                f"</div>", unsafe_allow_html=True
            )
        st.markdown("---")
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            st.subheader("Ninhos por Região")  # Gráfico de barras
            fig, ax = plt.subplots(figsize=(5, 2))
            sns.countplot(data=df_limpo, x='Região', ax=ax, palette='viridis', order=df_limpo['Região'].value_counts().index)
            ax.set_title('Distribuição de Ninhos por Região', fontsize=10)
            ax.set_xlabel('Região', fontsize=8)
            ax.set_ylabel('Quantidade de Ninhos', fontsize=8)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            st.pyplot(fig)
        with g_col2:
            st.subheader("Status dos Ovos") #Gráfico de pizza
            status_counts = df_limpo['Status dos ovos'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(4, 2))
            ax2.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'), textprops={'fontsize': 10})
            ax2.axis('equal')
            st.pyplot(fig2)


# ********************** SAIR *******************************

def sair():
    st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 10px; text-align:center;'>
            <h2 style='color: #1b4d28; font-weight: bold; font-size: 2.8em;'> 🐢 🐢 🐢 Missão concluída! 🐢🐢🐢</h2>
                <p style='color: #1b4d28; font-weight: bold; font-size: 1.7em;'>Seus dados foram salvos com sucesso!</p>
        <p style='color: #1b4d28; font-weight: bold; font-size: 1.7em;'>Volte em breve!</p>
            </div>
    """, unsafe_allow_html=True)

    
# ********************** EXECUÇÃO PRINCIPAL DO APLICATIVO **********************************

with st.sidebar:
    menu_lateral(st.session_state.pagina)

if st.session_state.pagina == "Início":
    mostrar_tela_inicial()
elif st.session_state.pagina == "Cadastrar":
    cadastrar_ninho()
elif st.session_state.pagina == "Alterar":
    alterar_ninho()
elif st.session_state.pagina == "Excluir":
    excluir_ninho()
elif st.session_state.pagina == "Relatório":
    relatorio()
elif st.session_state.pagina == "Estatísticas":
    estatisticas()
elif st.session_state.pagina == "Sair":

    sair()
