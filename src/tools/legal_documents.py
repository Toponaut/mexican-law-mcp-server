"""
Legal document generation tools for Mexican legal system.
"""

from datetime import date, datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from jinja2 import Template
import json


@dataclass
class AmparoData:
    """Data structure for Amparo legal action."""
    quejoso_nombre: str
    quejoso_domicilio: str
    autoridad_responsable: str
    acto_reclamado: str
    derecho_violado: str
    conceptos_violacion: List[str]
    fecha_acto: date
    juzgado: str
    fecha_presentacion: Optional[date] = None


@dataclass
class ContratoData:
    """Data structure for contract generation."""
    tipo_contrato: str
    parte_1_nombre: str
    parte_1_datos: str
    parte_2_nombre: str
    parte_2_datos: str
    objeto_contrato: str
    precio: Optional[str] = None
    plazo: Optional[str] = None
    condiciones_especiales: List[str] = None
    fecha_firma: Optional[date] = None


@dataclass
class DemandaData:
    """Data structure for lawsuit (demanda)."""
    demandante_nombre: str
    demandante_domicilio: str
    demandado_nombre: str
    demandado_domicilio: str
    prestaciones: List[str]
    hechos: List[str]
    fundamentos_derecho: List[str]
    juzgado: str
    fecha_presentacion: Optional[date] = None


