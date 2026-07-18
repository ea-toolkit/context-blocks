"""
DDC Entity Meta-Model — 17 Types in 6 Layers.

This is the SOURCE OF TRUTH for entity classification.
Every extracted entity MUST map to one of these types.
"""

from enum import Enum

from pydantic import BaseModel


class EntityLayer(str, Enum):
    """The six knowledge layers, each answering a distinct class of question."""

    STRUCTURAL = "structural"  # "What exists?"
    BEHAVIORAL = "behavioral"  # "How does it work?"
    REFERENCE = "reference"  # "What are the allowed values?"
    ORGANIZATIONAL = "organizational"  # "Who is involved?"
    LANGUAGE = "language"  # "What do terms mean?"
    DECISION = "decision"  # "Why was this chosen?"


class EntityType(str, Enum):
    """The 18 entity types organized by layer."""

    # Structural layer — "What exists?"
    SYSTEM = "system"
    SOFTWARE_COMPONENT = "software-component"
    API = "api"
    DATA_MODEL = "data-model"
    DATA_PRODUCT = "data-product"
    PLATFORM = "platform"

    # Behavioral layer — "How does it work?"
    PROCESS = "process"
    BUSINESS_EVENT = "business-event"
    DOMAIN_LOGIC = "domain-logic"

    # Reference layer — "What are the allowed values?"
    REFERENCE_DATA = "reference-data"

    # Organizational layer — "Who is involved?"
    TEAM = "team"
    PERSONA = "persona"
    CAPABILITY = "capability"
    OFFERING = "offering"
    EXTERNAL_PARTY = "external-party"

    # Language layer — "What do terms mean?"
    JARGON_BUSINESS = "jargon-business"
    JARGON_TECH = "jargon-tech"

    # Decision layer — "Why was this chosen?"
    DECISION = "decision"


class RelationshipType(str, Enum):
    """Relationship types between entities — generic + type-specific."""

    # Generic (available on every entity type)
    RELATED_TO = "related_to"
    DEPENDS_ON = "depends_on"
    SUPERSEDES = "supersedes"
    PART_OF = "part_of"

    # Ownership & governance
    OWNED_BY = "owned_by"
    GOVERNED_BY = "governed_by"
    MADE_BY = "made_by"

    # Structural / deployment
    DEPLOYED_ON = "deployed_on"
    BELONGS_TO = "belongs_to"
    HOSTS = "hosts"
    HOSTED_BY = "hosted_by"
    USED_BY = "used_by"
    ENABLES = "enables"
    REQUIRES = "requires"

    # Interface / API
    EXPOSES = "exposes"
    EXPOSED_BY = "exposed_by"
    CONSUMED_BY = "consumed_by"
    CONTRACTS = "contracts"

    # Data
    PERSISTS = "persists"
    SOURCED_FROM = "sourced_from"
    CONTAINS = "contains"
    MAPS_TO = "maps_to"
    PRODUCED_BY = "produced_by"
    PARAMETERISES = "parameterises"

    # Behavioral
    TRIGGERS = "triggers"
    TRIGGERED_BY = "triggered_by"
    PRODUCES = "produces"
    CONSUMES = "consumes"
    PUBLISHED_BY = "published_by"
    CARRIES = "carries"
    HANDLES = "handles"
    COMMUNICATES_WITH = "communicates_with"

    # Process / people
    EXECUTED_BY = "executed_by"
    INVOLVES = "involves"
    INITIATES = "initiates"
    SERVES = "serves"
    SERVED_BY = "served_by"
    IMPLEMENTS = "implements"
    REALISED_BY = "realised_by"
    POWERED_BY = "powered_by"
    PROVIDED_BY = "provided_by"
    INTEGRATED_VIA = "integrated_via"
    PROVIDES = "provides"

    # Logic / decisions
    ENFORCED_BY = "enforced_by"
    APPLIES_TO = "applies_to"
    DERIVES_FROM = "derives_from"
    DOCUMENTED_IN = "documented_in"
    ENFORCED_VIA = "enforced_via"
    MOTIVATED_BY = "motivated_by"

    # Jargon
    USED_IN = "used_in"
    DEFINED_BY = "defined_by"
    SYNONYMOUS_WITH = "synonymous_with"
    CONTRASTS_WITH = "contrasts_with"


