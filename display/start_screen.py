class StartScreen:
    def show_start_screen(self):
        print("Welcome to the Game!")
        print("1. Start Game")
        print("2. Wait for Players")

    def handle_user_input(self):
        choice = input("Enter your choice: ")
        if choice == "1":
            return "start_game"
        elif choice == "2":
            return "wait_for_players"
        else:
            print("Invalid choice. Please try again.")
            return self.handle_user_input()
