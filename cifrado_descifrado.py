import html
import unicodedata

import streamlit as st

# 1

# 2
ASCII_IMPRIMIBLE = ""
for codigo in range(32, 127):
    ASCII_IMPRIMIBLE = ASCII_IMPRIMIBLE + chr(codigo)

CONJUNTOS_BASE = {
    "Abecedario (español)": "aábcdeéfghiíjklmnñoópqrstuúüvwxyz",    # 3
    "ASCII imprimible": ASCII_IMPRIMIBLE, # 4
}

# 5
FREQ_POR_IDIOMA = {
    'Español': {
        'a': 11.525, 'b': 2.215, 'c': 4.019, 'd': 5.010, 'e': 12.181,
        'f': 0.692, 'g': 1.768, 'h': 0.703, 'i': 6.247, 'j': 0.493,
        'k': 0.011, 'l': 4.967, 'm': 3.157, 'n': 6.712, 'ñ': 0.311,
        'o': 8.683, 'p': 2.510, 'q': 0.877, 'r': 6.871, 's': 7.977,
        't': 4.632, 'u': 2.927, 'v': 1.138, 'w': 0.017, 'x': 0.215,
        'y': 1.008, 'z': 0.467, 'á': 0.502, 'é': 0.433, 'í': 0.725,
        'ó': 0.827, 'ú': 0.168, 'ü': 0.012,
    },
    'Inglés': {
        'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23,
        'g': 2.02, 'h': 6.09, 'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03,
        'm': 2.41, 'n': 6.75, 'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99,
        's': 6.33, 't': 9.06, 'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15,
        'y': 1.97, 'z': 0.07,
    },
    'Francés': {
        'a': 7.636, 'b': 0.901, 'c': 3.260, 'd': 3.669, 'e': 11.876,
        'f': 1.066, 'g': 0.866, 'h': 0.737, 'i': 7.529, 'j': 0.613,
        'k': 0.074, 'l': 5.456, 'm': 2.968, 'n': 7.095, 'o': 5.378,
        'p': 3.021, 'q': 1.362, 'r': 6.553, 's': 7.948, 't': 7.244,
        'u': 6.311, 'v': 1.628, 'w': 0.114, 'x': 0.387, 'y': 0.308,
        'z': 0.136, 'à': 0.486, 'â': 0.051, 'ç': 0.085, 'è': 0.271,
        'é': 1.504, 'ê': 0.218, 'ë': 0.008, 'î': 0.045, 'ï': 0.005,
        'ô': 0.023, 'ù': 0.058, 'û': 0.060, 'ü': 0.001,
    },
}

# 6
CATEGORIAS_OCULTAS = ('Mn', 'Me', 'Cf', 'Cc')

# 7
def construir_alfabeto(cadena: str) -> list:
    registrados = []
    for c in cadena:
        if unicodedata.category(c) in CATEGORIAS_OCULTAS: # 8
            continue
        if c not in registrados:
            registrados.append(c)
    return registrados

# 9
def _indice_en_alfabeto(c: str, alfabeto: list):
    if c in alfabeto:
        return alfabeto.index(c), False
    bajo = c.lower()
    if bajo != c and bajo in alfabeto:
        return alfabeto.index(bajo), True
    return None, False


def _restaurar_caso(caracter: str, era_mayuscula: bool) -> str:
    if era_mayuscula:
        return caracter.upper()
    return caracter



# 10
def cesar_cifrar(texto: str, corrimiento: int, alfabeto: list) -> str:
    n = len(alfabeto)
    resultado = []
    for c in texto: # 11
        idx, era_may = _indice_en_alfabeto(c, alfabeto)
        if idx is None:
            resultado.append(c)  # 12
        else:
            nuevo = alfabeto[(idx + corrimiento) % n]
            resultado.append(_restaurar_caso(nuevo, era_may))
    return ''.join(resultado)


def cesar_descifrar(texto: str, corrimiento: int, alfabeto: list) -> str:
    return cesar_cifrar(texto, -corrimiento, alfabeto)


# 13
def atbash(texto: str, alfabeto: list) -> str:
    n = len(alfabeto)
    resultado = []
    for c in texto:
        idx, era_may = _indice_en_alfabeto(c, alfabeto)
        if idx is None:
            resultado.append(c)
        else:
            nuevo = alfabeto[n - 1 - idx]
            resultado.append(_restaurar_caso(nuevo, era_may))
    return ''.join(resultado)

