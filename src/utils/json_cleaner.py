from typing import Optional
import json


class JSONCleaner:
    @staticmethod
    def clean_content(content: str) -> Optional[str]:
        """Clean and validate JSON content"""
        try:
            # First try to parse as-is
            json.loads(content)
            return content
        except json.JSONDecodeError:
            # Only clean if necessary
            try:
                # Basic cleanup
                cleaned = content.strip()
                cleaned = cleaned.replace("'", '"')
                cleaned = cleaned.replace("\n", " ")
                cleaned = cleaned.replace(",}", "}")
                cleaned = cleaned.replace(",]", "]")

                # Validate JSON structure
                data = json.loads(cleaned)

                # Clean values while preserving structure
                def clean_value(val):
                    if isinstance(val, str):
                        return val.strip().strip('"')
                    elif isinstance(val, dict):
                        return {k.strip(): clean_value(v) for k, v in val.items()}
                    elif isinstance(val, list):
                        return [clean_value(item) for item in val]
                    return val

                cleaned_data = clean_value(data)
                return json.dumps(cleaned_data, indent=2)
            except Exception:
                return None

    @staticmethod
    def clean_art_content(content: str) -> Optional[str]:
        """Clean AI-generated art content"""
        try:
            # Try to parse as JSON first
            data = json.loads(content)

            # Handle different JSON structures
            if isinstance(data, dict):
                if "ascii_art" in data:
                    art = data["ascii_art"]
                    if isinstance(art, list):
                        return "\n".join(art)
                    return str(art)

            # If it's not JSON or doesn't contain art, return the raw content
            return content.strip()

        except json.JSONDecodeError:
            # If it's not JSON, clean and return the raw content
            cleaned = content.strip()
            # Remove any markdown code block markers
            cleaned = cleaned.replace("```", "")
            cleaned = cleaned.replace("ascii", "")
            cleaned = cleaned.replace("art", "")
            return cleaned.strip()
