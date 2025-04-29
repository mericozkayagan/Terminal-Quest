from typing import Dict, List, Any, Optional
import time
import random

from src.display.base.base_view import BaseView
from src.display.themes.dark_theme import DECORATIONS as dec
from src.display.themes.dark_theme import SYMBOLS as sym
from src.models.npc import NPC, NPCQuest, NPCDialogue
from src.models.character import Player
from src.services.npc_generator import NPCGenerator
from src.display.common.message_view import MessageView


class NPCView(BaseView):
    """View for displaying NPC encounters and interactions"""

    @staticmethod
    def show_npc(npc: NPC):
        """Display NPC information"""
        BaseView.clear_screen()
        print(f"\n{dec['TITLE']['PREFIX']}NPC Encounter{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        print(f"\n{sym['NPC']} {npc.name}")
        print(f"\n{npc.description}")

        # Display ASCII art
        if npc.ascii_art:
            print(f"\n{npc.ascii_art}")

        # Display greeting
        print(f'\n"{npc.get_greeting()}"')

    @staticmethod
    def show_dialogue_options(npc: NPC, dialogue: NPCDialogue = None):
        """Display dialogue options for the player"""
        if not dialogue:
            # Show main dialogue options if no specific dialogue is provided
            print(f"\n{dec['SECTION']['START']}Talk About{dec['SECTION']['END']}")

            # Filter to non-quest dialogues for the main menu
            regular_dialogues = [d for d in npc.dialogues if not d.is_quest_dialogue]

            for i, d in enumerate(
                regular_dialogues[:3], 1
            ):  # Show up to 3 dialogue options
                print(f"  {sym['CURSOR']} {i}. {d.text[:40]}...")

            # Show quest option if there are available quests
            if any(not q.completed for q in npc.quests):
                print(f"  {sym['CURSOR']} 4. Ask about tasks")

            print(f"  {sym['CURSOR']} 5. Chat freely")
            print(f"  {sym['CURSOR']} 0. Leave")
        else:
            # Show responses for a specific dialogue
            print(f"\n{dec['SECTION']['START']}Your Response{dec['SECTION']['END']}")
            for i, response in enumerate(dialogue.responses, 1):
                print(f"  {sym['CURSOR']} {i}. {response['text']}")
            print(f"  {sym['CURSOR']} 0. Back")

    @staticmethod
    def show_quest_list(npc: NPC, player: Player):
        """Display list of quests from this NPC"""
        BaseView.clear_screen()
        print(
            f"\n{dec['TITLE']['PREFIX']}Tasks from {npc.name}{dec['TITLE']['SUFFIX']}"
        )
        print(f"{dec['SEPARATOR']}")

        available_quests = npc.get_available_quests(player.level)
        active_quests = [
            q for q in npc.quests if not q.completed and q not in available_quests
        ]
        completed_quests = [q for q in npc.quests if q.completed]

        if available_quests:
            print(f"\n{dec['SECTION']['START']}Available Tasks{dec['SECTION']['END']}")
            for i, quest in enumerate(available_quests, 1):
                print(f"  {sym['CURSOR']} {i}. {quest.name}")

        if active_quests:
            print(f"\n{dec['SECTION']['START']}Active Tasks{dec['SECTION']['END']}")
            for quest in active_quests:
                progress = f"({quest.progress}/{quest.required_progress})"
                print(f"  {sym['CURSOR']} {quest.name} {progress}")

        if completed_quests:
            print(f"\n{dec['SECTION']['START']}Completed Tasks{dec['SECTION']['END']}")
            for quest in completed_quests:
                print(f"  {sym['CURSOR']} {quest.name}")

        if not (available_quests or active_quests or completed_quests):
            print("\nNo tasks available from this NPC.")

        print(f"\n{dec['SECTION']['START']}Options{dec['SECTION']['END']}")
        print(f"  {sym['CURSOR']} 0. Back")

    @staticmethod
    def show_quest_details(quest: NPCQuest):
        """Display detailed information about a quest"""
        BaseView.clear_screen()
        print(f"\n{dec['TITLE']['PREFIX']}{quest.name}{dec['TITLE']['SUFFIX']}")
        print(f"{dec['SEPARATOR']}")

        print(f"\n{quest.description}")
        print(f"\nObjective: {quest.objective}")

        if quest.required_progress > 1:
            print(f"Progress: {quest.progress}/{quest.required_progress}")

        print(f"\n{dec['SECTION']['START']}Rewards{dec['SECTION']['END']}")
        print(f"  {sym['GOLD']} Gold: {quest.reward_gold}")
        print(f"  {sym['EXP']} Experience: {quest.reward_exp}")

        if quest.reward_item_id:
            print(f"  {sym['ITEM']} Item: [To be implemented]")

        print(f"\n{dec['SECTION']['START']}Options{dec['SECTION']['END']}")
        if not quest.completed:
            print(f"  {sym['CURSOR']} 1. Accept quest")
        print(f"  {sym['CURSOR']} 0. Back")

    @staticmethod
    def show_chat_interface(npc: NPC, conversation_history: List[str] = None):
        """Display free chat interface with the NPC"""
        if not conversation_history:
            conversation_history = []

        BaseView.clear_screen()
        print(
            f"\n{dec['TITLE']['PREFIX']}Talking with {npc.name}{dec['TITLE']['SUFFIX']}"
        )
        print(f"{dec['SEPARATOR']}")

        # Show a mini version of the NPC's portrait
        if npc.ascii_art:
            art_lines = npc.ascii_art.strip().split("\n")
            if len(art_lines) > 4:
                condensed_art = "\n".join(art_lines[:4])
                print(f"\n{condensed_art}")
            else:
                print(f"\n{npc.ascii_art}")

        # Show conversation history
        if conversation_history:
            print(f"\n{dec['SECTION']['START']}Conversation{dec['SECTION']['END']}")
            for message in conversation_history[-5:]:  # Show last 5 messages
                print(f"  {message}")

        print(f"\n{dec['SECTION']['START']}Chat{dec['SECTION']['END']}")
        print("  Type your message or '/exit' to end the conversation.")

    @staticmethod
    def handle_npc_interaction(npc: NPC, player: Player):
        """Handle complete NPC interaction session"""
        conversation_history = []
        current_dialogue = None

        while True:
            BaseView.clear_screen()
            NPCView.show_npc(npc)

            if current_dialogue:
                # We're in a specific dialogue
                NPCView.show_dialogue_options(npc, current_dialogue)
                choice = input("\nChoose your response: ").strip()

                if choice == "0":
                    # Go back to main menu
                    current_dialogue = None
                    continue

                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(current_dialogue.responses):
                        response = current_dialogue.responses[choice_idx]

                        # Handle relationship change
                        if "relationship_change" in response:
                            npc.update_relationship(response["relationship_change"])

                        # Handle quest actions
                        if "action" in response:
                            if (
                                response["action"] == "accept_quest"
                                and "quest_id" in response
                            ):
                                quest = npc.get_quest_by_id(response["quest_id"])
                                if quest:
                                    MessageView.show_success(
                                        f"Quest accepted: {quest.name}"
                                    )
                                    # Add to player's active quests (implementation needed)
                            elif response["action"] == "decline_quest":
                                MessageView.show_info("Quest declined.")

                        # Display action result
                        if "action" in response:
                            print(f"\n{response['action']}")
                            time.sleep(2)

                        # Add to conversation history
                        conversation_history.append(f"You: {response['text']}")

                        # Move to next dialogue if specified
                        if response.get("next_dialogue"):
                            next_dialogue = npc.get_dialogue_by_id(
                                response["next_dialogue"]
                            )
                            if next_dialogue:
                                current_dialogue = next_dialogue
                                conversation_history.append(
                                    f"{npc.name}: {next_dialogue.text}"
                                )
                            else:
                                current_dialogue = None
                        else:
                            current_dialogue = None
                    else:
                        MessageView.show_error("Invalid choice.")
                except ValueError:
                    MessageView.show_error("Please enter a number.")

                input("\nPress Enter to continue...")

            else:
                # Main interaction menu
                NPCView.show_dialogue_options(npc)
                choice = input("\nChoose your action: ").strip()

                if choice == "0":
                    # Exit the interaction
                    break

                elif choice == "4":
                    # Show quest menu
                    NPCView.handle_quest_menu(npc, player)

                elif choice == "5":
                    # Free chat mode
                    NPCView.handle_free_chat(npc, conversation_history)

                else:
                    try:
                        choice_idx = int(choice) - 1
                        regular_dialogues = [
                            d for d in npc.dialogues if not d.is_quest_dialogue
                        ]

                        if 0 <= choice_idx < len(regular_dialogues):
                            current_dialogue = regular_dialogues[choice_idx]
                            print(f'\n{npc.name}: "{current_dialogue.text}"')
                            conversation_history.append(
                                f"{npc.name}: {current_dialogue.text}"
                            )
                            time.sleep(1)
                        else:
                            MessageView.show_error("Invalid choice.")
                    except ValueError:
                        MessageView.show_error("Please enter a number.")

                    input("\nPress Enter to continue...")

    @staticmethod
    def handle_quest_menu(npc: NPC, player: Player):
        """Handle the quest menu"""
        while True:
            NPCView.show_quest_list(npc, player)

            choice = input("\nEnter your choice: ").strip()

            if choice == "0":
                # Go back
                break

            try:
                choice_idx = int(choice) - 1
                available_quests = npc.get_available_quests(player.level)

                if 0 <= choice_idx < len(available_quests):
                    selected_quest = available_quests[choice_idx]
                    NPCView.handle_quest_details(selected_quest, npc, player)
                else:
                    MessageView.show_error("Invalid choice.")
            except ValueError:
                MessageView.show_error("Please enter a number.")

            time.sleep(1)

    @staticmethod
    def handle_quest_details(quest: NPCQuest, npc: NPC, player: Player):
        """Handle quest details and acceptance"""
        while True:
            NPCView.show_quest_details(quest)

            if quest.completed:
                input("\nThis quest is already completed. Press Enter to go back.")
                break

            choice = input("\nEnter your choice: ").strip()

            if choice == "0":
                # Go back
                break

            if choice == "1":
                # Accept quest
                quest_dialogue = None
                for dialogue in npc.dialogues:
                    if dialogue.is_quest_dialogue and dialogue.quest_id == quest.id:
                        quest_dialogue = dialogue
                        break

                if quest_dialogue:
                    print(f'\n{npc.name}: "{quest_dialogue.text}"')

                    # For simplicity, automatically accept
                    MessageView.show_success(f"Quest accepted: {quest.name}")

                    # In a full implementation, we would add to player's active quests
                    # player.add_active_quest(quest)

                    time.sleep(2)
                    break
                else:
                    # No specific dialogue found, use generic acceptance
                    print(
                        f'\n{npc.name}: "I\'ll be grateful for your help with this task."'
                    )
                    MessageView.show_success(f"Quest accepted: {quest.name}")

                    # In a full implementation, we would add to player's active quests
                    # player.add_active_quest(quest)

                    time.sleep(2)
                    break

    @staticmethod
    def handle_free_chat(npc: NPC, conversation_history: List[str]):
        """Handle free-form chat with the NPC"""
        local_history = conversation_history.copy()

        while True:
            NPCView.show_chat_interface(npc, local_history)

            player_input = input("\nYou: ").strip()

            if player_input.lower() == "/exit":
                break

            if not player_input:
                continue

            # Add player's message to history
            local_history.append(f"You: {player_input}")

            # Generate NPC response
            response = NPCGenerator.generate_npc_response(
                npc, player_input, local_history
            )

            # Add NPC's response to history
            local_history.append(f"{npc.name}: {response}")

            # Update main conversation history
            conversation_history.clear()
            conversation_history.extend(local_history)

            # Show response and wait for player to continue
            BaseView.clear_screen()
            NPCView.show_chat_interface(npc, local_history)
            input("\nPress Enter to continue...")

    @staticmethod
    def handle_quest_completion_check(quest: NPCQuest, npc: NPC, player: Player):
        """Handle checking if a quest is complete and giving rewards"""
        if quest.completed:
            return

        # In a full implementation, we would check quest completion criteria here
        # For now, we'll assume the quest is complete based on progress
        if quest.progress >= quest.required_progress:
            BaseView.clear_screen()
            print(f"\n{dec['TITLE']['PREFIX']}Quest Completed{dec['TITLE']['SUFFIX']}")
            print(f"{dec['SEPARATOR']}")

            print(f"\nYou have completed: {quest.name}")
            print(f'\n{npc.name}: "Thank you for your help with this task!"')

            # Mark quest as completed
            quest.completed = True

            # Give rewards
            print(f"\n{dec['SECTION']['START']}Rewards{dec['SECTION']['END']}")
            print(f"  {sym['GOLD']} Gold: {quest.reward_gold}")
            print(f"  {sym['EXP']} Experience: {quest.reward_exp}")

            # Add rewards to player
            player.inventory["Gold"] += quest.reward_gold
            player.exp += quest.reward_exp

            # Improve relationship with NPC
            npc.update_relationship(15)

            input("\nPress Enter to continue...")
            return True
        return False
