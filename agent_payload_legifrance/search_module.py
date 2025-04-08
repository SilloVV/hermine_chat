import requests
import json
from typing import Dict, List, Optional, Union, Any
from enum import Enum
from dataclasses import dataclass, field

# Définition des énumérations pour les valeurs possibles
class Fond(str, Enum):
    """Fonds documentaires disponibles dans l'API Légifrance"""
    JORF = "JORF" # Journal officiel de la République française
    CNIL = "CNIL" # Commission nationale de l'informatique et des libertés
    CETAT = "CETAT" # Conseil d'Etat
    JURI = "JURI" # Jurisprudence
    JUFI = "JUFI" # Jurisprudence financière
    CONSTIT = "CONSTIT" # Conseil constitutionnel
    KALI = "KALI" # Jurisprudence administrative
    CODE_DATE = "CODE_DATE" # Codes juridiques par date
    CODE_ETAT = "CODE_ETAT" # Codes juridiques par état
    LODA_DATE = "LODA_DATE" # Lois et décrets par date
    LODA_ETAT = "LODA_ETAT" # Lois et décrets par état
    ALL = "ALL" # Tous les fonds
    CIRC = "CIRC" # Circulaires : informations administratives et techniques à propos de la mise en œuvre des lois et règlements
    ACCO = "ACCO" # Accords collectifs : accords de branche ou d'entreprise

class TypeChamp(str, Enum):
    """Types de champs disponibles pour la recherche"""
    ALL = "ALL"
    TITLE = "TITLE"
    TABLE = "TABLE"
    NOR = "NOR"
    NUM = "NUM"
    ADVANCED_TEXTE_ID = "ADVANCED_TEXTE_ID"
    NUM_DELIB = "NUM_DELIB"
    NUM_DEC = "NUM_DEC"
    NUM_ARTICLE = "NUM_ARTICLE"
    ARTICLE = "ARTICLE"
    MINISTERE = "MINISTERE"
    VISA = "VISA"
    NOTICE = "NOTICE"
    VISA_NOTICE = "VISA_NOTICE"
    TRAVAUX_PREP = "TRAVAUX_PREP"
    SIGNATURE = "SIGNATURE"
    NOTA = "NOTA"
    NUM_AFFAIRE = "NUM_AFFAIRE"
    ABSTRATS = "ABSTRATS"
    RESUMES = "RESUMES"
    TEXTE = "TEXTE"
    ECLI = "ECLI"
    NUM_LOI_DEF = "NUM_LOI_DEF"
    TYPE_DECISION = "TYPE_DECISION"
    NUMERO_INTERNE = "NUMERO_INTERNE"
    REF_PUBLI = "REF_PUBLI"
    RESUME_CIRC = "RESUME_CIRC"
    TEXTE_REF = "TEXTE_REF"
    TITRE_LOI_DEF = "TITRE_LOI_DEF"
    RAISON_SOCIALE = "RAISON_SOCIALE"
    MOTS_CLES = "MOTS_CLES"
    IDCC = "IDCC"

class TypeRecherche(str, Enum):
    """Types de recherche possibles"""
    UN_DES_MOTS = "UN_DES_MOTS"
    EXACTE = "EXACTE"
    TOUS_LES_MOTS_DANS_UN_CHAMP = "TOUS_LES_MOTS_DANS_UN_CHAMP"
    AUCUN_DES_MOTS = "AUCUN_DES_MOTS"
    AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION = "AUCUNE_CORRESPONDANCE_A_CETTE_EXPRESSION"

class Operateur(str, Enum):
    """Opérateurs logiques pour combiner les critères"""
    ET = "ET"
    OU = "OU"

class TypePagination(str, Enum):
    """Types de pagination disponibles"""
    DEFAUT = "DEFAUT"
    ARTICLE = "ARTICLE"

class TriPossible(str, Enum):
    """Méthodes de tri possibles"""
    PERTINENCE = "PERTINENCE"
    DATE_PUBLI_ASC = "DATE_PUBLI_ASC"
    DATE_PUBLI_DESC = "DATE_PUBLI_DESC"
    SIGNATURE_DATE_ASC = "SIGNATURE_DATE_ASC"
    SIGNATURE_DATE_DESC = "SIGNATURE_DATE_DESC"
    ID_ASC = "ID_ASC"
    ID_DESC = "ID_DESC"
    TITLE_ASC = "TITLE_ASC"
    TITLE_DESC = "TITLE_DESC"

