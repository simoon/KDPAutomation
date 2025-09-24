"""
Keywords Search Operations Controller - Text Operations with Natural Behaviors
Specialized controller for keyword research and text manipulation operations
"""

import time
import random
import platform
import pyautogui

# Import our simplified utilities
from utils.browser_utils import (
    quick_open_chrome,
    wait_for_page_load,
    close_browser_process,
    setup_pyautogui_safety,
    get_screen_center
)

# Import for natural behaviors
from utils.random_helper import RandomHelper, create_casual_profile

# Import configurations from separate file
from config.keywords_config import (
    CLICK_AREAS,
    ACTION_SEQUENCES,
    DEFAULT_URL,
    BROWSER_CONFIG,
    get_available_sequences,
    get_available_areas,
    validate_sequence,
    validate_area,
    get_sequence_info
)

# =============================================================================

class KeywordsSearchController:
    """
    Advanced controller for keyword research operations with natural timing and human behaviors
    """
    
    def __init__(self):
        self.browser_process = None
        self.clipboard_content = ""
        
        # Initialize RandomHelper with casual behavioral profile
        self.random_helper = RandomHelper(create_casual_profile())
        self.random_helper.behavior_profile.mistake_proneness = 0.0  # Disable errors for reliability
        
        print("🔍 Keywords Search Controller initialized")
        print("🧠 Human behavior profile: Casual User (Errors DISABLED)")
        print("📝 Specialized in text operations and keyword research")
    
    def click_in_area(self, area_config, area_name="", click_type="single"):
        """
        Click in a random point within the specified area with different click types
        
        Args:
            area_config: Dict with 'coordinates' (x1, y1, x2, y2)
            area_name: Descriptive name of the area
            click_type: Type of click - 'single', 'double', 'triple'
        """
        try:
            coords = area_config['coordinates']
            x1, y1, x2, y2 = coords
            
            # Ensure coordinates are in correct order
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            
            # Generate random point in area
            click_x = random.randint(min_x, max_x)
            click_y = random.randint(min_y, max_y)
            
            print(f"🎯 {click_type.capitalize()} clicking in {area_name}")
            print(f"   • Area: ({min_x}, {min_y}) to ({max_x}, {max_y})")
            print(f"   • Click point: ({click_x}, {click_y})")
            
            # Move to position with natural timing
            move_duration = self.random_helper.get_click_delay(0.3, 0.8)
            pyautogui.moveTo(click_x, click_y, duration=move_duration)
            
            # Small pause before clicking
            pre_click_pause = self.random_helper.get_click_delay(0.1, 0.3)
            time.sleep(pre_click_pause)
            
            # Execute click based on type
            if click_type == "double":
                pyautogui.doubleClick()
                print(f"✅ Double-clicked successfully in {area_name}")
            elif click_type == "triple":
                pyautogui.tripleClick()
                print(f"✅ Triple-clicked successfully in {area_name}")
            else:
                pyautogui.click()
                print(f"✅ Single-clicked successfully in {area_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ {click_type.capitalize()} click failed in {area_name}: {e}")
            return False
    
    def select_all_text(self):
        """
        Select all text (Ctrl+A or Cmd+A)
        """
        try:
            print("📋 Selecting all text...")
            if platform.system() == "Darwin":  # macOS
                pyautogui.hotkey('cmd', 'a')
            else:  # Windows/Linux
                pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.3)
            print("✅ Select all executed")
            return True
        except Exception as e:
            print(f"❌ Select all failed: {e}")
            return False
    
    def clear_field(self):
        """
        Clear current field by selecting all and deleting
        """
        try:
            print("🧹 Clearing field...")
            self.select_all_text()
            time.sleep(0.2)
            pyautogui.press('delete')
            time.sleep(0.2)
            print("✅ Field cleared")
            return True
        except Exception as e:
            print(f"❌ Clear field failed: {e}")
            return False
    
    def copy_text(self):
        """
        Copy selected text to clipboard
        """
        try:
            print("📄 Copying text to clipboard...")
            if platform.system() == "Darwin":  # macOS
                pyautogui.hotkey('cmd', 'c')
            else:  # Windows/Linux
                pyautogui.hotkey('ctrl', 'c')
            
            # Small delay to ensure copy operation completes
            time.sleep(0.5)
            print("✅ Text copied to clipboard")
            return True
        except Exception as e:
            print(f"❌ Copy text failed: {e}")
            return False
    
    def paste_text(self):
        """
        Paste text from clipboard
        """
        try:
            print("📝 Pasting text from clipboard...")
            if platform.system() == "Darwin":  # macOS
                pyautogui.hotkey('cmd', 'v')
            else:  # Windows/Linux
                pyautogui.hotkey('ctrl', 'v')
            
            time.sleep(0.3)
            print("✅ Text pasted successfully")
            return True
        except Exception as e:
            print(f"❌ Paste text failed: {e}")
            return False
    
    def select_word(self, area_config, area_name=""):
        """
        Double-click to select a word in the specified area
        """
        try:
            print(f"🔤 Selecting word in {area_name}")
            return self.click_in_area(area_config, area_name, "double")
        except Exception as e:
            print(f"❌ Word selection failed in {area_name}: {e}")
            return False
    
    def select_paragraph(self, area_config, area_name=""):
        """
        Triple-click to select a paragraph in the specified area
        """
        try:
            print(f"📄 Selecting paragraph in {area_name}")
            return self.click_in_area(area_config, area_name, "triple")
        except Exception as e:
            print(f"❌ Paragraph selection failed in {area_name}: {e}")
            return False
    
    def press_key(self, key):
        """
        Press a specific key
        
        Args:
            key: Key to press (e.g., 'enter', 'tab', 'escape')
        """
        try:
            print(f"⌨️ Pressing key: {key}")
            pyautogui.press(key)
            
            # Natural delay after key press
            key_delay = self.random_helper.get_typing_delay()
            time.sleep(key_delay)
            
            print(f"✅ Key '{key}' pressed")
            return True
        except Exception as e:
            print(f"❌ Key press failed for '{key}': {e}")
            return False
    
    def type_text_naturally(self, text):
        """
        Type text with natural human-like timing and behavior
        
        Args:
            text: Text to type
        """
        try:
            print(f"⌨️ Typing naturally: '{text}'")
            
            for i, char in enumerate(text):
                pyautogui.write(char)
                
                # Natural delay based on character
                char_delay = self.random_helper.get_typing_delay(char=char)
                time.sleep(char_delay)
                
                # Occasional brief pauses for natural rhythm
                if i > 0 and i % 5 == 0 and random.random() < 0.3:
                    brief_pause = self.random_helper.get_word_pause(len(text))
                    time.sleep(brief_pause)
            
            print(f"✅ Typed naturally: '{text}'")
            return True
        except Exception as e:
            print(f"❌ Natural typing failed: {e}")
            return False
    
    def mouse_drag_select(self, start_area, end_area):
        """
        Perform mouse drag selection between two areas
        
        Args:
            start_area: Starting area configuration
            end_area: Ending area configuration
        """
        try:
            print("🖱️ Performing drag selection...")
            
            # Get random points in both areas
            start_coords = start_area['coordinates']
            end_coords = end_area['coordinates']
            
            start_x = random.randint(start_coords[0], start_coords[2])
            start_y = random.randint(start_coords[1], start_coords[3])
            
            end_x = random.randint(end_coords[0], end_coords[2])
            end_y = random.randint(end_coords[1], end_coords[3])
            
            print(f"   • Drag from: ({start_x}, {start_y})")
            print(f"   • Drag to: ({end_x}, {end_y})")
            
            # Move to start position
            pyautogui.moveTo(start_x, start_y, duration=0.5)
            time.sleep(0.2)
            
            # Perform drag
            pyautogui.dragTo(end_x, end_y, duration=1.0, button='left')
            time.sleep(0.3)
            
            print("✅ Drag selection completed")
            return True
            
        except Exception as e:
            print(f"❌ Drag selection failed: {e}")
            return False
    
    def execute_single_action(self, action):
        """
        Execute a single action with natural timing
        
        Args:
            action: Dict with action details
            
        Returns:
            bool: True if action succeeded
        """
        try:
            action_type = action['type']
            
            # Possibility of hesitation before action
            if action_type in ['click_area', 'type_text', 'double_click', 'triple_click']:
                if self.random_helper.should_hesitate("normal"):
                    hesitation = self.random_helper.get_natural_pause("hesitation")
                    print(f"   🤔 Pre-action hesitation: {hesitation:.1f}s")
                    time.sleep(hesitation)
            
            # Execute based on action type
            if action_type == "click_area":
                area_name = action['area']
                if area_name in CLICK_AREAS:
                    return self.click_in_area(CLICK_AREAS[area_name], CLICK_AREAS[area_name]['name'], "single")
                else:
                    print(f"❌ Area '{area_name}' not found")
                    return False
            
            elif action_type == "double_click":
                area_name = action['area']
                if area_name in CLICK_AREAS:
                    return self.click_in_area(CLICK_AREAS[area_name], CLICK_AREAS[area_name]['name'], "double")
                else:
                    print(f"❌ Area '{area_name}' not found")
                    return False
            
            elif action_type == "triple_click":
                area_name = action['area']
                if area_name in CLICK_AREAS:
                    return self.click_in_area(CLICK_AREAS[area_name], CLICK_AREAS[area_name]['name'], "triple")
                else:
                    print(f"❌ Area '{area_name}' not found")
                    return False
            
            elif action_type == "select_all":
                return self.select_all_text()
            
            elif action_type == "clear_field":
                return self.clear_field()
            
            elif action_type == "copy_text":
                return self.copy_text()
            
            elif action_type == "paste_text":
                return self.paste_text()
            
            elif action_type == "select_word":
                area_name = action['area']
                if area_name in CLICK_AREAS:
                    return self.select_word(CLICK_AREAS[area_name], CLICK_AREAS[area_name]['name'])
                else:
                    print(f"❌ Area '{area_name}' not found")
                    return False
            
            elif action_type == "select_paragraph":
                area_name = action['area']
                if area_name in CLICK_AREAS:
                    return self.select_paragraph(CLICK_AREAS[area_name], CLICK_AREAS[area_name]['name'])
                else:
                    print(f"❌ Area '{area_name}' not found")
                    return False
            
            elif action_type == "type_text":
                text = action['text']
                return self.type_text_naturally(text)
            
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
            
            elif action_type == "drag_select":
                start_area = action.get('start_area')
                end_area = action.get('end_area')
                if start_area and end_area and start_area in CLICK_AREAS and end_area in CLICK_AREAS:
                    return self.mouse_drag_select(CLICK_AREAS[start_area], CLICK_AREAS[end_area])
                else:
                    print(f"❌ Invalid drag areas: {start_area} -> {end_area}")
                    return False
            
            else:
                print(f"❌ Unknown action type: {action_type}")
                return False
                
        except Exception as e:
            print(f"❌ Action execution failed: {e}")
            return False
    
    def execute_action_sequence(self, sequence_name):
        """
        Execute a defined action sequence
        
        Args:
            sequence_name: Name of the sequence to execute
            
        Returns:
            bool: True if sequence completed successfully
        """
        try:
            # Validate sequence first
            is_valid, message = validate_sequence(sequence_name)
            if not is_valid:
                print(f"❌ {message}")
                return False
            
            sequence = ACTION_SEQUENCES[sequence_name]
            print(f"🎬 Executing sequence: {sequence['name']}")
            print(f"   Actions: {len(sequence['actions'])}")
            
            for i, action in enumerate(sequence['actions']):
                print(f"\n   📍 Step {i+1}/{len(sequence['actions'])}: {action['type']}")
                
                # Execute the action
                success = self.execute_single_action(action)
                if not success:
                    print(f"❌ Sequence failed at step {i+1}")
                    return False
                
                # Natural wait after action if specified
                if 'wait_min' in action and 'wait_max' in action:
                    wait_time = self.random_helper.get_click_delay(action['wait_min'], action['wait_max'])
                    print(f"   ⏸️ Natural wait: {wait_time:.2f}s (range: {action['wait_min']}-{action['wait_max']})")
                    time.sleep(wait_time)
                elif 'wait' in action:
                    # Fallback for old format
                    wait_time = action['wait'] + random.uniform(-0.2, 0.3)
                    wait_time = max(0.1, wait_time)
                    print(f"   ⏸️ Natural wait: {wait_time:.2f}s")
                    time.sleep(wait_time)
            
            print(f"✅ Sequence '{sequence['name']}' completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Sequence execution failed: {e}")
            return False
    
    def list_available_sequences(self):
        """Show all available sequences"""
        print("\n🎬 Available Action Sequences:")
        for seq_name in get_available_sequences():
            seq_info = get_sequence_info(seq_name)
            if seq_info:
                print(f"   • {seq_name}: {seq_info['name']} ({seq_info['action_count']} actions)")
                if seq_info.get('description'):
                    print(f"     {seq_info['description']}")
    
    def list_available_areas(self):
        """Show all available click areas"""
        print("\n🎯 Available Click Areas:")
        for area_name in get_available_areas():
            area = CLICK_AREAS[area_name]
            coords = area['coordinates']
            print(f"   • {area_name}: {area['name']}")
            print(f"     Coordinates: ({coords[0]}, {coords[1]}) → ({coords[2]}, {coords[3]})")
            print(f"     {area['description']}")
    
    def execute_keywords_search_workflow(self, url=None, sequences=None):
        """
        Execute complete keywords search workflow using Action Sequences
        
        Args:
            url: Target URL (defaults to config default)
            sequences: List of sequences to execute (defaults to basic workflow)
        """
        try:
            print("🔍 Starting Keywords Search operations with Action Sequences...")
            print("="*60)
            
            # Step 1: Setup pyautogui safety
            print("🔧 Setting up safety configurations...")
            setup_pyautogui_safety()
            
            # Step 2: Open browser using configuration
            target_url = url or DEFAULT_URL
            print("🌐 Opening positioned browser...")
            self.browser_process = quick_open_chrome(
                url=target_url,
                position=BROWSER_CONFIG["position"],
                width_fraction=BROWSER_CONFIG["width_fraction"]
            )
            
            if not self.browser_process:
                print("❌ Failed to open browser")
                return False
            
            # Step 3: Wait for loading
            print("⏳ Waiting for page load...")
            wait_for_page_load(BROWSER_CONFIG["page_load_timeout"], show_progress=True)
            
            # Step 4: Show available sequences if none specified
            if not sequences:
                self.list_available_sequences()
                sequences = ["basic_search", "text_selection_copy"]  # Default workflow
            
            # Step 5: Execute specified sequences
            for i, sequence_name in enumerate(sequences):
                print(f"\n🎬 Step {i+1}: Executing sequence '{sequence_name}'")
                
                if not self.execute_action_sequence(sequence_name):
                    print(f"❌ Failed at sequence '{sequence_name}'")
                    return False
                
                # Brief pause between sequences
                if i < len(sequences) - 1:
                    inter_sequence_pause = self.random_helper.get_click_delay(2.0, 4.0)
                    print(f"⏳ Inter-sequence pause: {inter_sequence_pause:.1f}s")
                    time.sleep(inter_sequence_pause)
            
            print("\n🎉 All keyword search sequences completed successfully!")
            print("✅ Keywords Search automation finished!")
            
            return True
            
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            return False
    
    def cleanup(self):
        """Close browser using utilities"""
        if self.browser_process:
            print("🧹 Cleaning up...")
            close_browser_process(self.browser_process)

