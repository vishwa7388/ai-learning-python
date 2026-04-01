# ============================================
# prompt_builder.py — Service Layer
# Builds AI prompts using ROLE/CONTEXT/TASK/FORMAT pattern
# Java Analogy: Like Service layer — contains business logic (prompt engineering)
#               but does NOT call external APIs itself
# 
# KEY DESIGN: Every function returns a prompt STRING only.
#             AI call is NOT made here — that's ai_client's job.
#             This is SRP (Single Responsibility Principle)!
# 
# GENERIC: All prompts work on ANY Spring Boot project.
#          No project-specific language (no "DP API", no "pharmacy routing").
# ============================================


def build_docs_prompt(all_code):
    """Markdown documentation ka prompt — like building a search query in Service layer"""
    return f"""ROLE: You are a Senior Spring Boot architect who writes Confluence documentation.

CONTEXT: Analyze the following Spring Boot microservice codebase.

TASK: Generate complete API documentation.

FORMAT (Markdown):

## 1. Overview
(What does this API do - 2 lines max)

## 2. Entry Point
(Controller, endpoint, HTTP method)

## 3. Request
(What fields come in the request)

## 4. Processing Flow
Step 1: ...
Step 2: ...

## 5. External API Calls
| API Name | Purpose | Called From |
|----------|---------|-------------|

## 6. Business Rules
(List each rule and what it does)

## 7. Response
(What fields go back in response)

Do NOT explain annotations or Spring Boot basics.
Do NOT repeat any point. Keep it concise.

CODE:
{all_code}"""


def build_html_prompt(all_code):
    """HTML documentation ka prompt"""
    return f"""ROLE: You are a Senior Spring Boot architect who writes Confluence documentation.

CONTEXT: Analyze the following Spring Boot microservice codebase.

TASK: Generate complete API documentation.

FORMAT:
Generate output in clean HTML format.
Use <h2> for sections, <table> for tables, <ol> for steps.
Do NOT use Markdown. Use only HTML tags.
OUTPUT ONLY HTML TAGS. No Markdown symbols like # or ** or ```. Only use <h2>, <p>, <table>, <ol> tags.

Sections:
1. Overview (2 lines max)
2. Entry Point (Controller, endpoint, HTTP method)
3. Request (fields)
4. Processing Flow (step by step)
5. External API Calls (table: API Name, Purpose, Called From)
6. Business Rules (list each rule)
7. Response (fields)

Do NOT explain annotations or Spring Boot basics.
Do NOT repeat any point. Keep it concise.

CODE:
{all_code}"""


def build_hld_prompt(all_code):
    """High-Level Design prompt — architecture overview"""
    return f"""ROLE: You are a Senior Spring Boot architect who writes high-level design documents.

CONTEXT: Analyze the following Spring Boot microservice codebase.

TASK: Produce a concise high-level design from the codebase.

FORMAT (Markdown only). Use exactly these ## section headings in order:

## System Overview
(2 lines max: what the system does and its main boundary)

## Architecture Layers
Describe how code maps to: Controller, Service, Adaptor (or Adapter), Model layers. Use bullets or short paragraphs.

## Component Responsibilities
| Component | Layer | Responsibility |
|-----------|-------|----------------|
(One row per significant class or package; infer from code)

## External Systems and APIs
| System/API | Purpose | Called From |
|------------|---------|-------------|
(HTTP clients, RSS, DB, message queues, third-party URLs, etc.—only what appears in code)

## Tech Stack
(Bullet list: language, framework, key libraries, build tool—only what is evidenced by the code)

## Data Flow Summary
(Short numbered or bulleted summary: request in → layers → external calls → response out)

Do NOT explain annotations or Spring Boot basics.
Do NOT repeat any point. Keep tables aligned and readable.

CODE:
{all_code}"""


