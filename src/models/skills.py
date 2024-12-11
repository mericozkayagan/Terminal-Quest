from dataclasses import dataclass
from typing import Optional


@dataclass
class Skill:
    name: str
    damage: int
    mana_cost: int
    description: str
    cooldown: int = 0
    current_cooldown: int = 0

    def is_available(self) -> bool:
        """Check if skill is available to use"""
        return self.current_cooldown == 0

    def use(self) -> None:
        """Use skill and set cooldown"""
        self.current_cooldown = self.cooldown

    def update_cooldown(self) -> None:
        """Update cooldown at end of turn"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def __str__(self) -> str:
        status = (
            "Ready" if self.is_available() else f"Cooldown: {self.current_cooldown}"
        )
        return f"{self.name} ({status})"
