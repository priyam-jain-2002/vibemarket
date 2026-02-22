"""
LLM Backend Abstraction Layer

Supports multiple LLM providers:
- Anthropic Claude (default)
- OpenAI GPT-4
- Google Gemini
- Easy to add more

Usage:
    backend = get_llm_backend()  # Auto-detects from .env
    response = backend.generate(prompt, system_message)
"""

import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

# Load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class LLMBackend(ABC):
    """Abstract base class for LLM backends"""

    @abstractmethod
    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate text from prompt"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if API key is configured"""
        pass


class ClaudeBackend(LLMBackend):
    """Anthropic Claude backend"""

    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.model = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514')
        self.client = None

        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                print("⚠️  anthropic package not installed. Run: pip install anthropic")

    def is_available(self) -> bool:
        return self.client is not None

    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("Claude API not configured. Set ANTHROPIC_API_KEY in .env")

        messages = [{"role": "user", "content": prompt}]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_message or "You are a helpful assistant.",
            messages=messages
        )

        return response.content[0].text


class OpenAIBackend(LLMBackend):
    """OpenAI GPT-4 backend"""

    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        self.client = None

        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("⚠️  openai package not installed. Run: pip install openai")

    def is_available(self) -> bool:
        return self.client is not None

    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("OpenAI API not configured. Set OPENAI_API_KEY in .env")

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )

        return response.choices[0].message.content


class GeminiBackend(LLMBackend):
    """Google Gemini backend"""

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        self.model = os.getenv('GEMINI_MODEL', 'gemini-pro')
        self.client = None

        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model)
            except ImportError:
                print("⚠️  google-generativeai package not installed. Run: pip install google-generativeai")

    def is_available(self) -> bool:
        return self.client is not None

    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("Gemini API not configured. Set GEMINI_API_KEY in .env")

        # Combine system message and prompt for Gemini
        full_prompt = prompt
        if system_message:
            full_prompt = f"{system_message}\n\n{prompt}"

        response = self.client.generate_content(full_prompt)
        return response.text


class OllamaBackend(LLMBackend):
    """Ollama (local LLM) backend"""

    def __init__(self):
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'llama3')
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if Ollama is running"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def is_available(self) -> bool:
        return self.available

    def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        if not self.is_available():
            raise ValueError("Ollama not running. Start with: ollama serve")

        import requests

        # Use /api/chat for better instruction following (system/user separation)
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.1,   # Low temp = more consistent JSON output
                    "num_ctx": 8192       # Large context window for lead analysis
                }
            },
            timeout=120  # 2 min timeout for large prompts
        )

        data = response.json()

        # /api/chat response format: {"message": {"content": "..."}}
        if "message" in data:
            return data["message"]["content"]

        # Fallback for error responses
        if "error" in data:
            raise ValueError(f"Ollama error: {data['error']}")

        raise ValueError(f"Unexpected Ollama response: {list(data.keys())}")


# Factory function to get the right backend
def get_llm_backend(provider: Optional[str] = None) -> LLMBackend:
    """
    Get LLM backend based on environment configuration.

    Args:
        provider: Force specific provider ('claude', 'openai', 'gemini', 'ollama')
                 If None, auto-detects from available API keys

    Returns:
        LLMBackend instance

    Raises:
        ValueError: If no LLM backend is available
    """

    # If provider specified, use it
    if provider:
        provider = provider.lower()
        if provider == 'claude':
            backend = ClaudeBackend()
            if backend.is_available():
                return backend
        elif provider == 'openai':
            backend = OpenAIBackend()
            if backend.is_available():
                return backend
        elif provider == 'gemini':
            backend = GeminiBackend()
            if backend.is_available():
                return backend
        elif provider == 'ollama':
            backend = OllamaBackend()
            if backend.is_available():
                return backend

        raise ValueError(f"LLM provider '{provider}' not available. Check API key in .env")

    # Auto-detect from environment variable
    llm_provider = os.getenv('LLM_PROVIDER', '').lower()
    if llm_provider:
        return get_llm_backend(llm_provider)

    # Try each backend in order of preference
    backends = [
        ('Claude (Anthropic)', ClaudeBackend()),
        ('OpenAI GPT-4', OpenAIBackend()),
        ('Google Gemini', GeminiBackend()),
        ('Ollama (Local)', OllamaBackend()),
    ]

    for name, backend in backends:
        if backend.is_available():
            print(f"✅ Using {name}")
            return backend

    # No backend available
    raise ValueError(
        "No LLM backend available! Please configure one:\n"
        "  - Claude: Set ANTHROPIC_API_KEY in .env\n"
        "  - OpenAI: Set OPENAI_API_KEY in .env\n"
        "  - Gemini: Set GEMINI_API_KEY in .env\n"
        "  - Ollama: Run 'ollama serve' for local LLM"
    )


def list_available_backends() -> Dict[str, bool]:
    """List all available LLM backends"""
    return {
        'claude': ClaudeBackend().is_available(),
        'openai': OpenAIBackend().is_available(),
        'gemini': GeminiBackend().is_available(),
        'ollama': OllamaBackend().is_available(),
    }


if __name__ == '__main__':
    # Test which backends are available
    print("🔍 Checking available LLM backends...\n")

    backends = list_available_backends()
    for name, available in backends.items():
        status = "✅ Available" if available else "❌ Not configured"
        print(f"{name.capitalize():15} {status}")

    print("\n" + "="*60)

    # Try to get a backend
    try:
        backend = get_llm_backend()
        print(f"\n🎯 Auto-selected backend ready!")
        print(f"   You can start using the lead generator now.")
    except ValueError as e:
        print(f"\n⚠️  {e}")
        print("\n💡 Configure at least one LLM backend in your .env file")
