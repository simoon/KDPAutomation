"""
Browser Utilities - Versione Semplificata per Singolo Monitor
Funzioni generiche per gestione browser, senza complessità multi-monitor
"""

import time
import subprocess
import platform
import os
import pyautogui

def get_screen_size():
    """
    Ottieni dimensioni dello schermo corrente.
    
    Returns:
        tuple: (width, height)
    """
    width, height = pyautogui.size()
    print(f"🖥️  Screen size: {width}x{height}")
    return width, height

def get_chrome_path():
    """
    Trova il percorso dell'eseguibile Chrome in base al sistema operativo.
    
    Returns:
        str: Path di Chrome o None se non trovato
    """
    system = platform.system()
    
    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]
    elif system == "Darwin":  # macOS
        possible_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ]
    else:  # Linux
        possible_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium-browser"
        ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def open_positioned_browser(url, width_fraction=2/3, height_fraction=1.0, position="left"):
    """
    Apre browser Chrome posizionato e dimensionato.
    
    Args:
        url: URL da aprire
        width_fraction: Frazione larghezza schermo (0.0-1.0)
        height_fraction: Frazione altezza schermo (0.0-1.0)  
        position: Posizione ("left", "right", "center")
        
    Returns:
        subprocess.Popen: Processo browser o None se errore
    """
    try:
        chrome_path = get_chrome_path()
        if not chrome_path:
            print("❌ Chrome not found on system")
            return None
        
        # Ottieni dimensioni schermo
        screen_width, screen_height = get_screen_size()
        
        # Calcola dimensioni finestra
        window_width = int(screen_width * width_fraction)
        window_height = int(screen_height * height_fraction)
        
        # Calcola posizione finestra
        if position == "left":
            window_x = 0
        elif position == "right":
            window_x = screen_width - window_width
        elif position == "center":
            window_x = (screen_width - window_width) // 2
        else:
            window_x = 0  # Default left
        
        window_y = 0  # Sempre top dello schermo
        
        print(f"🌐 Opening Chrome browser:")
        print(f"   • URL: {url}")
        print(f"   • Target position: ({window_x}, {window_y})")
        print(f"   • Target size: {window_width}x{window_height}")
        
        # Argomenti browser
        browser_args = [
            chrome_path,
            f"--window-size={window_width},{window_height}",
            f"--window-position={window_x},{window_y}",
            "--disable-blink-features=AutomationControlled",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-default-apps",
            "--force-device-scale-factor=1.0",  # Forza scala 1:1
            url
        ]
        
        # Avvia processo browser
        if platform.system() == "Windows":
            browser_process = subprocess.Popen(
                browser_args,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            browser_process = subprocess.Popen(browser_args)
        
        print("✅ Chrome browser process started")
        
        # Aspetta che Chrome si avvii
        time.sleep(3)
        
        # Forza il posizionamento usando AppleScript (macOS) o altri metodi
        force_window_position(window_x, window_y, window_width, window_height)
        
        return browser_process
        
    except Exception as e:
        print(f"❌ Failed to open Chrome browser: {e}")
        return None

def force_window_position(x, y, width, height):
    """
    Forza il posizionamento della finestra Chrome usando metodi OS-specifici.
    
    Args:
        x, y: Posizione target
        width, height: Dimensioni target
    """
    try:
        system = platform.system()
        
        if system == "Darwin":  # macOS
            # Usa AppleScript per forzare posizionamento
            applescript = f'''
            tell application "Google Chrome"
                activate
                set bounds of front window to {{{x}, {y}, {x + width}, {y + height}}}
            end tell
            '''
            
            print(f"🔧 Forcing window position with AppleScript...")
            subprocess.run(['osascript', '-e', applescript], capture_output=True)
            print(f"✅ Window forced to position ({x}, {y}) size {width}x{height}")
            
        elif system == "Windows":
            # Per Windows, potresti usare pywin32 se disponibile
            print(f"⚠️  Windows window positioning not implemented yet")
            print(f"   Manual positioning may be needed")
            
        else:  # Linux
            # Per Linux, potresti usare xdotool se disponibile
            print(f"⚠️  Linux window positioning not implemented yet")
            print(f"   Manual positioning may be needed")
            
    except Exception as e:
        print(f"⚠️  Could not force window position: {e}")
        print(f"   Browser opened but position may not be exact")

def wait_for_page_load(seconds=5, show_progress=True):
    """
    Aspetta che la pagina si carichi.
    
    Args:
        seconds: Secondi da aspettare
        show_progress: Mostra countdown progressivo
    """
    if show_progress:
        print(f"⏳ Waiting {seconds} seconds for page load...")
        for i in range(seconds, 0, -1):
            print(f"   ⏱️  {i} seconds remaining...", end='\r')
            time.sleep(1)
        print("   ✅ Page load wait completed!     ")
    else:
        print(f"⏳ Waiting {seconds} seconds for page load...")
        time.sleep(seconds)
        print("✅ Page load wait completed!")

def close_browser_process(browser_process, timeout=5):
    """
    Chiude processo browser in modo pulito.
    
    Args:
        browser_process: Processo da subprocess.Popen
        timeout: Secondi da aspettare prima di forzare chiusura
        
    Returns:
        bool: True se chiusura riuscita
    """
    try:
        if not browser_process:
            print("ℹ️  No browser process to close")
            return True
            
        print("🔄 Closing browser...")
        
        # Tentativo graceful
        browser_process.terminate()
        
        # Aspetta chiusura
        try:
            browser_process.wait(timeout=timeout)
            print("✅ Browser closed gracefully")
            return True
        except subprocess.TimeoutExpired:
            print("⚠️  Browser not responding, forcing close...")
            browser_process.kill()
            browser_process.wait(timeout=2)
            print("✅ Browser force closed")
            return True
            
    except Exception as e:
        print(f"❌ Error closing browser: {e}")
        return False

def get_screen_center():
    """
    Calcola le coordinate del centro dello schermo.
    
    Returns:
        tuple: (center_x, center_y)
    """
    width, height = get_screen_size()
    center_x = width // 2
    center_y = height // 2
    print(f"🎯 Screen center: ({center_x}, {center_y})")
    return center_x, center_y

def setup_pyautogui_safety():
    """
    Configura pyautogui con impostazioni di sicurezza standard.
    """
    pyautogui.FAILSAFE = True   # Mouse in angolo (0,0) per stop emergenza
    pyautogui.PAUSE = 0.1       # Pausa tra comandi pyautogui
    print("✅ PyAutoGUI safety settings configured")

def move_mouse_to_center():
    """
    Muove il mouse al centro dello schermo.
    
    Returns:
        bool: True se movimento riuscito
    """
    try:
        center_x, center_y = get_screen_center()
        print(f"🖱️  Moving mouse to screen center: ({center_x}, {center_y})")
        pyautogui.moveTo(center_x, center_y, duration=0.5)
        print("✅ Mouse moved to center")
        return True
    except Exception as e:
        print(f"❌ Failed to move mouse to center: {e}")
        return False

# Funzioni di convenienza per setup rapido
def quick_setup():
    """
    Setup rapido con configurazioni standard.
    
    Returns:
        dict: Info schermo
    """
    setup_pyautogui_safety()
    width, height = get_screen_size()
    return {
        'width': width,
        'height': height,
        'center': (width // 2, height // 2)
    }

def quick_open_chrome(url, position="left", width_fraction=2/3):
    """
    Apertura rapida Chrome con impostazioni standard.
    
    Args:
        url: URL da aprire
        position: Posizione finestra
        width_fraction: Frazione larghezza schermo
        
    Returns:
        subprocess.Popen: Processo browser
    """
    setup_pyautogui_safety()
    return open_positioned_browser(
        url=url, 
        width_fraction=width_fraction, 
        position=position
    )

# Test e esempio uso
if __name__ == "__main__":
    print("🧪 Testing simple browser utilities...")
    
    # Test screen detection
    print("\n1. Testing screen detection...")
    screen_info = quick_setup()
    print(f"Screen info: {screen_info}")
    
    # Test Chrome path
    print("\n2. Testing Chrome detection...")
    chrome_path = get_chrome_path()
    if chrome_path:
        print(f"✅ Chrome found: {chrome_path}")
    else:
        print("❌ Chrome not found")
    
    # Test screen center
    print("\n3. Testing screen center...")
    center = get_screen_center()
    print(f"Center coordinates: {center}")
    
    print("\n✅ All tests completed!")
    
    # Optional: Test browser opening (commented out)
    # print("\n4. Testing browser opening...")
    # browser = quick_open_chrome("https://www.google.com")
    # if browser:
    #     input("Press Enter to close browser...")
    #     close_browser_process(browser)