# Expected relationships per entity type — the agent should actively look for these
EXPECTED_RELATIONSHIPS: dict[EntityType, list[dict]] = {
    EntityType.SYSTEM: [
        {"rel": "deployed_on", "target": "platform", "meaning": "Infrastructure this system runs on"},
        {"rel": "exposes", "target": "api", "meaning": "APIs this system makes available"},
        {"rel": "owned_by", "target": "team", "meaning": "Team operationally responsible"},
        {"rel": "persists", "target": "data-model", "meaning": "Primary data model this system stores"},
        {"rel": "communicates_with", "target": "system", "meaning": "Runtime communication with another system"},
        {"rel": "handles", "target": "business-event", "meaning": "Business events this system reacts to or produces"},
    ],
    EntityType.SOFTWARE_COMPONENT: [
        {"rel": "belongs_to", "target": "system", "meaning": "System this component is part of"},
        {"rel": "implements", "target": "capability", "meaning": "Capability this component realises"},
        {"rel": "used_by", "target": "system", "meaning": "Systems that depend on this component"},
        {"rel": "owned_by", "target": "team", "meaning": "Team responsible"},
        {"rel": "deployed_on", "target": "platform", "meaning": "Platform this component runs on"},
    ],
    EntityType.API: [
        {"rel": "exposed_by", "target": "system", "meaning": "System that serves this API"},
        {"rel": "consumed_by", "target": "system", "meaning": "Systems that call this API"},
        {"rel": "contracts", "target": "data-model", "meaning": "Data models exchanged through this API"},
        {"rel": "governed_by", "target": "team", "meaning": "Team responsible for versioning"},
        {"rel": "triggers", "target": "business-event", "meaning": "Events that result from calling this API"},
    ],
    EntityType.DATA_MODEL: [
        {"rel": "owned_by", "target": "system", "meaning": "System that is authoritative source"},
        {"rel": "used_by", "target": "system", "meaning": "Systems that read or depend on this model"},
        {"rel": "implements", "target": "domain-logic", "meaning": "Business rules encoded in constraints"},
        {"rel": "maps_to", "target": "data-model", "meaning": "Equivalent model in another bounded context"},
    ],
    EntityType.DATA_PRODUCT: [
        {"rel": "produced_by", "target": "system", "meaning": "System that generates this data product"},
        {"rel": "consumed_by", "target": "system", "meaning": "Downstream consumers"},
        {"rel": "owned_by", "target": "team", "meaning": "Team accountable for quality and SLA"},
        {"rel": "contains", "target": "data-model", "meaning": "Data models this product exposes"},
        {"rel": "sourced_from", "target": "data-product", "meaning": "Upstream data products this derives from"},
    ],
    EntityType.PLATFORM: [
        {"rel": "hosted_by", "target": "external-party", "meaning": "Cloud provider supplying this platform"},
        {"rel": "owned_by", "target": "team", "meaning": "Platform team responsible"},
        {"rel": "enables", "target": "capability", "meaning": "Capabilities this platform makes possible"},
        {"rel": "used_by", "target": "system", "meaning": "Systems that run on this platform"},
    ],
    EntityType.PROCESS: [
        {"rel": "owned_by", "target": "team", "meaning": "Team responsible for this process"},
        {"rel": "triggered_by", "target": "business-event", "meaning": "Event that starts this process"},
        {"rel": "produces", "target": "business-event", "meaning": "Event emitted on completion"},
        {"rel": "executed_by", "target": "system", "meaning": "System that automates this process"},
        {"rel": "involves", "target": "persona", "meaning": "Human roles that participate"},
        {"rel": "governed_by", "target": "domain-logic", "meaning": "Business rules that constrain this process"},
    ],
    EntityType.BUSINESS_EVENT: [
        {"rel": "published_by", "target": "system", "meaning": "System that emits this event"},
        {"rel": "consumed_by", "target": "system", "meaning": "Systems that react to this event"},
        {"rel": "triggers", "target": "process", "meaning": "Processes that start in response"},
        {"rel": "carries", "target": "data-model", "meaning": "Payload model this event transports"},
        {"rel": "governed_by", "target": "domain-logic", "meaning": "Rules that determine when this event is valid"},
    ],
    EntityType.DOMAIN_LOGIC: [
        {"rel": "enforced_by", "target": "system", "meaning": "System implementing this rule"},
        {"rel": "applies_to", "target": "data-model", "meaning": "Data model this rule constrains"},
        {"rel": "owned_by", "target": "team", "meaning": "Team that owns and can change this rule"},
        {"rel": "derives_from", "target": "reference-data", "meaning": "Reference data that parameterises this rule"},
        {"rel": "documented_in", "target": "decision", "meaning": "Decision that established this rule"},
    ],
    EntityType.REFERENCE_DATA: [
        {"rel": "owned_by", "target": "team", "meaning": "Team responsible for maintaining this data"},
        {"rel": "used_by", "target": "system", "meaning": "Systems that read this data at runtime"},
        {"rel": "parameterises", "target": "domain-logic", "meaning": "Business rules configured by this data"},
        {"rel": "sourced_from", "target": "external-party", "meaning": "External provider of this data"},
    ],
    EntityType.TEAM: [
        {"rel": "owns", "target": "system", "meaning": "Systems this team is responsible for"},
        {"rel": "depends_on", "target": "team", "meaning": "Other teams this team relies on"},
        {"rel": "responsible_for", "target": "process", "meaning": "Processes this team runs"},
        {"rel": "serves", "target": "persona", "meaning": "User personas this team benefits"},
    ],
    EntityType.PERSONA: [
        {"rel": "uses", "target": "system", "meaning": "Systems this persona interacts with"},
        {"rel": "initiates", "target": "process", "meaning": "Processes this persona starts"},
        {"rel": "served_by", "target": "offering", "meaning": "Offerings that deliver value to this persona"},
        {"rel": "belongs_to", "target": "external-party", "meaning": "If this persona is external"},
    ],
    EntityType.CAPABILITY: [
        {"rel": "enabled_by", "target": "system", "meaning": "Systems that implement this capability"},
        {"rel": "realised_by", "target": "software-component", "meaning": "Components that deliver this"},
        {"rel": "supports", "target": "offering", "meaning": "Offering this capability underpins"},
        {"rel": "owned_by", "target": "team", "meaning": "Team responsible"},
        {"rel": "requires", "target": "platform", "meaning": "Platform prerequisites"},
    ],
    EntityType.OFFERING: [
        {"rel": "provided_by", "target": "team", "meaning": "Team that owns delivery"},
        {"rel": "powered_by", "target": "capability", "meaning": "Capabilities that enable this"},
        {"rel": "consumed_by", "target": "persona", "meaning": "User type that receives value"},
    ],
    EntityType.EXTERNAL_PARTY: [
        {"rel": "provides", "target": "platform", "meaning": "Platforms this party supplies"},
        {"rel": "consumes", "target": "api", "meaning": "APIs this party calls"},
        {"rel": "governed_by", "target": "domain-logic", "meaning": "Contracts governing this party"},
        {"rel": "integrated_via", "target": "api", "meaning": "Integration interface used"},
    ],
    EntityType.JARGON_BUSINESS: [
        {"rel": "used_in", "target": "process", "meaning": "Processes where this term appears"},
        {"rel": "defined_by", "target": "domain-logic", "meaning": "Rule that formally defines this term"},
        {"rel": "synonymous_with", "target": "jargon-business", "meaning": "Equivalent term in adjacent context"},
        {"rel": "contrasts_with", "target": "jargon-business", "meaning": "Commonly confused term"},
    ],
    EntityType.JARGON_TECH: [
        {"rel": "used_in", "target": "system", "meaning": "Systems where this term is used"},
        {"rel": "applies_to", "target": "software-component", "meaning": "Components using this pattern"},
        {"rel": "documented_in", "target": "decision", "meaning": "Decisions that reference this term"},
        {"rel": "contrasts_with", "target": "jargon-tech", "meaning": "Commonly confused term"},
    ],
    EntityType.DECISION: [
        {"rel": "made_by", "target": "team", "meaning": "Team that made this decision"},
        {"rel": "applies_to", "target": "system", "meaning": "Systems this decision constrains"},
        {"rel": "supersedes", "target": "decision", "meaning": "Previous decision this replaces"},
        {"rel": "motivated_by", "target": "business-event", "meaning": "Incident that triggered this decision"},
        {"rel": "enforced_via", "target": "domain-logic", "meaning": "Rule that implements this decision"},
    ],
}


