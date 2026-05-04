# !pip install streamlit
# python -m streamlit run app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
from pathlib import Path

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Prêmio Municípios Mineradores",
    layout="wide"
)

# =========================
# CAMINHOS RELATIVOS (FUNCIONA LOCAL E NO STREAMLIT CLOUD)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho do arquivo de dados
DATA_PATH = os.path.join(BASE_DIR, "data", "pmm2026_agenda_norm.xlsx")

# Caminho da imagem do cabeçalho
LOGO_COMPLETO = os.path.join(BASE_DIR, "images", "logo_completo_2.png")

# URL do dashboard (será atualizada após o deploy)
DASHBOARD_URL = "https://pmm2026-dashboard.streamlit.app/"

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_excel(DATA_PATH)

df = load_data()

# =========================
# FUNÇÃO AUXILIAR PARA IMAGENS
# =========================
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.warning(f"Imagem não encontrada: {image_path}")
        return ""

# =========================
# ESTILOS GLOBAIS
# =========================
st.markdown("""
<style>
/* Container do topo com imagem */
.header-image-container {
    background-color: #ffecb3;
    text-align: center;
}

/* Container dos links de compartilhamento - FUNDO TRANSPARENTE */
.share-links-container {
    background-color: transparent !important;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    padding: 8px 30px 10px 30px;
    margin: 0;
    font-family: 'Arial', sans-serif;
}

/* Texto "Compartilhe:" */
.share-text {
    font-size: 12px;
    color: #FFFFFF !important;
    font-weight: 500;
}

/* Links de compartilhamento */
.share-link {
    font-size: 12px;
    color: #5B6C24 !important;
    text-decoration: none;
    padding: 3px 6px;
    border-radius: 4px;
    font-weight: 600;
    transition: all 0.2s ease;
    border: 1px solid #5B6C24;
}

.share-link:hover {
    color: #F2994A !important;
    background-color: rgba(91, 108, 36, 0.1);
    border-color: #F2994A;
}

/* Separador entre links */
.share-divider {
    color: #5B6C24;
    font-size: 12px;
    font-weight: bold;
}

/* Separador visual abaixo do header */
.header-separator {
    border: none;
    height: 1px;
    background-color: #5B6C24;
    margin: 0;
}

/* Título das seções */
.section-title {
    font-family: Arial, sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #000000;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Imagem do cabeçalho
try:
    st.image(LOGO_COMPLETO, use_container_width=True)
except Exception as e:
    st.warning(f"Logo completo não encontrado em: {LOGO_COMPLETO}")

# Seção de compartilhamento com fundo transparente
st.markdown(f"""
<div class="share-links-container">
    <span class="share-text">📤 Compartilhe:</span>
    <a href="https://wa.me/?text=Confira%20o%20dashboard%20Prêmio%20Municípios%20Mineradores%202026:%20{DASHBOARD_URL}" target="_blank" class="share-link">WhatsApp</a>
    <span class="share-divider">|</span>
    <a href="https://www.linkedin.com/sharing/share-offsite/?url={DASHBOARD_URL}" target="_blank" class="share-link">LinkedIn</a>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="header-separator">', unsafe_allow_html=True)

# =========================
# DICIONÁRIO DE NOMES AMIGÁVEIS E FORMATOS
# =========================
FRIENDLY_NAMES = {
    "concat": ("Município", "plain"),
    "microrregiao": ("Microrregião", "plain"),
    "pop_mun": ("População", "int"),
    "area": ("Área (km²)", "int"),
    "indice_geral": ("Nota Geral", "float3"),
    "ranking_geral": ("Ranking", "int"),

    "ranking_saude": ("# Posição Saúde", "int"),
    "indice_saude": ("Índice Saúde", "float3"),
    "cobert_aps_mun": ("Cobertura APS", "percent0"),
    "cobert_vacin_mun": ("Cobertura Vacinal", "percent0"),
    "gastos_saud_cap_mun": ("Gasto Saúde per capita", "money"),
    "mortalid_infant_mun": ("Mortalidade Infantil", "float1"),
    "equip_sus_cap_mun": ("Equip. SUS per capita", "float2"),
    "subnutr_mun": ("Subnutrição Infantil", "percent1"),
    "obesid_mun": ("Obesidade Infantil", "percent1"),

    "ranking_educacao": ("# Posição Educação", "int"),
    "indice_educacao": ("Índice Educação", "float3"),
    "ideb_5ano": ("IDEB - Anos iniciais", "float1"),
    "ideb_9ano": ("IDEB - Anos finais", "float1"),
    "aband_fund_mun": ("Abandono Fundamental", "percent1"),
    "gastos_edu_cap_mun": ("Gasto Educação per cap.", "money"),
    "creche_mun": ("Cobertura de Creches", "percent1"),
    "tdis_fund_mun": ("Distorção Idade-Série", "percent1"),

    "ranking_desenvolvimento_economico": ("# Posição Desen. Econ.", "int"),
    "indice_desenvolvimento_economico": ("Índice Desen. Econ.", "float3"),
    "pib_cap_mun": ("PIB per capita", "money1"),
    "saldo_empr_form_mun": ("Saldo Emp. Formais", "percent0"),
    "sal_med_mun": ("Salário Médio", "money"),
    "pop_ocup_mun": ("População Ocupada", "percent0"),
    "temp_med_empr_mun": ("Tempo Médio Empresas", "float1"),
    "rend_median_mun": ("Renda Mediana", "money"),

    "ranking_financas_publicas": ("# Posição Finanças Públicas", "int"),
    "indice_financas_publicas": ("Índice Finanças Públicas", "float3"),
    "auton_mun": ("IFGF Autonomia", "float2"),
    "desp_corrent_mun": ("Despesa Corrente", "percent1"),
    "gast_pess_mun": ("IFGF Gastos com Pessoal", "float2"),
    "invest_mun": ("IFGF Investimentos", "float2"),
    "liq_mun": ("IFGF Liquidez", "float2"),
    "prev_mun": ("Previdência", "int"),

    "ranking_infraestrutura": ("# Posição Infraestrutura", "int"),
    "indice_infraestrutura": ("Índice Infraestrutura", "float3"),
    "gast_ubran_mun": ("Gasto Urbanismo", "percent0"),
    "acess_agua_mun": ("Acesso à Água", "percent1"),
    "acess_esgot_mun": ("Acesso a Esgoto", "percent1"),
    "ilum_pub_mun": ("Iluminação Pública", "percent1"),
    "vias_pav_mun": ("Vias Pavimentadas", "percent1"),
    "cob_int_mun": ("Cobertura de Internet (4G)", "percent1"),

    "ranking_meio_ambiente": ("# Posição Meio Ambiente", "int"),
    "indice_meio_ambiente": ("Índice Meio Ambiente", "float3"),
    "gast_meio_amb_mun": ("Gasto Meio Ambiente", "percent0"),
    "disp_resid_mun": ("Disposição de Resíduos", "percent1"),
    "pct_pop_colet_mun": ("Pop. com Coleta Lixo", "percent1"),
    "mat_rec_mun": ("Materiais Reciclados", "percent1"),
    "desmat_veget_mun": ("Desmatamento", "percent2"),

    "ranking_gestao": ("# Posição Gestão", "int"),
    "indice_gestao": ("Índice Gestão", "float3"),
    "efet_educ_mun": ("Efetividade Educação", "money"),
    "efet_saud_mun": ("Efetividade Saúde", "money"),
    "serv_efet_mun": ("Servidores Efetivos", "percent0"),
    "transp_mun": ("Índice Transp. Municipal", "float2"),
    "gest_mun": ("Índice de Gestão Municipal", "float2"),
    "digi_mun": ("Índice de Oferta de Governo Digital", "float1"),

    "ranking_protecao_social": ("# Posição Proteção Social", "int"),
    "indice_protecao_social": ("Índice Proteção Social", "float3"),
    "pob_cap_mun": ("Pobreza", "percent0"),
    "atual_cad_mun": ("Atualização Cadastral", "percent0"),
    "cras_mun": ("Número de CRAS por 10 mil habitantes", "float4"),
}

def format_value(value, fmt):
    """Formata um valor de acordo com o tipo especificado."""
    if pd.isna(value) or value == "-":
        return "-"
    try:
        if fmt == "int":
            return f"{int(value):,}".replace(",", ".")
        elif fmt == "float1":
            return f"{float(value):,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
        elif fmt == "float2":
            return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        elif fmt == "float3":
            return f"{float(value):,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
        elif fmt == "float4":
            return f"{float(value*10):,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
        elif fmt == "money":
            return f"R$ {int(value):,}".replace(",", ".")
        elif fmt == "money1":
            return f"R$ {int(value/1000):,} mil".replace(",", ".")
        elif fmt == "percent0":
            return f"{float(value)*100:,.1f} %".replace(",", "X").replace(".", ",").replace("X", ".")
        elif fmt == "percent1":
            return f"{float(value):,.1f} %".replace(",", "X").replace(".", ",").replace("X", ".")
        elif fmt == "percent2":
            return f"{float(value):,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return str(value)
    except (ValueError, TypeError):
        return str(value)

# =========================
# FUNÇÃO DE CARDS
# =========================
def render_section(title, indice_col, ranking_col, cols, line_color="#B36C32"):
    st.markdown(f'<h2 class="section-title">{title}</h2>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="width: 100%; height: 3px; background-color: {line_color}; margin-bottom: 15px;"></div>',
        unsafe_allow_html=True,
    )
    for i in range(0, len(cols), 3):
        row = st.columns(3)
        for j in range(3):
            if i + j < len(cols):
                var_name = cols[i + j]
                friendly, fmt = FRIENDLY_NAMES.get(var_name, (var_name, "plain"))
                raw = df_sel.get(var_name, "-")
                displayed = format_value(raw, fmt)
                with row[j]:
                    st.markdown(
                        f"""
                        <div class="indicator-card-small">
                            <div class="indicator-label-small">{friendly}</div>
                            <div class="indicator-value-small">{displayed}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

# =========================
# VARIÁVEIS DE ESTILO
# =========================
INDICATOR_BG_COLOR = "#5B6C24"
INDICATOR_LABEL_COLOR = "#FFFFFF"
INDICATOR_VALUE_COLOR = "#F2994A"
INDICATOR_BORDER_RADIUS = "10px"
INDICATOR_FONT_FAMILY = "Arial, sans-serif"
INDICATOR_LABEL_FONT_SIZE = "13px"
INDICATOR_VALUE_FONT_SIZE = "22px"
INDICATOR_VALUE_FONT_WEIGHT = "700"
INDICATOR_PADDING = "15px"
INDICATOR_MARGIN_BOTTOM = "10px"

# =========================
# FILTRO CUSTOMIZADO
# =========================
FILTRO_BG = "#5B6C24"
FILTRO_BORDER = "#F2994A"
FILTRO_TEXT = "#FFFFFF"
FILTRO_HOVER_BG = "#F2994A"
FILTRO_HOVER_TEXT = "#000000"
FILTRO_LABEL_COLOR = "#F2994A"

st.markdown("""
<style>
section[data-testid="stSidebar"] {
    display: none;
}

div[data-testid="stSelectbox"] > div {
    background-color: transparent !important;
}

div[data-testid="stSelectbox"] > div > div {
    background-color: transparent !important;
}

div[data-baseweb="select"] > div {
    background-color: #5B6C24 !important;
    border: 2px solid #F2994A !important;
    border-radius: 8px !important;
    transition: all 0.3s ease;
}

div[data-baseweb="select"] > div > div {
    background-color: #5B6C24 !important;
}

div[data-baseweb="select"] input {
    background-color: transparent !important;
    color: #FFFFFF !important;
    font-family: 'Arial', sans-serif !important;
    font-size: 14px !important;
}

div[data-baseweb="select"] span {
    color: #FFFFFF !important;
    font-family: 'Arial', sans-serif !important;
    font-size: 14px !important;
}

div[data-baseweb="select"] input::placeholder {
    color: #FFFFFF !important;
    opacity: 0.7;
}

div[data-baseweb="popover"] {
    background-color: #5B6C24 !important;
    border: 1px solid #F2994A !important;
    border-radius: 8px !important;
    margin-top: 4px !important;
}

div[data-baseweb="popover"] ul {
    background-color: #5B6C24 !important;
    padding: 5px !important;
}

div[data-baseweb="popover"] li {
    background-color: #5B6C24 !important;
    color: #FFFFFF !important;
    font-family: 'Arial', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 15px !important;
    border-radius: 4px !important;
    transition: all 0.2s ease;
}

div[data-baseweb="popover"] li:hover {
    background-color: #F2994A !important;
    color: #000000 !important;
    font-weight: bold;
}

div[data-baseweb="popover"] li[aria-selected="true"] {
    background-color: #F2994A !important;
    color: #000000 !important;
    font-weight: bold;
}

div[data-baseweb="select"] svg {
    fill: #FFFFFF !important;
    transition: transform 0.3s ease;
}

div[data-baseweb="select"][aria-expanded="true"] svg {
    transform: rotate(180deg);
}

div[data-baseweb="select"] > div:focus-within {
    border-color: #F2994A !important;
    box-shadow: 0 0 0 2px #F2994A40 !important;
}

div[data-baseweb="select"] > div > div > div {
    background-color: transparent !important;
    border: none !important;
    outline: none !important;
}

div[data-baseweb="select"] * {
    background-color: transparent;
}

div[data-baseweb="select"] > div {
    background-color: #5B6C24 !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #5B6C24 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="background-color: transparent; padding: 15px 0;">', unsafe_allow_html=True)
# Cor laranja #F2994A
st.markdown(
    '<p style="font-family: Arial, sans-serif; font-size: 16px; font-weight: 600; color: #FFFFFF; margin-bottom: 8px;">'
    '📍 Selecione o município:</p>',
    unsafe_allow_html=True,
)

col_filtro, col_espaco = st.columns([1, 3])

with col_filtro:
    municipio = st.selectbox(
        label="",
        options=df["concat"].sort_values().unique(),
        index=0,
        key="municipio_filter",
        label_visibility="collapsed",
    )

st.markdown('</div>', unsafe_allow_html=True)

df_sel = df[df["concat"] == municipio].iloc[0]

# =========================
# TOP SECTION (MAPA + INDICADORES MUNICIPAIS)
# =========================
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h2 class="section-title">Localização</h2>', unsafe_allow_html=True)
    st.markdown(
        '<div style="width: 100%; height: 3px; background-color: #B36C32; margin-bottom: 15px;"></div>',
        unsafe_allow_html=True,
    )

    fig_map = px.scatter_mapbox(
        df[df["concat"] == municipio],
        lat="latitude",
        lon="longitude",
        size="pib_cap_mun",
        zoom=12,
        height=380,
    )

    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=0, b=0),
    )

    fig_map.update_traces(
        marker_color="#000000",
        marker_size=10,
        marker_opacity=0.8,
    )

    st.plotly_chart(fig_map, use_container_width=True, config={"displayModeBar": False})

with col2:
    st.markdown('<h2 class="section-title">Indicadores</h2>', unsafe_allow_html=True)
    st.markdown(
        '<div style="width: 100%; height: 3px; background-color: #B36C32; margin-bottom: 15px;"></div>',
        unsafe_allow_html=True,
    )
    st.markdown("""
    <style>
    .indicator-card {
        background-color: """ + INDICATOR_BG_COLOR + """;
        padding: """ + INDICATOR_PADDING + """;
        border-radius: """ + INDICATOR_BORDER_RADIUS + """;
        text-align: left;
        margin-bottom: """ + INDICATOR_MARGIN_BOTTOM + """;
        font-family: """ + INDICATOR_FONT_FAMILY + """;
    }
    .indicator-label {
        font-size: """ + INDICATOR_LABEL_FONT_SIZE + """;
        color: """ + INDICATOR_LABEL_COLOR + """;
        margin-bottom: 5px;
    }
    .indicator-value {
        font-size: """ + INDICATOR_VALUE_FONT_SIZE + """;
        color: """ + INDICATOR_VALUE_COLOR + """;
        font-weight: """ + INDICATOR_VALUE_FONT_WEIGHT + """;
    }
    .indicator-card-small {
        background-color: """ + INDICATOR_BG_COLOR + """;
        padding: 8px 12px;
        border-radius: """ + INDICATOR_BORDER_RADIUS + """;
        text-align: left;
        font-family: """ + INDICATOR_FONT_FAMILY + """;
        margin-bottom: 8px;
    }
    .indicator-label-small {
        font-size: 12px;
        color: """ + INDICATOR_LABEL_COLOR + """;
        margin-bottom: 3px;
    }
    .indicator-value-small {
        font-size: 20px;
        color: """ + INDICATOR_VALUE_COLOR + """;
        font-weight: """ + INDICATOR_VALUE_FONT_WEIGHT + """;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="indicator-card">
        <div class="indicator-label">Município</div>
        <div class="indicator-value">{df_sel['concat']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="indicator-card">
        <div class="indicator-label">Microrregião</div>
        <div class="indicator-value">{df_sel.get('microrregiao', '-')}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="indicator-card-small">
            <div class="indicator-label-small">População</div>
            <div class="indicator-value-small">{df_sel['pop_mun']:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="indicator-card-small">
            <div class="indicator-label-small">Área (km²)</div>
            <div class="indicator-value-small">{df_sel['area']:,}</div>
        </div>
        """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
        <div class="indicator-card-small">
            <div class="indicator-label-small">Índice Geral</div>
            <div class="indicator-value-small">{round(df_sel['indice_geral'], 3)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="indicator-card-small">
            <div class="indicator-label-small"># Posição Geral</div>
            <div class="indicator-value-small">{int(df_sel['ranking_geral'])}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# SEÇÕES TEMÁTICAS
# =========================
col3, col4 = st.columns([1, 1])

with col3:
    render_section(
        "Saúde",
        "indice_saude",
        "ranking_saude",
        [
            "ranking_saude", "indice_saude", "cobert_aps_mun", "cobert_vacin_mun",
            "gastos_saud_cap_mun", "mortalid_infant_mun", "equip_sus_cap_mun",
            "subnutr_mun", "obesid_mun"
        ]
    )

with col4:
    render_section(
        "Educação",
        "indice_educacao",
        "ranking_educacao",
        [
            "ranking_educacao", "indice_educacao", "ideb_5ano", "ideb_9ano",
            "aband_fund_mun", "gastos_edu_cap_mun", "creche_mun", "tdis_fund_mun"
        ]
    )

col4, col5 = st.columns([1, 1])

with col4:
    render_section(
        "Desenvolvimento Econômico",
        "indice_desenvolvimento_economico",
        "ranking_desenvolvimento_economico",
        [
            "ranking_desenvolvimento_economico", "indice_desenvolvimento_economico",
            "pib_cap_mun", "saldo_empr_form_mun", "sal_med_mun", "pop_ocup_mun",
            "temp_med_empr_mun", "rend_median_mun"
        ]
    )

with col5:
    render_section(
        "Finanças Públicas",
        "indice_financas_publicas",
        "ranking_financas_publicas",
        [
            "ranking_financas_publicas", "indice_financas_publicas",
            "auton_mun", "desp_corrent_mun", "gast_pess_mun", "invest_mun",
            "liq_mun", "prev_mun"
        ]
    )

col6, col7 = st.columns([1, 1])

with col6:
    render_section(
        "Infraestrutura",
        "indice_infraestrutura",
        "ranking_infraestrutura",
        [
            "ranking_infraestrutura", "indice_infraestrutura",
            "gast_ubran_mun", "acess_agua_mun", "acess_esgot_mun",
            "ilum_pub_mun", "vias_pav_mun", "cob_int_mun"
        ]
    )

with col7:
    render_section(
        "Meio Ambiente",
        "indice_meio_ambiente",
        "ranking_meio_ambiente",
        [
            "ranking_meio_ambiente", "indice_meio_ambiente",
            "gast_meio_amb_mun", "disp_resid_mun", "pct_pop_colet_mun",
            "mat_rec_mun", "desmat_veget_mun"
        ]
    )

col8, col9 = st.columns([1, 1])

with col8:
    render_section(
        "Gestão",
        "indice_gestao",
        "ranking_gestao",
        [
            "ranking_gestao", "indice_gestao", "efet_educ_mun", "efet_saud_mun",
            "serv_efet_mun", "transp_mun", "gest_mun", "digi_mun"
        ]
    )

with col9:
    render_section(
        "Proteção Social",
        "indice_protecao_social",
        "ranking_protecao_social",
        [
            "ranking_protecao_social", "indice_protecao_social",
            "pob_cap_mun", "atual_cad_mun", "cras_mun"
        ]
    )