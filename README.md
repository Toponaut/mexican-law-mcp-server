# Mexican Legal MCP Server

Un servidor MCP (Model Context Protocol) para el sistema legal mexicano que proporciona herramientas para:

- 🔍 Búsqueda de legislación en el Diario Oficial de la Federación (DOF)
- 📄 Generación de documentos legales (amparos, contratos, demandas, etc.)
- ⚖️ Razonamiento legal basado en la legislación mexicana
- 🏛️ Análisis de derechos constitucionales

## Características

### Búsqueda en DOF
- Búsqueda por términos en el Diario Oficial de la Federación
- Filtrado por fechas y tipo de documento
- Obtención de contenido completo de documentos
- Acceso a las últimas publicaciones

### Generación de Documentos
- **Amparo**: Generación de demandas de amparo constitucional
- **Contratos**: Creación de diversos tipos de contratos
- **Demandas**: Generación de demandas civiles
- **Poder Notarial**: Documentos de poder legal
- **Testamentos**: Documentos testamentarios

### Análisis Legal
- Análisis de casos legales por área del derecho
- Verificación de derechos constitucionales
- Evaluación de validez contractual
- Evaluación de responsabilidad penal

## Instalación

1. Clona el repositorio:
```bash
git clone <repository-url>
cd mexican_legal_mcp
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta el servidor:
```bash
python src/server.py
```

## Configuración para Claude Desktop

Agrega la siguiente configuración a tu archivo `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mexican-legal-mcp": {
      "command": "python",
      "args": ["/ruta/a/mexican_legal_mcp/src/server.py"],
      "env": {}
    }
  }
}
```

## Herramientas Disponibles

### Búsqueda DOF
- `search_dof`: Buscar legislación en el DOF
- `get_dof_document`: Obtener contenido completo de un documento
- `search_by_document_type`: Buscar por tipo de documento
- `get_latest_publications`: Obtener últimas publicaciones

### Generación de Documentos
- `generate_amparo`: Generar demanda de amparo
- `generate_contract`: Generar contrato
- `generate_lawsuit`: Generar demanda civil

### Análisis Legal
- `analyze_legal_case`: Analizar caso legal
- `check_constitutional_rights`: Verificar derechos constitucionales
- `analyze_contract_validity`: Analizar validez contractual
- `assess_criminal_liability`: Evaluar responsabilidad penal

## Ejemplos de Uso

### Búsqueda de Legislación
```python
# Buscar leyes sobre transparencia
search_dof(query="ley transparencia", limit=10)

# Buscar decretos en un rango de fechas
search_dof(query="decreto", date_from="2024-01-01", date_to="2024-12-31")
```

### Generación de Amparo
```python
generate_amparo(
    quejoso_nombre="Juan Pérez",
    quejoso_domicilio="Calle Falsa 123, CDMX",
    autoridad_responsable="Secretaría de Hacienda",
    acto_reclamado="Negativa de devolución de impuestos",
    derecho_violado="Derecho de petición",
    conceptos_violacion=["Violación al artículo 8 constitucional"],
    fecha_acto="2024-01-15",
    juzgado="Primer Tribunal Colegiado"
)
```

### Análisis Legal
```python
analyze_legal_case(
    facts=["El empleado fue despedido sin causa justificada", "No se pagó finiquito"],
    legal_question="¿Procede demanda laboral por despido injustificado?",
    area="laboral"
)
```

## Áreas del Derecho Soportadas

- **Constitucional**: Derechos fundamentales, amparo
- **Civil**: Contratos, responsabilidad civil, obligaciones
- **Penal**: Delitos, responsabilidad penal
- **Laboral**: Relaciones de trabajo, despidos
- **Mercantil**: Derecho comercial, sociedades
- **Administrativo**: Actos de autoridad
- **Fiscal**: Impuestos, derecho tributario
- **Familiar**: Matrimonio, divorcio, patria potestad

## Limitaciones

- Este servidor está diseñado para asistencia legal informativa únicamente
- No constituye asesoría legal profesional
- Siempre consulte con un abogado para casos específicos
- La información puede no estar actualizada en tiempo real

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

MIT License - ver archivo LICENSE para detalles

## Disclaimer Legal

Este software es solo para fines informativos y educativos. No constituye asesoría legal profesional. Siempre consulte con un abogado calificado para asuntos legales específicos.