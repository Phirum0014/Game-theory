import random

# ============================================================
# Payoff Matrix according to TP1 rules[cite: 1]
# (move_A, move_B) -> (score_A, score_B)[cite: 1]
# ============================================================
PAYOFF_MATRIX = {
    ("C", "C"): (3, 3),  # Both cooperate[cite: 1]
    ("C", "D"): (0, 5),  # A cooperates, B defects[cite: 1]
    ("D", "C"): (5, 0),  # A defects, B cooperates[cite: 1]
    ("D", "D"): (1, 1),  # Both defect[cite: 1]
}


def get_payoff(move_a, move_b):
    """Returns the payoffs (score_a, score_b) for a given pair of moves[cite: 1]."""
    return PAYOFF_MATRIX[(move_a.upper(), move_b.upper())]


def get_human_choice(player_name):
    """Prompts a human player to enter C or D with input validation[cite: 1, 2]."""
    while True:
        choice = input(f"{player_name}, enter choice (C for Cooperate / D for Defect): ").strip().upper()
        if choice in ["C", "D"]:
            return choice
        print("Invalid choice! Please enter 'C' or 'D'.")


def get_positive_int(prompt):
    """Prompts the user for a valid positive integer[cite: 2]."""
    while True:
        val = input(prompt).strip()
        if val.isdigit() and int(val) > 0:
            return int(val)
        print("Please enter a valid positive integer.")


def get_bot_choice(strategy_name, opponent_history):
    """Selects a move based on the specified bot strategy[cite: 2]."""
    if strategy_name == "Always Cooperate":
        return "C"
    elif strategy_name == "Always Defect":
        return "D"
    elif strategy_name == "Random":
        return random.choice(["C", "D"])
    elif strategy_name == "Tit-for-Tat":
        # Strategy 4: Cooperate initially, then copy opponent's previous move[cite: 2]
        if not opponent_history:
            return "C"
        return opponent_history[-1]
    return "C"


def display_results_table(history, name_a="Player A", name_b="Player B"):
    """Displays the formatted table of decisions and scores for each round[cite: 2]."""
    print("\n" + "=" * 65)
    print(f"{'Round':<8} | {name_a + ' (Move)':<18} | {name_b + ' (Move)':<18} | {'Payoff (A, B)':<12}")
    print("-" * 65)
    total_a, total_b = 0, 0
    for r, (move_a, move_b, score_a, score_b) in enumerate(history, 1):
        total_a += score_a
        total_b += score_b
        print(f"{r:<8} | {move_a:<18} | {move_b:<18} | {f'({score_a}, {score_b})':<12}")
    print("-" * 65)
    print(f"Final Score: {name_a} = {total_a} | {name_b} = {total_b}")
    print("=" * 65 + "\n")
    return total_a, total_b


# ============================================================
# Exercise 1: One-round game with 2 human players[cite: 2]
# ============================================================
def exercise_1():
    print("\n" + "#" * 50)
    print("  EXERCISE 1: One-Round Game (2 Players)")
    print("#" * 50)
    move_a = get_human_choice("Player A")
    move_b = get_human_choice("Player B")
    score_a, score_b = get_payoff(move_a, move_b)
    display_results_table([(move_a, move_b, score_a, score_b)], "Player A", "Player B")


# ============================================================
# Exercise 2: N-rounds game with 2 human players[cite: 2]
# ============================================================
def exercise_2():
    print("\n" + "#" * 50)
    print("  EXERCISE 2: N-Rounds Game (2 Players)")
    print("#" * 50)
    rounds = get_positive_int("Enter number of rounds to play: ")
    history = []
    for r in range(1, rounds + 1):
        print(f"\n--- Round {r} ---")
        move_a = get_human_choice("Player A")
        move_b = get_human_choice("Player B")
        score_a, score_b = get_payoff(move_a, move_b)
        history.append((move_a, move_b, score_a, score_b))
    display_results_table(history, "Player A", "Player B")


# ============================================================
# Exercise 3: Human vs Computer[cite: 2]
# ============================================================
def exercise_3():
    print("\n" + "#" * 50)
    print("  EXERCISE 3: Human vs Computer")
    print("#" * 50)
    strategies = {
        "1": "Always Cooperate",
        "2": "Always Defect",
        "3": "Random",
        "4": "Tit-for-Tat",
    }
    print("Select Computer Strategy:")
    for key, val in strategies.items():
        print(f"  {key}. {val}")

    choice = ""
    while choice not in strategies:
        choice = input("Enter choice (1-4): ").strip()

    strategy = strategies[choice]
    rounds = get_positive_int("Enter number of rounds to play: ")

    history = []
    human_history = []
    for r in range(1, rounds + 1):
        print(f"\n--- Round {r} ---")
        move_human = get_human_choice("Human")
        move_comp = get_bot_choice(strategy, human_history)
        score_human, score_comp = get_payoff(move_human, move_comp)

        history.append((move_human, move_comp, score_human, score_comp))
        human_history.append(move_human)

    display_results_table(history, "Human", f"Computer ({strategy})")


