"""
Mexican Legal MCP Server
"""

import asyncio
import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import AnyUrl

from tools.dof_search import DOFSearcher, DOFSearchResult
from tools.legal_documents import (
    LegalDocumentGenerator, 
    AmparoData, 
    ContratoData, 
    DemandaData
)
from tools.legal_reasoning import MexicanLegalReasoner, LegalArea, LegalAnalysis


# Create global instances
dof_searcher = DOFSearcher()
doc_generator = LegalDocumentGenerator()
legal_reasoner = MexicanLegalReasoner()

# Create MCP server
server = Server("mexican-legal-mcp")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_dof",
            description="Search the Diario Oficial de la Federación for Mexican legislation",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for legislation"
                    },
                    "date_from": {
                        "type": "string",
                        "format": "date",
                        "description": "Start date for search (YYYY-MM-DD)"
                    },
                    "date_to": {
                        "type": "string", 
                        "format": "date",
                        "description": "End date for search (YYYY-MM-DD)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 20
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_dof_document",
            description="Get full content of a DOF document by URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL of the DOF document"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="search_by_document_type",
            description="Search DOF by document type (decreto, ley, reglamento, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "enum": ["decreto", "ley", "reglamento", "acuerdo", "norma"],
                        "description": "Type of document to search"
                    },
                    "query": {
                        "type": "string",
                        "description": "Additional search terms"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 20
                    }
                },
                "required": ["doc_type"]
            }
        ),
        Tool(
            name="get_latest_publications",
            description="Get latest DOF publications",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "default": 10
                    }
                }
            }
        ),
        Tool(
            name="generate_amparo",
            description="Generate an Amparo (constitutional protection) document",
            inputSchema={
                "type": "object",
                "properties": {
                    "quejoso_nombre": {"type": "string", "description": "Name of the complainant"},
                    "quejoso_domicilio": {"type": "string", "description": "Address of the complainant"},
                    "autoridad_responsable": {"type": "string", "description": "Responsible authority"},
                    "acto_reclamado": {"type": "string", "description": "Act being challenged"},
                    "derecho_violado": {"type": "string", "description": "Right that was violated"},
                    "conceptos_violacion": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Concepts of violation"
                    },
                    "fecha_acto": {"type": "string", "format": "date", "description": "Date of the act"},
                    "juzgado": {"type": "string", "description": "Court/jurisdiction"}
                },
                "required": ["quejoso_nombre", "quejoso_domicilio", "autoridad_responsable", 
                           "acto_reclamado", "derecho_violado", "conceptos_violacion", "juzgado"]
            }
        ),
        Tool(
            name="generate_contract",
            description="Generate a contract document",
            inputSchema={
                "type": "object",
                "properties": {
                    "tipo_contrato": {"type": "string", "description": "Type of contract"},
                    "parte_1_nombre": {"type": "string", "description": "First party name"},
                    "parte_1_datos": {"type": "string", "description": "First party details"},
                    "parte_2_nombre": {"type": "string", "description": "Second party name"},
                    "parte_2_datos": {"type": "string", "description": "Second party details"},
                    "objeto_contrato": {"type": "string", "description": "Contract object/purpose"},
                    "precio": {"type": "string", "description": "Price"},
                    "plazo": {"type": "string", "description": "Term/duration"},
                    "condiciones_especiales": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Special conditions"
                    }
                },
                "required": ["tipo_contrato", "parte_1_nombre", "parte_1_datos", 
                           "parte_2_nombre", "parte_2_datos", "objeto_contrato"]
            }
        ),
        Tool(
            name="generate_lawsuit",
            description="Generate a lawsuit (demanda) document",
            inputSchema={
                "type": "object",
                "properties": {
                    "demandante_nombre": {"type": "string", "description": "Plaintiff name"},
                    "demandante_domicilio": {"type": "string", "description": "Plaintiff address"},
                    "demandado_nombre": {"type": "string", "description": "Defendant name"},
                    "demandado_domicilio": {"type": "string", "description": "Defendant address"},
                    "prestaciones": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Claims/demands"
                    },
                    "hechos": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Facts of the case"
                    },
                    "fundamentos_derecho": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Legal foundations"
                    },
                    "juzgado": {"type": "string", "description": "Court/jurisdiction"}
                },
                "required": ["demandante_nombre", "demandante_domicilio", "demandado_nombre",
                           "demandado_domicilio", "prestaciones", "hechos", "fundamentos_derecho", "juzgado"]
            }
        ),
        Tool(
            name="analyze_legal_case",
            description="Analyze a legal case based on Mexican law",
            inputSchema={
                "type": "object",
                "properties": {
                    "facts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Facts of the case"
                    },
                    "legal_question": {
                        "type": "string",
                        "description": "The legal question to analyze"
                    },
                    "area": {
                        "type": "string",
                        "enum": ["constitucional", "civil", "penal", "mercantil", "laboral", 
                                "administrativo", "fiscal", "familiar", "amparo"],
                        "description": "Area of law"
                    }
                },
                "required": ["facts", "legal_question"]
            }
        ),
        Tool(
            name="check_constitutional_rights",
            description="Check if a situation violates constitutional rights",
            inputSchema={
                "type": "object",
                "properties": {
                    "situation": {
                        "type": "string",
                        "description": "Description of the situation to analyze"
                    }
                },
                "required": ["situation"]
            }
        ),
        Tool(
            name="analyze_contract_validity",
            description="Analyze contract validity under Mexican civil law",
            inputSchema={
                "type": "object",
                "properties": {
                    "contract_terms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Contract terms to analyze"
                    }
                },
                "required": ["contract_terms"]
            }
        ),
        Tool(
            name="assess_criminal_liability",
            description="Assess criminal liability under Mexican penal law",
            inputSchema={
                "type": "object",
                "properties": {
                    "facts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Facts of the case"
                    }
                },
                "required": ["facts"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    
    try:
        if name == "search_dof":
            query = arguments["query"]
            date_from = None
            date_to = None
            limit = arguments.get("limit", 20)
            
            if "date_from" in arguments:
                date_from = datetime.strptime(arguments["date_from"], "%Y-%m-%d").date()
            if "date_to" in arguments:
                date_to = datetime.strptime(arguments["date_to"], "%Y-%m-%d").date()
            
            results = dof_searcher.search_legislation(query, date_from, date_to, limit)
            
            response = "# Resultados de búsqueda en DOF\n\n"
            for i, result in enumerate(results, 1):
                response += f"## {i}. {result.title}\n"
                response += f"**Fecha:** {result.date}\n"
                response += f"**Tipo:** {result.type}\n"
                response += f"**URL:** {result.url}\n"
                response += f"**Resumen:** {result.summary}\n\n"
            
            return [TextContent(type="text", text=response)]
        
        elif name == "get_dof_document":
            url = arguments["url"]
            content = dof_searcher.get_document_content(url)
            
            return [TextContent(type="text", text=f"# Contenido del documento\n\n{content}")]
        
        elif name == "search_by_document_type":
            doc_type = arguments["doc_type"]
            query = arguments.get("query")
            limit = arguments.get("limit", 20)
            
            results = dof_searcher.search_by_type(doc_type, query, limit)
            
            response = f"# Resultados de búsqueda por tipo: {doc_type}\n\n"
            for i, result in enumerate(results, 1):
                response += f"## {i}. {result.title}\n"
                response += f"**Fecha:** {result.date}\n"
                response += f"**URL:** {result.url}\n"
                response += f"**Resumen:** {result.summary}\n\n"
            
            return [TextContent(type="text", text=response)]
        
        elif name == "get_latest_publications":
            limit = arguments.get("limit", 10)
            results = dof_searcher.get_latest_publications(limit)
            
            response = "# Últimas publicaciones del DOF\n\n"
            for i, result in enumerate(results, 1):
                response += f"## {i}. {result.title}\n"
                response += f"**Fecha:** {result.date}\n"
                response += f"**URL:** {result.url}\n"
                response += f"**Resumen:** {result.summary}\n\n"
            
            return [TextContent(type="text", text=response)]
        
        elif name == "generate_amparo":
            fecha_acto = datetime.strptime(arguments["fecha_acto"], "%Y-%m-%d").date()
            
            amparo_data = AmparoData(
                quejoso_nombre=arguments["quejoso_nombre"],
                quejoso_domicilio=arguments["quejoso_domicilio"],
                autoridad_responsable=arguments["autoridad_responsable"],
                acto_reclamado=arguments["acto_reclamado"],
                derecho_violado=arguments["derecho_violado"],
                conceptos_violacion=arguments["conceptos_violacion"],
                fecha_acto=fecha_acto,
                juzgado=arguments["juzgado"]
            )
            
            document = doc_generator.generate_amparo(amparo_data)
            
            return [TextContent(type="text", text=document)]
        
        elif name == "generate_contract":
            contract_data = ContratoData(
                tipo_contrato=arguments["tipo_contrato"],
                parte_1_nombre=arguments["parte_1_nombre"],
                parte_1_datos=arguments["parte_1_datos"],
                parte_2_nombre=arguments["parte_2_nombre"],
                parte_2_datos=arguments["parte_2_datos"],
                objeto_contrato=arguments["objeto_contrato"],
                precio=arguments.get("precio"),
                plazo=arguments.get("plazo"),
                condiciones_especiales=arguments.get("condiciones_especiales", [])
            )
            
            document = doc_generator.generate_contrato(contract_data)
            
            return [TextContent(type="text", text=document)]
        
        elif name == "generate_lawsuit":
            lawsuit_data = DemandaData(
                demandante_nombre=arguments["demandante_nombre"],
                demandante_domicilio=arguments["demandante_domicilio"],
                demandado_nombre=arguments["demandado_nombre"],
                demandado_domicilio=arguments["demandado_domicilio"],
                prestaciones=arguments["prestaciones"],
                hechos=arguments["hechos"],
                fundamentos_derecho=arguments["fundamentos_derecho"],
                juzgado=arguments["juzgado"]
            )
            
            document = doc_generator.generate_demanda(lawsuit_data)
            
            return [TextContent(type="text", text=document)]
        
        elif name == "analyze_legal_case":
            facts = arguments["facts"]
            legal_question = arguments["legal_question"]
            area = None
            
            if "area" in arguments:
                area = LegalArea(arguments["area"])
            
            analysis = legal_reasoner.analyze_legal_case(facts, legal_question, area)
            
            response = f"""# Análisis Legal

## Área del Derecho
{analysis.area_derecho.value.title()}

## Artículos Aplicables
{chr(10).join(f"- {art}" for art in analysis.articulos_aplicables)}

## Fundamentos Legales
{chr(10).join(f"- {fund}" for fund in analysis.fundamentos)}

## Recomendaciones
{chr(10).join(f"- {rec}" for rec in analysis.recomendaciones)}

## Riesgo Legal
**{analysis.riesgo_legal}**

## Opinión Legal
{analysis.opinion_legal}
"""
            
            return [TextContent(type="text", text=response)]
        
        elif name == "check_constitutional_rights":
            situation = arguments["situation"]
            result = legal_reasoner.check_constitutional_rights(situation)
            
            response = f"""# Análisis de Derechos Constitucionales

## Derechos Potencialmente Violados
{chr(10).join(f"- {derecho}" for derecho in result["derechos_violados"])}

## Artículos Constitucionales Aplicables
{chr(10).join(f"- {art}" for art in result["articulos_constitucionales"])}

## Procedencia de Amparo
**{"SÍ" if result["procedencia_amparo"] else "NO"}**

## Recomendación
{result["recomendacion"]}
"""
            
            return [TextContent(type="text", text=response)]
        
        elif name == "analyze_contract_validity":
            contract_terms = arguments["contract_terms"]
            result = legal_reasoner.analyze_contract_validity(contract_terms)
            
            response = f"""# Análisis de Validez Contractual

## Validez del Contrato
**{"VÁLIDO" if result["es_valido"] else "INVÁLIDO"}**

## Requisitos Cumplidos
{chr(10).join(f"- {req}: {'✓' if cumplido else '✗'}" for req, cumplido in result["requisitos_cumplidos"].items())}

## Problemas Identificados
{chr(10).join(f"- {problema}" for problema in result["problemas_identificados"])}

## Artículos Aplicables
{chr(10).join(f"- {art}" for art in result["articulos_aplicables"])}

## Recomendaciones
{chr(10).join(f"- {rec}" for rec in result["recomendaciones"])}
"""
            
            return [TextContent(type="text", text=response)]
        
        elif name == "assess_criminal_liability":
            facts = arguments["facts"]
            result = legal_reasoner.assess_criminal_liability(facts)
            
            response = f"""# Evaluación de Responsabilidad Penal

## Posibles Delitos
{chr(10).join(f"- {delito}" for delito in result["posibles_delitos"])}

## Elementos Constitutivos
{chr(10).join(f"**{delito}:** {', '.join(elementos)}" for delito, elementos in result["elementos_constitutivos"].items())}

## Penalidades
{chr(10).join(f"**{delito}:** {pena}" for delito, pena in result["penalidades"].items())}

## Defensas Posibles
{chr(10).join(f"- {defensa}" for defensa in result["defensas_posibles"])}

## Recomendación Procesal
{result["recomendacion_procesal"]}
"""
            
            return [TextContent(type="text", text=response)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]





async def main():
    """Main function to run the server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mexican-legal-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities=None,
                )
            )
        )




if __name__ == "__main__":
    asyncio.run(main())
