import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Copa FeBAMBA - Clasificaciones",
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

.categoria-header {
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

.invicto {
    background-color: #e8f5e8 !important;
    border-left: 4px solid #28a745 !important;
}

.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #28a745;
    margin: 0.5rem 0;
}

.zona-stats {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.racha-positiva {
    color: #28a745;
    font-weight: bold;
}

.racha-negativa {
    color: #dc3545;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carga los datos desde el archivo JSON"""
    try:
        # Aquí deberías cargar tu archivo JSON
        # Para demo, uso datos de ejemplo basados en tu JSON
        with open('basketball_complete_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # Datos de ejemplo si no encuentra el archivo
        return {
            "metadata": {
                "categorias_procesadas": ["U17 MASCULINO"],
                "total_grupos": 25,
                "fecha_scraping": "2025-06-09 01:01:01"
            },
            "datos": []
        }

def calculate_diff(pf, pc):
    """Calcula la diferencia de puntos"""
    return pf - pc

def format_racha(racha):
    """Formatea la racha con colores"""
    if racha > 0:
        return f'<span class="racha-positiva">+{racha}</span>'
    elif racha < 0:
        return f'<span class="racha-negativa">{racha}</span>'
    else:
        return '<span>0</span>'

def classify_teams_by_region(grupos, region_name):
    """Clasifica equipos por región según el sistema FeBAMBA"""
    region_grupos = [g for g in grupos if region_name.upper() in g['nombre'].upper()]
    
    primeros = []
    segundos = []
    terceros = []
    
    for grupo in region_grupos:
        clasificacion = sorted(grupo['clasificacion'], key=lambda x: (
            -x['puntos_totales'],  # Más puntos primero
            -(x['puntos_favor'] - x['puntos_contra']),  # Mejor diferencia
            -x['puntos_favor']  # Más puntos a favor
        ))
        
        if len(clasificacion) >= 1:
            primeros.append({**clasificacion[0], 'zona': grupo['nombre']})
        if len(clasificacion) >= 2:
            segundos.append({**clasificacion[1], 'zona': grupo['nombre']})
        if len(clasificacion) >= 3:
            terceros.append({**clasificacion[2], 'zona': grupo['nombre']})
    
    # Ordenar terceros por sistema olímpico
    terceros_sorted = sorted(terceros, key=lambda x: (
        -x['puntos_totales'],
        -(x['puntos_favor'] - x['puntos_contra']),
        -x['puntos_favor']
    ))
    
    return primeros, segundos, terceros_sorted

def show_team_table(teams, title, classification_spots=None):
    """Muestra tabla de equipos con formato"""
    if not teams:
        st.info(f"No hay datos para {title}")
        return
    
    # Preparar datos para DataFrame
    data = []
    for i, team in enumerate(teams):
        diff = calculate_diff(team['puntos_favor'], team['puntos_contra'])
        racha_formatted = format_racha(team['racha'])
        
        # Determinar estado de clasificación
        estado = "✅ CLASIFICA"
        if classification_spots and i >= classification_spots:
            estado = "❌ ELIMINADO"
        
        # Detectar invictos
        invicto = "🏆" if team['partidos_perdidos'] == 0 and team['partidos_jugados'] > 0 else ""
        
        data.append({
            'Pos': i + 1,
            'Equipo': f"{invicto} {team['equipo']}",
            'Zona': team.get('zona', ''),
            'J': team['partidos_jugados'],
            'G': team['partidos_ganados'],
            'P': team['partidos_perdidos'],
            'PF': team['puntos_favor'],
            'PC': team['puntos_contra'],
            'Diff': f"{diff:+d}",
            'Pts': team['puntos_totales'],
            'Racha': racha_formatted,
            'Estado': estado if classification_spots else ""
        })
    
    df = pd.DataFrame(data)
    
    # Mostrar tabla con formato
    st.markdown(f"### {title}")
    
    # Aplicar estilos según clasificación
    if classification_spots:
        def highlight_rows(row):
            if row.name < 2:  # Primeros 2 (1° y 2°)
                return ['background-color: #d4edda'] * len(row)
            elif classification_spots and row.name < classification_spots:
                return ['background-color: #fff3cd'] * len(row)
            else:
                return ['background-color: #f8d7da; opacity: 0.7'] * len(row)
        
        styled_df = df.style.apply(highlight_rows, axis=1)
    else:
        styled_df = df.style.apply(lambda x: ['background-color: #d4edda'] * len(x), axis=1)
    
    # Mostrar tabla sin índice y permitir HTML en la columna Racha
    st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🏀 COPA FeBAMBA - CLASIFICACIONES OFICIALES</h1>
        <p>Sistema de clasificación a Liga Federal de Básquet por categorías</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cargar datos
    data = load_data()
    
    if not data['datos']:
        st.error("No se pudieron cargar los datos. Asegúrate de que el archivo JSON esté disponible.")
        return
    
    # Información de metadata
    with st.expander("📊 Información del Dataset", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Categorías Procesadas", len(data['metadata']['categorias_procesadas']))
        with col2:
            st.metric("Total de Grupos", data['metadata']['total_grupos'])
        with col3:
            st.metric("Última Actualización", data['metadata']['fecha_scraping'].split()[0])
        
        st.markdown("**Categorías disponibles:**")
        st.write(", ".join(data['metadata']['categorias_procesadas']))
    
    # Sidebar para navegación
    st.sidebar.title("🏀 Navegación")
    
    # Selector de categoría
    categorias_disponibles = [d['categoria'] for d in data['datos']]
    categoria_seleccionada = st.sidebar.selectbox(
        "Seleccionar Categoría:",
        categorias_disponibles,
        index=0
    )
    
    # Obtener datos de la categoría seleccionada
    categoria_data = next(d for d in data['datos'] if d['categoria'] == categoria_seleccionada)
    grupos = categoria_data['grupos']
    
    # Selector de región
    regiones_disponibles = list(set([g['nombre'].split()[0] for g in grupos]))
    regiones_disponibles.sort()
    
    region_view = st.sidebar.selectbox(
        "Seleccionar Vista:",
        ["📊 Resumen General"] + [f"📍 {region}" for region in regiones_disponibles]
    )
    
    # Mostrar información de la categoría
    st.markdown(f"""
    <div class="categoria-header">
        <h2>{categoria_data['categoria']} - {categoria_data['fase']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Banner de estado
    st.markdown("""
    <div class="warning-banner">
        ⚠️ CLASIFICACIONES OFICIALES - SISTEMA OLÍMPICO DE DESEMPATE ⚠️
    </div>
    """, unsafe_allow_html=True)
    
    if region_view == "📊 Resumen General":
        show_general_summary(grupos, regiones_disponibles)
    else:
        region_name = region_view.replace("📍 ", "")
        show_region_details(grupos, region_name)

def show_general_summary(grupos, regiones):
    """Muestra resumen general de todas las regiones"""
    st.markdown("## 📊 Resumen General por Regiones")
    
    # Estadísticas por región
    cols = st.columns(min(len(regiones), 4))
    
    for i, region in enumerate(regiones):
        with cols[i % 4]:
            region_grupos = [g for g in grupos if region.upper() in g['nombre'].upper()]
            total_equipos = sum(len(g['clasificacion']) for g in region_grupos)
            invictos = sum(1 for g in region_grupos for equipo in g['clasificacion'] 
                          if equipo['partidos_perdidos'] == 0 and equipo['partidos_jugados'] > 0)
            
            st.metric(
                f"🏀 {region.upper()}",
                f"{len(region_grupos)} zonas",
                f"{total_equipos} equipos"
            )
            st.caption(f"🏆 {invictos} invictos")
    
    # Mejores equipos por categoría
    st.markdown("### 🏆 Equipos Destacados")
    
    # Encontrar los mejores equipos
    todos_equipos = []
    for grupo in grupos:
        for equipo in grupo['clasificacion']:
            equipo_info = {**equipo, 'zona': grupo['nombre']}
            equipo_info['diferencia'] = equipo['puntos_favor'] - equipo['puntos_contra']
            todos_equipos.append(equipo_info)
    
    # Mejores por diferentes criterios
    col1, col2, col3 = st.columns(3)
    
    with col1:
        mejor_record = max(todos_equipos, key=lambda x: (x['puntos_totales'], x['diferencia']))
        st.success(f"""
        **🥇 Mejor Récord**
        {mejor_record['equipo']}
        {mejor_record['zona']}
        {mejor_record['partidos_ganados']}-{mejor_record['partidos_perdidos']} ({mejor_record['puntos_totales']} pts)
        """)
    
    with col2:
        mejor_ataque = max(todos_equipos, key=lambda x: x['puntos_favor'])
        st.info(f"""
        **⚡ Mejor Ataque**
        {mejor_ataque['equipo']}
        {mejor_ataque['zona']}
        {mejor_ataque['puntos_favor']} puntos a favor
        """)
    
    with col3:
        mejor_defensa = min(todos_equipos, key=lambda x: x['puntos_contra'])
        st.warning(f"""
        **🛡️ Mejor Defensa**
        {mejor_defensa['equipo']}
        {mejor_defensa['zona']}
        {mejor_defensa['puntos_contra']} puntos en contra
        """)
    
    # Equipos invictos
    invictos = [e for e in todos_equipos if e['partidos_perdidos'] == 0 and e['partidos_jugados'] > 0]
    if invictos:
        st.markdown("### 🏆 Equipos Invictos")
        invictos_sorted = sorted(invictos, key=lambda x: (-x['puntos_totales'], -x['diferencia']))
        
        for equipo in invictos_sorted[:10]:  # Top 10 invictos
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.write(f"**{equipo['equipo']}** ({equipo['zona']})")
            with col2:
                st.write(f"{equipo['partidos_ganados']}-0")
            with col3:
                st.write(f"{equipo['puntos_totales']} pts")
            with col4:
                st.write(f"{equipo['diferencia']:+d}")

def show_region_details(grupos, region_name):
    """Muestra detalles de una región específica"""
    st.markdown(f"## 📍 REGIÓN {region_name.upper()}")
    
    # Clasificar equipos de la región
    primeros, segundos, terceros = classify_teams_by_region(grupos, region_name)
    
    # Información de clasificación
    with st.expander("📋 Sistema de Clasificación", expanded=False):
        if region_name.upper() == "SUR":
            st.info("**SUR (7 zonas):** Los 2 mejores de cada zona + los 2 mejores 3eros = 16 clasificados")
            terceros_clasifican = 2
        else:
            st.info("**NORTE/CENTRO/OESTE (6 zonas c/u):** Los 2 mejores de cada zona + los 4 mejores 3eros = 16 clasificados")
            terceros_clasifican = 4
        
        st.markdown("**⚖️ Desempate Olímpico:** Puntos → Diferencia → Puntos a favor → Enfrentamiento directo")
    
    # Mostrar clasificaciones
    if primeros:
        show_team_table(primeros, "🥇 Primeros Lugares (Clasificados Directos)")
    
    if segundos:
        show_team_table(segundos, "🥈 Segundos Lugares (Clasificados Directos)")
    
    if terceros:
        show_team_table(terceros, f"🥉 Mejores Terceros ({terceros_clasifican if region_name.upper() != 'SUR' else 2} clasifican)", 
                       terceros_clasifican if region_name.upper() != 'SUR' else 2)
    
    # Estadísticas de la región
    st.markdown("### 📈 Estadísticas de la Región")
    region_grupos = [g for g in grupos if region_name.upper() in g['nombre'].upper()]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_equipos = sum(len(g['clasificacion']) for g in region_grupos)
        st.metric("Total Equipos", total_equipos)
    
    with col2:
        invictos = len([e for e in primeros + segundos + terceros 
                       if e['partidos_perdidos'] == 0 and e['partidos_jugados'] > 0])
        st.metric("Equipos Invictos", invictos)
    
    with col3:
        st.metric("Zonas", len(region_grupos))

if __name__ == "__main__":
    main()
