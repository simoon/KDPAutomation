import time
import platform
import pyautogui

assert platform.system() == "Darwin", "Questo script è pensato per macOS"

# Piccola pausa automatica tra azioni
pyautogui.PAUSE = 0.05

def select_all_keydown():
    # Sequenza esplicita con micro-delay: più affidabile di hotkey in alcuni contesti
    pyautogui.keyDown('command')
    time.sleep(0.06)
    pyautogui.press('a')
    time.sleep(0.02)
    pyautogui.keyUp('command')

def select_all_left():
    # Alcune tastiere/ambienti rispondono meglio al lato sinistro
    pyautogui.keyDown('commandleft')
    time.sleep(0.06)
    pyautogui.press('a')
    time.sleep(0.02)
    pyautogui.keyUp('commandleft')

def select_all_hotkey():
    # Variante classica, con intervallo tra i tasti
    pyautogui.hotkey('command', 'a', interval=0.1)

if __name__ == "__main__":
    # 2 secondi per fare click nella casella di testo
    time.sleep(2)

    # Prova 1 (più affidabile)
    select_all_keydown()

    # Se ancora scrive solo "a", commenta la riga sopra e prova una delle seguenti:
    # select_all_left()
    # select_all_hotkey()
