# ============================================
# ai_client.py — WebClient / RestTemplate Layer
# Only job: call Ollama (or AI Gateway) and return response
# Java Analogy: Like RestTemplate/WebClient — sends request, gets response
# ============================================

import requests

# --- Configuration ---
# Local: Ollama (FREE)
# Production: AI Gateway GPT-4o (Okta M2M)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:7b"
TIMEOUT = 600  # 10 minutes — LLM can be slow on big codebases


def call_ai(prompt):
    """
    Ollama ko prompt bhejta hai aur response laata hai.
    
    Java Analogy:
        RestTemplate.postForObject(OLLAMA_URL, request, String.class)
    
    Production mein yeh AI Gateway + Okta M2M ban jaayega:
        OLLAMA_URL → https://ai-gateway.cigna.com/v1/completions
        MODEL → gpt-4o
        Headers → Bearer token from Okta
    """
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=TIMEOUT)

        return response.json().get("response", "")

    except requests.exceptions.ConnectionError:
        print("  ERROR: Ollama not running! Start with: ollama serve")
        return None
    except Exception as e:
        print(f"  ERROR: AI call failed - {e}")
        return None