# 14
def contar_simbolos_ajenos(texto: str, alfabeto: list) -> int:
    ajenos = 0
    for c in texto:
        if c.isspace():
            continue
        idx, era_may = _indice_en_alfabeto(c, alfabeto)
        if idx is None:
            ajenos = ajenos + 1
    return ajenos


# 15
FREQ_OTROS = 0.5


def chi_cuadrada(texto: str, tabla_frecuencias: dict) -> float:
    considerados = []
    for c in texto.lower():
        if not c.isspace():
            considerados.append(c)
    total = len(considerados)

    # 16
    if total < 15:
        return float('inf')

    # 17
    conteo = {}
    otros = 0
    for c in considerados:
        if c in tabla_frecuencias:
            if c in conteo:
                conteo[c] = conteo[c] + 1
            else:
                conteo[c] = 1
        else:
            otros = otros + 1

    chi2 = 0.0
    for letra, freq_esperada in tabla_frecuencias.items():
        if letra in conteo:
            observado = conteo[letra]
        else:
            observado = 0
        esperado = (freq_esperada / 100) * total
        diferencia = observado - esperado
        chi2 = chi2 + (diferencia * diferencia) / esperado

    esperado_otros = (FREQ_OTROS / 100) * total
    diferencia_otros = otros - esperado_otros
    chi2 = chi2 + (diferencia_otros * diferencia_otros) / esperado_otros

    return chi2 / total


def descifrado_automatico(texto: str, alfabeto: list) -> dict:
    """
    Prueba Atbash y TODOS los desplazamientos posibles de César, para
    CADA idioma disponible en FREQ_POR_IDIOMA, y regresa SOLO la mejor
    combinación (idioma, método, módulo). El humano nunca elige nada:
    el sistema decide con base en la estadística del idioma.
    """
    opciones = []
    n = len(alfabeto)

    for idioma, tabla in FREQ_POR_IDIOMA.items():
        resultado_atbash = atbash(texto, alfabeto)
        opciones.append({
            'idioma': idioma,
            'metodo': 'Atbash',
            'modulo': None,
            'texto': resultado_atbash,
            'score': chi_cuadrada(resultado_atbash, tabla)
        })

        for d in range(1, n):
            resultado = cesar_descifrar(texto, d, alfabeto)
            opciones.append({
                'idioma': idioma,
                'metodo': 'César',
                'modulo': d,
                'texto': resultado,
                'score': chi_cuadrada(resultado, tabla)
            })

    ganadora = opciones[0]
    for opcion in opciones:
        if opcion['score'] < ganadora['score']:
            ganadora = opcion
    return ganadora

# 18
TONO_AZUL = "#9dcbfa"
TONO_NARANJA = "#feb072"

st.set_page_config(
    page_title="Cifrado César / Atbash",
    page_icon="cesar.png",
    layout="wide",
)

# 19
if "conjunto_activo" not in st.session_state:
    st.session_state["conjunto_activo"] = CONJUNTOS_BASE["Abecedario (español)"]
if "conjunto_borrador" not in st.session_state:
    st.session_state["conjunto_borrador"] = st.session_state["conjunto_activo"]
# 20
if "conjunto_propio" not in st.session_state:
    st.session_state["conjunto_propio"] = CONJUNTOS_BASE["Abecedario (español)"]

# 21
def _cambiar_preset():
    anterior = st.session_state.get("opcion_anterior", "Personalizado")
    nuevo = st.session_state["opcion_elegida"]

    if anterior == "Personalizado": # 22
        st.session_state["conjunto_propio"] = st.session_state["conjunto_borrador"]

    if nuevo in CONJUNTOS_BASE:
        st.session_state["conjunto_borrador"] = CONJUNTOS_BASE[nuevo]
    else:
        st.session_state["conjunto_borrador"] = st.session_state["conjunto_propio"]

    st.session_state["opcion_anterior"] = nuevo

