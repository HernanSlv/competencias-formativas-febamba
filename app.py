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
    
    # REGIÓN CENTRO
    centro_primeros = [
        ["Arquitectura Negro A", "Centro 1", 10, 8, 2, 860, 636, 224, 18],
        ["Ferrocarril Oeste Blanco B", "Centro 2", 10, 9, 1, 707, 341, 366, 19],
        ["Ferrocarril Oeste Verde A", "Centro 3", 8, 8, 0, 921, 299, 622, 16],
        ["Claridad", "Centro 4", 7, 7, 0, 646, 328, 318, 14],
        ["Armenia", "Centro 5", 8, 8, 0, 644, 253, 391, 16],
        ["GEVP Celeste B", "Centro 6", 8, 8, 0, 618, 203, 415, 16]
    ]
    
    centro_segundos = [
        ["El Talar", "Centro 1", 9, 8, 1, 628, 457, 171, 17],
        ["Italiano B", "Centro 2", 9, 9, 0, 729, 377, 352, 18],
        ["Italiano", "Centro 3", 8, 6, 2, 530, 412, 118, 14],
        ["José Hernández A", "Centro 4", 7, 5, 2, 443, 365, 78, 12],
        ["Club Atlético Huracán de Parque Patricios", "Centro 5", 9, 7, 2, 380, 423, -43, 16],
        ["Vélez Sarsfield Azul B", "Centro 6", 8, 6, 2, 505, 303, 202, 14]
    ]
    
    centro_terceros = [
        ["Pinocho", "Centro 1", 9, 8, 1, 695, 487, 208, 17, "✅"],
        ["Pinocho Blanco", "Centro 2", 10, 6, 4, 514, 441, 73, 16, "✅"],
        ["San Lorenzo Azul", "Centro 3", 8, 5, 3, 507, 501, 6, 13, "✅"],
        ["Ferrocarril Oeste Naranja C", "Centro 6", 8, 5, 3, 417, 417, 0, 13, "✅"],
        ["Deportivo Crovara A", "Centro 4", 8, 4, 4, 429, 480, -51, 12, "❌"],
        ["Estrella de Boedo", "Centro 5", 7, 5, 2, 445, 235, 210, 12, "❌"]
    ]
    
    # REGIÓN OESTE
    oeste_primeros = [
        ["Vélez Sarsfield Blanco A", "Oeste 1", 12, 11, 1, 945, 520, 425, 23],
        ["Estudiantil Porteño A", "Oeste 2", 11, 11, 0, 980, 510, 470, 22],
        ["C.A.S.A Padua A", "Oeste 3", 11, 11, 0, 925, 408, 517, 22],
        ["San Miguel Verde", "Oeste 4", 11, 11, 0, 1046, 478, 568, 22],
        ["Dep. Morón Rojo", "Oeste 5", 9, 8, 1, 520, 283, 237, 17],
        ["Estudiantil Porteño B", "Oeste 6", 11, 11, 0, 784, 474, 310, 22]
    ]
    
    oeste_segundos = [
        ["Institución Sarmiento Verde A", "Oeste 1", 11, 10, 1, 889, 549, 340, 21],
        ["Morón Rojo", "Oeste 2", 11, 9, 2, 959, 509, 450, 20],
        ["Argentino de Castelar Norte A", "Oeste 3", 11, 9, 2, 996, 535, 461, 20],
        ["Indios U17 Negro", "Oeste 4", 11, 9, 2, 876, 375, 501, 20],
        ["San Miguel Blanco", "Oeste 5", 9, 8, 1, 514, 272, 242, 17],
        ["Indios U17 Blanco", "Oeste 6", 11, 9, 2, 709, 505, 204, 20]
    ]
    
    oeste_terceros = [
        ["GEVP Blanco A", "Oeste 1", 11, 9, 2, 971, 571, 400, 20, "✅"],
        ["Dep. Morón Blanco", "Oeste 2", 11, 8, 3, 815, 577, 238, 19, "✅"],
        ["Argentino de Castelar Centro B", "Oeste 6", 11, 8, 3, 737, 485, 252, 19, "✅"],
        ["Porteño Azul A", "Oeste 4", 11, 8, 3, 681, 518, 163, 19, "✅"],
        ["Club GEI Azul A", "Oeste 3", 10, 8, 2, 820, 467, 353, 18, "❌"],
        ["Morón Blanco", "Oeste 5", 9, 7, 2, 564, 350, 214, 16, "❌"]
    ]
    
    # REGIÓN SUR
    sur_primeros = [
        ["Racing Club", "Sur 1", 8, 8, 0, 642, 450, 192, 16],
        ["Boca Juniors A", "Sur 2", 10, 10, 0, 1071, 265, 806, 20],
        ["Gimnasia y Esgrima de Lomas de Zamora", "Sur 3", 10, 10, 0, 918, 372, 546, 20],
        ["Burzaco FC Azul A", "Sur 4", 9, 7, 2, 589, 414, 175, 16],
        ["Tristán Suárez", "Sur 5", 9, 8, 1, 585, 378, 207, 17],
        ["Club Gimnasia y Esgrima La Plata Azul A", "Sur 6", 9, 9, 0, 960, 322, 638, 18],
        ["Boca Juniors B", "Sur 7", 9, 9, 0, 829, 391, 438, 18]
    ]
    
    sur_segundos = [
        ["Wilde Sporting", "Sur 1", 9, 7, 2, 676, 542, 134, 16],
        ["Lanús A", "Sur 2", 10, 8, 2, 804, 427, 377, 18],
        ["Temperley", "Sur 3", 10, 8, 2, 834, 408, 426, 18],
        ["Lobos Athletic Club", "Sur 4", 9, 7, 2, 553, 472, 81, 16],
        ["Cañuelas FC", "Sur 5", 8, 8, 0, 569, 389, 180, 16],
        ["Berazategui", "Sur 6", 8, 7, 1, 643, 327, 316, 15],
        ["Gimnasia y Esgrima de Lomas de Zamora B", "Sur 7", 9, 7, 2, 660, 433, 227, 16]
    ]
    
    sur_terceros = [
        ["Social Lanús", "Sur 2", 10, 7, 3, 556, 611, -55, 17, "✅"],
        ["Def. Banfield", "Sur 3", 10, 6, 4, 646, 476, 170, 16, "✅"],
        ["Varela JRS", "Sur 6", 9, 6, 3, 744, 442, 302, 15, "❌"],
        ["Independiente de Burzaco", "Sur 4", 8, 6, 2, 588, 419, 169, 14, "❌"],
        ["Lanús B", "Sur 7", 8, 6, 2, 579, 375, 204, 14, "❌"],
        ["Monte Grande A Rojo", "Sur 5", 8, 5, 3, 533, 457, 76, 13, "❌"],
        ["Independiente", "Sur 1", 8, 5, 3, 543, 503, 40, 13, "❌"]
    ]
    
    return (norte_primeros, norte_segundos, norte_terceros,
            centro_primeros, centro_segundos, centro_terceros,
            oeste_primeros, oeste_segundos, oeste_terceros,
            sur_primeros, sur_segundos, sur_terceros)

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
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🔴 NORTE", "16 equipos", "12 directos + 4 terceros")
    
    with col2:
        st.metric("🟠 CENTRO", "16 equipos", "12 directos + 4 terceros")
    
    with col3:
        st.metric("🟢 OESTE", "16 equipos", "12 directos + 4 terceros")
    
    with col4:
        st.metric("🟣 SUR", "16 equipos", "14 directos + 2 terceros")
    
    # Equipos destacados por región
    st.markdown("### 🏆 Equipos Destacados por Región")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔴 NORTE - Equipos Invictos:**
        - 🥇 **Banade Rojo** (12-0, 24 pts) - *Mejor récord general*
        - 🥇 Comunicaciones (11-0, 22 pts)
        - 🥇 Obras Basket (11-0, 22 pts)
        - 🥇 Caza y Pesca Blanco B (11-0, 22 pts)
        - 🥇 Sportivo Escobar (9-0, 18 pts)
        
        **🟠 CENTRO - Equipos Invictos:**
        - 🥇 Ferrocarril Oeste Verde A (8-0, 16 pts)
        - 🥇 Claridad (7-0, 14 pts)
        - 🥇 Armenia (8-0, 16 pts)
        - 🥇 GEVP Celeste B (8-0, 16 pts)
        """)
    
    with col2:
        st.markdown("""
        **🟢 OESTE - Equipos Invictos:**
        - 🥇 Estudiantil Porteño A (11-0, 22 pts)
        - 🥇 C.A.S.A Padua A (11-0, 22 pts)
        - 🥇 San Miguel Verde (11-0, 22 pts)
        - 🥇 Estudiantil Porteño B (11-0, 22 pts)
        
        **🟣 SUR - Equipos Invictos:**
        - 🥇 **Boca Juniors A** (10-0, 20 pts) - *Mejor ataque: 1071 PF*
        - 🥇 Gimnasia y Esgrima de Lomas de Zamora (10-0, 20 pts)
        - 🥇 Racing Club (8-0, 16 pts)
        - 🥇 Club Gimnasia y Esgrima La Plata Azul A (9-0, 18 pts)
        - 🥇 Boca Juniors B (9-0, 18 pts)
        """)
    
    # Estadísticas destacadas
    st.markdown("### 📈 Estadísticas Destacadas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🥇 Mejor Récord**
        Banade Rojo (Norte 4)
        12-0, 24 puntos
        """)
    
    with col2:
        st.success("""
        **🛡️ Mejor Defensa**
        Caza y Pesca Blanco B (Norte 6)
        Solo 112 puntos en contra
        """)
    
    with col3:
        st.warning("""
        **⚡ Mejor Ataque**
        Club 3 de Febrero Blanco A (Norte 1)
        1137 puntos a favor
        """)
    
    # Resumen final
    st.markdown("### 🎯 Resumen Final")
    st.success("**Total: 64 equipos** clasificados a playoffs → **16 equipos finales** a Liga Federal de Básquet")
    
    # Datos curiosos
    with st.expander("📊 Datos Curiosos", expanded=False):
        st.markdown("""
        - **20 equipos invictos** de 25 zonas totales (80% de efectividad)
        - **Oeste** es la región más dominante con 6 equipos invictos
        - **Sur** es la más competitiva: solo 2 cupos de repechaje para 7 terceros
        - **Norte 4** tiene el equipo con mejor récord: Banade Rojo (12-0)
        - **3 fechas restantes** pueden cambiar todo el panorama
        """)
    
    st.info("⚠️ **Recordatorio:** Estas son posiciones provisorias con 3 fechas restantes")

