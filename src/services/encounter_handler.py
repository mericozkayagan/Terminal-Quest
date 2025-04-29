from typing import Dict, Any, Optional, Tuple
import random
import time
import logging
from src.models.character import Player, Enemy
from src.models.base_types import EncounterType
from src.services.encounter import EncounterService
from src.services.shop import Shop
from src.services.combat import combat, handle_combat_rewards, handle_level_up
from src.display.encounter.encounter_view import EncounterView
from src.display.encounter.npc_view import NPCView
from src.display.combat.combat_view import CombatView
from src.display.common.message_view import MessageView
from src.display.base.base_view import BaseView
from src.services.boss import BossService
from src.display.boss.boss_view import BossView
from src.config.settings import GAME_BALANCE
from src.config.settings import DISPLAY_SETTINGS

logger = logging.getLogger(__name__)


class EncounterHandler:
    """Handles all encounter-related logic in the game"""

    def __init__(self):
        self.encounter_service = EncounterService(boss_threshold=10)
        self.boss_service = BossService()

    def handle_exploration(
        self, player: Player, combat_view: CombatView, boss_view: BossView, shop: Shop
    ) -> bool:
        """
        Handle exploration and encounters

        Returns:
            bool: False if player died, True otherwise
        """
        # Generate regular encounter
        encounter = self.encounter_service.get_next_encounter(player)
        encounter_type = encounter.get("type")

        # Update the encounters_until_boss counter in EncounterService
        # This is the ONLY place where we should decrement the counter
        previous = self.encounter_service.encounters_until_boss
        self.encounter_service.encounters_until_boss -= 1

        # Log counter updates with additional context
        logger.info(
            f"Updated boss counter: {previous} -> {self.encounter_service.encounters_until_boss} (remaining)"
        )
        logger.info(
            f"Total boss interval: {self.encounter_service.total_boss_interval}"
        )
        logger.info(
            f"Progress: {((self.encounter_service.total_boss_interval - self.encounter_service.encounters_until_boss) / self.encounter_service.total_boss_interval) * 100:.1f}%"
        )

        # Handle different encounter types
        if encounter_type == EncounterType.COMBAT:
            return self._handle_combat_encounter(player, combat_view, shop, encounter)
        elif encounter_type == EncounterType.PUZZLE:
            return self._handle_puzzle_encounter(player, encounter)
        elif encounter_type == EncounterType.TREASURE:
            return self._handle_treasure_encounter(player, encounter)
        elif encounter_type == EncounterType.TRAP:
            return self._handle_trap_encounter(player, encounter)
        elif encounter_type == EncounterType.NPC:
            return self._handle_npc_encounter(player, encounter)
        else:
            # Fallback to combat
            return self._handle_combat_encounter(player, combat_view, shop, encounter)

    def _handle_boss_encounter(
        self, player: Player, combat_view: CombatView, boss_view: BossView, shop: Shop
    ) -> bool:
        """Handle boss encounter using defined bosses and intro"""
        # Get the specific boss based on player status and requirements
        boss = self.boss_service.check_boss_encounter(player)

        # Check if a specific boss was found
        if not boss:
            logger.error(
                "Failed to find a suitable defined boss for the player. Falling back."
            )
            # Option 1: Fallback to a generic encounter (less ideal)
            # encounter = self.encounter_service.get_next_encounter(player)
            # return self._handle_combat_encounter(player, combat_view, shop, encounter)

            # Option 2: Inform player and do nothing (safer)
            MessageView.show_error(
                "The time is not yet right... The Corruption stirs but does not fully manifest."
            )
            # We should NOT reset the boss counter here, let the player try again
            time.sleep(2)
            return True  # Player didn't die, return to main menu

        # Show boss introduction/animation VIEW
        BaseView.clear_screen()
        boss_view.show_boss_encounter(boss)  # Use the BossView
        time.sleep(
            DISPLAY_SETTINGS.get("BOSS_INTRO_DELAY", 3)
        )  # Add a delay after intro

        # Combat with the specific boss
        combat_result = combat(
            player, boss, combat_view, shop
        )  # Pass the specific Boss object

        if combat_result is None:  # Player died
            MessageView.show_info(
                f"You have fallen to the {boss.title}, {boss.name}..."
            )
            time.sleep(2)
            return False
        elif combat_result:  # Victory
            exp_gained = boss.exp_reward  # Use boss specific exp reward
            player.exp += exp_gained
            MessageView.show_success(
                f"A mighty victory over {boss.name}! Gained {exp_gained} experience!"
            )

            # Handle boss drops (using the guaranteed_drops from Boss model)
            if hasattr(boss, "guaranteed_drops") and boss.guaranteed_drops:
                for drop in boss.guaranteed_drops:
                    # Check if the drop is an ItemSet or a single Item
                    if isinstance(drop, ItemSet):
                        # Grant all items in the set
                        set_items = drop.get_all_items()
                        player.inventory["items"].extend(set_items)
                        MessageView.show_success(f"Obtained the {drop.name} set!")
                        for item in set_items:
                            MessageView.show_info(f"  - {item.name}")
                    elif isinstance(drop, Item):
                        # Grant single item drop
                        player.inventory["items"].append(drop)
                        MessageView.show_success(f"Obtained {drop.name}!")
                    else:
                        logger.warning(
                            f"Unknown drop type in boss {boss.name}: {type(drop)}"
                        )
            else:
                logger.warning(f"Boss {boss.name} has no guaranteed_drops defined.")

            # Check for level up
            if player.exp >= player.exp_to_level:
                handle_level_up(player)
            time.sleep(5)
        else:  # Retreat
            MessageView.show_info(f"You retreat from the powerful {boss.name}...")
            time.sleep(2)

        return True  # Player is still alive

    def _handle_combat_encounter(
        self,
        player: Player,
        combat_view: CombatView,
        shop: Shop,
        encounter_data: Dict[str, Any],
    ) -> bool:
        """Handle combat encounter"""
        enemy = encounter_data.get("enemy")

        if not enemy:
            MessageView.show_error("Failed to generate enemy")
            return True

        combat_result = combat(player, enemy, combat_view, shop)

        if combat_result is None:  # Player died
            MessageView.show_error("You have fallen in battle...")
            time.sleep(2)
            return False
        elif combat_result:  # Victory
            exp_gained = enemy.exp_reward
            player.exp += exp_gained
            MessageView.show_success(f"Victory! Gained {exp_gained} experience!")
            time.sleep(2)

            # Handle combat rewards
            gold_gained, dropped_items = handle_combat_rewards(player, enemy, shop)

            # Display rewards
            rewards = {
                "exp": exp_gained,
                "gold": gold_gained,
                "items": dropped_items,
            }
            combat_view.show_battle_result(player, enemy, rewards)

            if player.exp >= player.exp_to_level:
                handle_level_up(player)
        else:  # Retreat
            MessageView.show_info("You retreat from battle...")
            time.sleep(2)

        return True  # Player is still alive

    def _handle_puzzle_encounter(
        self, player: Player, encounter_data: Dict[str, Any]
    ) -> bool:
        """Handle puzzle encounter"""
        # Display puzzle
        EncounterView.show_encounter(encounter_data)

        hints_given = 0
        max_attempts = 3
        attempt = 0

        while attempt < max_attempts:
            choice = input("\nChoose your action: ").strip()

            if choice == "1":  # Solve puzzle
                answer = input("\nEnter your solution: ").strip().lower()
                solution = encounter_data.get("solution", "").lower()

                if answer == solution:
                    # Success
                    reward = encounter_data.get(
                        "reward", {"type": "gold", "amount": 10}
                    )
                    EncounterView.show_puzzle_success(reward)

                    # Apply reward
                    reward_type = reward.get("type", "gold")
                    amount = reward.get("amount", 10)

                    if reward_type == "gold":
                        player.inventory["Gold"] += amount
                    elif reward_type == "health":
                        player.health = min(player.max_health, player.health + amount)
                    elif reward_type == "mana":
                        player.mana = min(player.max_mana, player.mana + amount)
                    elif reward_type == "exp":
                        player.exp += amount
                        if player.exp >= player.exp_to_level:
                            handle_level_up(player)

                    input()
                    return True
                else:
                    # Failure
                    attempt += 1
                    print(
                        f"\nIncorrect solution! Attempts remaining: {max_attempts - attempt}"
                    )
                    time.sleep(1)

            elif choice == "2":  # Request hint
                if hints_given < len(encounter_data.get("hints", [])):
                    hint = encounter_data["hints"][hints_given]
                    EncounterView.show_hint(hint)
                    hints_given += 1
                else:
                    print("\nNo more hints available!")
                time.sleep(1.5)

            elif choice == "3":  # Skip puzzle
                MessageView.show_info(
                    "You decide to move on without solving the puzzle."
                )
                time.sleep(1.5)
                return True

        # Failed all attempts
        EncounterView.show_puzzle_failure()
        input()
        return True

    def _handle_treasure_encounter(
        self, player: Player, encounter_data: Dict[str, Any]
    ) -> bool:
        """Handle treasure encounter"""
        # Display treasure
        EncounterView.show_encounter(encounter_data)

        # Apply rewards
        gold = encounter_data.get("gold", 0)
        player.inventory["Gold"] += gold

        # Handle potential item
        has_item = encounter_data.get("has_item", False)
        if has_item:
            # Use shop's item service to generate an item
            # This will be replaced with actual implementation
            pass

        input()  # Wait for user input
        return True

    def _handle_trap_encounter(
        self, player: Player, encounter_data: Dict[str, Any]
    ) -> bool:
        """Handle trap encounter"""
        # Display trap
        EncounterView.show_encounter(encounter_data)

        choice = input("\nChoose your action: ").strip()

        # Calculate success chance based on player level vs trap difficulty
        difficulty = encounter_data.get("difficulty", player.level + 2)
        base_chance = 0.5  # 50% base chance

        # Adjust chance based on player level vs difficulty
        level_diff = player.level - difficulty
        success_mod = level_diff * 0.1  # 10% per level difference
        success_chance = min(
            0.9, max(0.1, base_chance + success_mod)
        )  # Clamp between 10% and 90%

        if choice == "1" or choice == "2":  # Try to disarm/avoid
            # Different actions have slightly different chances
            if choice == "1":  # Disarm has higher risk/reward
                success_chance = min(0.9, max(0.1, success_chance + 0.05))

            success = random.random() < success_chance
            EncounterView.show_trap_result(success, encounter_data)

            if not success:
                # Apply damage
                damage = encounter_data.get("damage", 5)
                player.health -= damage

                # Check if player died
                if player.health <= 0:
                    return False

        elif choice == "3":  # Accept consequences
            # Always trigger the trap
            EncounterView.show_trap_result(False, encounter_data)

            # Apply damage
            damage = encounter_data.get("damage", 5)
            player.health -= damage

            # Check if player died
            if player.health <= 0:
                return False

        input()  # Wait for user input
        return True

    def _handle_npc_encounter(
        self, player: Player, encounter_data: Dict[str, Any]
    ) -> bool:
        """Handle NPC encounter with enhanced functionality"""
        # Check if this is a simple or enhanced NPC
        if "npc" in encounter_data:
            # This is an enhanced NPC with dialogue and quests
            npc = encounter_data.get("npc")

            # Use the NPCView to handle the complete interaction
            NPCView.handle_npc_interaction(npc, player)

            # Check for quest completions after interaction
            for quest in npc.quests:
                # In a full implementation, we'd have a better way to track quest progress
                # For now, we'll randomly advance some quests for testing
                if not quest.completed and random.random() < 0.2:
                    quest.progress += 1
                    if NPCView.handle_quest_completion_check(quest, npc, player):
                        # Quest was completed and rewards given
                        pass

            return True
        else:
            # This is a simple NPC (fallback)
            # Use the old encounter view
            EncounterView.show_encounter(encounter_data)

            options = encounter_data.get("options", [])

            try:
                choice = int(input("\nChoose your response: ").strip())

                if 1 <= choice <= len(options):
                    outcome = options[choice - 1].get("outcome", "Nothing happens.")
                    EncounterView.show_npc_outcome(outcome)

                    # Handle specific outcomes
                    if "gold" in outcome.lower():
                        try:
                            gold_amount = int("".join(filter(str.isdigit, outcome)))
                            if "lose" in outcome.lower():
                                player.inventory["Gold"] = max(
                                    0, player.inventory["Gold"] - gold_amount
                                )
                            else:
                                player.inventory["Gold"] += gold_amount
                        except:
                            pass

                    if "health" in outcome.lower():
                        try:
                            health_amount = int("".join(filter(str.isdigit, outcome)))
                            if "lose" in outcome.lower():
                                player.health = max(1, player.health - health_amount)
                            else:
                                player.health = min(
                                    player.max_health, player.health + health_amount
                                )
                        except:
                            pass

                    if "xp" in outcome.lower() or "experience" in outcome.lower():
                        try:
                            xp_amount = int("".join(filter(str.isdigit, outcome)))
                            player.exp += xp_amount
                            if player.exp >= player.exp_to_level:
                                handle_level_up(player)
                        except:
                            pass
                else:
                    print("\nInvalid choice. The NPC looks at you with confusion.")
            except ValueError:
                print("\nInvalid input. The NPC sighs and walks away.")

            input()  # Wait for user input
            return True
