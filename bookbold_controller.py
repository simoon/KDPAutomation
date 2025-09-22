"""
BookBolt Operations Controller - Enhanced Version with User Input and Dynamic Text Generation
Operazioni specifiche per BookBolt Studio con sequenze di azioni e comportamenti umani
Enhanced: User input for template selection, start number, and total notebooks
"""

import time
import random
import platform
import pyautogui

# Import delle nostre utilities semplificate
from utils.browser_utils import (
    quick_open_chrome,
    wait_for_page_load,
    close_browser_process,
    setup_pyautogui_safety,
    get_screen_center
)

# Import per comportamenti naturali
from utils.random_helper import RandomHelper, create_casual_profile

# =============================================================================
# 🎯 CONFIGURAZIONE AREE CLICK - MODIFICA QUI LE COORDINATE
# =============================================================================

# Definisci le aree dove cliccare (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
CLICK_AREAS = {
    "area_1": {
        "name": "Prima Area",
        "coordinates": (19, 149, 63, 177),
        "description": "Prima area di click"
    },
    "area_2": {
        "name": "Seconda Area", 
        "coordinates": (17, 243, 61, 268),
        "description": "Seconda area di click"
    },
    "area_3": {
        "name": "Terza Area",
        "coordinates": (412, 384, 842, 403),
        "description": "Terza area di click"
    },
    "area_4": {
        "name": "area4",
        "coordinates": (573, 455, 843, 461),
        "description": "Quarta area di click"
    },
    "area_5": {
        "name": "area5",
        "coordinates": (20, 152, 56, 175),
        "description": "Quinta area di click"
    },
    "area_6": {
        "name": "area6",
        "coordinates": (15, 281, 49, 303),
        "description": "Sesta area di click"
    },
    "area_7": {
        "name": "area7",
        "coordinates": (447, 197, 785, 214),
        "description": "Settima area di click"
    },    
    "area_8": {
        "name": "area8",
        "coordinates": (779, 256, 833, 275),
        "description": "Ottava area di click"
    },
    "area_9": {
        "name": "area9",
        "coordinates": (782, 204, 829, 223),
        "description": "Nona area di click"
    }, 
    "area_10": {
        "name": "area10",
        "coordinates": (19, 357, 31, 371),
        "description": "Decima area di click"
    }, 
    "area_11": {
        "name": "area11",
        "coordinates": (959, 252, 1057, 265),
        "description": "Undicesima area di click"
    }, 
    "area_11_1": {
        "name": "area11",
        "coordinates": (989, 188, 1100, 200),
        "description": "Undicesima area di click"
    },     
    "area_11_2": {
        "name": "area11",
        "coordinates": (959, 252, 1057, 265),
        "description": "Undicesima area di click"
    }, 
    "area_12": {
        "name": "area12",
        "coordinates": (957, 322, 1047, 331),
        "description": "Dodicesima area di click"
    },     
    "area_13": {
        "name": "area13",
        "coordinates": (82, 350, 155, 400),
        "description": "Tredicesima area di click"
    },  
    "area_14": {
        "name": "area14",
        "coordinates": (477, 206, 492, 224),
        "description": "Quattordicesima area di click"
    }, 
    "area_15": {
        "name": "area15",
        "coordinates": (476, 361, 565, 379),
        "description": "Quindicesima area di click"
    }, 
    "area_16": {
        "name": "area16",
        "coordinates": (636, 358, 723, 377),
        "description": "Sedicesima area di click"
    }, 
    "area_17": {
        "name": "area17",
        "coordinates": (473, 442, 562, 459),
        "description": "Diciassettesima area di click"
    }, 
    "area_18": {
        "name": "area18",
        "coordinates": (633, 442, 722, 460),
        "description": "Diciottesima area di click"
    }, 
    "area_19": {
        "name": "area19",
        "coordinates": (736, 632, 761, 646),
        "description": "Diciannovesima area di click"
    },
    "area_20": {
        "name": "area20",
        "coordinates": (1247, 241, 1254, 256),
        "description": "Diciannovesima area di click"
    },
    "area_21": {
        "name": "area21",
        "coordinates": (1110, 515, 1151, 519),
        "description": "Diciannovesima area di click"
    },
    "area_22": {
        "name": "area22",
        "coordinates": (1247, 241, 1254, 256),
        "description": "Diciannovesima area di click"
    },
    "area_23": {
        "name": "area23",
        "coordinates": (1110, 515, 1151, 519),
        "description": "Diciannovesima area di click"
    },
    "area_24": {
        "name": "area24",
        "coordinates": (693, 331, 831, 288),
        "description": "Diciannovesima area di click"
    }                     
}

