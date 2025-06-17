import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import random

# Configuración de la página
st.set_page_config(
    page_title="Copa FeBAMBA - Clasificaciones y Playoffs",
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

.playoff-header {
    background: linear-gradient(135deg, #e74c3c, #c0392b);
    color: white;
    padding: 1rem;
    border-radius: 10px 10px 0 0;
    text-align: center;
    font-weight: bold;
}

.zona-playoff-header {
    background: linear-gradient(135deg, #8e44ad, #9b59b6);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    margin: 1rem 0;
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

.playoff-card {
    background: white;
    border: 2px solid #e74c3c;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.team-superior {
    background: linear-gradient(135deg, #27ae60, #2ecc71);
    color: white;
    padding: 0.5rem;
    border-radius: 5px;
    margin: 0.25rem 0;
}

.team-inferior {
    background: linear-gradient(135deg, #e67e22, #f39c12);
    color: white;
    padding: 0.5rem;
    border-radius: 5px;
    margin: 0.25rem 0;
}

.vs-separator {
    text-align: center;
    font-size: 1.2rem;
    font-weight: bold;
    color: #e74c3c;
    margin: 0.25rem 0;
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

/* Estilos para el bracket de playoffs */
.bracket-container {
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    padding: 2rem;
    border-radius: 15px;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}

.bracket-round {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    min-height: 600px;
    margin: 0 1rem;
}

.bracket-game {
    background: white;
    border: 2px solid #e74c3c;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 6px 20px rgba(231, 76, 60, 0.15);
    transition: all 0.3s ease;
    position: relative;
}

.bracket-game:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(231, 76, 60, 0.25);
}

.game-header {
    text-align: center;
    font-weight: bold;
    color: #e74c3c;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.bracket-team {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    border-radius: 8px;
    margin: 0.25rem 0;
    font-weight: 500;
    transition: all 0.2s ease;
}

.bracket-team:hover {
    transform: scale(1.02);
}

.team-seed-1-4 {
    background: linear-gradient(135deg, #28a745, #20c997);
    color: white;
    border-left: 4px solid #155724;
}

.team-seed-5-8 {
    background: linear-gradient(135deg, #17a2b8, #6f42c1);
    color: white;
    border-left: 4px solid #0c5460;
}

.team-seed-9-12 {
    background: linear-gradient(135deg, #ffc107, #fd7e14);
    color: #212529;
    border-left: 4px solid #856404;
}

.team-seed-13-16 {
    background: linear-gradient(135deg, #dc3545, #e83e8c);
    color: white;
    border-left: 4px solid #721c24;
}

.team-info {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.team-name {
    font-weight: bold;
    font-size: 1rem;
    margin-bottom: 0.2rem;
}

.team-details {
    font-size: 0.85rem;
    opacity: 0.9;
}

.team-seed {
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 0.3rem 0.6rem;
    border-radius: 50%;
    font-weight: bold;
    font-size: 0.9rem;
    min-width: 2rem;
    text-align: center;
    margin-right: 0.75rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.bracket-vs {
    text-align: center;
    font-weight: bold;
    color: #e74c3c;
    font-size: 1.1rem;
    margin: 0.25rem 0;
    text-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.round-title {
    text-align: center;
    background: linear-gradient(135deg, #6f42c1, #e83e8c);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    font-weight: bold;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(111, 66, 193, 0.3);
}

.future-round {
    background: linear-gradient(135deg, #6c757d, #495057);
    color: white;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    margin: 0.5rem 0;
    font-weight: 500;
    opacity: 0.8;
}

.champion-spot {
    background: linear-gradient(135deg, #ffd700, #ffed4e);
    color: #212529;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    font-weight: bold;
    font-size: 1.2rem;
    box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
    border: 3px solid #ffc107;
}

.playoff-button {
    background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-weight: bold !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3) !important;
}

.playoff-button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4) !important;
    background: linear-gradient(135deg, #c0392b, #a93226) !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carga los datos desde el archivo JSON"""
    try:
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

def get_zona_from_group_name(group_name):
    """Determina la zona correcta basándose en el nombre del grupo"""
    group_upper = group_name.upper()
    
    if "CENTRO OESTE" in group_upper:
        return "CENTRO"
    elif "NORTE" in group_upper:
        return "NORTE"
    elif "CENTRO" in group_upper:
        return "CENTRO"
    elif "OESTE" in group_upper:
        return "OESTE"
    elif "SUR" in group_upper:
        return "SUR"
    else:
        # Fallback: usar la primera palabra
        return group_name.split()[0].upper()

def get_clasificados_por_zona(grupos, zona):
    """Obtiene los 16 clasificados de una zona específica ordenados correctamente"""
    # Filtrar grupos de la zona
    grupos_zona = [g for g in grupos if get_zona_from_group_name(g['nombre']) == zona]
    
    if not grupos_zona:
        return []
    
    primeros = []
    segundos = []
    terceros = []
    
    # Obtener equipos por posición en cada grupo
    for grupo in grupos_zona:
        clasificacion = sorted(grupo['clasificacion'], key=lambda x: x['posicion'])
        
        if len(clasificacion) >= 1:
            equipo = clasificacion[0].copy()
            equipo['zona_grupo'] = grupo['nombre']
            equipo['tipo_clasificacion'] = "1º puesto"
            primeros.append(equipo)
        
        if len(clasificacion) >= 2:
            equipo = clasificacion[1].copy()
            equipo['zona_grupo'] = grupo['nombre']
            equipo['tipo_clasificacion'] = "2º puesto"
            segundos.append(equipo)
            
        if len(clasificacion) >= 3:
            equipo = clasificacion[2].copy()
            equipo['zona_grupo'] = grupo['nombre']
            equipo['tipo_clasificacion'] = "3º puesto"
            terceros.append(equipo)
    
    # Función para ordenar por puntos, diferencia y puntos a favor
    def sort_teams_by_points(teams):
        return sorted(teams, key=lambda x: (
            -x['puntos_totales'],                           # 1º criterio: puntos totales
            -(x['puntos_favor'] - x['puntos_contra']),      # 2º criterio: diferencia de puntos  
            -x['puntos_favor']                              # 3º criterio: puntos a favor
        ))
    
    # Ordenar cada categoría por separado
    primeros_ordenados = sort_teams_by_points(primeros)
    segundos_ordenados = sort_teams_by_points(segundos)
    terceros_ordenados = sort_teams_by_points(terceros)
    
    # Determinar cuántos terceros clasifican según la zona
    if zona == "SUR":
        terceros_clasifican = 2  # SUR: 7 zonas, 2 terceros
    else:
        terceros_clasifican = 4  # NORTE/CENTRO/OESTE: 6 zonas, 4 terceros
    
    # CORRECCIÓN: Mantener el orden jerárquico correcto
    # 1º TODOS los primeros (ya ordenados por puntos)
    # 2º TODOS los segundos (ya ordenados por puntos)  
    # 3º Los mejores terceros (ya ordenados por puntos)
    clasificados_finales = (
        primeros_ordenados + 
        segundos_ordenados + 
        terceros_ordenados[:terceros_clasifican]
    )
    
    # Asignar posiciones finales de playoff (1-16) manteniendo el orden jerárquico
    for i, equipo in enumerate(clasificados_finales):
        equipo['posicion_playoff'] = i + 1
    
    return clasificados_finales[:16]  # Asegurar máximo 16 equipos

def generate_playoff_matchups(clasificados):
    """Genera los enfrentamientos de playoff: 1vs16, 2vs15, etc."""
    if len(clasificados) != 16:
        return []
    
    enfrentamientos = []
    
    # Crear enfrentamientos: 1vs16, 2vs15, 3vs14, etc.
    for i in range(8):
        superior = clasificados[i]
        inferior = clasificados[15 - i]
        
        enfrentamiento = {
            'numero': i + 1,
            'equipo_superior': {
                'nombre': superior['equipo'],
                'posicion': superior['posicion_playoff'],
                'zona_grupo': superior['zona_grupo'],
                'tipo': superior['tipo_clasificacion'],
                'record': f"{superior['partidos_ganados']}-{superior['partidos_perdidos']}",
                'puntos_totales': superior['puntos_totales'],
                'diferencia': superior['puntos_favor'] - superior['puntos_contra']
            },
            'equipo_inferior': {
                'nombre': inferior['equipo'],
                'posicion': inferior['posicion_playoff'],
                'zona_grupo': inferior['zona_grupo'],
                'tipo': inferior['tipo_clasificacion'],
                'record': f"{inferior['partidos_ganados']}-{inferior['partidos_perdidos']}",
                'puntos_totales': inferior['puntos_totales'],
                'diferencia': inferior['puntos_favor'] - inferior['puntos_contra']
            }
        }
        
        enfrentamientos.append(enfrentamiento)
    
    return enfrentamientos

def get_team_seed_class(posicion):
    """Obtiene la clase CSS según la posición del equipo"""
    if posicion <= 4:
        return "team-seed-1-4"
    elif posicion <= 8:
        return "team-seed-5-8"
    elif posicion <= 12:
        return "team-seed-9-12"
    else:
        return "team-seed-13-16"

def show_playoff_bracket_modal(enfrentamientos, zona):
    """Muestra el bracket de playoffs con diseño tipo modal"""
    
    # Header prominente tipo modal
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #e74c3c, #c0392b); 
        color: white; 
        padding: 2rem; 
        border-radius: 15px; 
        text-align: center; 
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(231, 76, 60, 0.3);
        border: 2px solid #ffffff;
    ">
        <h1 style="margin: 0; font-size: 2.5rem;">🏆 PLAYOFFS ZONA {zona}</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Bracket Eliminatorio • 16 Equipos • Partido Único
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if not enfrentamientos:
        st.error("❌ No hay enfrentamientos disponibles")
        return
    
    # Crear contenedor tipo modal
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8f9fa, #e9ecef); 
        padding: 2rem; 
        border-radius: 15px; 
        margin: 1rem 0;
        border: 1px solid #dee2e6;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    ">
    """, unsafe_allow_html=True)
    
    # Dividir en pestañas
    tab1, tab2, tab3 = st.tabs(["🏀 Octavos de Final", "🏆 Rondas Siguientes", "📊 Análisis"])
    
    with tab1:
        st.markdown("### ⚔️ ENFRENTAMIENTOS ELIMINATORIOS")
        
        # Mostrar todos los octavos en un grid
        for i in range(0, len(enfrentamientos), 2):
            col1, col2 = st.columns(2)
            
            # Partido de la columna izquierda
            with col1:
                if i < len(enfrentamientos):
                    enfrentamiento = enfrentamientos[i]
                    superior = enfrentamiento['equipo_superior']
                    inferior = enfrentamiento['equipo_inferior']
                    
                    # Container del partido
                    st.markdown(f"""
                    <div style="
                        background: white; 
                        border-radius: 12px; 
                        padding: 1.5rem; 
                        margin: 0.5rem 0;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                        border-left: 5px solid #e74c3c;
                    ">
                        <h4 style="color: #e74c3c; margin: 0 0 1rem 0; text-align: center;">
                            ⚡ PARTIDO {i+1}
                        </h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Equipo superior
                    if superior['posicion'] <= 4:
                        st.success(f"🥇 **SEED #{superior['posicion']} - {superior['nombre']}**")
                    elif superior['posicion'] <= 8:
                        st.info(f"🥈 **SEED #{superior['posicion']} - {superior['nombre']}**")
                    else:
                        st.warning(f"🥉 **SEED #{superior['posicion']} - {superior['nombre']}**")
                    
                    st.caption(f"📊 {superior['record']} • {superior['puntos_totales']} pts • {superior['tipo']}")
                    
                    # VS
                    st.markdown("**<center>⚔️ VERSUS ⚔️</center>**", unsafe_allow_html=True)
                    
                    # Equipo inferior
                    if inferior['posicion'] >= 13:
                        st.error(f"💥 **SEED #{inferior['posicion']} - {inferior['nombre']}**")
                    elif inferior['posicion'] >= 9:
                        st.warning(f"⚡ **SEED #{inferior['posicion']} - {inferior['nombre']}**")
                    else:
                        st.info(f"🎯 **SEED #{inferior['posicion']} - {inferior['nombre']}**")
                    
                    st.caption(f"📊 {inferior['record']} • {inferior['puntos_totales']} pts • {inferior['tipo']}")
            
            # Partido de la columna derecha
            with col2:
                if i + 1 < len(enfrentamientos):
                    enfrentamiento = enfrentamientos[i + 1]
                    superior = enfrentamiento['equipo_superior']
                    inferior = enfrentamiento['equipo_inferior']
                    
                    # Container del partido
                    st.markdown(f"""
                    <div style="
                        background: white; 
                        border-radius: 12px; 
                        padding: 1.5rem; 
                        margin: 0.5rem 0;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                        border-left: 5px solid #e74c3c;
                    ">
                        <h4 style="color: #e74c3c; margin: 0 0 1rem 0; text-align: center;">
                            ⚡ PARTIDO {i+2}
                        </h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Equipo superior
                    if superior['posicion'] <= 4:
                        st.success(f"🥇 **SEED #{superior['posicion']} - {superior['nombre']}**")
                    elif superior['posicion'] <= 8:
                        st.info(f"🥈 **SEED #{superior['posicion']} - {superior['nombre']}**")
                    else:
                        st.warning(f"🥉 **SEED #{superior['posicion']} - {superior['nombre']}**")
                    
                    st.caption(f"📊 {superior['record']} • {superior['puntos_totales']} pts • {superior['tipo']}")
                    
                    # VS
                    st.markdown("**<center>⚔️ VERSUS ⚔️</center>**", unsafe_allow_html=True)
                    
                    # Equipo inferior
                    if inferior['posicion'] >= 13:
                        st.error(f"💥 **SEED #{inferior['posicion']} - {inferior['nombre']}**")
                    elif inferior['posicion'] >= 9:
                        st.warning(f"⚡ **SEED #{inferior['posicion']} - {inferior['nombre']}**")
                    else:
                        st.info(f"🎯 **SEED #{inferior['posicion']} - {inferior['nombre']}**")
                    
                    st.caption(f"📊 {inferior['record']} • {inferior['puntos_totales']} pts • {inferior['tipo']}")
    
    with tab2:
        st.markdown("### 🏆 CAMINO AL TÍTULO")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### ⚡ CUARTOS DE FINAL")
            cuartos = [
                ("Ganador P1", "Ganador P8"),
                ("Ganador P2", "Ganador P7"),
                ("Ganador P3", "Ganador P6"),
                ("Ganador P4", "Ganador P5")
            ]
            
            for i, (equipo1, equipo2) in enumerate(cuartos):
                st.info(f"**Cuarto {i+1}**  \n{equipo1}  \n🆚  \n{equipo2}")
        
        with col2:
            st.markdown("#### 🔥 SEMIFINALES")
            semis = [
                ("Ganador C1", "Ganador C4"),
                ("Ganador C2", "Ganador C3")
            ]
            
            for i, (equipo1, equipo2) in enumerate(semis):
                st.warning(f"**Semifinal {i+1}**  \n{equipo1}  \n🆚  \n{equipo2}")
        
        with col3:
            st.markdown("#### 👑 FINAL")
            st.success("**GRAN FINAL**  \nGanador SF1  \n🆚  \nGanador SF2")
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #ffd700, #ffed4e); 
                color: #212529; 
                padding: 1.5rem; 
                border-radius: 15px; 
                text-align: center; 
                margin-top: 1rem; 
                border: 3px solid #ffc107;
                box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
            ">
                <h3 style="margin: 0;">👑 CAMPEÓN</h3>
                <h2 style="margin: 0.5rem 0 0 0;">ZONA {zona}</h2>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📊 ANÁLISIS DEL BRACKET")
        
        # Análisis de seeds
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 FAVORITOS (Seeds 1-4)")
            mejores_seeds = sorted(enfrentamientos, key=lambda x: x['equipo_superior']['posicion'])[:4]
            for i, enf in enumerate(mejores_seeds):
                superior = enf['equipo_superior']
                st.success(f"**#{superior['posicion']} {superior['nombre']}**")
                st.caption(f"📊 {superior['record']} • Diferencia: {superior['diferencia']:+d}")
        
        with col2:
            st.markdown("#### 💥 DARK HORSES (Seeds 13-16)")
            equipos_bajos = [enf['equipo_inferior'] for enf in enfrentamientos if enf['equipo_inferior']['posicion'] >= 13]
            equipos_bajos.sort(key=lambda x: -x['puntos_totales'])
            for equipo in equipos_bajos:
                st.error(f"**#{equipo['posicion']} {equipo['nombre']}**")
                st.caption(f"📊 {equipo['record']} • Diferencia: {equipo['diferencia']:+d}")
        
        # Métricas del bracket
        st.markdown("#### 📈 MÉTRICAS DEL BRACKET")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            seeds_top = len([e for e in enfrentamientos if e['equipo_superior']['posicion'] <= 4])
            st.metric("🥇 Top Seeds", seeds_top)
        
        with col2:
            seeds_bajo = len([e for e in enfrentamientos if e['equipo_inferior']['posicion'] >= 13])
            st.metric("💥 Underdogs", seeds_bajo)
        
        with col3:
            promedio_sup = sum(e['equipo_superior']['puntos_totales'] for e in enfrentamientos) / len(enfrentamientos)
            st.metric("📊 Promedio Superior", f"{promedio_sup:.1f}")
        
        with col4:
            promedio_inf = sum(e['equipo_inferior']['puntos_totales'] for e in enfrentamientos) / len(enfrentamientos)
            st.metric("📊 Promedio Inferior", f"{promedio_inf:.1f}")
        
        # Partidos interesantes
        st.markdown("#### 🎯 PARTIDOS PARA VIGILAR")
        partidos_interesantes = []
        for enf in enfrentamientos:
            superior = enf['equipo_superior']
            inferior = enf['equipo_inferior']
            
            if inferior['puntos_totales'] >= superior['puntos_totales'] * 0.85:
                partidos_interesantes.append({
                    'partido': f"P{enf['numero']}",
                    'descripcion': f"#{superior['posicion']} {superior['nombre']} vs #{inferior['posicion']} {inferior['nombre']}",
                    'razon': f"Diferencia de solo {superior['puntos_totales'] - inferior['puntos_totales']} puntos"
                })
        
        if partidos_interesantes:
            for partido in partidos_interesantes:
                st.warning(f"**{partido['partido']}:** {partido['descripcion']}")
                st.caption(f"⚠️ {partido['razon']}")
        else:
            st.info("No hay partidos especialmente parejos detectados")
    
    st.markdown("</div>", unsafe_allow_html=True)

def show_playoff_bracket(enfrentamientos, zona):
    """Muestra el bracket completo de playoffs de forma visual"""
    st.markdown(f"#### 🏆 BRACKET DE PLAYOFFS - ZONA {zona}")
    
    if not enfrentamientos:
        st.warning("No hay enfrentamientos disponibles")
        return
    
    # Crear el bracket visual usando columnas de Streamlit
    st.markdown("##### 🥇 PRIMERA RONDA - OCTAVOS DE FINAL")
    
    # Dividir en dos columnas para mejor visualización
    col1, col2 = st.columns(2)
    
    # Primera mitad (enfrentamientos 1-4)
    with col1:
        st.markdown("**🔥 ZONA SUPERIOR**")
        for i in range(0, 4):
            if i < len(enfrentamientos):
                enfrentamiento = enfrentamientos[i]
                superior = enfrentamiento['equipo_superior']
                inferior = enfrentamiento['equipo_inferior']
                
                # Crear una caja visual para cada enfrentamiento
                with st.container():
                    st.markdown(f"""
                    **Partido {i+1}**
                    """)
                    
                    # Equipo superior (mejor clasificado)
                    st.success(f"🥇 **#{superior['posicion']} {superior['nombre']}**  \n"
                              f"📊 {superior['record']} ({superior['puntos_totales']} pts)  \n"  
                              f"📍 {superior['zona_grupo']}")
                    
                    st.markdown("<div style='text-align: center; font-weight: bold; color: red;'>⚔️ VS ⚔️</div>", 
                               unsafe_allow_html=True)
                    
                    # Equipo inferior (peor clasificado)
                    st.warning(f"📍 **#{inferior['posicion']} {inferior['nombre']}**  \n"
                              f"📊 {inferior['record']} ({inferior['puntos_totales']} pts)  \n"
                              f"📍 {inferior['zona_grupo']}")
                    
                    st.markdown("---")
    
    # Segunda mitad (enfrentamientos 5-8)
    with col2:
        st.markdown("**🔥 ZONA INFERIOR**")
        for i in range(4, 8):
            if i < len(enfrentamientos):
                enfrentamiento = enfrentamientos[i]
                superior = enfrentamiento['equipo_superior']
                inferior = enfrentamiento['equipo_inferior']
                
                # Crear una caja visual para cada enfrentamiento
                with st.container():
                    st.markdown(f"""
                    **Partido {i+1}**
                    """)
                    
                    # Equipo superior (mejor clasificado)
                    st.success(f"🥇 **#{superior['posicion']} {superior['nombre']}**  \n"
                              f"📊 {superior['record']} ({superior['puntos_totales']} pts)  \n"
                              f"📍 {superior['zona_grupo']}")
                    
                    st.markdown("<div style='text-align: center; font-weight: bold; color: red;'>⚔️ VS ⚔️</div>", 
                               unsafe_allow_html=True)
                    
                    # Equipo inferior (peor clasificado)
                    st.warning(f"📍 **#{inferior['posicion']} {inferior['nombre']}**  \n"
                              f"📊 {inferior['record']} ({inferior['puntos_totales']} pts)  \n"
                              f"📍 {inferior['zona_grupo']}")
                    
                    st.markdown("---")
    
    # Mostrar siguiente ronda (visual)
    st.markdown("##### 🏆 PRÓXIMAS RONDAS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **⚡ CUARTOS DE FINAL**
        - Ganador P1 vs Ganador P8
        - Ganador P2 vs Ganador P7  
        - Ganador P3 vs Ganador P6
        - Ganador P4 vs Ganador P5
        """)
    
    with col2:
        st.info("""
        **🔥 SEMIFINALES**
        - Ganador CF1 vs Ganador CF4
        - Ganador CF2 vs Ganador CF3
        """)
    
    with col3:
        st.info("""
        **🏆 FINAL**
        - Ganador SF1 vs Ganador SF2
        
        **👑 CAMPEÓN ZONAL**
        """)
    
    # Mostrar estadísticas del bracket
    with st.expander(f"📊 Estadísticas del Bracket - Zona {zona}", expanded=False):
        # Top seeds
        mejores_seeds = sorted(enfrentamientos, key=lambda x: x['equipo_superior']['posicion'])[:4]
        st.markdown("**🥇 Mejores Clasificados (Seeds 1-4):**")
        
        for i, enf in enumerate(mejores_seeds):
            superior = enf['equipo_superior']
            st.write(f"**#{superior['posicion']} {superior['nombre']}** - {superior['record']} ({superior['diferencia']:+d})")
        
        # Equipos peligrosos (seeds bajos pero con buen récord)
        st.markdown("**⚡ Equipos Peligrosos (Seeds 13-16):**")
        equipos_bajos = [enf['equipo_inferior'] for enf in enfrentamientos if enf['equipo_inferior']['posicion'] >= 13]
        equipos_bajos.sort(key=lambda x: -x['puntos_totales'])
        
        for equipo in equipos_bajos[:4]:
            st.write(f"**#{equipo['posicion']} {equipo['nombre']}** - {equipo['record']} ({equipo['diferencia']:+d})")
    
    st.markdown("---")

def show_playoffs_section(categoria_data, formato_playoff):
    """Muestra la sección completa de playoffs por zona"""
    st.markdown(f"""
    <div class="playoff-header">
        <h2>🏆 PLAYOFFS - {categoria_data['categoria']}</h2>
        <p>Enfrentamientos por zona: 1vs16, 2vs15, 3vs14, 4vs13, 5vs12, 6vs11, 7vs10, 8vs9</p>
    </div>
    """, unsafe_allow_html=True)
    
    grupos = categoria_data['grupos']
    
    # Obtener todas las zonas disponibles
    zonas_disponibles = list(set([get_zona_from_group_name(g['nombre']) for g in grupos]))
    zonas_disponibles.sort()
    
    # Mostrar información general
    st.markdown("### 📊 Información General")
    st.info("**Sistema de Playoffs:** Cada zona clasifica 16 equipos (primeros + segundos + mejores terceros) que se enfrentan en eliminación directa a partido único.")
    
    # Procesar cada zona
    for zona in zonas_disponibles:
        st.markdown(f"""
        <div class="zona-playoff-header">
            <h3>🏀 ZONA {zona} - PLAYOFFS</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Obtener clasificados de la zona
        clasificados = get_clasificados_por_zona(grupos, zona)
        
        if len(clasificados) < 16:
            st.warning(f"⚠️ Zona {zona}: Solo {len(clasificados)} equipos clasificados. Se necesitan 16 para playoffs completos.")
            continue
        
        # Mostrar estadísticas de la zona
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            primeros = len([e for e in clasificados if e['tipo_clasificacion'] == "1º puesto"])
            st.metric("Primeros", primeros)
        
        with col2:
            segundos = len([e for e in clasificados if e['tipo_clasificacion'] == "2º puesto"])
            st.metric("Segundos", segundos)
        
        with col3:
            terceros = len([e for e in clasificados if e['tipo_clasificacion'] == "3º puesto"])
            st.metric("Terceros", terceros)
        
        with col4:
            invictos = len([e for e in clasificados if e['partidos_perdidos'] == 0])
            st.metric("Invictos", invictos)
        
        # Generar enfrentamientos
        enfrentamientos = generate_playoff_matchups(clasificados)
        
        if enfrentamientos:
            # Mostrar bracket visual completo
            show_playoff_bracket(enfrentamientos, zona)
        
        # Mostrar tabla de clasificados
        with st.expander(f"📋 Ver tabla completa de clasificados - Zona {zona}", expanded=False):
            data = []
            for equipo in clasificados:
                data.append({
                    'Pos': equipo['posicion_playoff'],
                    'Equipo': equipo['equipo'],
                    'Grupo': equipo['zona_grupo'],
                    'Tipo': equipo['tipo_clasificacion'],
                    'J': equipo['partidos_jugados'],
                    'G': equipo['partidos_ganados'],
                    'P': equipo['partidos_perdidos'],
                    'PF': equipo['puntos_favor'],
                    'PC': equipo['puntos_contra'],
                    'Diff': f"{equipo['puntos_favor'] - equipo['puntos_contra']:+d}",
                    'Pts': equipo['puntos_totales']
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        
        st.markdown("---")

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
    region_grupos = [g for g in grupos if get_zona_from_group_name(g['nombre']) == region_name.upper()]
    
    primeros = []
    segundos = []
    terceros = []
    
    # Obtener equipos por posición en cada grupo
    for grupo in region_grupos:
        # Tomar clasificacion tal como viene del JSON (ya tiene las posiciones correctas por grupo)
        clasificacion = grupo['clasificacion']  
        
        # Encontrar por posición, no por índice
        primer_puesto = next((equipo for equipo in clasificacion if equipo['posicion'] == 1), None)
        segundo_puesto = next((equipo for equipo in clasificacion if equipo['posicion'] == 2), None)  
        tercer_puesto = next((equipo for equipo in clasificacion if equipo['posicion'] == 3), None)
        
        if primer_puesto:
            equipo = primer_puesto.copy()
            equipo['zona'] = grupo['nombre']
            primeros.append(equipo)
            
        if segundo_puesto:
            equipo = segundo_puesto.copy() 
            equipo['zona'] = grupo['nombre']
            segundos.append(equipo)
            
        if tercer_puesto:
            equipo = tercer_puesto.copy()
            equipo['zona'] = grupo['nombre'] 
            terceros.append(equipo)
    
    # Función para ordenar por puntos (dentro de cada categoría)
    def sort_teams_by_performance(teams):
        return sorted(teams, key=lambda x: (
            -x['puntos_totales'],                           # 1º: Puntos totales (más puntos primero)
            -(x['puntos_favor'] - x['puntos_contra']),      # 2º: Diferencia de puntos (mejor diferencia primero)  
            -x['puntos_favor']                              # 3º: Puntos a favor (más puntos a favor primero)
        ))
    
    # Ordenar cada categoría por separado (MANTENER JERARQUÍA)
    primeros_ordenados = sort_teams_by_performance(primeros)
    segundos_ordenados = sort_teams_by_performance(segundos)
    terceros_ordenados = sort_teams_by_performance(terceros)
    
    return primeros_ordenados, segundos_ordenados, terceros_ordenados

def show_team_table(teams, title, classification_spots=None):
    """Muestra tabla de equipos con formato"""
    if not teams:
        st.info(f"No hay datos para {title}")
        return
    
    data = []
    for i, team in enumerate(teams):
        diff = calculate_diff(team['puntos_favor'], team['puntos_contra'])
        racha_formatted = format_racha(team['racha'])
        
        estado = "✅ CLASIFICA"
        if classification_spots and i >= classification_spots:
            estado = "❌ ELIMINADO"
        
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
    
    st.markdown(f"### {title}")
    
    if classification_spots:
        def highlight_rows(row):
            if row.name < 2:
                return ['background-color: #d4edda'] * len(row)
            elif classification_spots and row.name < classification_spots:
                return ['background-color: #fff3cd'] * len(row)
            else:
                return ['background-color: #f8d7da; opacity: 0.7'] * len(row)
        
        styled_df = df.style.apply(highlight_rows, axis=1)
    else:
        styled_df = df.style.apply(lambda x: ['background-color: #d4edda'] * len(x), axis=1)
    
    st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)

def show_general_summary(grupos, regiones):
    """Muestra resumen general de todas las regiones"""
    st.markdown("## 📊 Resumen General por Regiones")
    
    cols = st.columns(min(len(regiones), 4))
    
    for i, region in enumerate(regiones):
        with cols[i % 4]:
            region_grupos = [g for g in grupos if get_zona_from_group_name(g['nombre']) == region.upper()]
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
    
    todos_equipos = []
    for grupo in grupos:
        for equipo in grupo['clasificacion']:
            equipo_info = {**equipo, 'zona': grupo['nombre']}
            equipo_info['diferencia'] = equipo['puntos_favor'] - equipo['puntos_contra']
            todos_equipos.append(equipo_info)
    
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
        
        for equipo in invictos_sorted[:10]:
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
    
    # Inicializar estado de sesión para controlar la vista de playoffs
    if f"show_playoffs_{region_name}" not in st.session_state:
        st.session_state[f"show_playoffs_{region_name}"] = False
    
    primeros, segundos, terceros = classify_teams_by_region(grupos, region_name)
    
    # Botones para alternar entre vistas
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        if st.button(f"🏆 Ver Playoffs", key=f"show_playoff_btn_{region_name}", 
                    help="Ver bracket completo de playoffs para esta región",
                    use_container_width=True):
            st.session_state[f"show_playoffs_{region_name}"] = True
    
    with col3:
        if st.button(f"📊 Ver Clasificación", key=f"show_classification_btn_{region_name}", 
                    help="Volver a ver las clasificaciones",
                    use_container_width=True):
            st.session_state[f"show_playoffs_{region_name}"] = False
    
    # Mostrar contenido según el estado
    if st.session_state[f"show_playoffs_{region_name}"]:
        # Vista de Playoffs
        st.markdown("---")
        
        # Obtener clasificados para playoffs
        clasificados = get_clasificados_por_zona(grupos, region_name.upper())
        
        if len(clasificados) >= 16:
            enfrentamientos = generate_playoff_matchups(clasificados)
            if enfrentamientos:
                show_playoff_bracket_modal(enfrentamientos, region_name.upper())
        else:
            st.error(f"⚠️ No hay suficientes equipos clasificados en {region_name.upper()} para generar playoffs completos ({len(clasificados)}/16)")
            
        st.markdown("---")
        
        # Botón para volver
        if st.button("⬅️ Volver a Clasificaciones", key=f"back_btn_{region_name}"):
            st.session_state[f"show_playoffs_{region_name}"] = False
            st.rerun()
    
    else:
        # Vista de Clasificaciones (por defecto)
        with st.expander("📋 Sistema de Clasificación", expanded=False):
            if region_name.upper() == "SUR":
                st.info("**SUR (7 zonas):** Los 2 mejores de cada zona + los 2 mejores 3eros = 16 clasificados")
                terceros_clasifican = 2
            else:
                st.info("**NORTE/CENTRO/OESTE (6 zonas c/u):** Los 2 mejores de cada zona + los 4 mejores 3eros = 16 clasificados")
                terceros_clasifican = 4
            
            st.markdown("**⚖️ Desempate Olímpico:** Puntos → Diferencia → Puntos a favor → Enfrentamiento directo")
        
        if primeros:
            show_team_table(primeros, "🥇 Primeros Lugares (Clasificados Directos)")
        
        if segundos:
            show_team_table(segundos, "🥈 Segundos Lugares (Clasificados Directos)")
        
        if terceros:
            show_team_table(terceros, f"🥉 Mejores Terceros ({terceros_clasifican if region_name.upper() != 'SUR' else 2} clasifican)", 
                           terceros_clasifican if region_name.upper() != 'SUR' else 2)
        
        # Estadísticas de la región
        st.markdown("### 📈 Estadísticas de la Región")
        region_grupos = [g for g in grupos if get_zona_from_group_name(g['nombre']) == region_name.upper()]
        
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

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🏀 COPA FeBAMBA - CLASIFICACIONES Y PLAYOFFS</h1>
        <p>Sistema completo de clasificación y generación de playoffs</p>
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
    
    # Selector de sección principal
    seccion_principal = st.sidebar.radio(
        "Sección Principal:",
        ["📊 Clasificaciones"]
    )
    
    if seccion_principal == "📊 Clasificaciones":
        # Selector de región para clasificaciones
        regiones_disponibles = list(set([get_zona_from_group_name(g['nombre']) for g in grupos]))
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

if __name__ == "__main__":
    main()