class QualityState(str, Enum):
    """Five-class quality model for demand classification."""

    CLEAN = "clean"  # Fully documented, current, reliable
    STALE = "stale"  # Documented but outdated
    INCOMPLETE = "incomplete"  # Partially documented
    MISSING = "missing"  # Not documented anywhere
    TRIBAL = "tribal"  # Exists only in people's heads


# Entity type metadata — maps each type to its layer and output directory
ENTITY_TYPE_CONFIG: dict[EntityType, dict] = {
    # Structural
    EntityType.SYSTEM: {
        "layer": EntityLayer.STRUCTURAL,
        "directory": "systems",
        "description": "Software that implements business logic specific to this domain — e.g., an inventory tracker, an order processor, a fraud detection engine, a claim adjudicator, a scheduling optimizer",
    },
    EntityType.SOFTWARE_COMPONENT: {
        "layer": EntityLayer.STRUCTURAL,
        "directory": "software-components",
        "description": "Named infrastructure software that supports but doesn't implement business logic — e.g., databases (PostgreSQL, MongoDB), API gateways, message brokers (Kafka, RabbitMQ), secret managers, CI/CD tools, monitoring tools",
    },
    EntityType.API: {
        "layer": EntityLayer.STRUCTURAL,
        "directory": "apis",
        "description": "Named API interfaces exposed or consumed by the domain — e.g., an order management API, a pricing query endpoint, a webhook receiver. Not generic 'REST API' but specific named interfaces",
    },
    EntityType.DATA_MODEL: {
        "layer": EntityLayer.STRUCTURAL,
        "directory": "data-models",
        "description": "The structure and schema of domain data — e.g., an order schema, a customer data model, an invoice format, a pricing rule structure. The shape of data, NOT the database that stores it",
    },
    EntityType.DATA_PRODUCT: {
        "layer": EntityLayer.STRUCTURAL,
        "directory": "data-products",
        "description": "Curated data assets published for consumption by other teams or systems — e.g., a daily sales summary, an analytics dataset, a customer churn dashboard feed",
    },
    EntityType.PLATFORM: {
        "layer": EntityLayer.STRUCTURAL,
        "directory": "platforms",
        "description": "Hosting environments and cloud infrastructure — e.g., Kubernetes clusters, AWS/GCP/Azure accounts, container orchestration platforms. The environment where systems RUN, not specific software components",
    },
    # Behavioral
    EntityType.PROCESS: {
        "layer": EntityLayer.BEHAVIORAL,
        "directory": "processes",
        "description": "Business processes and workflows with defined steps — e.g., an order fulfillment process, an invoice approval workflow, a supplier onboarding procedure, a monthly reconciliation cycle",
    },
    EntityType.BUSINESS_EVENT: {
        "layer": EntityLayer.BEHAVIORAL,
        "directory": "business-events",
        "description": "Named event flows that carry domain data between systems — e.g., order placed events, payment completed notifications, status change events, data sync triggers. Each distinct event flow is its own entity",
    },
    EntityType.DOMAIN_LOGIC: {
        "layer": EntityLayer.BEHAVIORAL,
        "directory": "domain-logic",
        "description": "Algorithmic rules, formulas, and business calculations that the system EXECUTES at runtime — e.g., pricing calculation rules, discount eligibility logic, routing algorithms, validation checks. These are the WHAT and HOW of computation. If it runs as code or a decision table, it's domain-logic. If it was a one-time choice about architecture or technology, it's a decision instead.",
    },
    # Reference
    EntityType.REFERENCE_DATA: {
        "layer": EntityLayer.REFERENCE,
        "directory": "reference-data",
        "description": "Code tables, enumerations, and taxonomies that power operational decisions — e.g., country codes, product categories, status types, currency mappings, zone definitions",
    },
    # Organizational
    EntityType.TEAM: {
        "layer": EntityLayer.ORGANIZATIONAL,
        "directory": "teams",
        "description": "Product teams and organizational units that own or operate parts of the domain",
    },
    EntityType.PERSONA: {
        "layer": EntityLayer.ORGANIZATIONAL,
        "directory": "personas",
        "description": "User roles and their responsibilities — e.g., a business analyst, an operations specialist, a supplier account manager. The PEOPLE who use or interact with the domain",
    },
    EntityType.CAPABILITY: {
        "layer": EntityLayer.ORGANIZATIONAL,
        "directory": "capabilities",
        "description": "Business capabilities the domain provides — e.g., cost calculation, invoice generation, supplier management. What the domain CAN DO at a business level",
    },
    EntityType.OFFERING: {
        "layer": EntityLayer.ORGANIZATIONAL,
        "directory": "offerings",
        "description": "Products and services the domain delivers to its customers or users",
    },
    EntityType.EXTERNAL_PARTY: {
        "layer": EntityLayer.ORGANIZATIONAL,
        "directory": "external-parties",
        "description": "Organizations outside the enterprise that participate in the domain — e.g., logistics suppliers, payment processors, regulatory bodies, partner companies",
    },
    # Language
    EntityType.JARGON_BUSINESS: {
        "layer": EntityLayer.LANGUAGE,
        "directory": "jargon-business",
        "description": "Business terminology and concepts specific to this domain that a new joiner wouldn't know — e.g., domain-specific abbreviations, business process names, organizational terms",
    },
    EntityType.JARGON_TECH: {
        "layer": EntityLayer.LANGUAGE,
        "directory": "jargon-tech",
        "description": "Technical terminology specific to this domain's implementation — e.g., internal project names, custom framework names, domain-specific technical abbreviations",
    },
    # Decision
    EntityType.DECISION: {
        "layer": EntityLayer.DECISION,
        "directory": "decisions",
        "description": "Architecture and design decisions — one-time choices that shaped the system. WHY something was chosen over alternatives — e.g., why one database technology over another, why a monolith was split into services, why events over REST. If the team decided it once and it constrains future work, it's a decision. If it's a rule the system evaluates repeatedly at runtime, it's domain-logic instead.",
    },
}


