import logging
from typing import Optional, Any
import json
from functools import wraps


class DebugLogger:
    def __init__(self):
        self.ai_logger = logging.getLogger("ai")
        self.game_logger = logging.getLogger("game")
        self.enabled = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def log_ai_interaction(
        self,
        prompt: str,
        response: Optional[str] = None,
        error: Optional[Exception] = None,
        attempt: int = 0,
        metadata: Optional[dict] = None,
    ):
        if not self.enabled:
            return

        self.ai_logger.debug("\n=== AI Interaction ===")
        self.ai_logger.debug(f"Attempt: {attempt + 1}")

        if metadata:
            self.ai_logger.debug("\nMetadata:")
            self.ai_logger.debug(json.dumps(metadata, indent=2))

        self.ai_logger.debug("\nPrompt:")
        self.ai_logger.debug(prompt)

        if response:
            self.ai_logger.debug("\nResponse:")
            self.ai_logger.debug(response)

            try:
                parsed = json.loads(response)
                self.ai_logger.debug("\nParsed JSON:")
                self.ai_logger.debug(json.dumps(parsed, indent=2))
            except json.JSONDecodeError as e:
                self._log_json_error(e, response)

        if error:
            self.ai_logger.error("\nError:")
            self.ai_logger.error(str(error))

    def log_game_event(self, event_type: str, data: Any):
        if not self.enabled:
            return
        self.game_logger.info(f"\n=== {event_type} ===")
        self.game_logger.info(json.dumps(data, indent=2))

    def _log_json_error(self, error: json.JSONDecodeError, content: str):
        self.ai_logger.error(f"\nJSON Parse Error:")
        self.ai_logger.error(f"Error message: {str(error)}")
        self.ai_logger.error(f"Error position: character {error.pos}")
        self.ai_logger.error(f"Line {error.lineno}, Column {error.colno}")
        context_start = max(0, error.pos - 50)
        context_end = min(len(content), error.pos + 50)
        self.ai_logger.error(f"Context: ...{content[context_start:context_end]}...")


# Create singleton instance
debug = DebugLogger()


def debug_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not debug.enabled:
            return func(*args, **kwargs)

        debug.ai_logger.debug(f"\nCalling {func.__name__}")
        try:
            result = func(*args, **kwargs)
            debug.ai_logger.debug(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            debug.ai_logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    return wrapper
