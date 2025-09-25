import random
import os
import sys
import time

# Created by https://github.com/rebugging

HIGH_SCORE_FILE = "bubble_gum_highscore.txt"

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

def draw_bubble(size):
    radius = size + 2
    for y in range(-radius, radius + 1):
        line = ""
        for x in range(-radius * 2, radius * 2 + 1):
            if x**2 / 4 + y**2 <= radius**2:
                line += "O"
            else:
                line += " "
        print(line)
    print()

def skill_bar(size, bar_len=30, min_target_width=2, max_target_width=8, min_speed=0.01, max_speed=0.05):
    target_width = max(max_target_width - size // 3, min_target_width)
    speed = max(max_speed - size * 0.002, min_speed)
    target_start = random.randint(4, bar_len - target_width - 4)
    target_end = target_start + target_width
    pos = 0
    direction = 1
    print("Press [Space] or [Enter] to blow when the | is inside the [====] zone! (q to quit)")
    print()
    sys.stdout.flush()
    while True:
        bar = ""
        for i in range(bar_len):
            if i == pos:
                bar += "|"
            elif target_start <= i < target_end:
                bar += "="
            else:
                bar += "-"
        bar_display = f"[{bar[:target_start]}[{bar[target_start:target_end]}]{bar[target_end:]}]"
        print("\r" + bar_display, end="")
        sys.stdout.flush()
        start_time = time.time()
        while time.time() - start_time < speed:
            if os.name == 'nt':
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key in [b'\r', b' ']:
                        print()
                        return target_start <= pos < target_end
                    elif key == b'q':
                        print()
                        return None
            else:
                import select, termios, tty
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setcbreak(fd)
                    dr, dw, de = select.select([sys.stdin], [], [], 0)
                    if dr:
                        ch = sys.stdin.read(1)
                        if ch in ['\n', ' ', '\r']:
                            print()
                            return target_start <= pos < target_end
                        elif ch == 'q':
                            print()
                            return None
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            time.sleep(0.005)
        pos += direction
        if pos >= bar_len - 1:
            direction = -1
            pos = bar_len - 1
        elif pos <= 0:
            direction = 1
            pos = 0

def play_game(high_score):
    size = 0
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to Bubble Gum CLI! Made by rebugging")
        print("Skill Mode: Press [Space] or [Enter] when the | is in the [====] zone to blow!")
        print("The zone shrinks and the bar speeds up as your bubble grows!")
        print("If you miss, the bubble pops!\n")
        print(f"Current High Score: {high_score}\n")
        draw_bubble(size)
        print(f"Bubble size: {size}")
        print()
        result = skill_bar(size)
        if result is None:
            return None
        elif not result:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("POP! You missed the zone!")
            draw_bubble(size)
            print(f"Your bubble burst at size {size}!")
            if size > high_score:
                print("New High Score!")
                save_high_score(size)
                high_score = size
            else:
                print(f"High Score remains: {high_score}")
            return high_score
        else:
            size += 1

def main():
    while True:
        high_score = load_high_score()
        result = play_game(high_score)
        if result is None:
            print("Thanks for playing!")
            break
        again = input("\nPlay again? (y/n): ")
        if again.lower() != "y":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()