"""Core AI functionality for generating game content using OpenAI's API."""

from openai import OpenAI
import json
import os
from typing import Optional
from ..config.settings import AI_SETTINGS
from ..utils.debug import debug_log
from ..utils.json_cleaner import JSONCleaner
import logging

logger = logging.getLogger("ai")

SYSTEM_PROMPT = (
    "You are a dark fantasy RPG content generator that MUST return ONLY valid JSON.\n"
    "Rules:\n"
    "1. Return ONLY the JSON object, no other text\n"
    '2. Use ONLY double quotes (") for ALL properties and values\n'
    "3. NO special characters in property names or values\n"
    "4. ALL numbers must be single integers (no ranges, no decimals, no quotes)\n"
    "5. When given a range, pick ONE number within that range\n"
    "6. NO trailing commas\n"
    "7. NO comments or explanations\n"
    "8. NO additional properties beyond the template\n"
    "9. NO formatting symbols (%$, etc)\n"
    "10. Property names must match EXACTLY as shown\n"
    "11. Follow the EXACT structure of the template"
)


def setup_openai() -> Optional[OpenAI]:
    """Initialize and return an OpenAI client instance.

    Returns:
        Optional[OpenAI]: Configured OpenAI client or None if initialization fails.
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        logger.debug(f"API Key present: {bool(api_key)}")

        if not api_key:
            logger.error("No OpenAI API key found")
            return None

        client = OpenAI(api_key=api_key)
        logger.debug("OpenAI client initialized successfully")
        return client

    except Exception:
        logger.exception("Error initializing OpenAI client")
        return None


@debug_log
def generate_content(prompt: str, retries: int = None) -> Optional[str]:
    """Generate content using OpenAI's API with retry mechanism.

    Args:
        prompt (str): The prompt to send to the AI
        retries (int, optional): Number of retry attempts. Defaults to AI_SETTINGS["MAX_RETRIES"]

    Returns:
        Optional[str]: Generated content or None if all attempts fail
    """
    if retries is None:
        retries = AI_SETTINGS["MAX_RETRIES"]

    client = setup_openai()
    if not client:
        logger.error("Failed to initialize OpenAI client")
        return None

    base_temperature = AI_SETTINGS["TEMPERATURE"]

    for attempt in range(retries):
        try:
            current_temperature = base_temperature + (attempt * 0.1)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=min(current_temperature, 1.2),
                max_tokens=AI_SETTINGS["MAX_TOKENS"],
                presence_penalty=AI_SETTINGS["PRESENCE_PENALTY"],
                frequency_penalty=AI_SETTINGS["FREQUENCY_PENALTY"],
            )

            content = response.choices[0].message.content.strip()

            # Log the raw response
            logger.debug(f"Raw content received: {content}")

            # Clean and validate JSON
            cleaned_content = JSONCleaner.clean_content(content)
            if cleaned_content:
                try:
                    parsed = json.loads(cleaned_content)
                    logger.debug(
                        "Cleaned and parsed content: \n"
                        f"{json.dumps(parsed, indent=2)}"
                    )
                    return cleaned_content
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parsing failed after cleaning: {str(e)}")
                    logger.debug(f"Failed content: {cleaned_content}")
                    continue
            else:
                logger.error("Content cleaning returned None")
                logger.debug(f"Original content that failed cleaning: {content}")

            logger.warning(f"Content cleaning failed on attempt {attempt + 1}")
            continue

        except Exception as e:
            logger.error(f"Error on attempt {attempt + 1}: {str(e)}")
            continue

    logger.error("All generation attempts failed")
    return None