def show_configuration():
    """Show current configuration of areas and sequences"""
    print("\n" + "="*60)
    print("🎯 KEYWORDS SEARCH CONFIGURATION")
    print("="*60)
    
    print(f"\n🔗 Default URL: {DEFAULT_URL}")
    
    # Show screen info
    screen_center = get_screen_center()
    print(f"🖥️ Screen center: {screen_center}")
    
    print(f"\n📍 CLICK AREAS ({len(CLICK_AREAS)} total):")
    for key, area in CLICK_AREAS.items():
        coords = area['coordinates']
        width = coords[2] - coords[0]
        height = coords[3] - coords[1]
        print(f"   • {area['name']}: ({coords[0]}, {coords[1]}) → ({coords[2]}, {coords[3]}) [{width}x{height}]")
        print(f"     {area['description']}")
    
    print(f"\n🎬 ACTION SEQUENCES ({len(ACTION_SEQUENCES)} total):")
    for seq_name, seq_data in ACTION_SEQUENCES.items():
        print(f"   • {seq_name}: {seq_data['name']} ({len(seq_data['actions'])} actions)")
        if seq_data.get('description'):
            print(f"     {seq_data['description']}")
    
    print(f"\n🌐 BROWSER SETTINGS:")
    print(f"   • Position: {BROWSER_CONFIG['position']}")
    print(f"   • Width: {BROWSER_CONFIG['width_fraction']*100:.0f}% of screen")
    print(f"   • Height: {BROWSER_CONFIG['height_fraction']*100:.0f}% of screen")
    print(f"   • Page load timeout: {BROWSER_CONFIG['page_load_timeout']}s")
    
    print(f"\n📝 SUPPORTED OPERATIONS:")
    print(f"   • Single, double, triple clicks")
    print(f"   • Text selection (word, paragraph, all)")
    print(f"   • Copy and paste operations")
    print(f"   • Natural typing with human timing")
    print(f"   • Mouse drag selections")
    print(f"   • Field clearing operations")
    
    print(f"\n🔧 TO MODIFY:")
    print(f"   • Coordinates & Sequences: Edit config/keywords_config.py")
    print(f"   • Browser settings: Modify BROWSER_CONFIG")
    print(f"   • Add new operations: Update execute_single_action() method")
    
    print("\n" + "="*60)