# 23
@st.dialog("Configurar charset", width="large")
def dialogo_charset():

    st.caption(
        "Este conjunto es la pauta de todo el sistema: el cifrado y el "
        "descifrado trabajan sobre la posición de cada símbolo dentro de él."
    )

    st.radio(
        "Punto de partida",
        list(CONJUNTOS_BASE.keys()) + ["Personalizado"],
        horizontal=True,
        key="opcion_elegida",
        on_change=_cambiar_preset,
        label_visibility="collapsed",
    )

    with st.container(key="area_charset"):
        st.text_area(
            "Caracteres del alfabeto",
            key="conjunto_borrador",
            height=220,
            help="Letras, números o símbolos, estén o no en ASCII (kanjis, emojis...). "
                 "El orden importa: define el corrimiento de César y el espejo de Atbash.",
        )

    simbolos_del_borrador = construir_alfabeto(st.session_state["conjunto_borrador"])
    # 24
    if len(simbolos_del_borrador) >= 2:
        st.caption(
            f"{len(simbolos_del_borrador)} símbolos únicos. Se descartan los repetidos "
        )
    else:
        st.warning("Escribe al menos 2 símbolos para poder cifrar con este conjunto.")

    col_guardar, col_cancelar = st.columns(2)
    with col_guardar:
        if st.button("Guardar", type="primary", use_container_width=True):
            if len(construir_alfabeto(st.session_state["conjunto_borrador"])) >= 2:
                st.session_state["conjunto_activo"] = st.session_state["conjunto_borrador"]
                st.rerun()
    with col_cancelar:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()

# 25
def nombre_charset_activo() -> str:
    actual = st.session_state["conjunto_activo"]
    for nombre, valor in CONJUNTOS_BASE.items():
        if actual == valor:
            return nombre
    return "Personalizado"

# 26
def fila_configuracion_alfabeto(contexto: str):
    st.markdown(
        '<div class="etiqueta-charset">Configuración del alfabeto actual</div>',
        unsafe_allow_html=True,
    )
    col_campo, col_boton = st.columns([2, 1], vertical_alignment="center")
    with col_campo:
        st.markdown(
            f'<div class="vista-charset">{html.escape(nombre_charset_activo())}</div>',
            unsafe_allow_html=True,
        )
    with col_boton:
        if st.button(
            "Configurar charset",
            key=f"btn_charset_{contexto}",
            use_container_width=True,
        ):
            # 27
            activo = nombre_charset_activo()
            st.session_state["conjunto_borrador"] = st.session_state["conjunto_activo"]
            st.session_state["opcion_elegida"] = activo
            st.session_state["opcion_anterior"] = activo
            if activo == "Personalizado":
                st.session_state["conjunto_propio"] = st.session_state["conjunto_activo"]
            dialogo_charset()

st.markdown('<div class="banda banda-header"></div>', unsafe_allow_html=True)

col_imagen, col_contenido = st.columns([1.8, 1.5], gap="large")

with col_imagen:
    with st.container(key="caja_imagen"):
        st.image("cesar.png", use_container_width=True)

with col_contenido:
    st.markdown(
        '<div class="titulo-app">Sistema de <span> cifrado y descifrado</span></div>',
        unsafe_allow_html=True,
    )

    alfabeto = construir_alfabeto(st.session_state["conjunto_activo"])

    tab_cifrar, tab_descifrar = st.tabs(["Cifrar", "Descifrar"])

    with tab_cifrar:
        mensaje_claro = st.text_area("Texto a cifrar", key="mensaje_claro")
        metodo = st.selectbox(
            "Método de cifrado", ["César", "Atbash"], key="metodo_elegido"
        )

        corrimiento = None
        if metodo == "César":
            # 28
            tope = len(alfabeto) - 1
            if tope < 1:
                tope = 1
            if "corrimiento" in st.session_state:
                guardado = int(st.session_state["corrimiento"])
                if guardado < 1:
                    guardado = 1
                if guardado > tope:
                    guardado = tope
                st.session_state["corrimiento"] = guardado
            if tope < 3:
                inicial = tope
            else:
                inicial = 3
            corrimiento = st.number_input(
                "Desplazamiento",
                min_value=1, max_value=tope, value=inicial,
                key="corrimiento",
            )

        fila_configuracion_alfabeto("cifrar")

        if st.button("Cifrar", type="primary", key="btn_cifrar"):
            if not alfabeto:
                st.error("Define primero un conjunto de caracteres válido.")
            else:
                if metodo == "César":
                    resultado = cesar_cifrar(mensaje_claro, corrimiento, alfabeto)
                else:
                    resultado = atbash(mensaje_claro, alfabeto)
                st.success("Texto cifrado:")
                st.code(resultado)

                fuera = contar_simbolos_ajenos(mensaje_claro, alfabeto)
                if fuera:
                    st.info(
                        f"{fuera} carácter(es) no pertenecen al alfabeto definido "
                        "y se dejaron sin cifrar."
                    )

    with tab_descifrar:
        st.caption(
            "El sistema detecta el método y el módulo por sí solo. "
            "Solo verás la línea correcta."
        )
        mensaje_cifrado = st.text_area("Texto cifrado a analizar", key="mensaje_cifrado")

        fila_configuracion_alfabeto("descifrar")

        if st.button("Descifrar automáticamente", type="primary", key="btn_descifrar"):
            if not alfabeto:
                st.error("Define primero un conjunto de caracteres válido.")
            else:
                ganador = descifrado_automatico(mensaje_cifrado, alfabeto)
                if ganador['modulo']:
                    etiqueta_modulo = f" (módulo {ganador['modulo']})"
                else:
                    etiqueta_modulo = ""
                if ganador['score'] == float('inf'):
                    st.warning(
                        "El texto es demasiado corto o no está escrito con el "
                        "alfabeto definido, así que no se puede descifrar "
                        "de forma confiable."
                    )
                else:
                    st.success(
                        f"Idioma detectado: {ganador['idioma']} | "
                        f"Método: {ganador['metodo']}{etiqueta_modulo}"
                    )
                    st.write("**Texto descifrado:**")
                    st.code(ganador['texto'])

