"""
Amazon KDP Operations Controller - Simplified Version with Static Content
Operazioni specifiche per Amazon KDP (Kindle Direct Publishing) con sequenze di azioni e comportamenti umani
Simplified: Static book data embedded in code for single book publishing
"""

import time
import random
import platform
import pyautogui
import pyperclip  # Added for clipboard operations

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
    "create_paperback_button": {
        "name": "Create Paperback Button",
        "coordinates": (656, 754, 778, 768),
        "description": "Bottone 'Crea versione cartacea'"
    },
    "language_combo": {
        "name": "Language Combo",
        "coordinates": (563, 521, 570, 539),
        "description": "Combo box selezione lingua"
    },
    "english_option": {
        "name": "English Language Option",
        "coordinates": (342, 593, 527, 601),
        "description": "Opzione 'English' nel combo lingua"
    },
    "book_title_field": {
        "name": "Book Title Field",
        "coordinates": (361, 722, 636, 735),
        "description": "Campo titolo del libro"
    },
    "author_first_name_field": {
        "name": "Author First Name Field",
        "coordinates": (471, 514, 630, 536),
        "description": "Campo nome autore"
    },
    "author_last_name_field": {
        "name": "Author Last Name Field",
        "coordinates": (804, 517, 948, 533),
        "description": "Campo cognome autore"
    },
    "description_field": {
        "name": "Description Field",
        "coordinates": (374, 952, 568, 1012),
        "description": "Campo descrizione libro"
    },
    "click_for_scroll_field": {
        "name": "Description Field",
        "coordinates":  (173, 830, 228, 882),
        "description": "Campo descrizione libro"
    },
    "publishing_rights_field": {
        "name": "Publishing Rights Field",
        "coordinates": (385, 320, 651, 326),
        "description": "Campo diritti di pubblicazione"
    },
    "main_audience_no": {
        "name": "Main Audience No",
        "coordinates": (359, 547, 370, 554),
        "description": "Destinatari principali - No"
    },
    "low_content_book": {
        "name": "Low Content Book",
        "coordinates": (371, 293, 550, 296),
        "description": "Libro con pochi contenuti"
    },
    "categories_field1": {
        "name": "Categories Field 1",
        "coordinates": (345, 993, 428, 1010),
        "description": "Campo categorie"
    },
    "categories_field2": {
        "name": "Categories Field 2",
        "coordinates": (214, 589, 280, 597),
        "description": "Campo categorie"
    },
    "categories_field3": {
        "name": "Categories Field 3",
        "coordinates":(246, 620, 300, 625),
        "description": "Campo categorie"
    },
    "categories_field4": {
        "name": "Categories Field 4",
        "coordinates": (629, 707, 660, 717),
        "description": "Campo categorie"
    },
    "categories_field5": {
        "name": "Categories Field 5",
        "coordinates": (178, 776, 326, 792),
        "description": "Campo categorie"
    },
    "categories_field6": {
        "name": "Categories Field 6",
        "coordinates": (216, 631, 325, 644),
        "description": "Campo categorie"
    },
    "categories_field7": {
        "name": "Categories Field 7",
        "coordinates": (221, 384, 307, 391),
        "description": "Campo categorie"
    },
    "categories_field8": {
        "name": "Categories Field 8",
        "coordinates": (214, 692, 300, 705),
        "description": "Campo categorie"
    },
        "categories_field9": {
        "name": "Categories Field 9",
        "coordinates": (220, 761, 312, 769),
        "description": "Campo categorie"
    },
        "categories_field10": {
        "name": "Categories Field10",
        "coordinates": (628, 700, 662, 705),
        "description": "Campo categorie"
    },
        "categories_field11": {
        "name": "Categories Field 11",
        "coordinates": (1016, 943, 1096, 956),
        "description": "Campo categorie"
    },                        
    "keyword_1_field": {
        "name": "Keyword 1 Field",
        "coordinates": (345, 520, 580, 534),
        "description": "Campo parola chiave 1"
    },
    "keyword_2_field": {
        "name": "Keyword 2 Field",
        "coordinates": (741, 520, 822, 534),
        "description": "Campo parola chiave 1"
    },
    "keyword_3_field": {
        "name": "Keyword 3 Field",
        "coordinates": (346, 579, 449, 593),
        "description": "Campo parola chiave 1"
    },
    "keyword_4_field": {
        "name": "Keyword 4 Field",
        "coordinates": (741, 580, 842, 595),
        "description": "Campo parola chiave 1"
    },
    "keyword_5_field": {
        "name": "Keyword 5 Field",
        "coordinates": (360, 638, 526, 652),
        "description": "Campo parola chiave 1"
    },
    "keyword_6_field": {
        "name": "Keyword 6 Field",
        "coordinates":(747, 636, 871, 653),
        "description": "Campo parola chiave 1"
    },
    "keyword_7_field": {
        "name": "Keyword 7 Field",
        "coordinates": (345, 697, 589, 710),
        "description": "Campo parola chiave 1"
    },                         
    "save_and_continue": {
        "name": "Save and Continue Button",
        "coordinates": (919, 692, 1109, 707),
        "description": "Bottone 'Salva e continua'"
    }
}