def get_directory_for_type(entity_type: "EntityType | str", ontology=None) -> str:
    """Get the output directory name for an entity type.

    Honors the active/custom ontology (its per-type `directory`) when set, falling back to the
    built-in default config, then to the type name itself for unmapped custom types.
    """
    from context_blocks.ontology import get_active_ontology

    ont = ontology if ontology is not None else get_active_ontology()
    type_str = entity_type.value if isinstance(entity_type, EntityType) else str(entity_type)

    if ont is not None:
        directory = ont.directory_for(type_str)
        if directory:
            return directory

    try:
        return ENTITY_TYPE_CONFIG[EntityType(type_str)]["directory"]
    except (ValueError, KeyError):
        return type_str


def get_layer_for_type(entity_type: EntityType) -> EntityLayer:
    """Get the layer an entity type belongs to."""
    return ENTITY_TYPE_CONFIG[entity_type]["layer"]


def get_all_types_for_layer(layer: EntityLayer) -> list[EntityType]:
    """Get all entity types belonging to a specific layer."""
    return [
        et for et, config in ENTITY_TYPE_CONFIG.items() if config["layer"] == layer
    ]


class EntityTypeReference(BaseModel):
    """Complete reference for a single entity type — used in prompts."""

    type: EntityType
    layer: EntityLayer
    directory: str
    description: str