st.markdown('<div class="banda banda-footer"></div>', unsafe_allow_html=True)


st.markdown(
    f"""
    <style>
    /* ---------- Paleta ---------- */
    :root {{
        --azul: {TONO_AZUL};
        --naranja: {TONO_NARANJA};
        --azul-oscuro: #1c4a7a;
        --naranja-oscuro: #b8631d;
    }}

    html {{ font-size: 18px; }}

    .block-container {{
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 1500px;
    }}

    /* ---------- Botones ---------- */
    button[kind="primary"], [data-testid="stBaseButton-primary"] {{
        background-color: var(--naranja) !important;
        border: 2px solid var(--naranja) !important;
        color: #4a2c0c !important;
        font-weight: 600 !important;
    }}
    button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {{
        background-color: #fd9d52 !important;
        border-color: #fd9d52 !important;
        color: #3a2008 !important;
    }}
    button[kind="secondary"], [data-testid="stBaseButton-secondary"] {{
        background-color: #ffffff !important;
        border: 2px solid var(--azul) !important;
        color: var(--azul-oscuro) !important;
        font-weight: 600 !important;
    }}
    button[kind="secondary"]:hover, [data-testid="stBaseButton-secondary"]:hover {{
        background-color: var(--azul) !important;
        color: #0c2c4d !important;
    }}

    /* ---------- Pestañas ---------- */
    [data-testid="stTabs"] [role="tablist"] {{
        gap: .5rem;
        border-bottom: none !important;
    }}
    [data-testid="stTab"] {{
        padding: .55rem 1.4rem;
        border-radius: 12px 12px 0 0;
        background-color: #eef4fb;
    }}
    [data-testid="stTab"] p {{
        font-weight: 600;
        color: var(--azul-oscuro);
    }}
    [data-testid="stTab"][aria-selected="true"] {{
        background-color: var(--azul) !important;
    }}
    [data-testid="stTab"][aria-selected="true"] p {{
        color: #ffffff !important;
    }}
    .react-aria-SelectionIndicator {{ display: none !important; }}

    /* ---------- Campos ---------- */
    input:focus, textarea:focus {{
        border-color: var(--azul) !important;
        box-shadow: 0 0 0 2px {TONO_AZUL}66 !important;
    }}

    /* ---------- Flechas del campo de corrimiento ---------- */
    [data-testid="stNumberInputStepUp"] svg,
    [data-testid="stNumberInputStepDown"] svg {{
        display: none !important;
    }}
    [data-testid="stNumberInputStepUp"],
    [data-testid="stNumberInputStepDown"] {{
        display: inline-flex !important;
        align-items: center;
        justify-content: center;
        color: var(--azul-oscuro);
        font-size: .7rem;
        line-height: 1;
    }}
    [data-testid="stNumberInputStepDown"]::after {{ content: "\\25BC"; }}
    [data-testid="stNumberInputStepUp"]::after {{ content: "\\25B2"; }}
    [data-testid="stNumberInputStepUp"]:hover:enabled,
    [data-testid="stNumberInputStepUp"]:focus:enabled,
    [data-testid="stNumberInputStepDown"]:hover:enabled,
    [data-testid="stNumberInputStepDown"]:focus:enabled {{
        background-color: var(--naranja) !important;
        color: #4a2c0c !important;
    }}

    /* ---------- Cajas de resultado ---------- */
    [data-testid="stCode"], pre {{
        border: 2px solid var(--azul) !important;
        border-radius: 12px !important;
        background-color: #f2f8ff !important;
    }}
    /* Más altas y con scroll vertical: el texto se envuelve en vez de
       irse de largo, así que crece hacia abajo y ahí sí se puede hacer
       scroll para leerlo completo. */
    [data-testid="stCode"] pre {{
        min-height: 7rem;
        max-height: 11rem;
        overflow-y: auto !important;
        overflow-x: hidden !important;
    }}
    [data-testid="stCode"] pre code {{
        display: block;
        white-space: pre-wrap !important;
        word-break: break-word;
    }}
    [data-testid="stAlertContainer"] {{ border-radius: 12px; }}

    [data-testid="stToolbar"],
    [data-testid="stAppDeployButton"],
    [data-testid="stMainMenu"],
    [data-testid="stHeader"],
    #MainMenu {{
        display: none !important;
    }}

    /* ---------- Franjas de encabezado y pie ---------- */
    .banda {{
        width: 100vw;
        margin-left: calc(50% - 50vw);
        margin-right: calc(50% - 50vw);
    }}
    .banda-header {{
        background-color: var(--naranja);
        height: 4.5rem;
        /* Streamlit separa sus bloques con un gap de 1rem; se cancela para
           que la franja quede pegada al borde superior. */
        margin-top: -1rem;
        margin-bottom: 2rem;
    }}
    .banda-footer {{
        background-color: var(--azul);
        height: 4.5rem;
        margin-top: 3rem;
    }}

    [data-testid="stHorizontalBlock"] {{ align-items: stretch; }}
    [data-testid="stLayoutWrapper"]:has(> .st-key-caja_imagen) {{
        flex: 1;
        height: 100%;
    }}
    .st-key-caja_imagen,
    .st-key-caja_imagen [data-testid="stElementContainer"],
    .st-key-caja_imagen [data-testid="stImage"],
    .st-key-caja_imagen [data-testid="stImageContainer"] {{
        height: 100%;
        width: 100%;
    }}
    .st-key-caja_imagen {{ align-items: stretch; }}
    .st-key-caja_imagen img {{
        height: 100%;
        width: 100%;
        object-fit: contain;
    }}

    /* ---------- Encabezado ---------- */
    .titulo-app {{
        font-size: 2.1rem;
        font-weight: 800;
        color: var(--azul);
        line-height: 1.15;
        margin-bottom: .2rem;
    }}
    .titulo-app span {{ color: var(--naranja); }}
    .subtitulo-app {{ color: #5b6b7c; margin-bottom: 1.2rem; }}

    /* ---------- Modal de charset ---------- */
    div[role="radiogroup"] {{ gap: .6rem; }}
    div[role="radiogroup"] > label {{
        border: 2px solid var(--azul);
        border-radius: 999px;
        padding: .35rem 1rem .35rem .6rem;
        background: #f2f8ff;
        transition: all .15s ease;
    }}
    div[role="radiogroup"] > label:hover {{ border-color: var(--naranja); }}
    div[role="radiogroup"] > label:has(input:checked) {{
        background: var(--naranja);
        border-color: var(--naranja);
    }}
    .st-key-area_charset textarea {{
        font-family: Consolas, "SFMono-Regular", monospace !important;
        font-size: .95rem !important;
        line-height: 1.7 !important;
        border: 2px solid var(--azul) !important;
        border-radius: 12px !important;
        background-color: #f8fbff !important;
        overflow-y: auto !important;
    }}
    /* ---------- Campo de solo lectura del charset vigente ---------- */
    .etiqueta-charset {{
        font-size: .875rem;
        color: #5b6b7c;
        margin-bottom: .4rem;
    }}
    .vista-charset {{
        font-size: 1rem;
        font-weight: 600;
        color: var(--azul-oscuro);
        background-color: #f8fbff;
        border: 2px solid var(--azul);
        border-radius: 10px;
        padding: 0 .9rem;
        height: 2.5rem;
        display: flex;
        align-items: center;
        white-space: nowrap;
        overflow-x: auto;
    }}
    [data-testid="stMarkdownContainer"]:has(> .vista-charset) {{
        margin-bottom: 0 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
