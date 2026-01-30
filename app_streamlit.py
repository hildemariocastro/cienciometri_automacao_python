import streamlit as st
import pandas as pd
import os

# ==============================
# CONFIGURAÇÕES
# ==============================


ARQUIVO_ENTRADA = "data/banco_classificado.csv"

ARQUIVO_SAIDA = "data/banco_validado.csv"

st.set_page_config(
    page_title="Validação Manual de Artigos",
    layout="wide"
)

# ==============================
# FUNÇÕES AUXILIARES
# ==============================

def carregar_csv_seguro(caminho):
    """Leitura robusta para arquivos ISO-8859-1"""
    return pd.read_csv(
        caminho,
        encoding="ISO-8859-1",
        engine="python"
    )

def salvar_csv_seguro(df, caminho):
    df.to_csv(
        caminho,
        index=False,
        encoding="ISO-8859-1"
    )

# ==============================
# CARREGAMENTO DOS DADOS
# ==============================

if os.path.exists(ARQUIVO_SAIDA):
    df = carregar_csv_seguro(ARQUIVO_SAIDA)
    st.info("📂 Arquivo de validação encontrado. Continuando de onde parou.")
else:
    df = carregar_csv_seguro(ARQUIVO_ENTRADA)

    # Cria colunas de validação se não existirem
    if "decisao_manual" not in df.columns:
        df["decisao_manual"] = ""
    if "motivo_exclusao" not in df.columns:
        df["motivo_exclusao"] = ""

# ==============================
# CONTROLE DE NAVEGAÇÃO
# ==============================

total_artigos = len(df)

if "indice" not in st.session_state:
    st.session_state.indice = 0

indice = st.session_state.indice

if indice >= total_artigos:
    st.success("✅ Todos os artigos foram avaliados!")
    st.stop()

artigo = df.iloc[indice]

# ==============================
# INTERFACE
# ==============================

st.title("📚 Validação Manual de Artigos Científicos")
st.markdown(f"### Artigo {indice + 1} de {total_artigos}")

st.divider()

# ===== METADADOS =====
st.subheader("🔎 Metadados")

st.markdown(f"**Título:** {artigo.get('title', '')}")
st.markdown(f"**Autores:** {artigo.get('authors', '')}")
st.markdown(f"**Ano:** {artigo.get('year', '')}")
st.markdown(f"**Periódico:** {artigo.get('journal', '')}")

st.divider()

# ===== RESUMO =====
st.subheader("📝 Resumo")

st.text_area(
    label="Abstract",
    value=str(artigo.get("abstract", "")),
    height=300,
    disabled=True
)

st.divider()

# ==============================
# DECISÃO MANUAL
# ==============================

st.subheader("✅ Decisão")

decisao = st.radio(
    "Selecione a decisão:",
    ["Incluir", "Excluir"],
    index=None
)

motivo = ""

if decisao == "Excluir":
    motivo = st.selectbox(
        "Motivo da exclusão (PRISMA):",
        [
            "Fora do escopo",
            "Não trata de histologia",
            "Espécie diferente",
            "Tipo de estudo inadequado",
            "Revisão narrativa",
            "Duplicado",
            "Outro"
        ]
    )

# ==============================
# BOTÕES
# ==============================

col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Voltar") and indice > 0:
        st.session_state.indice -= 1
        st.rerun()

with col2:
    if st.button("💾 Salvar e Avançar"):
        df.at[indice, "decisao_manual"] = decisao
        df.at[indice, "motivo_exclusao"] = motivo

        salvar_csv_seguro(df, ARQUIVO_SAIDA)

        st.session_state.indice += 1
        st.rerun()

# ==============================
# RODAPÉ
# ==============================

st.divider()

incluidos = (df["decisao_manual"] == "Incluir").sum()
excluidos = (df["decisao_manual"] == "Excluir").sum()
pendentes = total_artigos - incluidos - excluidos

st.markdown(
    f"""
📊 **Resumo da triagem**  
- Incluídos: **{incluidos}**  
- Excluídos: **{excluidos}**  
- Pendentes: **{pendentes}**
"""
)


## streamlit run app_streamlit.py ##