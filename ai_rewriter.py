"""
AI Text Rewriter Module

This module provides a flexible interface for rewriting text using different AI providers.
Supports OpenAI, Anthropic, and can be extended for other providers.
"""

import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def rewrite_text(self, text: str, instructions: str) -> str:
        """Rewrite the given text according to instructions."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider for text rewriting."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable OPENAI_API_KEY
            model: Model to use for rewriting (default: gpt-3.5-turbo)
        """
        try:
            import openai

            self.client = openai.OpenAI(api_key=api_key)
            self.model = model
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI client: {e}")

    def rewrite_text(
        self,
        text: str,
        instructions: str,
        system_prompt: str,
        prompt: str,
        snippet: str,
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Rewrite text using OpenAI GPT."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        if prompt:
            messages.append({"role": "user", "content": prompt})
        if text:
            messages.append({"role": "user", "content": f"Text: {text}"})
        if snippet:
            messages.append({"role": "user", "content": f"Snippet: {snippet}"})
        if instructions:
            messages.append({"role": "user", "content": f"Instructions: {instructions}"})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"Instructions: {instructions}\n\nText to rewrite: {text}",
                    },
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider for text rewriting."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "claude-3-sonnet-20240229"
    ):
        """
        Initialize Anthropic provider.

        Args:
            api_key: Anthropic API key. If None, will try to get from environment variable ANTHROPIC_API_KEY
            model: Model to use for rewriting (default: claude-3-sonnet-20240229)
        """
        try:
            import anthropic

            self.client = anthropic.Anthropic(
                api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
            )
            self.model = model
        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Run: pip install anthropic"
            )
        except Exception as e:
            raise Exception(f"Failed to initialize Anthropic client: {e}")

    def rewrite_text(
        self,
        text: str,
        instructions: str = "Rewrite this text to be more engaging and clear.",
    ) -> str:
        """Rewrite text using Anthropic Claude."""
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": f"Instructions: {instructions}\n\nText to rewrite: {text}",
                    }
                ],
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise Exception(f"Anthropic API error: {e}")


class TextRewriter:
    """Main class for text rewriting with multiple AI providers."""

    def __init__(self, provider: str = "openai", **kwargs):
        """
        Initialize the text rewriter with a specific provider.

        Args:
            provider: AI provider to use ("openai", "anthropic")
            **kwargs: Additional arguments passed to the provider
        """
        self.provider_name = provider.lower()
        self.provider = self._create_provider(provider, **kwargs)

    def _create_provider(self, provider: str, **kwargs) -> AIProvider:
        """Create the appropriate provider instance."""
        provider_map = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
        }

        if provider.lower() not in provider_map:
            raise ValueError(
                f"Unsupported provider: {provider}. Supported providers: {list(provider_map.keys())}"
            )

        return provider_map[provider.lower()](**kwargs)

    def rewrite(
        self,
        text: str,
        instructions: str = "Rewrite this text to be more engaging and clear.",
    ) -> str:
        """
        Rewrite the given text.

        Args:
            text: Text to rewrite
            instructions: Instructions for how to rewrite the text

        Returns:
            Rewritten text
        """
        return self.provider.rewrite_text(text, instructions)

    def change_provider(self, new_provider: str, **kwargs):
        """
        Change the AI provider.

        Args:
            new_provider: New provider to use
            **kwargs: Additional arguments for the new provider
        """
        self.provider_name = new_provider.lower()
        self.provider = self._create_provider(new_provider, **kwargs)

    def get_provider_info(self) -> Dict[str, Any]:
        """Get information about the current provider."""
        return {
            "provider": self.provider_name,
            "model": getattr(self.provider, "model", "unknown"),
        }


def create_rewriter(provider: str = "openai", **kwargs) -> TextRewriter:
    """
    Convenience function to create a TextRewriter instance.

    Args:
        provider: AI provider to use
        **kwargs: Additional arguments for the provider

    Returns:
        TextRewriter instance
    """
    return TextRewriter(provider, **kwargs)


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    sample_text = "The weather is nice today. I went to the store and bought some food."

    print("=== AI Text Rewriter Demo ===\n")

    # Test with OpenAI (if API key is available)
    try:
        print("Testing OpenAI provider...")
        rewriter_openai = create_rewriter("openai", model="gpt-3.5-turbo")
        rewritten_openai = rewriter_openai.rewrite(
            sample_text, "Make this text more descriptive and engaging."
        )
        print(f"Original: {sample_text}")
        print(f"OpenAI Rewrite: {rewritten_openai}")
        print(f"Provider info: {rewriter_openai.get_provider_info()}\n")
    except Exception as e:
        print(f"OpenAI test failed: {e}\n")

    # Test with Anthropic (if API key is available)
    try:
        print("Testing Anthropic provider...")
        rewriter_anthropic = create_rewriter(
            "anthropic", model="claude-3-sonnet-20240229"
        )
        rewritten_anthropic = rewriter_anthropic.rewrite(
            sample_text, "Rewrite this in a more formal tone."
        )
        print(f"Original: {sample_text}")
        print(f"Anthropic Rewrite: {rewritten_anthropic}")
        print(f"Provider info: {rewriter_anthropic.get_provider_info()}\n")
    except Exception as e:
        print(f"Anthropic test failed: {e}\n")

    # Demonstrate provider switching
    try:
        print("Testing provider switching...")
        rewriter = create_rewriter("openai")
        print(f"Initial provider: {rewriter.get_provider_info()}")

        # Switch to Anthropic
        rewriter.change_provider("anthropic")
        print(f"After switching: {rewriter.get_provider_info()}")

    except Exception as e:
        print(f"Provider switching test failed: {e}")