def build_lld_prompt(all_code):
    """Low-Level Design prompt — class-by-class detail"""
    return f"""ROLE: You are a Senior Spring Boot architect who writes low-level design documents.

CONTEXT: Analyze the following Spring Boot microservice codebase.

TASK: Produce a low-level design from the codebase: class-by-class detail grounded in the actual code.

FORMAT (Markdown only). For each public or significant class, use this structure (repeat per class):

## <ClassName>

### Key fields / attributes
(Bullet list: field name, type, brief role—only members that matter for behavior or API contracts)

### Methods
| Method | Parameters | Return type | Purpose |
|--------|------------|-------------|---------|
(One row per non-trivial method; include constructors if they encode important wiring)

### Dependencies
(Bullets: which other classes this class calls or injects—caller → callee)

Also include one top section before the per-class blocks:

## Class dependency overview
(Short table or bullet list summarizing which class calls which across the project)

Skip boilerplate getters/setters unless they encode business meaning.
Do NOT explain annotations or Spring Boot basics.
Do NOT repeat the same method or field twice. Keep tables aligned and readable.

CODE:
{all_code}"""


def build_mermaid_prompt(all_code):
    """Mermaid sequence diagram ka prompt"""
    return f"""ROLE: Senior Spring Boot Architect.

TASK: Generate a Mermaid.js sequenceDiagram JSON array.

CRITICAL RULES:
1. Output ONLY a valid JSON array of strings.
2. Participant definitions MUST be separate from interaction arrows.
3. Use 'box' syntax for layers.
4. Participants inside the box should NOT have quotes in the name.
5. Flow interactions (arrows) must follow the participant definitions.

EXAMPLE:
["sequenceDiagram", "autonumber", "box rgba(230, 245, 255, 0.5) API", "participant SearchController", "end", "SearchController->>SearchService: process"]

CODE:
{all_code}"""


def build_flow_prompt(all_code):
    """Connected flow analysis prompt"""
    return f"""ROLE: You are a Senior Spring Boot architect.

CONTEXT: Analyze the following Spring Boot microservice codebase.

TASK: Trace the COMPLETE request flow from entry point to final response.
Show how classes connect to each other.

FORMAT:
Step 1: [What happens] (which class, which method)
Step 2: [What happens] (which class, which method)
...continue until response is sent back.

Do NOT explain annotations or Spring Boot basics.
Do NOT repeat any point. Keep it concise.

CODE:
{all_code}"""


def build_audit_prompt(all_code):
    """Security audit ka prompt"""
    return f"""ROLE: You are a Cyber Security Expert specializing in Spring Boot applications.

TASK: Analyze this code for security vulnerabilities.

FORMAT:

## Security Findings

For each finding:
- Severity: HIGH / MEDIUM / LOW
- Location: (which file, which line/method)
- Issue: (what is the problem)
- Fix: (how to fix it)

Check for:
- SQL Injection
- Missing input validation
- Hardcoded credentials
- Missing authentication
- Insecure API calls (HTTP vs HTTPS)
- Missing error handling that leaks info
- Missing rate limiting

Do NOT repeat any point. Keep it concise.

CODE:
{all_code}"""


def build_smart_prompt(category, code, filename):
    """File type ke hisaab se different prompt — like strategy pattern in Java"""
    prompts = {
        "controllers": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this REST Controller.
FORMAT:
- Endpoint URL and HTTP Method
- Request Body fields
- Response Body fields
- Which Service it calls
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "services": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this Service class and trace the business flow.
FORMAT:
- Purpose (1 line)
- Step-by-step business logic flow
- External calls made (which Adaptors)
- Business rules applied
- Return value
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "adaptors": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this Adaptor/Client class.
FORMAT:
- External API URL it calls
- HTTP Method used
- Request parameters
- Response type
- Error handling
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "rules": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this Business Rule class.
FORMAT:
- Rule Name
- What it checks
- Input parameters
- Decision logic
- Impact on application flow
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "models": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this model/DTO class.
FORMAT:
- Purpose
- Fields (name and type)
- Used as Request or Response
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}""",

        "config": f"""ROLE: You are a Senior Spring Boot architect.
TASK: Analyze this configuration class.
FORMAT:
- What it configures
- Beans defined
- Properties used
Do NOT explain annotations. Keep it concise. Do NOT repeat any point.
FILE: {filename}
CODE:
{code}"""
    }

    return prompts.get(category, prompts["services"])