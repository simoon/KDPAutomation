from pynput import mouse, keyboard

# Lista per memorizzare le coordinate dei click
clicks = []

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.right:  # Solo tasto destro
        clicks.append((int(x), int(y)))  # Salva come interi

def on_press(key):
    try:
        if key == keyboard.Key.enter:
            # Stampa le coordinate a coppie
            for i in range(0, len(clicks), 2):
                if i + 1 < len(clicks):
                    x1, y1 = clicks[i]
                    x2, y2 = clicks[i+1]
                    print(f"({x1}, {y1}, {x2}, {y2})")
            return False  # Ferma l’ascolto della tastiera dopo Invio
    except Exception as e:
        print("Errore:", e)

# Listener del mouse
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

# Listener della tastiera
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
