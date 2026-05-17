"""
LLM Abstraction Layer for CodeOracle
Supports: Groq, Ollama, IBM watsonx.ai
"""

import os
import json
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BaseLLM(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 4096) -> str:
        """Generate text from prompt"""
        pass
    
    @abstractmethod
    def generate_json(self, prompt: str, temperature: float = 0.1, max_tokens: int = 4096) -> Dict[str, Any]:
        """Generate and parse JSON response"""
        pass


class GroqLLM(BaseLLM):
    """Groq API implementation (Fast, Free Tier)"""
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
    
    def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 4096) -> str:
        """Generate text using Groq API with retry logic"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a precise code analysis assistant. Always respond with valid JSON when requested."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        import time as time_module
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(self.base_url, headers=headers, json=payload, timeout=120)
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except requests.exceptions.RequestException as e:
                if hasattr(e, 'response') and e.response is not None and e.response.status_code == 429 and attempt < max_retries - 1:
                    wait = 2 ** (attempt + 1)
                    time_module.sleep(wait)
                    continue
                raise Exception(f"Groq API error: {str(e)}")
    
    def generate_json(self, prompt: str, temperature: float = 0.1, max_tokens: int = 4096) -> Dict[str, Any]:
        """Generate and parse JSON response"""
        response_text = self.generate(prompt, temperature, max_tokens)
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            # Try to extract JSON from markdown code blocks
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            raise Exception(f"Failed to parse JSON response: {str(e)}\nResponse: {response_text[:500]}")


class OllamaLLM(BaseLLM):
    """Ollama local LLM implementation"""
    
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    
    def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 4096) -> str:
        """Generate text using Ollama"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result["response"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def generate_json(self, prompt: str, temperature: float = 0.1, max_tokens: int = 4096) -> Dict[str, Any]:
        """Generate and parse JSON response"""
        response_text = self.generate(prompt, temperature, max_tokens)
        try:
            # Try direct parsing
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            # Try to find JSON object in text
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
            raise Exception(f"Failed to parse JSON from Ollama response: {response_text[:500]}")


class WatsonxLLM(BaseLLM):
    """IBM watsonx.ai implementation"""
    
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.model = os.getenv("WATSONX_MODEL", "ibm/granite-13b-instruct-v2")
        
        if not self.api_key or not self.project_id:
            raise ValueError("WATSONX_API_KEY and WATSONX_PROJECT_ID required")
        
        # Get IAM token
        self.token = self._get_iam_token()
    
    def _get_iam_token(self) -> str:
        """Get IBM Cloud IAM token"""
        url = "https://iam.cloud.ibm.com/identity/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": self.api_key
        }
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=30)
            response.raise_for_status()
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get IAM token: {str(e)}")
    
    def generate(self, prompt: str, temperature: float = 0.1, max_tokens: int = 4096) -> str:
        """Generate text using watsonx.ai"""
        url = f"{self.url}/ml/v1/text/generation?version=2023-05-29"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model_id": self.model,
            "input": prompt,
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": max_tokens,
                "decoding_method": "greedy"
            },
            "project_id": self.project_id
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            return result["results"][0]["generated_text"]
        except requests.exceptions.RequestException as e:
            raise Exception(f"watsonx.ai API error: {str(e)}")
    
    def generate_json(self, prompt: str, temperature: float = 0.1, max_tokens: int = 4096) -> Dict[str, Any]:
        """Generate and parse JSON response"""
        response_text = self.generate(prompt, temperature, max_tokens)
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            start = response_text.find("{")
            end = response_text.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response_text[start:end]
                return json.loads(json_str)
            raise Exception(f"Failed to parse JSON from watsonx response: {response_text[:500]}")


def get_llm(provider: Optional[str] = None) -> BaseLLM:
    """
    Factory function to get LLM instance based on provider
    
    Args:
        provider: One of 'groq', 'ollama', 'watsonx'. If None, uses LLM_PROVIDER env var
    
    Returns:
        BaseLLM instance
    """
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "groq").lower()
    
    providers = {
        "groq": GroqLLM,
        "ollama": OllamaLLM,
        "watsonx": WatsonxLLM
    }
    
    if provider not in providers:
        raise ValueError(f"Unknown provider: {provider}. Choose from: {list(providers.keys())}")
    
    try:
        return providers[provider]()
    except Exception as e:
        raise Exception(f"Failed to initialize {provider} LLM: {str(e)}")


# Convenience function for quick testing
def test_llm(provider: Optional[str] = None):
    """Test LLM connection and JSON parsing"""
    llm = get_llm(provider)
    test_prompt = 'Respond with valid JSON: {"status": "working", "message": "LLM is operational"}'
    
    try:
        result = llm.generate_json(test_prompt)
        print(f"✅ {provider or os.getenv('LLM_PROVIDER')} LLM is working!")
        print(f"Response: {json.dumps(result, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ {provider or os.getenv('LLM_PROVIDER')} LLM test failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Test the configured LLM
    test_llm()

# Made with Bob
