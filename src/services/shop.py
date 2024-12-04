from typing import List, Dict
from ..models.character import Player
from ..models.items import Item, Equipment, Consumable, RUSTY_SWORD, LEATHER_ARMOR, HEALING_SALVE, POISON_VIAL, VAMPIRIC_BLADE, CURSED_AMULET
from ..utils.display import type_text, clear_screen
from ..config.settings import GAME_BALANCE, DISPLAY_SETTINGS

class Shop:
    def __init__(self):
        self.inventory: List[Item] = [
            RUSTY_SWORD,
            LEATHER_ARMOR,
            HEALING_SALVE,
            POISON_VIAL,
            VAMPIRIC_BLADE,
            CURSED_AMULET
        ]

    def show_inventory(self, player: Player):
        """Display shop inventory"""
        clear_screen()
        type_text("\nWelcome to the Shop!")
        print(f"\nYour Gold: {player.inventory['Gold']}")

        print("\nAvailable Items:")
        for i, item in enumerate(self.inventory, 1):
            print(f"\n{i}. {item.name} - {item.value} Gold")
            print(f"   {item.description}")
            if isinstance(item, Equipment):
                mods = [f"{stat}: {value}" for stat, value in item.stat_modifiers.items()]
                print(f"   Stats: {', '.join(mods)}")
                print(f"   Durability: {item.durability}/{item.max_durability}")
            elif isinstance(item, Consumable):
                effects = []
                for effect in item.effects:
                    if 'heal_health' in effect:
                        effects.append(f"Heals {effect['heal_health']} HP")
                    if 'heal_mana' in effect:
                        effects.append(f"Restores {effect['heal_mana']} MP")
                    if 'status_effect' in effect:
                        effects.append(f"Applies {effect['status_effect'].name}")
                print(f"   Effects: {', '.join(effects)}")
            print(f"   Rarity: {item.rarity.value}")

    def buy_item(self, player: Player, item_index: int) -> bool:
        """Process item purchase"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            if player.inventory['Gold'] >= item.value:
                player.inventory['Gold'] -= item.value
                player.inventory['items'].append(item)
                type_text(f"\nYou bought {item.name}!")
                return True
            else:
                type_text("\nNot enough gold!")
        return False

    def sell_item(self, player: Player, item_index: int) -> bool:
        """Process item sale"""
        if 0 <= item_index < len(player.inventory['items']):
            item = player.inventory['items'][item_index]
            sell_value = int(item.value * GAME_BALANCE["SELL_PRICE_MULTIPLIER"])
            player.inventory['Gold'] += sell_value
            player.inventory['items'].pop(item_index)
            type_text(f"\nSold {item.name} for {sell_value} Gold!")
            return True
        return False