def get_meta_model_reference() -> list[EntityTypeReference]:
    """Get the full meta-model as a list of references — for inclusion in LLM prompts."""
    return [
        EntityTypeReference(
            type=et,
            layer=config["layer"],
            directory=config["directory"],
            description=config["description"],
        )
        for et, config in ENTITY_TYPE_CONFIG.items()
    ]


def format_meta_model_for_prompt(ontology=None) -> str:
    """Format the meta-model as a readable string for LLM prompts.

    Honors the active/custom ontology when set (renders its types); otherwise the built-in default.
    """
    from context_blocks.ontology import get_active_ontology

    ont = ontology if ontology is not None else get_active_ontology()
    if ont is not None:
        return ont.format_for_prompt()

    lines = ["## Entity Meta-Model (18 Types in 6 Layers)\n"]
    current_layer = None

    for ref in get_meta_model_reference():
        if ref.layer != current_layer:
            current_layer = ref.layer
            lines.append(f"\n### {current_layer.value.title()} Layer")

        lines.append(f"- **{ref.type.value}**: {ref.description}")

    # Add expected relationships section
    lines.append("\n\n## Expected Relationships Per Entity Type")
    lines.append("\nFor each entity you create, actively look for these relationships.")
    lines.append("Generic relationships (`depends_on`, `related_to`, `supersedes`, `part_of`) are always available.\n")

    for entity_type, rels in EXPECTED_RELATIONSHIPS.items():
        lines.append(f"\n**{entity_type.value}:**")
        for rel in rels:
            lines.append(f"  - `{rel['rel']}` → {rel['target']} — {rel['meaning']}")

    return "\n".join(lines)
