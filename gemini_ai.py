import logging
import time
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME
from typing import List, Dict

class GeminiAI:
    """
    Gemini AI integration for generating responses when FAQ doesn't have answers.
    """
    
    def __init__(self):
        """Initialize Gemini AI with API key."""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=GEMINI_API_KEY)
        preferred = GEMINI_MODEL_NAME or 'gemini-pro'
        self.model = genai.GenerativeModel(preferred)
        self.model_name = preferred
        self.last_error: str | None = None
        self._availability_cache = {"ok": None, "ts": 0.0}
        # System prompt for customer support
        self.system_prompt = """You are a helpful AI customer support assistant for Unthinkable Solutions. 

Your role:
- Provide accurate, helpful responses to customer queries
- Be polite, professional, and empathetic
- Keep responses concise but informative
- If you don't know something, or the user demands it, escalate the query to a human agent for assistance
- Always end with asking if there's anything else you can help with

Guidelines:
- Be friendly and approachable
- Use simple, clear language
- Provide step-by-step instructions when helpful
- Ask clarifying questions when needed
- Maintain a positive tone throughout the conversation"""

    def _choose_supported_model(self):
        try:
            candidates = []
            for m in genai.list_models():
                methods = getattr(m, 'supported_generation_methods', []) or []
                if 'generateContent' in methods:
                    candidates.append(m)

            preferred_order = [
                'gemini-pro',
                'gemini-1.0-pro',
                'gemini-1.5-flash',
                'gemini-pro-vision',
            ]

            for name in preferred_order:
                for m in candidates:
                    n = getattr(m, 'name', '')
                    if n.endswith(name) or n == name or name in n:
                        return genai.GenerativeModel(n), n

            if candidates:
                n = getattr(candidates[0], 'name', 'unknown')
                return genai.GenerativeModel(n), n

        except Exception as e:
            self.last_error = f"model discovery failed: {e}"
            logging.warning(self.last_error)
        return None, None
    
    def generate_response(self, user_message: str, conversation_history: List[Dict] = None):
        """
        Generate AI response using Gemini API.
        
        Args:
            user_message (str): User's current message
            conversation_history (List[Dict]): Previous conversation context
            
        Returns:
            str: AI-generated response
        """
        # Build conversation context
        context = self.system_prompt + "\n\n"

        if conversation_history:
            context += "Previous conversation:\n"
            for msg in conversation_history[-5:]:  # Last 5 messages for context
                context += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n\n"

        context += f"Current user message: {user_message}"

        # Generate response using Gemini
        try:
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            self.last_error = str(e)
            raise
    
    def is_available(self):
        """
        Check if Gemini API is available and configured.
        
        Returns:
            bool: True if API is available, False otherwise
        """
        # Cache availability checks to avoid rate limits and unnecessary calls
        if not GEMINI_API_KEY:
            return False

        now = time.time()
        if self._availability_cache["ok"] is not None and (now - self._availability_cache["ts"]) < 60:
            return bool(self._availability_cache["ok"])

        try:
            # Discover a supported model without generating content
            alt_model, alt_name = self._choose_supported_model()
            if alt_model is not None:
                self.model = alt_model
                self.model_name = alt_name
                self.last_error = None
                self._availability_cache = {"ok": True, "ts": now}
                return True
            self.last_error = "no supported model found"
            self._availability_cache = {"ok": False, "ts": now}
            return False
        except Exception as e:
            self.last_error = str(e)
            logging.warning(f"Gemini availability check failed: {e}")
            self._availability_cache = {"ok": False, "ts": now}
            return False
