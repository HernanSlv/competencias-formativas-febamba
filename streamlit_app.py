import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Copa FeBAMBA - Clasificación",
    page_icon="🏀",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.warning-banner {
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    margin-bottom: 2rem;
}

.region-header {
    background: linear-gradient(135deg, #2c3e50, #3498db);
    color: white;
    padding: 1rem;
    border-radius: 10px 10px 0 0;
    text-align: center;
    font-weight: bold;
}

.clasificado-directo {
    background-color: #d4edda !important;
}

.playoff-tercero {
    background-color: #fff3cd !important;
}

.eliminado {
    background-color: #f8d7da !important;
    opacity: 0.7;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #28a745;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🏀 COPA FeBAMBA - CLASIFICACIÓN PROVISORIA A PLAYOFFS</h1>
</div>
""", unsafe_allow_html=True)

# Banner de advertencia
st.markdown("""
<div class="warning-banner">
    ⚠️ POSICIONES PROVISORIAS - FALTAN 3 FECHAS PARA COMPLETAR LAS 14 JORNADAS ⚠️
</div>
""", unsafe_allow_html=True)

# Información del sistema
with st.expander("📋 SISTEMA DE CLASIFICACIÓN - BÁSQUET", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Clasificación por Región:**
        - **Norte, Centro, Oeste (6 zonas c/u):** 2 mejores + 4 mejores 3eros = 16 clasificados
        - **Sur (7 zonas):** 2 mejores + 2 mejores 3eros = 16 clasificados
        - **Playoffs:** 16 equipos por región → eliminación directa → 4 por región
        - **Liga Federal de Básquet:** 16 equipos totales (4 por región)
        """)
    
    with col2:
        st.markdown("""
        **⚖️ Sistema de Desempate Olímpico:**
        1. Puntos totales
        2. Diferencia de puntos (PF - PC)
        3. Puntos a favor
        4. Enfrentamiento directo
        """)

# Leyenda
col1, col2, col3 = st.columns(3)
with col1:
    st.success("🟢 1° y 2° - Clasificados Directos")
with col2:
    st.warning("🟡 3° - Zona de Repechaje")
with col3:
    st.error("🔴 4° en adelante - Eliminados")

# Datos de equipos por región
def create_team_data():
    # REGIÓN NORTE
    norte_primeros = [
        ["Comunicaciones", "Norte 1", 11, 11, 0, 1102, 309, 793, 22],
        ["Sportivo Escobar", "Norte 2", 9, 9, 0, 743, 445, 298, 18],
        ["Obras Basket", "Norte 3", 11, 11, 0, 1134, 952, 182, 22],
        ["Banade Rojo", "Norte 4", 12, 12, 0, 1038, 552, 486, 24],
        ["C S D Presidente Derqui", "Norte 5", 11, 10, 1, 860, 565, 295, 21],
        ["Caza y Pesca Blanco B", "Norte 6", 11, 11, 0, 1043, 112, 931, 22]
    ]
    
    norte_segundos = [
        ["Club 3 de Febrero Blanco A", "Norte 1", 11, 10, 1, 1137, 516, 621, 21],
        ["Club Atlético Pilar", "Norte 2", 10, 8, 2, 891, 513, 378, 18],
        ["River Plate", "Norte 3", 11, 8, 3, 786, 566, 220, 19],
        ["Soc. Beccar", "Norte 4", 11, 9, 2, 939, 570, 369, 20],
        ["San Fernando Azul A", "Norte 5", 11, 10, 1, 802, 521, 281, 21],
        ["Platense B", "Norte 6", 11, 10, 1, 686, 443, 243, 21]
    ]
    
    norte_terceros = [
        ["Copello", "Norte 1", 11, 8, 3, 762, 665, 97, 19, "✅"],
        ["Caza y Pesca Azul A", "Norte 5", 11, 8, 3, 981, 547, 434, 19, "✅"],
        ["Platense A", "Norte 3", 11, 8, 2, 720, 577, 143, 18, "✅"],
        ["Union Vecinal de Munro", "Norte 4", 11, 7, 4, 770, 598, 172, 18, "✅"],
        ["San Fernando Blanco B", "Norte 6", 11, 7, 4, 623, 553, 70, 18, "❌"],
        ["Club Sportivo Pilar", "Norte 2", 8, 6, 2, 609, 405, 204, 14, "❌"]
    ]
    
    return norte_primeros, norte_segundos, norte_terceros

# Función para mostrar tabla con colores
def show_colored_table(data, columns, status_col=None):
    df = pd.DataFrame(data, columns=columns)
    
    def color_rows(row):
        if status_col and status_col in df.columns:
            if row[status_col] == "✅":
                return ['background-color: #d4edda'] * len(row)
            elif row[status_col] == "❌":
                return ['background-color: #f8d7da; opacity: 0.7'] * len(row)
        return [''] * len(row)
    
    if status_col:
        styled_df = df.style.apply(color_rows, axis=1)
    else:
        styled_df = df.style.apply(lambda x: ['background-color: #d4edda'] * len(x), axis=1)
    
    return styled_df

# Sidebar para navegación
st.sidebar.title("🏀 Navegación")
region = st.sidebar.selectbox(
    "Seleccionar Región:",
    ["📊 Resumen General", "🔴 Norte", "🟠 Centro", "🟢 Oeste", "🟣 Sur"]
)

# Contenido principal según la región seleccionada
if region == "📊 Resumen General":
    st.markdown("## 📊 Resumen General de Clasificados")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🔴 NORTE</h3>
            <p><strong>16 equipos</strong></p>
            <p>12 directos + 4 terceros</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>🟠 CENTRO</h3>
            <p><strong>16 equipos</strong></p>
            <p>12 directos + 4 terceros</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🟢 OESTE</h3>
            <p><strong>16 equipos</strong></p>
            <p>12 directos + 4 terceros</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🟣 SUR</h3>
            <p><strong>16 equipos</strong></p>
            <p>14 directos + 2 terceros</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("**Total: 64 equipos** clasificados a playoffs → **16 equipos finales** a Liga Federal de Básquet")

elif region == "🔴 Norte":
    st.markdown("## 🔴 REGIÓN NORTE (6 zonas) - PROVISORIO")
    
    norte_primeros, norte_segundos, norte_terceros = create_team_data()
    
    # Clasificados directos
    st.markdown("### 🥇 Primeros Lugares (Clasificados Directos)")
    df_primeros = show_colored_table(
        norte_primeros,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts"]
    )
    st.dataframe(df_primeros, use_container_width=True)
    
    st.markdown("### 🥈 Segundos Lugares (Clasificados Directos)")
    df_segundos = show_colored_table(
        norte_segundos,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts"]
    )
    st.dataframe(df_segundos, use_container_width=True)
    
    # Mejores terceros
    st.markdown("### 🟡 Mejores Terceros (4 clasifican)")
    df_terceros = show_colored_table(
        norte_terceros,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts", "Estado"],
        "Estado"
    )
    st.dataframe(df_terceros, use_container_width=True)
    
    # Corrección importante
    st.warning("🚨 **CORRECCIÓN POR DESEMPATE OLÍMPICO:** Norte 5 - C S D Presidente Derqui (21 pts, +295) supera a San Fernando Azul A (21 pts, +281) por mejor diferencia")

elif region == "🟠 Centro":
    st.markdown("## 🟠 REGIÓN CENTRO (6 zonas) - PROVISORIO")
    st.info("Datos de Centro en desarrollo...")

elif region == "🟢 Oeste":
    st.markdown("## 🟢 REGIÓN OESTE (6 zonas) - PROVISORIO")
    st.info("Datos de Oeste en desarrollo...")

elif region == "🟣 Sur":
    st.markdown("## 🟣 REGIÓN SUR (7 zonas) - PROVISORIO")
    st.info("Datos de Sur en desarrollo...")

# Footer
st.markdown("---")
st.markdown("""
**⚠️ Recordatorio:** Con **3 fechas restantes**, estas posiciones pueden cambiar significativamente. 
Los empates se resuelven por sistema olímpico: Puntos → Diferencia → Puntos a favor → Enfrentamiento directo.
""")

# Información adicional en sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📱 Información")
st.sidebar.info("App desarrollada para seguimiento de Copa FeBAMBA")
st.sidebar.markdown("### 🔄 Última actualización")
st.sidebar.text("Posiciones provisorias")