# Classes pour construire la requête
@dataclass
class Critere:
    """Critère de recherche"""
    valeur: str
    typeRecherche: TypeRecherche
    operateur: Operateur = Operateur.ET
    proximite: Optional[int] = None
    criteres: List['Critere'] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire"""
        result = {
            "valeur": self.valeur,
            "typeRecherche": self.typeRecherche,
            "operateur": self.operateur
        }
        
        if self.proximite is not None:
            result["proximite"] = self.proximite
            
        if self.criteres:
            result["criteres"] = [critere.to_dict() for critere in self.criteres]
            
        return result

@dataclass
class Champ:
    """Champ de recherche"""
    typeChamp: TypeChamp
    criteres: List[Critere] = field(default_factory=list)
    operateur: Operateur = Operateur.ET
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire"""
        return {
            "typeChamp": self.typeChamp,
            "criteres": [critere.to_dict() for critere in self.criteres],
            "operateur": self.operateur
        }

@dataclass
class DatePeriod:
    """Période de dates"""
    start: str  # Format YYYY-MM-DD
    end: str    # Format YYYY-MM-DD
    
    def to_dict(self) -> Dict[str, str]:
        """Convertit l'objet en dictionnaire"""
        return {
            "start": self.start,
            "end": self.end
        }

@dataclass
class Filtre:
    """Filtre de recherche"""
    facette: str
    valeurs: Optional[List[str]] = None
    dates: Optional[DatePeriod] = None
    singleDate: Optional[str] = None  # Format YYYY-MM-DD
    multiValeurs: Optional[Dict[str, List[str]]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire"""
        result = {"facette": self.facette}
        
        if self.valeurs is not None:
            result["valeurs"] = self.valeurs
            
        if self.dates is not None:
            result["dates"] = self.dates.to_dict()
            
        if self.singleDate is not None:
            result["singleDate"] = self.singleDate
            
        if self.multiValeurs is not None:
            result["multiValeurs"] = self.multiValeurs
            
        return result

@dataclass
class RechercheSpecifique:
    """Objet de recherche spécifique"""
    pageNumber: int = 1
    pageSize: int = 10
    operateur: Operateur = Operateur.ET
    sort: TriPossible = TriPossible.PERTINENCE
    typePagination: TypePagination = TypePagination.DEFAUT
    champs: List[Champ] = field(default_factory=list)
    filtres: List[Filtre] = field(default_factory=list)
    secondSort: Optional[TriPossible] = None
    fromAdvancedRecherche: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire"""
        result = {
            "pageNumber": self.pageNumber,
            "pageSize": self.pageSize,
            "operateur": self.operateur,
            "sort": self.sort,
            "typePagination": self.typePagination,
            "champs": [champ.to_dict() for champ in self.champs],
            "filtres": [filtre.to_dict() for filtre in self.filtres]
        }
        
        if self.secondSort is not None:
            result["secondSort"] = self.secondSort
            
        if self.fromAdvancedRecherche:
            result["fromAdvancedRecherche"] = True
            
        return result

@dataclass
class SearchRequest:
    """Requête de recherche"""
    fond: Fond
    recherche: RechercheSpecifique
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'objet en dictionnaire"""
        return {
            "fond": self.fond,
            "recherche": self.recherche.to_dict()
        }

# Fonction principale de recherche
def recherche_legifrance(
    query: Optional[str] = None,
    type_champ: Union[TypeChamp, str] = TypeChamp.ALL,
    type_recherche: Union[TypeRecherche, str] = TypeRecherche.EXACTE,
    fond: Union[Fond, str] = Fond.LODA_DATE,
    filtres: Optional[List[Dict[str, Any]]] = None,
    page: int = 1,
    page_size: int = 10,
    tri: Union[TriPossible, str] = TriPossible.PERTINENCE,
    second_tri: Optional[Union[TriPossible, str]] = None,
    operateur: Union[Operateur, str] = Operateur.ET,
    proximite: Optional[int] = None,
    type_pagination: Union[TypePagination, str] = TypePagination.DEFAUT,
    recherche_avancee: bool = False,
    token: Optional[str] = None,
    api_url: str = "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app/search"
) -> Dict[str, Any]:
    """
    Fonction générale pour rechercher dans l'API Legifrance avec de nombreuses options.
    
    Args:
        query: Texte à rechercher (None pour ne pas spécifier de recherche textuelle)
        type_champ: Type de champ pour la recherche (ALL, TITLE, NUM_ARTICLE, etc.)
        type_recherche: Type de recherche (EXACTE, UN_DES_MOTS, etc.)
        fond: Fond documentaire (LODA_DATE, CODE_DATE, JURI, ALL, etc.)
        filtres: Liste de dictionnaires de filtres
            Ex: [{"facette": "NATURE", "valeurs": ["LOI", "ORDONNANCE"]},
                 {"facette": "DATE_SIGNATURE", "dates": {"start": "2020-01-01", "end": "2022-12-31"}}]
        page: Numéro de page
        page_size: Nombre de résultats par page (max 100)
        tri: Méthode de tri principal
        second_tri: Méthode de tri secondaire
        operateur: Opérateur logique pour combiner les critères (ET ou OU)
        proximite: Proximité pour la recherche textuelle (nombre de mots séparant les termes)
        type_pagination: Type de pagination (DEFAUT ou ARTICLE)
        recherche_avancee: Indique s'il s'agit d'une recherche avancée
        token: Token d'authentification (obtenu automatiquement si non fourni)
        api_url: URL de l'API

    Returns:
        Résultats de la recherche en format dictionnaire
    """
    # Conversion des paramètres string en enum si nécessaire
    if isinstance(type_champ, str):
        type_champ = TypeChamp(type_champ)
    if isinstance(type_recherche, str):
        type_recherche = TypeRecherche(type_recherche)
    if isinstance(fond, str):
        fond = Fond(fond)
    if isinstance(tri, str):
        tri = TriPossible(tri)
    if isinstance(operateur, str):
        operateur = Operateur(operateur)
    if isinstance(type_pagination, str):
        type_pagination = TypePagination(type_pagination)
    if second_tri and isinstance(second_tri, str):
        second_tri = TriPossible(second_tri)

    # Construction de la requête
    recherche = RechercheSpecifique(
        pageNumber=page,
        pageSize=page_size,
        operateur=operateur,
        sort=tri,
        typePagination=type_pagination,
        secondSort=second_tri,
        fromAdvancedRecherche=recherche_avancee
    )
    
    # Ajout de la requête textuelle si spécifiée
    if query:
        critere = Critere(
            valeur=query,
            typeRecherche=type_recherche,
            operateur=operateur,
            proximite=proximite
        )
        champ = Champ(
            typeChamp=type_champ,
            criteres=[critere],
            operateur=operateur
        )
        recherche.champs.append(champ)
    
    # Ajout des filtres si spécifiés
    if filtres:
        for f in filtres:
            filtre = None
            
            if "dates" in f:
                dates = DatePeriod(start=f["dates"]["start"], end=f["dates"]["end"])
                filtre = Filtre(facette=f["facette"], dates=dates)
            elif "singleDate" in f:
                filtre = Filtre(facette=f["facette"], singleDate=f["singleDate"])
            elif "valeurs" in f:
                filtre = Filtre(facette=f["facette"], valeurs=f["valeurs"])
            elif "multiValeurs" in f:
                filtre = Filtre(facette=f["facette"], multiValeurs=f["multiValeurs"])
            
            if filtre:
                recherche.filtres.append(filtre)
    
    # Construction de la requête finale
    search_request = SearchRequest(fond=fond, recherche=recherche)
    payload = search_request.to_dict()
    
    # Récupération du token si non fourni
    if token is None:
        token = obtain_token()  # Fonction à implémenter selon votre système d'authentification
    
    # En-têtes de la requête
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # Appel à l'API
    response = requests.post(api_url, json=payload, headers=headers)
    
    # Vérification de la réponse
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erreur {response.status_code}: {response.text}")

from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# Configuration des identifiants API Legifrance Sandbox
LEGIFRANCE_CLIENT_ID = os.getenv("LEGIFRANCE_CLIENT_ID")
LEGIFRANCE_CLIENT_SECRET = os.getenv("LEGIFRANCE_CLIENT_SECRET")
LEGIFRANCE_BASE_URL = "https://sandbox-api.piste.gouv.fr/dila/legifrance/lf-engine-app"
LEGIFRANCE_OAUTH_URL = "https://sandbox-oauth.piste.gouv.fr/api/oauth/token"

def obtain_token():
    """Obtient un token OAuth pour l'API Legifrance."""
    url = LEGIFRANCE_OAUTH_URL
    
    payload = {
        "grant_type": "client_credentials",
        "client_id": LEGIFRANCE_CLIENT_ID,
        "client_secret": LEGIFRANCE_CLIENT_SECRET,
        "scope": "openid"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(url, data=payload, headers=headers)
    
     
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Erreur d'authentification: {response.status_code} - {response.text}")
        return None
  