# URL Amazon KDP
KDP_URL = "https://kdp.amazon.com/it_IT/create"

# =============================================================================
# 📚 DATI STATICI DEL LIBRO - MODIFICA QUI I CONTENUTI
# =============================================================================

BOOK_DATA = {
    "title": "My Beautiful Journal: A Daily Planner for Creativity and Productivity",
    "author_first_name": "Simon's",
    "author_last_name": "Studio Publications",
    "description": """Transform your daily routine with this beautifully designed journal that combines functionality with style. 

This comprehensive planner features:
- Daily planning pages with time slots
- Weekly and monthly overviews
- Goal-setting sections
- Inspirational quotes
- Note-taking space
- Habit tracker
- Premium quality paper
- Elegant cover design

Perfect for students, professionals, entrepreneurs, and anyone looking to organize their life and boost productivity. Whether you're planning your workday, tracking personal goals, or simply journaling your thoughts, this planner provides the perfect structure to keep you motivated and focused.

Size: 6x9 inches - perfect for your desk or bag
Pages: High-quality, thick paper that prevents bleed-through
Binding: Durable binding that lays flat when open

Start your journey to better organization and increased productivity today!""",
    "keyword_1": "daily planner1",
    "keyword_2": "daily planner2",
    "keyword_3": "daily planner3",
    "keyword_4": "daily planner4",
    "keyword_5": "daily planner5",
    "keyword_6": "daily planner6",
    "keyword_7": "daily planner7"
}

# =============================================================================