elif region == "🔴 Norte":
    st.markdown("## 🔴 REGIÓN NORTE (6 zonas) - PROVISORIO")
    
    data = create_team_data()
    norte_primeros, norte_segundos, norte_terceros = data[0], data[1], data[2]
    
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
    
    data = create_team_data()
    centro_primeros, centro_segundos, centro_terceros = data[3], data[4], data[5]
    
    # Clasificados directos
    st.markdown("### 🥇 Primeros Lugares (Clasificados Directos)")
    df_primeros = show_colored_table(
        centro_primeros,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts"]
    )
    st.dataframe(df_primeros, use_container_width=True)
    
    st.markdown("### 🥈 Segundos Lugares (Clasificados Directos)")
    df_segundos = show_colored_table(
        centro_segundos,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts"]
    )
    st.dataframe(df_segundos, use_container_width=True)
    
    # Mejores terceros
    st.markdown("### 🟡 Mejores Terceros (4 clasifican)")
    df_terceros = show_colored_table(
        centro_terceros,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts", "Estado"],
        "Estado"
    )
    st.dataframe(df_terceros, use_container_width=True)
    
    # Equipos invictos destacados
    st.success("🏆 **Equipos Invictos:** Ferrocarril Oeste Verde A, Claridad, Armenia, GEVP Celeste B")

