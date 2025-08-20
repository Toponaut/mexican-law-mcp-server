"""
Mexican legal reasoning and analysis tools.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class LegalArea(Enum):
    """Mexican legal areas."""
    CONSTITUTIONAL = "constitucional"
    CIVIL = "civil"
    PENAL = "penal"
    MERCANTIL = "mercantil"
    LABORAL = "laboral"
    ADMINISTRATIVE = "administrativo"
    FISCAL = "fiscal"
    FAMILIAR = "familiar"
    AMPARO = "amparo"


@dataclass
class LegalPrecedent:
    """Legal precedent structure."""
    titulo: str
    tesis: str
    tribunal: str
    epoca: str
    registro: str
    texto: str
    area_derecho: LegalArea


@dataclass
class LegalAnalysis:
    """Legal analysis result."""
    area_derecho: LegalArea
    articulos_aplicables: List[str]
    precedentes: List[LegalPrecedent]
    fundamentos: List[str]
    recomendaciones: List[str]
    riesgo_legal: str  # ALTO, MEDIO, BAJO
    opinion_legal: str


class MexicanLegalReasoner:
    """Mexican legal reasoning engine."""
    
    def __init__(self):
        self.constitution_articles = self._load_constitution_articles()
        self.codigo_civil = self._load_codigo_civil()
        self.codigo_penal = self._load_codigo_penal()
        self.legal_principles = self._load_legal_principles()
    
    def analyze_legal_case(
        self, 
        facts: List[str], 
        legal_question: str,
        area: Optional[LegalArea] = None
    ) -> LegalAnalysis:
        """
        Analyze a legal case based on Mexican law.
        
        Args:
            facts: List of factual circumstances
            legal_question: The legal question to analyze
            area: Specific area of law (optional)
            
        Returns:
            Legal analysis with applicable law and recommendations
        """
        
        # Determine legal area if not specified
        if not area:
            area = self._identify_legal_area(facts, legal_question)
        
        # Find applicable articles
        applicable_articles = self._find_applicable_articles(facts, legal_question, area)
        
        # Find relevant precedents
        precedents = self._find_precedents(legal_question, area)
        
        # Generate legal foundations
        foundations = self._generate_foundations(facts, applicable_articles, area)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(facts, legal_question, area)
        
        # Assess legal risk
        risk = self._assess_legal_risk(facts, area)
        
        # Generate legal opinion
        opinion = self._generate_legal_opinion(facts, legal_question, applicable_articles, area)
        
        return LegalAnalysis(
            area_derecho=area,
            articulos_aplicables=applicable_articles,
            precedentes=precedents,
            fundamentos=foundations,
            recomendaciones=recommendations,
            riesgo_legal=risk,
            opinion_legal=opinion
        )
    
    def check_constitutional_rights(self, situation: str) -> Dict[str, Any]:
        """
        Check if a situation violates constitutional rights.
        
        Args:
            situation: Description of the situation
            
        Returns:
            Analysis of constitutional rights
        """
        
        violated_rights = []
        applicable_articles = []
        
        # Check fundamental rights (Articles 1-29)
        fundamental_rights = {
            "igualdad": ["artículo 1", "igualdad ante la ley"],
            "libertad": ["artículo 5", "libertad de trabajo"],
            "expresion": ["artículo 6", "libertad de expresión"],
            "educacion": ["artículo 3", "derecho a la educación"],
            "debido_proceso": ["artículo 14", "debido proceso legal"],
            "legalidad": ["artículo 16", "principio de legalidad"],
            "propiedad": ["artículo 27", "derecho de propiedad"]
        }
        
        situation_lower = situation.lower()
        
        for right, details in fundamental_rights.items():
            if any(keyword in situation_lower for keyword in right.split("_")):
                violated_rights.append(right)
                applicable_articles.append(details[0])
        
        return {
            "derechos_violados": violated_rights,
            "articulos_constitucionales": applicable_articles,
            "procedencia_amparo": len(violated_rights) > 0,
            "recomendacion": self._get_constitutional_recommendation(violated_rights)
        }
    
    def analyze_contract_validity(self, contract_terms: List[str]) -> Dict[str, Any]:
        """
        Analyze contract validity under Mexican civil law.
        
        Args:
            contract_terms: List of contract terms
            
        Returns:
            Contract validity analysis
        """
        
        validity_issues = []
        requirements = {
            "consentimiento": False,
            "objeto": False,
            "causa": False,
            "forma": False
        }
        
        contract_text = " ".join(contract_terms).lower()
        
        # Check consent
        if any(word in contract_text for word in ["acepto", "convenimos", "acordamos"]):
            requirements["consentimiento"] = True
        else:
            validity_issues.append("Falta expresión clara del consentimiento")
        
        # Check object
        if any(word in contract_text for word in ["objeto", "prestación", "obligación"]):
            requirements["objeto"] = True
        else:
            validity_issues.append("Objeto del contrato no está claramente definido")
        
        # Check cause
        if any(word in contract_text for word in ["porque", "motivo", "causa", "razón"]):
            requirements["causa"] = True
        else:
            validity_issues.append("Causa del contrato no está especificada")
        
        is_valid = all(requirements.values()) and len(validity_issues) == 0
        
        return {
            "es_valido": is_valid,
            "requisitos_cumplidos": requirements,
            "problemas_identificados": validity_issues,
            "articulos_aplicables": ["artículo 1794", "artículo 1795", "artículo 1796"],
            "recomendaciones": self._get_contract_recommendations(validity_issues)
        }
    
    def assess_criminal_liability(self, facts: List[str]) -> Dict[str, Any]:
        """
        Assess criminal liability under Mexican penal law.
        
        Args:
            facts: Facts of the case
            
        Returns:
            Criminal liability assessment
        """
        
        potential_crimes = []
        facts_text = " ".join(facts).lower()
        
        # Common crimes patterns
        crime_patterns = {
            "homicidio": ["matar", "muerte", "asesinato"],
            "robo": ["robar", "sustraer", "hurtar"],
            "fraude": ["engañar", "defraudar", "estafar"],
            "lesiones": ["golpear", "herir", "lastimar"],
            "difamacion": ["calumniar", "difamar", "injuriar"],
            "violacion": ["violar", "abuso sexual", "agresión sexual"]
        }
        
        for crime, keywords in crime_patterns.items():
            if any(keyword in facts_text for keyword in keywords):
                potential_crimes.append(crime)
        
        return {
            "posibles_delitos": potential_crimes,
            "elementos_constitutivos": self._get_crime_elements(potential_crimes),
            "penalidades": self._get_penalties(potential_crimes),
            "defensas_posibles": self._get_possible_defenses(potential_crimes),
            "recomendacion_procesal": self._get_criminal_procedure_recommendation(potential_crimes)
        }
    
    def _identify_legal_area(self, facts: List[str], question: str) -> LegalArea:
        """Identify the primary legal area."""
        
        text = " ".join(facts + [question]).lower()
        
        area_keywords = {
            LegalArea.CONSTITUTIONAL: ["constitución", "derechos fundamentales", "amparo", "garantías"],
            LegalArea.CIVIL: ["contrato", "propiedad", "obligaciones", "responsabilidad civil"],
            LegalArea.PENAL: ["delito", "crimen", "penal", "criminal"],
            LegalArea.LABORAL: ["trabajo", "empleado", "salario", "despido"],
            LegalArea.MERCANTIL: ["comercio", "empresa", "mercantil", "sociedad"],
            LegalArea.ADMINISTRATIVE: ["autoridad", "funcionario", "administrativo", "gobierno"],
            LegalArea.FISCAL: ["impuesto", "fiscal", "tributario", "hacienda"],
            LegalArea.FAMILIAR: ["matrimonio", "divorcio", "patria potestad", "alimentos"]
        }
        
        for area, keywords in area_keywords.items():
            if any(keyword in text for keyword in keywords):
                return area
        
        return LegalArea.CIVIL  # Default
    
    def _find_applicable_articles(self, facts: List[str], question: str, area: LegalArea) -> List[str]:
        """Find applicable legal articles."""
        
        articles = []
        
        if area == LegalArea.CONSTITUTIONAL:
            articles.extend(["Artículo 1°", "Artículo 14", "Artículo 16"])
        elif area == LegalArea.CIVIL:
            articles.extend(["Artículo 1794", "Artículo 1910", "Artículo 2104"])
        elif area == LegalArea.PENAL:
            articles.extend(["Artículo 123", "Artículo 302", "Artículo 367"])
        
        return articles
    
    def _find_precedents(self, question: str, area: LegalArea) -> List[LegalPrecedent]:
        """Find relevant legal precedents."""
        
        # This would normally query a precedent database
        # For now, return sample precedents
        
        sample_precedents = [
            LegalPrecedent(
                titulo="Garantías individuales. Su violación",
                tesis="Las garantías individuales consagradas en la Constitución...",
                tribunal="Suprema Corte de Justicia de la Nación",
                epoca="Novena Época",
                registro="123456",
                texto="Texto completo de la tesis...",
                area_derecho=area
            )
        ]
        
        return sample_precedents[:3]  # Return up to 3 precedents
    
    def _generate_foundations(self, facts: List[str], articles: List[str], area: LegalArea) -> List[str]:
        """Generate legal foundations."""
        
        foundations = [
            f"Con fundamento en {', '.join(articles)} del ordenamiento aplicable",
            "Considerando los hechos expuestos y la normatividad vigente",
            "En aplicación de los principios generales del derecho"
        ]
        
        return foundations
    
    def _generate_recommendations(self, facts: List[str], question: str, area: LegalArea) -> List[str]:
        """Generate legal recommendations."""
        
        recommendations = [
            "Recabar toda la documentación probatoria disponible",
            "Consultar con un abogado especializado en la materia",
            "Evaluar las opciones procesales disponibles"
        ]
        
        if area == LegalArea.CONSTITUTIONAL:
            recommendations.append("Considerar la promoción de juicio de amparo")
        elif area == LegalArea.CIVIL:
            recommendations.append("Evaluar la posibilidad de una solución extrajudicial")
        
        return recommendations
    
    def _assess_legal_risk(self, facts: List[str], area: LegalArea) -> str:
        """Assess legal risk level."""
        
        # Simple risk assessment logic
        facts_text = " ".join(facts).lower()
        
        high_risk_indicators = ["penal", "criminal", "delito", "constitucional"]
        medium_risk_indicators = ["civil", "contractual", "laboral"]
        
        if any(indicator in facts_text for indicator in high_risk_indicators):
            return "ALTO"
        elif any(indicator in facts_text for indicator in medium_risk_indicators):
            return "MEDIO"
        else:
            return "BAJO"
    
    def _generate_legal_opinion(self, facts: List[str], question: str, articles: List[str], area: LegalArea) -> str:
        """Generate legal opinion."""
        
        opinion = f"""
        Basado en el análisis de los hechos expuestos y considerando la legislación mexicana aplicable 
        en materia {area.value}, se observa que la situación planteada se rige por {', '.join(articles)}.
        
        La evaluación legal sugiere que es necesario realizar un análisis más profundo de las 
        circunstancias específicas para determinar la estrategia legal más adecuada.
        
        Se recomienda la consulta con un profesional del derecho especializado en la materia.
        """
        
        return opinion.strip()
    
    def _load_constitution_articles(self) -> Dict[str, str]:
        """Load Constitution articles (simplified)."""
        return {
            "1": "Derechos humanos y garantías",
            "3": "Derecho a la educación",
            "14": "Debido proceso legal",
            "16": "Principio de legalidad"
        }
    
    def _load_codigo_civil(self) -> Dict[str, str]:
        """Load Civil Code articles (simplified)."""
        return {
            "1794": "Elementos del contrato",
            "1910": "Responsabilidad civil",
            "2104": "Obligaciones"
        }
    
    def _load_codigo_penal(self) -> Dict[str, str]:
        """Load Penal Code articles (simplified)."""
        return {
            "123": "Homicidio",
            "302": "Robo",
            "367": "Fraude"
        }
    
    def _load_legal_principles(self) -> List[str]:
        """Load general legal principles."""
        return [
            "Principio de legalidad",
            "Debido proceso",
            "Presunción de inocencia",
            "Igualdad ante la ley",
            "Seguridad jurídica"
        ]
    
    def _get_constitutional_recommendation(self, violated_rights: List[str]) -> str:
        """Get recommendation for constitutional violations."""
        if violated_rights:
            return "Se recomienda la promoción de juicio de amparo para la protección de los derechos fundamentales violados."
        return "No se identifican violaciones constitucionales evidentes."
    
    def _get_contract_recommendations(self, issues: List[str]) -> List[str]:
        """Get contract recommendations."""
        recommendations = []
        for issue in issues:
            if "consentimiento" in issue:
                recommendations.append("Incluir cláusula expresa de aceptación de términos")
            if "objeto" in issue:
                recommendations.append("Definir claramente el objeto del contrato")
        return recommendations
    
    def _get_crime_elements(self, crimes: List[str]) -> Dict[str, List[str]]:
        """Get elements of crimes."""
        elements = {}
        for crime in crimes:
            if crime == "homicidio":
                elements[crime] = ["Privar de la vida", "Dolo o culpa", "Nexo causal"]
        return elements
    
    def _get_penalties(self, crimes: List[str]) -> Dict[str, str]:
        """Get penalties for crimes."""
        penalties = {}
        for crime in crimes:
            if crime == "homicidio":
                penalties[crime] = "12 a 30 años de prisión"
        return penalties
    
    def _get_possible_defenses(self, crimes: List[str]) -> List[str]:
        """Get possible defenses."""
        return ["Legítima defensa", "Estado de necesidad", "Error de hecho"]
    
    def _get_criminal_procedure_recommendation(self, crimes: List[str]) -> str:
        """Get criminal procedure recommendation."""
        if crimes:
            return "Se recomienda contactar inmediatamente con un abogado penalista especializado."
        return "No se identifican elementos que configuren delito."