class KDPController:
    """
    Controller semplificato per operazioni Amazon KDP con timing naturali e comportamenti umani
    Simplified with static book data for single book publishing
    """
    
    def __init__(self):
        self.browser_process = None
        self.is_macos = platform.system() == "Darwin"
        
        # Inizializza RandomHelper con profilo comportamentale casual
        self.random_helper = RandomHelper(create_casual_profile())
        self.random_helper.behavior_profile.mistake_proneness = 0.0
        
        print("🚀 KDP Controller initialized (Errors DISABLED)")
        print("🚀 KDP Controller initialized (With Natural Timing)")
        print("🧠 Human behavior profile: Casual User")
        print(f"📖 Book to publish: '{BOOK_DATA['title']}'")
        print(f"👤 Author: {BOOK_DATA['author_first_name']} {BOOK_DATA['author_last_name']}")

    def scroll_down(self, scroll_amount=3):
        """
        Scrolla verso il basso usando Page Down per coprire tutta l'altezza dello schermo
        
        Args:
            scroll_amount: Numero di volte da premere Page Down (default 1 per schermo intero)
        """
        try:
            print(f"📜 Scrolling down using Page Down...")
            
            # Usa Page Down per scroll naturale di tutta la pagina
            pyautogui.press('pagedown')
            
            # Pausa naturale dopo scroll
            scroll_pause = self.random_helper.get_click_delay(0.5, 1.2)
            time.sleep(scroll_pause)
            
            print(f"✅ Page Down scroll completed")
            return True
            
        except Exception as e:
            print(f"❌ Scroll failed: {e}")
            return False


    def scroll_down(self, scroll_amount=3):
        
        """
        Scrolla verso il basso usando Page Down per coprire tutta l'altezza dello schermo
        
        Args:
            scroll_amount: Numero di volte da premere Page Down (default 1 per schermo intero)
        """

        try:
            print(f"📜 Scrolling down using Page Down...")
            
            # Usa Page Down per scroll naturale di tutta la pagina
            pyautogui.press('pagedown')
            
            # Pausa naturale dopo scroll
            scroll_pause = self.random_helper.get_click_delay(0.5, 1.2)
            time.sleep(scroll_pause)
            
            print(f"✅ Page Down scroll completed")
            return True
            
        except Exception as e:
            print(f"❌ Scroll failed: {e}")
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
            
            # Controlla se le coordinate sono placeholder (0,0,0,0)
            if all(coord == 0 for coord in coords):
                print(f"⚠️ WARNING: {area_name} has placeholder coordinates (0,0,0,0)")
                print(f"   Please update coordinates in CLICK_AREAS configuration")
                # Per ora continua con coordinate centro schermo per test
                center_x, center_y = get_screen_center()
                click_x, click_y = center_x, center_y
            else:
                # Assicurati che le coordinate siano nell'ordine corretto
                min_x, max_x = min(x1, x2), max(x1, x2)
                min_y, max_y = min(y1, y2), max(y1, y2)
                
                # Genera punto casuale nell'area
                click_x = random.randint(min_x, max_x)
                click_y = random.randint(min_y, max_y)
            
            print(f"🎯 Clicking in {area_name}")
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
    
    def paste_text(self, text):
        """
        Copia il testo negli appunti e lo incolla
        
        Args:
            text: Testo da incollare
            
        Returns:
            bool: True se operazione riuscita
        """
        try:
            print(f"📋 Pasting text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            
            # Copia negli appunti usando pyperclip
            pyperclip.copy(text)
            print(f"   📋 Copied to clipboard ({len(text)} chars)")
            
            # Pausa naturale per "pensare" prima di incollare
            think_pause = self.random_helper.get_click_delay(0.3, 0.8)
            print(f"   🤔 Brief pause before paste: {think_pause:.1f}s")
            time.sleep(think_pause)
            
            # Incolla usando Ctrl+V o Cmd+V
            if self.is_macos:
                pyautogui.keyDown('command')
                time.sleep(0.06)
                pyautogui.press('v')
                time.sleep(0.02)
                pyautogui.keyUp('command')
            else:
                pyautogui.hotkey('ctrl', 'v', interval=0.1)
            
            # Pausa naturale dopo incolla
            paste_pause = self.random_helper.get_click_delay(0.2, 0.6)
            time.sleep(paste_pause)
            
            print("✅ Text pasted successfully")
            return True
            
        except Exception as e:
            print(f"❌ Text paste failed: {e}")
            return False
    
    def execute_single_action(self, action):
        """
        Esegue una singola azione con timing naturale
        
        Args:
            action: Dict con dettagli dell'azione
            
        Returns:
            bool: True se azione riuscita
        """
        try:
            action_type = action['type']
            
            # Possibilità di esitazione prima dell'azione
            if action_type in ['click_area', 'paste_text'] and self.random_helper.should_hesitate("normal"):
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
                    
            elif action_type == "paste_text":
                text = action['text']
                return self.paste_text(text)
                
            elif action_type == "scroll_down":
                amount = action.get('amount', 3)
                return self.scroll_down(amount)
                
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
    
    def execute_kdp_sequence(self):
        """
        Esegue la sequenza completa di operazioni KDP
        
        Returns:
            bool: True se sequenza completata con successo
        """
        try:
            print("🚀 Starting Amazon KDP operations...")
            print("="*60)
            
            # Step 1: Setup pyautogui safety
            print("🔧 Setting up safety configurations...")
            setup_pyautogui_safety()
            
            # Step 2: Open browser
            print("🌐 Opening positioned browser...")
            self.browser_process = quick_open_chrome(
                url=KDP_URL,
                position="left",
                width_fraction=2/3
            )
            
            if not self.browser_process:
                print("❌ Failed to open browser")
                return False
            
            # Step 3: Wait for page load
            print("⏳ Waiting for page load...")
            wait_for_page_load(10, show_progress=True)
            
            # Step 4: Execute KDP sequence
            print(f"\n🎬 Step 4: Executing KDP publishing sequence")
            sequence = self.get_kdp_action_sequence()
            
            print(f"📖 Publishing: {BOOK_DATA['title']}")
            print(f"👤 Author: {BOOK_DATA['author_first_name']} {BOOK_DATA['author_last_name']}")
            
            for i, action in enumerate(sequence['actions']):
                print(f"\n   🔢 Step {i+1}/{len(sequence['actions'])}: {action['type']}")
                
                # Mostra dettagli specifici per alcune azioni
                if action['type'] == 'paste_text':
                    text_preview = action['text'][:30] + "..." if len(action['text']) > 30 else action['text']
                    print(f"      Text: '{text_preview}'")
                elif action['type'] == 'click_area':
                    print(f"      Area: {action['area']}")
                
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
            
            print("\n🎉 KDP publishing sequence completed successfully!")
            print("✅ Book submission finished!")
            
            return True
            
        except Exception as e:
            print(f"❌ KDP sequence failed: {e}")
            return False
    
    def get_kdp_action_sequence(self):
        """
        Genera la sequenza di azioni per pubblicazione KDP con dati statici
        
        Returns:
            dict: Sequenza di azioni per KDP
        """
        return {
            "name": "KDP Publishing Sequence - Static Data",
            "actions": [
                # Step 1: Click "Crea versione cartacea"
                {"type": "click_area", "area": "create_paperback_button", "wait_min": 1.0, "wait_max": 2.0},
                
                # Step 2: Lingua - click combo
                {"type": "click_area", "area": "language_combo", "wait_min": 0.5, "wait_max": 1.0},
                
                # Step 3: Lingua - select English
                {"type": "click_area", "area": "english_option", "wait_min": 0.3, "wait_max": 0.8},
                
                # Step 4: Titolo del libro
                {"type": "click_area", "area": "book_title_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['title'], "wait_min": 0.5, "wait_max": 1.2},
                
                # Step 5: Scroll verso il basso
                {"type": "scroll_down", "wait_min": 0.5, "wait_max": 1.0},
                
                # Step 6: Nome autore
                {"type": "click_area", "area": "author_first_name_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['author_first_name'], "wait_min": 0.5, "wait_max": 1.2},
                
                # Step 7: Cognome autore
                {"type": "click_area", "area": "author_last_name_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['author_last_name'], "wait_min": 0.5, "wait_max": 1.2},
                
                # Step 8: Descrizione
                {"type": "click_area", "area": "description_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['description'], "wait_min": 1.0, "wait_max": 2.0},

                #clicchiamo su una parte vuota dello schermo per fare scroll down
                {"type": "click_area", "area": "click_for_scroll_field", "wait_min": 0.5, "wait_max": 1.0},

                #scrolliamo verso il basso per vedere il resto
                {"type": "scroll_down", "wait_min": 0.5, "wait_max": 1.0},
                
                # Step 9: Diritti di pubblicazione
                {"type": "click_area", "area": "publishing_rights_field", "wait_min": 0.5, "wait_max": 1.0},
                
                # Step 10: Destinatari principali - No
                {"type": "click_area", "area": "main_audience_no", "wait_min": 0.5, "wait_max": 1.0},
    
                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field1", "wait_min": 0.5, "wait_max": 1.0},

                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field2", "wait_min": 0.5, "wait_max": 1.0},
                
                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field3", "wait_min": 0.5, "wait_max": 1.0},
                
                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field4", "wait_min": 0.5, "wait_max": 1.0},
                
                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field5", "wait_min": 0.5, "wait_max": 1.0},

                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field6", "wait_min": 0.5, "wait_max": 1.0},

                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field7", "wait_min": 0.5, "wait_max": 1.0},

                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field8", "wait_min": 0.5, "wait_max": 1.0},

                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field9", "wait_min": 0.5, "wait_max": 1.0},

                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field10", "wait_min": 0.5, "wait_max": 1.0},

                # Step 12: Categorie (placeholder - implementazione futura)
                {"type": "click_area", "area": "categories_field11", "wait_min": 0.5, "wait_max": 1.0},

                #scrolliamo verso il basso per vedere il resto
                {"type": "scroll_down", "wait_min": 0.5, "wait_max": 1.0},   

                # Step 11: Libro con pochi contenuti
                {"type": "click_area", "area": "low_content_book", "wait_min": 0.5, "wait_max": 1.0},
                                                        
                # Step 13: Prima parola chiave
                {"type": "click_area", "area": "keyword_1_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['keyword_1'], "wait_min": 0.5, "wait_max": 1.2},

                # Step 14: Prima parola chiave
                {"type": "click_area", "area": "keyword_2_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['keyword_2'], "wait_min": 0.5, "wait_max": 1.2},

                # Step 15: Prima parola chiave
                {"type": "click_area", "area": "keyword_3_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['keyword_3'], "wait_min": 0.5, "wait_max": 1.2},

                # Step 16: Prima parola chiave
                {"type": "click_area", "area": "keyword_4_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['keyword_4'], "wait_min": 0.5, "wait_max": 1.2},

                # Step 17: Prima parola chiave
                {"type": "click_area", "area": "keyword_5_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['keyword_5'], "wait_min": 0.5, "wait_max": 1.2},

                # Step 18: Prima parola chiave
                {"type": "click_area", "area": "keyword_6_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['keyword_6'], "wait_min": 0.5, "wait_max": 1.2},

                # Step 19: Prima parola chiave
                {"type": "click_area", "area": "keyword_7_field", "wait_min": 0.5, "wait_max": 1.0},
                {"type": "paste_text", "text": BOOK_DATA['keyword_7'], "wait_min": 0.5, "wait_max": 1.2},

                #scrolliamo verso il basso per vedere il resto
                {"type": "scroll_down", "wait_min": 0.5, "wait_max": 1.0},                

                # Step 21: Salva e continua
                {"type": "click_area", "area": "save_and_continue", "wait_min": 1.0, "wait_max": 2.0}
            ]
        }
    
    def cleanup(self):
        """Chiude il browser usando utilities"""
        if self.browser_process:
            print("🧹 Cleaning up...")
            close_browser_process(self.browser_process)

def show_configuration():
    """Mostra la configurazione corrente delle aree e dei dati statici"""
    print("\n" + "="*60)
    print("🎯 CURRENT CONFIGURATION")
    print("="*60)
    
    print(f"\n🔗 URL: {KDP_URL}")
    
    # Show screen info
    screen_center = get_screen_center()
    print(f"🖥️ Screen center: {screen_center}")
    
    print("\n🎯 CLICK AREAS:")
    for key, area in CLICK_AREAS.items():
        coords = area['coordinates']
        status = "⚠️ PLACEHOLDER" if all(coord == 0 for coord in coords) else "✅ CONFIGURED"
        print(f"   • {area['name']}: ({coords[0]}, {coords[1]}) → ({coords[2]}, {coords[3]}) {status}")
    
    print(f"\n📚 STATIC BOOK DATA:")
    print(f"   • Title: '{BOOK_DATA['title']}'")
    print(f"   • Author: {BOOK_DATA['author_first_name']} {BOOK_DATA['author_last_name']}")
    print(f"   • Keyword 1: '{BOOK_DATA['keyword_1']}'")
    print(f"   • Description: {len(BOOK_DATA['description'])} characters")
    print(f"     Preview: '{BOOK_DATA['description'][:100]}...'")
    
    print(f"\n🎬 SEQUENCE STEPS:")
    print(f"   1. Click 'Crea versione cartacea'")
    print(f"   2. Select language combo")
    print(f"   3. Choose 'English'")
    print(f"   4. Enter book title (PASTE)")
    print(f"   5. Scroll down")
    print(f"   6. Enter author first name (PASTE)")
    print(f"   7. Enter author last name (PASTE)")
    print(f"   8. Enter description (PASTE)")
    print(f"   9. Click publishing rights")
    print(f"   10. Select 'Destinatari principali - No'")
    print(f"   11. Select 'Libro con pochi contenuti'")
    print(f"   12. Click categories (placeholder)")
    print(f"   13. Enter first keyword (PASTE)")
    print(f"   14. Click 'Salva e continua'")
    
    print(f"\n🔧 TO MODIFY:")
    print(f"   • Book data: Edit BOOK_DATA dictionary (lines 90-115)")
    print(f"   • Coordinates: Edit CLICK_AREAS (lines 25-85)")
    print(f"   • Sequence: Modify get_kdp_action_sequence() method")
    
    print("\n" + "="*60)

def main():
    """Main execution function"""
    
    # Show current configuration
    show_configuration()
    
    # Ask user confirmation
    print("\n🤔 Ready to start Amazon KDP automation?")
    print("   The book data shown above will be used for publishing.")
    response = input("   Press ENTER to continue, or 'q' to quit: ").strip().lower()
    
    if response == 'q':
        print("👋 Exiting...")
        return
    
    # Warning about placeholder coordinates
    placeholder_areas = [area for area, config in CLICK_AREAS.items() 
                        if all(coord == 0 for coord in config['coordinates'])]
    
    if placeholder_areas:
        print(f"\n⚠️  WARNING: {len(placeholder_areas)} areas have placeholder coordinates!")
        print("   The automation will use screen center for these areas.")
        print("   Update coordinates in CLICK_AREAS for proper functionality.")
        confirm = input("   Continue anyway? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("👋 Exiting...")
            return
    
    # Create controller and execute
    controller = KDPController()
    
    try:
        success = controller.execute_kdp_sequence()
        
        if success:
            print("\n🎊 SUCCESS! KDP book submission completed.")
            print("   Check the KDP dashboard to verify all information.")
        else:
            print("\n💥 FAILED! Check the coordinates and sequence configuration.")
            
        # Keep browser open for inspection
        print("\n⏸️ Browser will stay open for inspection...")
        input("Press ENTER to close browser and exit...")
            
    except KeyboardInterrupt:
        print("\nℹ️ Operations interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        controller.cleanup()
        print("\n👋 Program finished!")

if __name__ == "__main__":
    main()