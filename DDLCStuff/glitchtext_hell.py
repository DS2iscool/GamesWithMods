#!/usr/bin/env python3
"""
glitchtext_hell.py

An unhinged escalation of DDLC's glitchtext() function.
Original was: pick `length` random accented/Latin-Extended chars.
This one stacks Zalgo combining marks on top of real (or corrupted)
text so it visually crawls above/below/through the line.
"""

import random

# --- Original DDLC pool, for flavor ---
NONUNICODE = ("¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß"
              "àáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚě"
              "ĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕ"
              "ŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽž")

# --- Zalgo combining diacritical marks, by direction ---
ZALGO_UP = [chr(c) for c in range(0x0300, 0x0315)]        # stack above
ZALGO_MID = [chr(c) for c in range(0x0315, 0x0334)]        # stack through
ZALGO_DOWN = [chr(c) for c in range(0x0323, 0x0360) if c not in range(0x0334, 0x0338)]  # stack below


def glitchtext(length):
    """Original DDLC behavior — kept intact."""
    return "".join(random.choice(NONUNICODE) for _ in range(length))


def zalgo(text, intensity=8):
    """Wrap each character of `text` in stacked combining marks.
    intensity = roughly how many marks pile onto each character."""
    out = []
    for ch in text:
        out.append(ch)
        out.extend(random.choice(ZALGO_UP) for _ in range(random.randint(0, intensity)))
        out.extend(random.choice(ZALGO_MID) for _ in range(random.randint(0, intensity // 3)))
        out.extend(random.choice(ZALGO_DOWN) for _ in range(random.randint(0, intensity)))
    return "".join(out)


def hellglitch(text, corruption=0.5, intensity=10):
    """The full combo: randomly swap letters for nonunicode noise,
    THEN zalgo the result. corruption = 0..1 chance per character
    of being replaced outright before the zalgo pass."""
    corrupted = "".join(
        random.choice(NONUNICODE) if (c != " " and random.random() < corruption) else c
        for c in text
    )
    return zalgo(corrupted, intensity=intensity)


def demon_scream(length=40, intensity=14):
    """No source text at all — pure noise, maximally stacked."""
    base = glitchtext(length)
    return zalgo(base, intensity=intensity)


def _prompt_int(msg, default):
    raw = input(f"{msg} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print("  (not a number, using default)")
        return default


def _prompt_float(msg, default):
    raw = input(f"{msg} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        print("  (not a number, using default)")
        return default


def main():
    print("=" * 50)
    print("   GLITCHTEXT HELL")
    print("=" * 50)
    print("1) glitchtext   - random noise, no input text")
    print("2) zalgo        - stack combining marks on YOUR text")
    print("3) hellglitch   - corrupt + zalgo YOUR text (full hell)")
    print("4) demon_scream - pure noise, maximally stacked")
    print("5) quit")
    print()

    while True:
        choice = input("Pick a mode (1-5): ").strip()

        if choice == "1":
            length = _prompt_int("Length", 30)
            print()
            print(glitchtext(length))

        elif choice == "2":
            text = input("Text to zalgo: ")
            intensity = _prompt_int("Intensity (try 4-10)", 8)
            print()
            print(zalgo(text, intensity=intensity))

        elif choice == "3":
            text = input("Text to send to hell: ")
            corruption = _prompt_float("Corruption 0.0-1.0 (try 0.3-0.9)", 0.5)
            intensity = _prompt_int("Intensity (try 4-16)", 10)
            print()
            print(hellglitch(text, corruption=corruption, intensity=intensity))

        elif choice == "4":
            length = _prompt_int("Length", 25)
            intensity = _prompt_int("Intensity (try 4-18)", 14)
            print()
            print(demon_scream(length=length, intensity=intensity))

        elif choice == "5" or choice.lower() in ("q", "quit", "exit"):
            break

        else:
            print("Not a valid option, try 1-5.")
            continue

        print()
        again = input("Go again? (Y/n): ").strip().lower()
        print()
        if again == "n":
            break


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        pass
    try:
        input("\nPress Enter to exit...")
    except EOFError:
        pass
