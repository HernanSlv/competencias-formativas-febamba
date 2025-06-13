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
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.team-local {
    background: linear-gradient(135deg, #3498db, #2980b9);
    color: white;
    padding: 0.5rem;
    border-radius: 5px;
    margin: 0.25rem 0;
}

.team-visitante {
    background: linear-gradient(135deg, #95a5a6, #7f8c8d);
    color: white;
    padding: 0.5rem;
    border-radius: 5px;
    margin: 0.25rem 0;
}

.vs-separator {
    text-align: center;
    font-size: 1.5rem;
    font-weight: bold;
    color: #e74c3c;
    margin: 0.5rem 0;
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

.playoff-format-selector {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #e74c3c;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

class PlayoffGenerator:
    def __init__(self):
        self.playoff_formats = {
            '1vs3': 'Primeros vs Terceros cruzados',
            '1vs2': 'Primeros vs Segundos de otras zonas',
            '1vs3vs2': 'Eliminación con 1°, 2° y 3°',
            'round_robin': 'Round Robin por posición'
        }
    
    def get_teams_by_position(self, grupos, positions):
        """Obtiene equipos por posición en cada zona"""
        teams_by_position = {}
        
        for pos in positions:
            teams_by_position[f"pos_{pos}"] = []
        
        for grupo in grupos:
            zona = grupo['nombre']
            standings = sorted(grupo['clasificacion'], key=lambda x: x['posicion'])
            
            for pos in positions:
                if len(standings) >= pos:
                    team = standings[pos - 1].copy()
                    team['zona_origen'] = zona
                    teams_by_position[f"pos_{pos}"].append(team)
        
        return teams_by_position
    
    def sort_teams(self, teams):
        """Ordena equipos por criterios de clasificación"""
        return sorted(teams, key=lambda x: (
            -x['puntos_totales'],
            -x['partidos_ganados'],
            -(x['puntos_favor'] - x['puntos_contra']),
            -x['puntos_favor']
        ))
    
    def format_team_info(self, team, description):
        """Formatea información del equipo"""
        return {
            'equipo': team['equipo'],
            'zona': team['zona_origen'],
            'posicion_zona': team['posicion'],
            'descripcion': description,
            'puntos_totales': team['puntos_totales'],
            'partidos_jugados': team['partidos_jugados'],
            'partidos_ganados': team['partidos_ganados'],
            'partidos_perdidos': team['partidos_perdidos'],
            'diferencia_puntos': team['puntos_favor'] - team['puntos_contra'],
            'puntos_favor': team['puntos_favor'],
            'puntos_contra': team['puntos_contra']
        }
    
    def generate_1vs3_playoffs(self, grupos):
        """Genera playoffs formato 1º vs 3º"""
        teams = self.get_teams_by_position(grupos, [1, 3])
        
        primeros = self.sort_teams(teams['pos_1'])
        terceros = self.sort_teams(teams['pos_3'])
        terceros_invertidos = terceros[::-1]
        
        matchups = []
        min_teams = min(len(primeros), len(terceros))
        
        for i in range(min_teams):
            primero = primeros[i]
            tercero = terceros_invertidos[i]
            
            matchups.append({
                'match_id': i + 1,
                'local': self.format_team_info(primero, f"1º de {primero['zona_origen']}"),
                'visitante': self.format_team_info(tercero, f"3º de {tercero['zona_origen']}"),
                'description': f"#{i+1} de primeros vs #{len(terceros_invertidos)-i} de terceros",
                'fecha': None,
                'hora': None
            })
        
        return {
            'format': '1vs3',
            'description': 'Primeros vs Terceros cruzados',
            'matches': matchups,
            'total_matches': len(matchups),
            'participating_teams': len(matchups) * 2
        }
    
    def generate_1vs2_playoffs(self, grupos):
        """Genera playoffs formato 1º vs 2º"""
        teams = self.get_teams_by_position(grupos, [1, 2])
        
        primeros = self.sort_teams(teams['pos_1'])
        segundos = self.sort_teams(teams['pos_2'])
        segundos_invertidos = segundos[::-1]
        
        matchups = []
        min_teams = min(len(primeros), len(segundos))
        
        for i in range(min_teams):
            primero = primeros[i]
            segundo = segundos_invertidos[i]
            
            matchups.append({
                'match_id': i + 1,
                'local': self.format_team_info(primero, f"1º de {primero['zona_origen']}"),
                'visitante': self.format_team_info(segundo, f"2º de {segundo['zona_origen']}"),
                'description': f"#{i+1} de primeros vs #{len(segundos_invertidos)-i} de segundos",
                'fecha': None,
                'hora': None
            })
        
        return {
            'format': '1vs2',
            'description': 'Primeros vs Segundos cruzados',
            'matches': matchups,
            'total_matches': len(matchups),
            'participating_teams': len(matchups) * 2
        }
    
    def generate_round_robin_playoffs(self, grupos, positions=[1]):
        """Genera playoffs formato todos contra todos por posición"""
        teams = self.get_teams_by_position(grupos, positions)
        
        all_matches = []
        
        for pos in positions:
            pos_teams = self.sort_teams(teams[f'pos_{pos}'])
            
            # Generar todos los enfrentamientos posibles
            for i in range(len(pos_teams)):
                for j in range(i + 1, len(pos_teams)):
                    team1 = pos_teams[i]
                    team2 = pos_teams[j]
                    
                    all_matches.append({
                        'match_id': len(all_matches) + 1,
                        'local': self.format_team_info(team1, f"{pos}º de {team1['zona_origen']}"),
                        'visitante': self.format_team_info(team2, f"{pos}º de {team2['zona_origen']}"),
                        'description': f"Round Robin entre {pos}º puestos",
                        'fecha': None,
                        'hora': None
                    })
        
        return {
            'format': 'round_robin',
            'description': f'Round Robin entre equipos de posiciones {positions}',
            'matches': all_matches,
            'total_matches': len(all_matches),
            'participating_teams': sum(len(teams[f'pos_{pos}']) for pos in positions)
        }
    
    def generate_playoff_schedule(self, playoff_data, start_date=None, days_between=7):
        """Genera calendario de partidos"""
        if not start_date:
            start_date = datetime.now() + timedelta(days=30)  # Empezar en 30 días
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        
        current_date = start_date
        
        for i, match in enumerate(playoff_data['matches']):
            match['fecha'] = current_date.strftime('%Y-%m-%d')
            match['hora'] = f"{random.randint(16, 20)}:{random.choice(['00', '30'])}"
            
            # Avanzar fecha (2-3 partidos por día máximo)
            if (i + 1) % 2 == 0:
                current_date += timedelta(days=1)
        
        return playoff_data

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
            -x['puntos_totales'],
            -(x['puntos_favor'] - x['puntos_contra']),
            -x['puntos_favor']
        ))
        
        if len(clasificacion) >= 1:
            primeros.append({**clasificacion[0], 'zona': grupo['nombre']})
        if len(clasificacion) >= 2:
            segundos.append({**clasificacion[1], 'zona': grupo['nombre']})
        if len(clasificacion) >= 3:
            terceros.append({**clasificacion[2], 'zona': grupo['nombre']})
    
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

def show_playoff_matchup(match):
    """Muestra un enfrentamiento de playoff"""
    local = match['local']
    visitante = match['visitante']
    
    with st.container():
        st.markdown(f"""
        <div class="playoff-card">
            <h4 style="text-align: center; color: #e74c3c;">ENFRENTAMIENTO #{match['match_id']}</h4>
            
            <div class="team-local">
                <strong>🏠 LOCAL: {local['equipo']}</strong><br>
                📍 {local['descripcion']}<br>
                📊 Record: {local['partidos_ganados']}G-{local['partidos_perdidos']}P ({local['puntos_totales']} pts)<br>
                ⚖️ Diferencia: {local['diferencia_puntos']:+d} puntos
            </div>
            
            <div class="vs-separator">VS</div>
            
            <div class="team-visitante">
                <strong>✈️ VISITANTE: {visitante['equipo']}</strong><br>
                📍 {visitante['descripcion']}<br>
                📊 Record: {visitante['partidos_ganados']}G-{visitante['partidos_perdidos']}P ({visitante['puntos_totales']} pts)<br>
                ⚖️ Diferencia: {visitante['diferencia_puntos']:+d} puntos
            </div>
            
            <div style="text-align: center; margin-top: 1rem; font-style: italic; color: #666;">
                {match['description']}
                {f"<br>📅 {match['fecha']} - {match['hora']}" if match.get('fecha') else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_playoffs_section(categoria_data):
    """Muestra la sección completa de playoffs"""
    st.markdown(f"""
    <div class="playoff-header">
        <h2>🏆 SISTEMA DE PLAYOFFS - {categoria_data['categoria']}</h2>
        <p>Generación automática de enfrentamientos</p>
    </div>
    """, unsafe_allow_html=True)
    
    grupos = categoria_data['grupos']
    generator = PlayoffGenerator()
    
    # Selector de formato de playoff
    st.markdown("""
    <div class="playoff-format-selector">
        <h4>⚔️ Selecciona el Formato de Playoff</h4>
    </div>
    """, unsafe_allow_html=True)
    
    format_options = {
        '1vs3': '🥇vs🥉 Primeros vs Terceros (Recomendado)',
        '1vs2': '🥇vs🥈 Primeros vs Segundos',
        'round_robin': '🔄 Round Robin - Todos contra todos'
    }
    
    selected_format = st.selectbox(
        "Formato de Playoff:",
        list(format_options.keys()),
        format_func=lambda x: format_options[x],
        index=0
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        generate_schedule = st.checkbox("📅 Generar calendario", value=False)
        if generate_schedule:
            start_date = st.date_input(
                "Fecha de inicio:",
                value=datetime.now() + timedelta(days=30)
            )
    
    # Generar playoffs según formato seleccionado
    if st.button("🔥 GENERAR PLAYOFFS", type="primary"):
        with st.spinner("Generando playoffs..."):
            if selected_format == '1vs3':
                playoff_data = generator.generate_1vs3_playoffs(grupos)
            elif selected_format == '1vs2':
                playoff_data = generator.generate_1vs2_playoffs(grupos)
            elif selected_format == 'round_robin':
                playoff_data = generator.generate_round_robin_playoffs(grupos, [1])
            
            # Generar calendario si está seleccionado
            if generate_schedule:
                playoff_data = generator.generate_playoff_schedule(playoff_data, start_date.strftime('%Y-%m-%d'))
        
        # Mostrar estadísticas del playoff
        st.markdown("### 📊 Resumen del Playoff")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Formato", playoff_data['description'])
        with col2:
            st.metric("Total Partidos", playoff_data['total_matches'])
        with col3:
            st.metric("Equipos Participantes", playoff_data['participating_teams'])
        
        # Mostrar enfrentamientos
        st.markdown("### ⚔️ Enfrentamientos")
        
        # Tabs para organizar por fechas si hay calendario
        if playoff_data['matches'] and playoff_data['matches'][0].get('fecha'):
            fechas = list(set(match['fecha'] for match in playoff_data['matches']))
            fechas.sort()
            
            if len(fechas) > 1:
                tabs = st.tabs([f"📅 {fecha}" for fecha in fechas])
                
                for i, fecha in enumerate(fechas):
                    with tabs[i]:
                        matches_fecha = [m for m in playoff_data['matches'] if m['fecha'] == fecha]
                        for match in matches_fecha:
                            show_playoff_matchup(match)
            else:
                for match in playoff_data['matches']:
                    show_playoff_matchup(match)
        else:
            for match in playoff_data['matches']:
                show_playoff_matchup(match)
        
        # Exportar datos
        with st.expander("💾 Exportar Datos del Playoff", expanded=False):
            playoff_json = json.dumps(playoff_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="⬇️ Descargar JSON",
                data=playoff_json,
                file_name=f"playoff_{categoria_data['categoria'].lower().replace(' ', '_')}_{selected_format}.json",
                mime="application/json"
            )
            
            # Crear resumen en texto
            texto_resumen = f"""
PLAYOFF - {categoria_data['categoria']}
{'='*50}
Formato: {playoff_data['description']}
Total partidos: {playoff_data['total_matches']}
Equipos participantes: {playoff_data['participating_teams']}

ENFRENTAMIENTOS:
{'-'*30}
"""
            for match in playoff_data['matches']:
                local = match['local']
                visitante = match['visitante']
                fecha_info = f"{match['fecha']} - {match['hora']}" if match.get('fecha') else "Sin fecha"
                
                texto_resumen += f"""
Enfrentamiento #{match['match_id']} - {fecha_info}
🏠 {local['equipo']} ({local['descripcion']})
   Record: {local['partidos_ganados']}G-{local['partidos_perdidos']}P
   Puntos: {local['puntos_totales']} ({local['diferencia_puntos']:+d})

✈️  {visitante['equipo']} ({visitante['descripcion']})
   Record: {visitante['partidos_ganados']}G-{visitante['partidos_perdidos']}P
   Puntos: {visitante['puntos_totales']} ({visitante['diferencia_puntos']:+d})

{'-'*50}
"""
            
            st.download_button(
                label="⬇️ Descargar TXT",
                data=texto_resumen,
                file_name=f"playoff_{categoria_data['categoria'].lower().replace(' ', '_')}_{selected_format}.txt",
                mime="text/plain"
            )

def show_general_summary(grupos, regiones):
    """Muestra resumen general de todas las regiones"""
    st.markdown("## 📊 Resumen General por Regiones")
    
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
    
    primeros, segundos, terceros = classify_teams_by_region(grupos, region_name)
    
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
        ["📊 Clasificaciones", "🏆 Playoffs"]
    )
    
    if seccion_principal == "📊 Clasificaciones":
        # Selector de región para clasificaciones
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
    
    elif seccion_principal == "🏆 Playoffs":
        show_playoffs_section(categoria_data)

if __name__ == "__main__":
    main()