# URL BookBolt
BOOKBOLT_URL = "https://studio.bookbolt.io/"

# =============================================================================
# 📚 TEMPLATE CONFIGURATIONS
# =============================================================================

TEMPLATE_OPTIONS = {
    1: {
        "name": "Flowers Composition Notebook College Ruled 7.5 x 9.25",
        "prefix": "Flowers",
        "suffix": "Composition Notebook College Ruled 7.5 x 9.25"
    },
    2: {
        "name": "Vintage illustration Composition Notebook College Ruled 7.5 x 9.25",
        "prefix": "Vintage illustration",
        "suffix": "Composition Notebook College Ruled 7.5 x 9.25"
    },
    3: {
        "name": "Cats Composition Notebook College Ruled 7.5 x 9.25",
        "prefix": "Cats",
        "suffix": "Composition Notebook College Ruled 7.5 x 9.25"
    } ,
    4: {
        "name": "Scientific Composition Notebook College Ruled 7.5 x 9.25",
        "prefix": "Scientific",
        "suffix": "Composition Notebook College Ruled 7.5 x 9.25"
    }         
}

# =============================================================================

class BookBoltController:
    """
    Controller avanzato per operazioni BookBolt con timing naturali e comportamenti umani
    Enhanced with dynamic text generation and user configuration
    """
    
    def __init__(self):
        self.browser_process = None
        self.is_macos = platform.system() == "Darwin"
        
        # User configuration variables
        self.selected_template = None
        self.start_number = None
        self.total_notebooks = None
        self.current_notebook_number = None
        
        # Inizializza RandomHelper con profilo comportamentale casual
        self.random_helper = RandomHelper(create_casual_profile())
        self.random_helper.behavior_profile.mistake_proneness = 0.0
        
        print("🚀 BookBolt Controller initialized (Errors DISABLED)")
        print("🚀 BookBolt Controller initialized (With Natural Timing)")
        print("🧠 Human behavior profile: Casual User")
    
    def get_user_configuration(self):
        """
        Raccoglie la configurazione dall'utente per template, numero inizio e totale notebook
        
        Returns:
            bool: True se configurazione completata con successo
        """
        try:
            print("\n" + "="*60)
            print("📋 USER CONFIGURATION")
            print("="*60)
            
            # Step 1: Template selection
            print("\n📚 STEP 1: Select Template Type")
            print("Available templates:")
            for key, template in TEMPLATE_OPTIONS.items():
                print(f"   {key}. {template['name']}")
            
            while True:
                try:
                    template_choice = input("\nEnter your choice (1 to 4): ").strip()
                    template_num = int(template_choice)
                    
                    if template_num in TEMPLATE_OPTIONS:
                        self.selected_template = TEMPLATE_OPTIONS[template_num]
                        print(f"✅ Selected: {self.selected_template['name']}")
                        break
                    else:
                        print("❌ Invalid choice. Please enter 1 or 2.")
                        
                except ValueError:
                    print("❌ Invalid input. Please enter a number (1 or 2).")
            
            # Step 2: Start number
            print(f"\n🔢 STEP 2: Enter Start Number")
            while True:
                try:
                    start_input = input("Enter the starting number (integer): ").strip()
                    self.start_number = int(start_input)
                    
                    if self.start_number >= 0:
                        print(f"✅ Start number: {self.start_number}")
                        break
                    else:
                        print("❌ Please enter a positive number or zero.")
                        
                except ValueError:
                    print("❌ Invalid input. Please enter a valid integer.")
            
            # Step 3: Total notebooks
            print(f"\n📖 STEP 3: Enter Total Number of Notebooks")
            while True:
                try:
                    total_input = input("Enter total number of notebooks to create (integer): ").strip()
                    self.total_notebooks = int(total_input)
                    
                    if self.total_notebooks > 0:
                        print(f"✅ Total notebooks: {self.total_notebooks}")
                        break
                    else:
                        print("❌ Please enter a positive number greater than 0.")
                        
                except ValueError:
                    print("❌ Invalid input. Please enter a valid integer.")
            
            # Initialize current notebook number
            self.current_notebook_number = self.start_number
            
            # Configuration summary
            print(f"\n📋 CONFIGURATION SUMMARY:")
            print(f"   • Template: {self.selected_template['name']}")
            print(f"   • Start Number: {self.start_number}")
            print(f"   • Total Notebooks: {self.total_notebooks}")
            print(f"   • Range: {self.start_number} to {self.start_number + self.total_notebooks - 1}")
            
            # Confirmation
            confirm = input(f"\n❓ Proceed with this configuration? (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                print("✅ Configuration confirmed!")
                return True
            else:
                print("❌ Configuration cancelled.")
                return False
                
        except Exception as e:
            print(f"❌ Configuration failed: {e}")
            return False
    
    def generate_dynamic_text(self):
        """
        Genera il testo dinamico basato sulla configurazione utente
        
        Returns:
            str: Testo generato con template e numero corrente
        """
        if not self.selected_template or self.current_notebook_number is None:
            return "Default Text"
        
        # Format: "Prefix" + number + "Suffix"
        dynamic_text = f"{self.selected_template['prefix']} {self.current_notebook_number} {self.selected_template['suffix']}"
        
        return dynamic_text

    def copy_graphic(self):
        """
        Copia elemento grafico selezionato (Ctrl+C o Cmd+C)
        """
        try:
            print("🎨 Copying graphic element...")
            if self.is_macos:
                pyautogui.keyDown('command')
                time.sleep(0.06)
                pyautogui.press('c')
                time.sleep(0.02)
                pyautogui.keyUp('command')
            else:
                pyautogui.hotkey('ctrl', 'c', interval=0.1)
            
            time.sleep(0.5)  # Tempo maggiore per elementi grafici
            print("✅ Graphic copy executed")
            return True
        except Exception as e:
            print(f"❌ Graphic copy failed: {e}")
            return False

    def paste_graphic(self):
        """
        Incolla elemento grafico (Ctrl+V o Cmd+V)
        """
        try:
            print("🎨 Pasting graphic element...")
            if self.is_macos:
                pyautogui.keyDown('command')
                time.sleep(0.06)
                pyautogui.press('v')
                time.sleep(0.02)
                pyautogui.keyUp('command')
            else:
                pyautogui.hotkey('ctrl', 'v', interval=0.1)
            
            time.sleep(1.0)  # Tempo maggiore per rendering grafico
            print("✅ Graphic paste executed")
            return True
        except Exception as e:
            print(f"❌ Graphic paste failed: {e}")
            return False

    def click_in_area(self, area_config, area_name=""):
        """
        Clicca in un punto casuale all'interno dell'area specificata
        
        Args:
            area_config: Dict con 'coordinates' (x1, y1, x2, y2)
            area_name: Nome descrittivo dell'area
        """
        try:
            coords = area_config['coordinates']
            x1, y1, x2, y2 = coords
            
            # Assicurati che le coordinate siano nell'ordine corretto
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            
            # Genera punto casuale nell'area
            click_x = random.randint(min_x, max_x)
            click_y = random.randint(min_y, max_y)
            
            print(f"🎯 Clicking in {area_name}")
            print(f"   • Area: ({min_x}, {min_y}) to ({max_x}, {max_y})")
            print(f"   • Click point: ({click_x}, {click_y})")
            
            # Muovi e clicca
            pyautogui.moveTo(click_x, click_y, duration=0.8)
            time.sleep(0.3)
            pyautogui.click()
            
            print(f"✅ Clicked successfully in {area_name}")
            return True
            
        except Exception as e:
            print(f"❌ Click failed in {area_name}: {e}")
            return False
    
    def select_all_text(self):
        """
        Seleziona tutto il testo (Ctrl+A o Cmd+A)
        """
        try:
            print("📋 Selecting all text...")
            if self.is_macos:
                print("📋 Selecting all text ON MAC")
                pyautogui.keyDown('command')
                time.sleep(0.06)
                pyautogui.press('a')
                time.sleep(0.02)
                pyautogui.keyUp('command')
            else:
                pyautogui.hotkey('ctrl', 'a', interval=0.1)
            
            time.sleep(0.3)
            print("✅ Select all executed")
            return True
        except Exception as e:
            print(f"❌ Select all failed: {e}")
            return False
    
    def press_key(self, key):
        """
        Preme un tasto specifico
        
        Args:
            key: Tasto da premere (es: 'enter', 'tab', 'escape')
        """
        try:
            print(f"⌨️ Pressing key: {key}")
            pyautogui.press(key)
            time.sleep(0.2)
            print(f"✅ Key '{key}' pressed")
            return True
        except Exception as e:
            print(f"❌ Key press failed for '{key}': {e}")
            return False
    
    def type_dynamic_text(self):
        """
        Digita il testo dinamico generato
        
        Returns:
            bool: True se digitazione riuscita
        """
        try:
            # Genera il testo dinamico
            text = self.generate_dynamic_text()
            
            print(f"⌨️ Typing dynamic text: '{text}'")
            print(f"📊 Notebook {self.current_notebook_number} of {self.total_notebooks} total")
            print(f"📝 Template: {self.selected_template['prefix']}")
            
            # Usa timing completamente naturale per ogni carattere
            for i, char in enumerate(text):
                print(f"📤 Typing char {i+1}/{len(text)}: '{char}'")
                pyautogui.write(char)
                
                # Delay naturale basato sul carattere
                char_delay = self.random_helper.get_typing_delay(char=char)
                time.sleep(char_delay)
                
                # Pause occasionali
                if i > 0 and i % 8 == 0 and random.random() < 0.15:
                    brief_pause = self.random_helper.get_typing_delay() * 2
                    print(f"   ⏸️ Brief pause: {brief_pause:.2f}s")
                    time.sleep(brief_pause)
            
            print(f"✅ Successfully typed dynamic text: '{text}'")
            return True
            
        except Exception as e:
            print(f"❌ Dynamic text typing failed: {e}")
            return False
    
    def execute_single_action(self, action):
        """
        Esegue una singola azione con timing naturale
        Supporta azioni dinamiche per il testo
        
        Args:
            action: Dict con dettagli dell'azione
            
        Returns:
            bool: True se azione riuscita
        """
        try:
            action_type = action['type']
            
            # Possibilità di esitazione prima dell'azione
            if action_type in ['click_area', 'type_text', 'type_dynamic_text'] and self.random_helper.should_hesitate("normal"):
                hesitation = self.random_helper.get_natural_pause("hesitation") 
                print(f"   🤔 Pre-action hesitation: {hesitation:.1f}s")
                time.sleep(hesitation)
            
            if action_type == "click_area":
                area_name = action['area']
                if area_name in CLICK_AREAS:
                    return self.click_in_area(CLICK_AREAS[area_name], CLICK_AREAS[area_name]['name'])
                else:
                    print(f"❌ Area '{area_name}' not found")
                    return False
                    
            elif action_type == "select_all":
                print(f"🔍 DEBUG: SELECT ALL")
                return self.select_all_text()
                
            elif action_type == "type_text":
                # Static text typing (fallback)
                text = action['text']
                print(f"⌨️ Typing static text: '{text}'")
                
                for i, char in enumerate(text):
                    pyautogui.write(char)
                    char_delay = self.random_helper.get_typing_delay(char=char)
                    time.sleep(char_delay)
                    
                    if i > 0 and i % 4 == 0 and random.random() < 0.2:
                        brief_pause = self.random_helper.get_typing_delay() * 3
                        time.sleep(brief_pause)
                
                print(f"✅ Typed static text: '{text}'")
                return True
                
            elif action_type == "type_dynamic_text":
                # Dynamic text typing using current configuration
                return self.type_dynamic_text()

            elif action_type == "copy_graphic":
                return self.copy_graphic()
                
            elif action_type == "paste_graphic":
                return self.paste_graphic()
                
            elif action_type == "press_key":
                key = action['key']
                return self.press_key(key)
                
            elif action_type == "wait":
                seconds = action.get('seconds', 1)
                natural_wait = seconds + random.uniform(-0.2, 0.5)
                natural_wait = max(0.1, natural_wait)
                print(f"⏸️ Natural wait: {natural_wait:.1f}s")
                time.sleep(natural_wait)
                return True
                
            else:
                print(f"❌ Unknown action type: {action_type}")
                return False
                
        except Exception as e:
            print(f"❌ Action execution failed: {e}")
            return False
    
    def get_dynamic_action_sequence(self):
        """
        Genera la sequenza di azioni con testo dinamico
        
        Returns:
            dict: Sequenza di azioni configurata dinamicamente
        """
        return {
            "name": f"Dynamic Sequence - Notebook {self.current_notebook_number}",
            "actions": [
                {"type": "click_area", "area": "area_1", "wait_min": 0.8, "wait_max": 1.5},
                {"type": "click_area", "area": "area_2", "wait_min": 1.5, "wait_max": 2.5},
                {"type": "click_area", "area": "area_3", "wait_min": 0.7, "wait_max": 1.3},
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},                
                {"type": "type_text", "text": "Template", "wait_min": 0.5, "wait_max": 1.2},
                {"type": "click_area", "area": "area_4", "wait_min": 0.7, "wait_max": 1.3},          
                {"type": "click_area", "area": "area_5", "wait_min": 0.7, "wait_max": 1.3},
                {"type": "click_area", "area": "area_6", "wait_min": 0.7, "wait_max": 1.3},
                {"type": "click_area", "area": "area_7", "wait_min": 0.7, "wait_max": 1.3},
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},
                {"type": "type_dynamic_text", "wait_min": 0.5, "wait_max": 1.2},  # Dynamic text here
                {"type": "click_area", "area": "area_8", "wait_min": 0.7, "wait_max": 1.3}, # OK button
                {"type": "click_area", "area": "area_9", "wait_min": 0.7, "wait_max": 1.3}, # Open notebook
                {"type": "click_area", "area": "area_10", "wait_min": 0.7, "wait_max": 1.3}, # Image icon
                {"type": "click_area", "area": "area_11", "wait_min": 0.7, "wait_max": 1.3}, # Combo box
                {"type": "click_area", "area": "area_11_1", "wait_min": 0.7, "wait_max": 1.3}, # selec top on Combo box                                
                {"type": "click_area", "area": "area_11_2", "wait_min": 0.7, "wait_max": 1.3}, # Combo box
                {"type": "click_area", "area": "area_12", "wait_min": 0.7, "wait_max": 1.3}, # Select item
                {"type": "click_area", "area": "area_13", "wait_min": 0.7, "wait_max": 1.3}, # First image
                {"type": "click_area", "area": "area_14", "wait_min": 0.7, "wait_max": 1.3}, # Position button
                {"type": "click_area", "area": "area_15", "wait_min": 0.7, "wait_max": 1.3}, # Left center
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},
                {"type": "type_text", "text": "30,29", "wait_min": 0.5, "wait_max": 1.2},
                {"type": "click_area", "area": "area_16", "wait_min": 0.7, "wait_max": 1.3}, # Top center
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},
                {"type": "type_text", "text": "12,06", "wait_min": 0.5, "wait_max": 1.2},                  
                {"type": "click_area", "area": "area_17", "wait_min": 0.7, "wait_max": 1.3}, # Width
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},
                {"type": "type_text", "text": "18,43", "wait_min": 0.5, "wait_max": 1.2},
                {"type": "click_area", "area": "area_18", "wait_min": 0.7, "wait_max": 1.3}, # Height
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},
                {"type": "type_text", "text": "24,47", "wait_min": 0.5, "wait_max": 1.2},
                {"type": "click_area", "area": "area_19", "wait_min": 0.7, "wait_max": 1.3}, # OK button
                {"type": "copy_graphic", "wait_min": 0.5, "wait_max": 1.0},  # Copy graphic
                {"type": "paste_graphic", "wait_min": 1.0, "wait_max": 2.0}, # Paste graphic
                {"type": "click_area", "area": "area_14", "wait_min": 0.7, "wait_max": 1.3}, # Position button
                {"type": "click_area", "area": "area_15", "wait_min": 0.7, "wait_max": 1.3}, # Left center
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},
                {"type": "type_text", "text": "9,07", "wait_min": 0.5, "wait_max": 1.2},
                {"type": "click_area", "area": "area_16", "wait_min": 0.7, "wait_max": 1.3}, # Top center
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},
                {"type": "type_text", "text": "12,06", "wait_min": 0.5, "wait_max": 1.2},                  
                {"type": "click_area", "area": "area_17", "wait_min": 0.7, "wait_max": 1.3}, # Width
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},
                {"type": "type_text", "text": "18,43", "wait_min": 0.5, "wait_max": 1.2},
                {"type": "click_area", "area": "area_18", "wait_min": 0.7, "wait_max": 1.3}, # Height
                {"type": "select_all", "wait_min": 0.3, "wait_max": 0.8},
                {"type": "type_text", "text": "24,47", "wait_min": 0.5, "wait_max": 1.2},
                {"type": "click_area", "area": "area_19", "wait_min": 0.7, "wait_max": 1.3}, # OK button
                {"type": "click_area", "area": "area_20", "wait_min": 0.7, "wait_max": 1.3}, # OK send to back
                {"type": "click_area", "area": "area_21", "wait_min": 0.7, "wait_max": 1.3}, # OK send to back     
                {"type": "click_area", "area": "area_22", "wait_min": 0.7, "wait_max": 1.3}, # OK send to back
                {"type": "click_area", "area": "area_23", "wait_min": 0.7, "wait_max": 1.3}, # OK send to back   
                {"type": "click_area", "area": "area_24", "wait_min": 0.7, "wait_max": 1.3}, # final click on screen                                            
            ]
        }
    
    def execute_single_sequence(self):
        """
        Esegue una singola sequenza per il notebook corrente
        
        Returns:
            bool: True se sequenza completata con successo
        """
        try:
            # Ottieni la sequenza dinamica
            sequence = self.get_dynamic_action_sequence()
            
            print(f"\n🎬 Executing: {sequence['name']}")
            print(f"   📊 Progress: {self.current_notebook_number - self.start_number + 1}/{self.total_notebooks}")
            print(f"   📤 Text will be: '{self.generate_dynamic_text()}'")
            
            for i, action in enumerate(sequence['actions']):
                print(f"\n   🔢 Step {i+1}/{len(sequence['actions'])}: {action['type']}")
                
                # Esegui l'azione
                success = self.execute_single_action(action)
                if not success:
                    print(f"❌ Sequence failed at step {i+1}")
                    return False
                
                # Wait naturale dopo azione se specificato
                if 'wait_min' in action and 'wait_max' in action:
                    wait_time = self.random_helper.get_click_delay(action['wait_min'], action['wait_max'])
                    print(f"   ⏸️ Post-action wait: {wait_time:.2f}s (range: {action['wait_min']}-{action['wait_max']})")
                    time.sleep(wait_time)
            
            print(f"✅ Sequence completed for notebook {self.current_notebook_number}")
            return True
            
        except Exception as e:
            print(f"❌ Single sequence execution failed: {e}")
            return False
    
    def execute_all_notebooks(self):
        """
        Esegue le sequenze per tutti i notebook configurati
        
        Returns:
            bool: True se tutte le sequenze completate con successo
        """
        try:
            print(f"\n🚀 Starting batch execution for {self.total_notebooks} notebooks")
            print(f"📈 Range: {self.start_number} to {self.start_number + self.total_notebooks - 1}")
            
            successful_notebooks = 0
            failed_notebooks = 0
            
            # Reset to start number
            self.current_notebook_number = self.start_number
            
            for i in range(self.total_notebooks):
                print(f"\n" + "="*50)
                print(f"📖 NOTEBOOK {i+1}/{self.total_notebooks} - Number: {self.current_notebook_number}")
                print(f"📤 Dynamic Text: '{self.generate_dynamic_text()}'")
                print("="*50)
                
                # Esegui sequenza per questo notebook
                success = self.execute_single_sequence()
                
                if success:
                    successful_notebooks += 1
                    print(f"✅ Notebook {self.current_notebook_number} completed successfully!")
                else:
                    failed_notebooks += 1
                    print(f"❌ Notebook {self.current_notebook_number} failed!")
                    
                    # Ask user if they want to continue
                    if failed_notebooks > 0:
                        continue_choice = input(f"\n❓ Continue with remaining notebooks? (y/n): ").strip().lower()
                        if continue_choice not in ['y', 'yes']:
                            print("ℹ️ Batch execution stopped by user.")
                            break
                
                # Increment notebook number for next iteration
                self.current_notebook_number += 1
                
                # Pause between notebooks (except for the last one)
                if i < self.total_notebooks - 1:
                    between_notebook_pause = self.random_helper.get_natural_pause("general")
                    print(f"⏸️ Pause between notebooks: {between_notebook_pause:.1f}s")
                    time.sleep(between_notebook_pause)
            
            # Final summary
            print(f"\n" + "="*60)
            print(f"📊 BATCH EXECUTION SUMMARY")
            print(f"="*60)
            print(f"✅ Successful: {successful_notebooks}")
            print(f"❌ Failed: {failed_notebooks}")
            print(f"📈 Success Rate: {(successful_notebooks/self.total_notebooks)*100:.1f}%")
            print(f"🔢 Range Processed: {self.start_number} to {self.current_notebook_number - 1}")
            
            return failed_notebooks == 0
            
        except Exception as e:
            print(f"❌ Batch execution failed: {e}")
            return False
    
    def execute_bookbolt_sequence(self):
        """
        Esegue la sequenza completa di operazioni BookBolt con configurazione utente
        """
        try:
            print("🚀 Starting BookBolt operations with User Configuration...")
            print("="*60)
            
            # Step 1: Get user configuration
            if not self.get_user_configuration():
                print("❌ User configuration failed or cancelled")
                return False
            
            # Step 2: Setup pyautogui safety
            print("\n🔧 Setting up safety configurations...")
            setup_pyautogui_safety()
            
            # Step 3: Open browser
            print("🌐 Opening positioned browser...")
            self.browser_process = quick_open_chrome(
                url=BOOKBOLT_URL,
                position="left",
                width_fraction=2/3
            )
            
            if not self.browser_process:
                print("❌ Failed to open browser")
                return False
            
            # Step 4: Wait for page load
            print("⏳ Waiting for page load...")
            wait_for_page_load(10, show_progress=True)
            
            # Step 5: Execute all notebooks
            print(f"\n🎬 Step 5: Executing batch sequences for all notebooks")
            success = self.execute_all_notebooks()
            
            if success:
                print("\n🎉 All notebooks completed successfully!")
                print("✅ BookBolt automation finished!")
            else:
                print("\n⚠️ Some notebooks failed. Check the logs above.")
            
            return success
            
        except Exception as e:
            print(f"❌ Main sequence failed: {e}")
            return False
    
    def cleanup(self):
        """Chiude il browser usando utilities"""
        if self.browser_process:
            print("🧹 Cleaning up...")
            close_browser_process(self.browser_process)