def select_sequences_interactively():
    """Interactive sequence selection"""
    available_sequences = get_available_sequences()
    
    print("\n🎬 Select sequences to execute:")
    print("   Enter sequence numbers separated by commas (e.g., 1,3,5)")
    print("   Or press ENTER for default workflow (basic_search + text_selection_copy)")
    
    for i, seq_name in enumerate(available_sequences, 1):
        seq_info = get_sequence_info(seq_name)
        print(f"   {i}. {seq_name}: {seq_info['name']}")
    
    choice = input("\nYour choice: ").strip()
    
    if not choice:
        return ["basic_search", "text_selection_copy"]
    
    try:
        indices = [int(x.strip()) - 1 for x in choice.split(',')]
        selected_sequences = [available_sequences[i] for i in indices if 0 <= i < len(available_sequences)]
        
        if selected_sequences:
            print(f"✅ Selected sequences: {', '.join(selected_sequences)}")
            return selected_sequences
        else:
            print("❌ Invalid selection, using default workflow")
            return ["basic_search", "text_selection_copy"]
    
    except (ValueError, IndexError):
        print("❌ Invalid input format, using default workflow")
        return ["basic_search", "text_selection_copy"]

def main():
    """Main execution function"""
    
    # Show current configuration
    show_configuration()
    
    # Interactive configuration
    print("\n🤔 Configuration Options:")
    custom_url = input("   Enter custom URL (or press ENTER for default): ").strip()
    if not custom_url:
        custom_url = DEFAULT_URL
    
    # Select sequences
    selected_sequences = select_sequences_interactively()
    
    print(f"\n🎯 Configuration Summary:")
    print(f"   • URL: {custom_url}")
    print(f"   • Sequences: {', '.join(selected_sequences)}")
    
    response = input("\n   Press ENTER to continue, or 'q' to quit: ").strip().lower()
    
    if response == 'q':
        print("👋 Exiting...")
        return
    
    # Create controller and execute
    controller = KeywordsSearchController()
    
    try:
        success = controller.execute_keywords_search_workflow(custom_url, selected_sequences)
        
        if success:
            print("\n🎊 SUCCESS! All keyword search sequences completed.")
            
            # Keep browser open for inspection
            print("\n⏸️ Browser will stay open for inspection...")
            print("   Press ENTER to close browser and exit...")
            input()
        else:
            print("\n💥 FAILED! Check the coordinates and sequences.")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n⏹️ Operations interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        controller.cleanup()
        print("\n👋 Keywords Search Controller finished!")

if __name__ == "__main__":
    main()