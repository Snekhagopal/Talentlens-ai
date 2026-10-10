
"""Gemini API client for TalentLens AI."""

import json

from google import genai
from google.genai import types
from src.config import GEMINI_MODEL


class GeminiError(RuntimeError):
    pass


class GeminiClient:
    def __init__(self, api_key: str | None = None):
        if api_key is None:
            import streamlit as st

            api_key = st.secrets.get("GEMINI_API_KEY", "")

        if not api_key:
            raise GeminiError(
                "GEMINI_API_KEY is missing. "
                "Configure .streamlit/secrets.toml."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = GEMINI_MODEL

    def is_available(self) -> bool:
        try:
            self.client.models.get(model=self.model)
            return True
        except Exception:
            return False

    def chat(
        self,
        system: str,
        user: str,
        json_mode: bool = False,
    ) -> str:
        try:
            config = {
                "system_instruction": system,
                "temperature": 0,
            }

            if json_mode:
                config["response_mime_type"] = "application/json"

            response = self.client.models.generate_content(
                model=self.model,
                contents=user,
                config=types.GenerateContentConfig(**config),
            )

            if not response.text:
                raise GeminiError("Gemini returned an empty response.")

            return response.text

        
        
        except GeminiError:
            raise
        except Exception as error:
            status_code = (
                getattr(error, "code", None)
                or getattr(error, "status_code", None)
            )
            detail = str(error)

            raise GeminiError(
                f"Gemini API request failed "
                f"(status={status_code or type(error).__name__}): "
                f"{detail}"
            ) from error


    def chat_json(self, system: str, user: str) -> dict:
        raw = self.chat(system, user, json_mode=True)

        try:
            result = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise GeminiError(
                "Gemini returned invalid JSON."
            ) from exc

        if not isinstance(result, dict):
            raise GeminiError("Expected a JSON object.")

        return result