# ============================================================
# Exercise 4: Computer vs Computer[cite: 2]
# ============================================================
def exercise_4():
    print("\n" + "#" * 50)
    print("  EXERCISE 4: Computer vs Computer")
    print("#" * 50)
    strategy_pool = ["Always Cooperate", "Always Defect", "Random", "Tit-for-Tat"]
    strat_a = random.choice(strategy_pool)
    strat_b = random.choice(strategy_pool)
    rounds = get_positive_int("Enter number of rounds to play: ")

    print(f"\nComputer A Strategy: {strat_a}")
    print(f"Computer B Strategy: {strat_b}")

    history = []
    history_a, history_b = [], []
    for _ in range(rounds):
        move_a = get_bot_choice(strat_a, history_b)
        move_b = get_bot_choice(strat_b, history_a)
        score_a, score_b = get_payoff(move_a, move_b)

        history.append((move_a, move_b, score_a, score_b))
        history_a.append(move_a)
        history_b.append(move_b)

    display_results_table(history, f"Bot A ({strat_a})", f"Bot B ({strat_b})")


# ============================================================
# Exercise 5: Single-Elimination Tournament[cite: 2]
# ============================================================
class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy


def play_match(player_a, player_b, rounds=5):
    print(f"\n>>> MATCH: {player_a.name} ({player_a.strategy}) vs {player_b.name} ({player_b.strategy}) <<<")
    history = []
    history_a, history_b = [], []

    for _ in range(rounds):
        move_a = get_bot_choice(player_a.strategy, history_b)
        move_b = get_bot_choice(player_b.strategy, history_a)
        score_a, score_b = get_payoff(move_a, move_b)

        history.append((move_a, move_b, score_a, score_b))
        history_a.append(move_a)
        history_b.append(move_b)

    score_total_a, score_total_b = display_results_table(
        history, f"{player_a.name} ({player_a.strategy})", f"{player_b.name} ({player_b.strategy})"
    )

    if score_total_a > score_total_b:
        winner = player_a
    elif score_total_b > score_total_a:
        winner = player_b
    else:
        winner = random.choice([player_a, player_b])
        print(f"Tie! Coin toss chooses winner: {winner.name}")

    print(f"-> Winner advancing: {winner.name} ({winner.strategy})")
    return winner


def exercise_5():
    print("\n" + "#" * 50)
    print("  EXERCISE 5: Tournament (Even Pair Players)")
    print("#" * 50)
    while True:
        num_players = get_positive_int("Enter number of players (must be a power of 2: 2, 4, 8, 16): ")
        if num_players >= 2 and (num_players & (num_players - 1)) == 0:
            break
        print("Please enter a valid power of 2 (e.g., 2, 4, 8, 16) for a balanced tournament bracket.")

    rounds_per_match = get_positive_int("Enter rounds per match: ")
    strategy_pool = ["Always Cooperate", "Always Defect", "Random", "Tit-for-Tat"]

    players = [Player(f"Player_{i+1}", random.choice(strategy_pool)) for i in range(num_players)]

    print("\nRegistered Participants:")
    for p in players:
        print(f"  - {p.name}: {p.strategy}")

    stage = 1
    current_players = players
    while len(current_players) > 1:
        print(f"\n{'='*20} TOURNAMENT STAGE {stage} {'='*20}")
        winners = []
        for i in range(0, len(current_players), 2):
            winner = play_match(current_players[i], current_players[i + 1], rounds=rounds_per_match)
            winners.append(winner)
        current_players = winners
        stage += 1

    print("\n" + "*" * 50)
    print(f"  TOURNAMENT CHAMPION: {current_players[0].name} ({current_players[0].strategy})")
    print("*" * 50)


# ============================================================
# Main Menu Runner
# ============================================================
def main_menu():
    while True:
        print("\n" + "=" * 45)
        print("      PRISONER'S DILEMMA - TP1 MENU")
        print("=" * 45)
        print("  1. One Round (2 Human Players)")
        print("  2. N Rounds (2 Human Players)")
        print("  3.Human vs Computer")
        print("  4. Computer vs Computer (Random Strategies)")
        print("  5. Knockout Tournament")
        print("  6. Exit")
        print("=" * 45)

        choice = input("Select an exercise to run (1-6): ").strip()

        if choice == "1":
            exercise_1()
        elif choice == "2":
            exercise_2()
        elif choice == "3":
            exercise_3()
        elif choice == "4":
            exercise_4()
        elif choice == "5":
            exercise_5()
        elif choice == "6":
            print("\nExiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main_menu()