def show_configuration():
    """Mostra la configurazione corrente delle aree e template"""
    print("\n" + "="*60)
    print("🎯 CURRENT CONFIGURATION")
    print("="*60)
    
    print(f"\n🔗 URL: {BOOKBOLT_URL}")
    
    # Show screen info
    screen_center = get_screen_center()
    print(f"🖥️ Screen center: {screen_center}")
    
    print("\n🎯 CLICK AREAS:")
    for key, area in CLICK_AREAS.items():
        coords = area['coordinates']
        print(f"   • {area['name']}: ({coords[0]}, {coords[1]}) → ({coords[2]}, {coords[3]})")
    
    print(f"\n📚 AVAILABLE TEMPLATES:")
    for key, template in TEMPLATE_OPTIONS.items():
        print(f"   {key}. {template['name']}")
        print(f"      Format: '{template['prefix']} [NUMBER] {template['suffix']}'")
    
    print(f"\n🎬 DYNAMIC SEQUENCE FEATURES:")
    print(f"   • User template selection")
    print(f"   • Configurable start number and total count")
    print(f"   • Dynamic text generation per notebook")
    print(f"   • Batch processing with progress tracking")
    print(f"   • Error handling and user continuation prompts")
    print(f"   • Copy/paste graphic operations")
    
    print("\n" + "="*60)

def main():
    """Main execution function"""
    
    # Show current configuration
    show_configuration()
    
    # Ask user confirmation
    print("\n🤔 Ready to start BookBolt automation with user configuration?")
    print("   You will be prompted to configure templates and numbers.")
    response = input("   Press ENTER to continue, or 'q' to quit: ").strip().lower()
    
    if response == 'q':
        print("👋 Exiting...")
        return
    
    # Create controller and execute
    controller = BookBoltController()
    
    try:
        success = controller.execute_bookbolt_sequence()
        
        if success:
            print("\n🎊 SUCCESS! All notebooks completed successfully.")
        else:
            print("\n💥 COMPLETED! Some operations may have failed - check logs above.")
            
    except KeyboardInterrupt:
        print("\nℹ️ Operations interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        controller.cleanup()
        print("\n👋 Program finished!")

if __name__ == "__main__":
    main()