class LegalDocumentGenerator:
    """Generate Mexican legal documents."""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def generate_amparo(self, data: AmparoData) -> str:
        """
        Generate an Amparo (constitutional protection) document.
        
        Args:
            data: Amparo data structure
            
        Returns:
            Generated document text
        """
        template = Template(self.templates['amparo'])
        
        return template.render(
            quejoso_nombre=data.quejoso_nombre,
            quejoso_domicilio=data.quejoso_domicilio,
            autoridad_responsable=data.autoridad_responsable,
            acto_reclamado=data.acto_reclamado,
            derecho_violado=data.derecho_violado,
            conceptos_violacion=data.conceptos_violacion,
            fecha_acto=data.fecha_acto.strftime('%d de %B de %Y') if data.fecha_acto else '',
            juzgado=data.juzgado,
            fecha_presentacion=data.fecha_presentacion.strftime('%d de %B de %Y') if data.fecha_presentacion else date.today().strftime('%d de %B de %Y'),
            fecha_hoy=date.today().strftime('%d de %B de %Y')
        )
    
    def generate_contrato(self, data: ContratoData) -> str:
        """
        Generate a contract document.
        
        Args:
            data: Contract data structure
            
        Returns:
            Generated contract text
        """
        template = Template(self.templates['contrato'])
        
        return template.render(
            tipo_contrato=data.tipo_contrato,
            parte_1_nombre=data.parte_1_nombre,
            parte_1_datos=data.parte_1_datos,
            parte_2_nombre=data.parte_2_nombre,
            parte_2_datos=data.parte_2_datos,
            objeto_contrato=data.objeto_contrato,
            precio=data.precio or "A convenir",
            plazo=data.plazo or "Por tiempo indefinido",
            condiciones_especiales=data.condiciones_especiales or [],
            fecha_firma=data.fecha_firma.strftime('%d de %B de %Y') if data.fecha_firma else date.today().strftime('%d de %B de %Y'),
            fecha_hoy=date.today().strftime('%d de %B de %Y')
        )
    
    def generate_demanda(self, data: DemandaData) -> str:
        """
        Generate a lawsuit (demanda) document.
        
        Args:
            data: Lawsuit data structure
            
        Returns:
            Generated lawsuit text
        """
        template = Template(self.templates['demanda'])
        
        return template.render(
            demandante_nombre=data.demandante_nombre,
            demandante_domicilio=data.demandante_domicilio,
            demandado_nombre=data.demandado_nombre,
            demandado_domicilio=data.demandado_domicilio,
            prestaciones=data.prestaciones,
            hechos=data.hechos,
            fundamentos_derecho=data.fundamentos_derecho,
            juzgado=data.juzgado,
            fecha_presentacion=data.fecha_presentacion.strftime('%d de %B de %Y') if data.fecha_presentacion else date.today().strftime('%d de %B de %Y'),
            fecha_hoy=date.today().strftime('%d de %B de %Y')
        )
    
    def generate_poder_notarial(self, poderdante: str, apoderado: str, facultades: List[str]) -> str:
        """Generate a power of attorney document."""
        template = Template(self.templates['poder_notarial'])
        
        return template.render(
            poderdante=poderdante,
            apoderado=apoderado,
            facultades=facultades,
            fecha_hoy=date.today().strftime('%d de %B de %Y')
        )
    
    def generate_testamento(self, testador: str, herederos: List[Dict[str, str]], bienes: List[str]) -> str:
        """Generate a will (testamento) document."""
        template = Template(self.templates['testamento'])
        
        return template.render(
            testador=testador,
            herederos=herederos,
            bienes=bienes,
            fecha_hoy=date.today().strftime('%d de %B de %Y')
        )
    
    def _load_templates(self) -> Dict[str, str]:
        """Load document templates."""
        return {
            'amparo': """
JUICIO DE AMPARO INDIRECTO

C. JUEZ {{ juzgado }}
P R E S E N T E

{{ quejoso_nombre }}, por mi propio derecho, con domicilio en {{ quejoso_domicilio }}, ante Usted comparezco y expongo:

Que por medio del presente escrito vengo a promover JUICIO DE AMPARO INDIRECTO en contra de:

AUTORIDAD RESPONSABLE: {{ autoridad_responsable }}

ACTO RECLAMADO: {{ acto_reclamado }}

CONCEPTOS DE VIOLACIÓN:

{% for concepto in conceptos_violacion %}
{{ loop.index }}.- {{ concepto }}
{% endfor %}

Por lo anterior, a Usted C. Juez, atentamente solicito:

PRIMERO.- Se admita la presente demanda de amparo.
SEGUNDO.- Se conceda la suspensión del acto reclamado.
TERCERO.- Se otorgue el amparo y protección de la Justicia Federal.

DERECHO VIOLADO: {{ derecho_violado }}

Fecha del acto reclamado: {{ fecha_acto }}

PROTESTO LO NECESARIO

{{ fecha_presentacion }}

_____________________________
{{ quejoso_nombre }}
QUEJOSO
""",
            
            'contrato': """
CONTRATO DE {{ tipo_contrato.upper() }}

En {{ fecha_firma }}, en la Ciudad de México, las partes que intervienen en este contrato son:

PRIMERA PARTE: {{ parte_1_nombre }}
{{ parte_1_datos }}

SEGUNDA PARTE: {{ parte_2_nombre }}
{{ parte_2_datos }}

DECLARACIONES

Ambas partes declaran que tienen capacidad legal para contratar y obligarse.

CLÁUSULAS

PRIMERA.- OBJETO DEL CONTRATO
{{ objeto_contrato }}

SEGUNDA.- PRECIO
El precio será de {{ precio }}

TERCERA.- PLAZO
El presente contrato tendrá una duración de {{ plazo }}

{% if condiciones_especiales %}
CUARTA.- CONDICIONES ESPECIALES
{% for condicion in condiciones_especiales %}
{{ loop.index }}.- {{ condicion }}
{% endfor %}
{% endif %}

QUINTA.- JURISDICCIÓN
Para la interpretación y cumplimiento de este contrato, las partes se someten a la jurisdicción de los tribunales de la Ciudad de México.

En fe de lo cual, firman las partes en la fecha señalada.

_____________________________        _____________________________
{{ parte_1_nombre }}                    {{ parte_2_nombre }}
""",
            
            'demanda': """
C. JUEZ {{ juzgado }}
P R E S E N T E

{{ demandante_nombre }}, con domicilio en {{ demandante_domicilio }}, por mi propio derecho, ante Usted comparezco y expongo:

Que por medio del presente escrito vengo a demandar de {{ demandado_nombre }}, con domicilio en {{ demandado_domicilio }}, las siguientes:

PRESTACIONES:

{% for prestacion in prestaciones %}
{{ loop.index }}.- {{ prestacion }}
{% endfor %}

HECHOS:

{% for hecho in hechos %}
{{ loop.index }}.- {{ hecho }}
{% endfor %}

FUNDAMENTOS DE DERECHO:

{% for fundamento in fundamentos_derecho %}
{{ loop.index }}.- {{ fundamento }}
{% endfor %}

Por lo anterior, a Usted C. Juez, atentamente solicito se sirva:

PRIMERO.- Tener por presentada la demanda y admitirla a trámite.
SEGUNDO.- Declarar procedente la demanda y condenar al demandado al cumplimiento de las prestaciones reclamadas.

PROTESTO LO NECESARIO

{{ fecha_presentacion }}

_____________________________
{{ demandante_nombre }}
DEMANDANTE
""",
            
            'poder_notarial': """
PODER NOTARIAL

Por medio del presente documento, yo {{ poderdante }}, otorgo poder amplio y suficiente a {{ apoderado }} para que en mi nombre y representación realice los siguientes actos:

FACULTADES:

{% for facultad in facultades %}
{{ loop.index }}.- {{ facultad }}
{% endfor %}

Este poder se otorga con las facultades necesarias para su debido cumplimiento.

{{ fecha_hoy }}

_____________________________
{{ poderdante }}
PODERDANTE

_____________________________
{{ apoderado }}
APODERADO
""",
            
            'testamento': """
TESTAMENTO

Yo, {{ testador }}, en pleno uso de mis facultades mentales, otorgo el presente testamento:

PRIMERA.- Revoco cualquier testamento anterior.

SEGUNDA.- Instituyo como mis herederos a:

{% for heredero in herederos %}
{{ loop.index }}.- {{ heredero.nombre }} - {{ heredero.porcentaje }}% - {{ heredero.parentesco }}
{% endfor %}

TERCERA.- Mis bienes son:

{% for bien in bienes %}
{{ loop.index }}.- {{ bien }}
{% endfor %}

CUARTA.- Es mi voluntad que se respeten estas disposiciones.

{{ fecha_hoy }}

_____________________________
{{ testador }}
TESTADOR
"""
        }
    
    def get_available_templates(self) -> List[str]:
        """Get list of available document templates."""
        return list(self.templates.keys())
    
    def validate_amparo_data(self, data: Dict[str, Any]) -> bool:
        """Validate amparo data structure."""
        required_fields = [
            'quejoso_nombre', 'quejoso_domicilio', 'autoridad_responsable',
            'acto_reclamado', 'derecho_violado', 'conceptos_violacion', 'juzgado'
        ]
        
        return all(field in data and data[field] for field in required_fields)
    
    def validate_contrato_data(self, data: Dict[str, Any]) -> bool:
        """Validate contract data structure."""
        required_fields = [
            'tipo_contrato', 'parte_1_nombre', 'parte_1_datos',
            'parte_2_nombre', 'parte_2_datos', 'objeto_contrato'
        ]
        
        return all(field in data and data[field] for field in required_fields)
    
    def validate_demanda_data(self, data: Dict[str, Any]) -> bool:
        """Validate lawsuit data structure."""
        required_fields = [
            'demandante_nombre', 'demandante_domicilio', 'demandado_nombre',
            'demandado_domicilio', 'prestaciones', 'hechos', 'fundamentos_derecho', 'juzgado'
        ]
        
        return all(field in data and data[field] for field in required_fields)