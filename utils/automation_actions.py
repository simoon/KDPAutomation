"""
Automation Actions Module
Contains all the basic automation actions for BookBolt operations
"""

import time
import random
import platform
import pyautogui
from typing import Dict, Any

class AutomationActions:
    """
    Contains all basic automation actions like clicking, typing, copying, etc.
    """
    
    def __init__(self, areas: Dict[str, Any], random_helper, user_config_manager):
        self.areas = areas
        self.random_helper = random_helper
        self.user_config = user_config_manager
        self.is_macos = platform.system() == "Darwin"
    
    def click_in_area(self, area_name: str) -> bool:
        """Click in a random point within the specified area."""
        try:
            if area_name not in self.areas:
                print(f"❌ Area '{area_name}' not found")
                return False
            
            area_config = self.areas[area_name]
            coords = area_config['coordinates']
            x1, y1, x2, y2 = coords
            
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            
            click_x = random.randint(min_x, max_x)
            click_y = random.randint(min_y, max_y)
            
            area_name_display = area_config.get('name', area_name)
            print(f"🎯 Clicking in {area_name_display} at ({click_x}, {click_y})")
            
            pyautogui.moveTo(click_x, click_y, duration=0.8)
            time.sleep(0.3)
            pyautogui.click()
            
            print(f"✅ Click successful")
            return True
            
        except Exception as e:
            print(f"❌ Click failed in {area_name}: {e}")
            return False
    
    def select_all_text(self) -> bool:
        """Select all text using enhanced implementation."""
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
    
    def type_text_naturally(self, text: str) -> bool:
        """Type text with natural timing."""
        try:
            print(f"⌨️ Typing: '{text}'")
            
            for i, char in enumerate(text):
                pyautogui.write(char)
                char_delay = self.random_helper.get_typing_delay(char=char)
                time.sleep(char_delay)
                
                if i > 0 and i % 4 == 0 and random.random() < 0.2:
                    brief_pause = self.random_helper.get_typing_delay() * 3
                    time.sleep(brief_pause)
            
            print(f"✅ Typed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Typing failed: {e}")
            return False
    
    def type_dynamic_text(self) -> bool:
        """Type dynamically generated text using UserConfigManager."""
        try:
            text = self.user_config.generate_dynamic_text()
            
            print(f"⌨️ Typing dynamic text: '{text}'")
            print(f"📊 Notebook {self.user_config.current_notebook_number}")
            
            for i, char in enumerate(text):
                pyautogui.write(char)
                char_delay = self.random_helper.get_typing_delay(char=char)
                time.sleep(char_delay)
                
                if i > 0 and i % 8 == 0 and random.random() < 0.15:
                    brief_pause = self.random_helper.get_typing_delay() * 2
                    time.sleep(brief_pause)
            
            print(f"✅ Dynamic text typed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Dynamic text typing failed: {e}")
            return False
    
    def copy_graphic(self) -> bool:
        """Copy selected graphic element."""
        try:
            print("🎨 Copying graphic...")
            if self.is_macos:
                pyautogui.keyDown('command')
                time.sleep(0.06)
                pyautogui.press('c')
                time.sleep(0.02)
                pyautogui.keyUp('command')
            else:
                pyautogui.hotkey('ctrl', 'c', interval=0.1)
            
            time.sleep(0.5)
            print("✅ Graphic copied")
            return True
        except Exception as e:
            print(f"❌ Copy failed: {e}")
            return False
    
    def paste_graphic(self) -> bool:
        """Paste copied graphic element."""
        try:
            print("🎨 Pasting graphic...")
            if self.is_macos:
                pyautogui.keyDown('command')
                time.sleep(0.06)
                pyautogui.press('v')
                time.sleep(0.02)
                pyautogui.keyUp('command')
            else:
                pyautogui.hotkey('ctrl', 'v', interval=0.1)
            
            time.sleep(1.0)
            print("✅ Graphic pasted")
            return True
        except Exception as e:
            print(f"❌ Paste failed: {e}")
            return False