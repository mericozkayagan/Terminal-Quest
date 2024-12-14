class WaitScreen:
    def show_wait_screen(self):
        print("Waiting for other players to connect...")
        print("1. Start Game")
        print("2. Cancel")

    def handle_user_input(self):
        choice = input("Enter your choice: ")
        if choice == "1":
            return "start_game"
        elif choice == "2":
            return "cancel"
        else:
            print("Invalid choice. Please try again.")
            return self.handle_user_input()