elif region == "🟢 Oeste":
    st.markdown("## 🟢 REGIÓN OESTE (6 zonas) - PROVISORIO")
    
    data = create_team_data()
    oeste_primeros, oeste_segundos, oeste_terceros = data[6], data[7], data[8]
    
    # Clasificados directos
    st.markdown("### 🥇 Primeros Lugares (Clasificados Directos)")
    df_primeros = show_colored_table(
        oeste_primeros,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts"]
    )
    st.dataframe(df_primeros, use_container_width=True)
    
    st.markdown("### 🥈 Segundos Lugares (Clasificados Directos)")
    df_segundos = show_colored_table(
        oeste_segundos,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts"]
    )
    st.dataframe(df_segundos, use_container_width=True)
    
    # Mejores terceros
    st.markdown("### 🟡 Mejores Terceros (4 clasifican)")
    df_terceros = show_colored_table(
        oeste_terceros,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts", "Estado"],
        "Estado"
    )
    st.dataframe(df_terceros, use_container_width=True)
    
    # La región más dominante
    st.success("🏆 **Región más dominante:** 6 equipos invictos - Estudiantil Porteño A, C.A.S.A Padua A, San Miguel Verde, Estudiantil Porteño B")

elif region == "🟣 Sur":
    st.markdown("## 🟣 REGIÓN SUR (7 zonas) - PROVISORIO")
    
    data = create_team_data()
    sur_primeros, sur_segundos, sur_terceros = data[9], data[10], data[11]
    
    # Clasificados directos
    st.markdown("### 🥇 Primeros Lugares (Clasificados Directos)")
    df_primeros = show_colored_table(
        sur_primeros,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts"]
    )
    st.dataframe(df_primeros, use_container_width=True)
    
    st.markdown("### 🥈 Segundos Lugares (Clasificados Directos)")
    df_segundos = show_colored_table(
        sur_segundos,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts"]
    )
    st.dataframe(df_segundos, use_container_width=True)
    
    # Mejores terceros (solo 2 clasifican)
    st.markdown("### 🟡 Mejores Terceros (⚠️ SOLO 2 clasifican)")
    df_terceros = show_colored_table(
        sur_terceros,
        ["Equipo", "Zona", "J", "G", "P", "PF", "PC", "Diff", "Pts", "Estado"],
        "Estado"
    )
    st.dataframe(df_terceros, use_container_width=True)
    
    # Competencia más reñida
    st.warning("⚠️ **Región más competitiva:** Solo 2 cupos de repechaje para 7 terceros lugares")
    st.success("🏆 **Equipos invictos:** Racing Club, Boca Juniors A, Gimnasia y Esgrima de Lomas de Zamora, Club Gimnasia y Esgrima La Plata Azul A, Boca Juniors B")

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
