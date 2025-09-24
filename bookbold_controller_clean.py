"""
BookBolt Operations Controller - Clean Architecture Version 5
Uses external modules for user configuration, batch processing, and automation actions
"""

import time
import random
from typing import Dict, Any

# Import our simplified utilities
from utils.browser_utils import (
    quick_open_chrome,
    wait_for_page_load,
    close_browser_process,
    setup_pyautogui_safety
)

# Import for natural behaviors
from utils.random_helper import RandomHelper, create_casual_profile

# Import our configuration loader
from utils.config_loader import ConfigLoader, ConfigurationError

# Import our modular components
from utils.user_config_manager import UserConfigManager
from utils.batch_processor import BatchProcessor
from utils.automation_actions import AutomationActions

# =============================================================================
# CLEAN CONTROLLER VERSION 5 - FULLY MODULAR ARCHITECTURE
# =============================================================================

BOOKBOLT_URL = "https://studio.bookbolt.io/"

class BookBoltController:
    """
    Clean BookBolt Controller Version 5 with fully modular architecture.
    Uses external modules for configuration, batch processing, and automation actions.
    """
    
    def __init__(self, config_dir: str = "config"):
        """Initialize controller with all modular components."""
        try:
            # Initialize configuration systems
            self.config_loader = ConfigLoader(config_dir)
            self.user_config = UserConfigManager(config_dir)
            
            # Load configurations
            print("Configuration loading...")
            self.areas_config = self.config_loader.load_areas()
            self.sequences_config = self.config_loader.load_sequences()
            self.settings_config = self.config_loader.load_settings()
            
            # Extract working data
            self.areas = self.areas_config.get('areas', {})
            self.sequences = self.sequences_config.get('sequences', {})
            self.browser_process = None
            
            # Initialize RandomHelper
            self.random_helper = RandomHelper(create_casual_profile())
            self.random_helper.behavior_profile.mistake_proneness = 0.0
            
            # Initialize automation actions handler
            self.actions = AutomationActions(self.areas, self.random_helper, self.user_config)
            
            # Initialize batch processor
            self.batch_processor = BatchProcessor(self.user_config, self.random_helper)
            
            print("BookBolt Controller V5 initialized (Fully Modular)")
            print(f"Areas loaded: {len(self.areas)}")
            print(f"Sequences loaded: {len(self.sequences)}")
            print(f"Templates loaded: {len(self.user_config.templates)}")
            print("Human behavior profile: Casual User")
            
        except ConfigurationError as e:
            print(f"Configuration error: {e}")
            raise
        except Exception as e:
            print(f"Initialization error: {e}")
            raise
    
    def execute_single_action(self, action: Dict[str, Any]) -> bool:
        """Execute a single action using AutomationActions module."""
        try:
            action_type = action['type']
            step = action.get('step', '?')
            
            print(f"   Step {step}: {action_type}")
            
            # Pre-action hesitation
            if action_type in ['click_area', 'type_text', 'type_dynamic_text']:
                if self.random_helper.should_hesitate("normal"):
                    hesitation = self.random_helper.get_natural_pause("hesitation")
                    print(f"   Hesitation: {hesitation:.1f}s")
                    time.sleep(hesitation)
            
            # Delegate to AutomationActions based on action type
            if action_type == "click_area":
                area_name = action.get('area')
                return self.actions.click_in_area(area_name) if area_name else False
                
            elif action_type == "select_all":
                return self.actions.select_all_text()
                
            elif action_type == "type_text":
                text = action.get('text', '')
                return self.actions.type_text_naturally(text) if text else False
                
            elif action_type == "type_dynamic_text":
                return self.actions.type_dynamic_text()
                
            elif action_type == "copy_graphic":
                return self.actions.copy_graphic()
                
            elif action_type == "paste_graphic":
                return self.actions.paste_graphic()
                
            elif action_type == "wait":
                seconds = action.get('seconds', 1)
                natural_wait = seconds + random.uniform(-0.2, 0.5)
                natural_wait = max(0.1, natural_wait)
                print(f"   Wait: {natural_wait:.1f}s")
                time.sleep(natural_wait)
                return True
                
            else:
                print(f"Unknown action type: {action_type}")
                return False
                
        except Exception as e:
            print(f"Action execution failed: {e}")
            return False
    
    def execute_single_sequence(self, sequence_name: str) -> bool:
        """Execute a single sequence for current notebook."""
        try:
            if sequence_name not in self.sequences:
                print(f"Sequence '{sequence_name}' not found")
                available_sequences = list(self.sequences.keys())
                print(f"Available: {available_sequences}")
                return False
            
            sequence = self.sequences[sequence_name]
            actions = sequence.get('actions', [])
            
            print(f"Executing: {sequence['name']}")
            if self.user_config.current_notebook_number is not None:
                print(f"   Notebook: {self.user_config.current_notebook_number}")
            
            for i, action in enumerate(actions):
                print(f"\n   Action {i+1}/{len(actions)}")
                
                success = self.execute_single_action(action)
                if not success:
                    print(f"Sequence failed at action {i+1}")
                    return False
                
                # Natural wait after action
                if 'wait_min' in action and 'wait_max' in action:
                    wait_time = self.random_helper.get_click_delay(
                        action['wait_min'], action['wait_max']
                    )
                    print(f"   Post-wait: {wait_time:.2f}s")
                    time.sleep(wait_time)
            
            print(f"Sequence completed successfully")
            return True
            
        except Exception as e:
            print(f"Sequence execution failed: {e}")
            return False
    
    def execute_bookbolt_automation(self, with_user_input: bool = True, 
                                  sequence_name: str = "template_creation_workflow") -> bool:
        """Execute complete BookBolt automation using all modular components."""
        try:
            print("Starting BookBolt automation V5 (Fully Modular)...")
            print("="*60)
            
            # Step 1: User configuration via UserConfigManager
            if with_user_input:
                if not self.user_config.get_user_configuration():
                    print("User configuration cancelled")
                    return False
            
            # Step 2: Safety setup
            print("\nSetting up safety...")
            setup_pyautogui_safety()
            
            # Step 3: Open browser
            print("\nOpening browser...")
            screen_settings = self.areas_config.get('screen_settings', {})
            browser_position = screen_settings.get('browser_position', 'left')
            width_fraction = screen_settings.get('browser_width_fraction', 2/3)
            
            self.browser_process = quick_open_chrome(
                url=BOOKBOLT_URL,
                position=browser_position,
                width_fraction=width_fraction
            )
            
            if not self.browser_process:
                print("Browser failed to open")
                return False
            
            # Step 4: Page load wait
            print("Waiting for page load...")
            wait_for_page_load(10, show_progress=True)
            
            # Step 5: Execute based on configuration
            if (with_user_input and self.user_config.total_notebooks and 
                self.user_config.total_notebooks > 1):
                print(f"\nStarting batch processing via BatchProcessor...")
                success = self.batch_processor.execute_batch_processing(
                    self.execute_single_sequence, sequence_name
                )
            else:
                print(f"\nExecuting single sequence...")
                success = self.execute_single_sequence(sequence_name)
            
            if success:
                print("\nBookBolt automation completed successfully!")
            else:
                print("\nSome operations failed")
            
            return success
            
        except Exception as e:
            print(f"Automation failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources and close browser."""
        if self.browser_process:
            print("Cleaning up...")
            close_browser_process(self.browser_process)
    
    def list_available_sequences(self):
        """Display available sequences."""
        print("\nAvailable Sequences:")
        for seq_name, seq_data in self.sequences.items():
            actions_count = len(seq_data.get('actions', []))
            print(f"   • {seq_name}: {seq_data['name']} ({actions_count} actions)")
    
    def list_available_templates(self):
        """Display available templates via UserConfigManager."""
        print("\nAvailable Templates:")
        for key, template in self.user_config.templates.items():
            template_id = template.get('id', '?')
            print(f"   {template_id}. {template['name']}")
            print(f"      Format: '{template['prefix']} [NUMBER] {template['suffix']}'")

def main():
    """Main execution function for V5."""
    
    try:
        # Create V5 controller
        controller = BookBoltController()
        
        print("\n" + "="*60)
        print("BOOKBOLT CONTROLLER V5 - FULLY MODULAR ARCHITECTURE")
        print("="*60)
        print(f"URL: {BOOKBOLT_URL}")
        print(f"Areas: {len(controller.areas)}")
        print(f"Sequences: {len(controller.sequences)}")
        print(f"Templates: {len(controller.user_config.templates)}")
        print("\nMODULAR COMPONENTS:")
        print("   • UserConfigManager: Template selection & user input")
        print("   • BatchProcessor: Multi-notebook execution with summaries")
        print("   • AutomationActions: All click, type, copy/paste actions")
        print("   • ConfigLoader: JSON configuration management")
        
        print("\nChoose an option:")
        print("   1. Full automation with user input (batch processing)")
        print("   2. Single sequence (no user input)")
        print("   3. List templates and sequences")
        print("   q. Quit")
        
        choice = input("\nEnter choice (1-3 or q): ").strip()
        
        if choice == 'q':
            print("Exiting...")
            return
        elif choice == '3':
            controller.list_available_templates()
            controller.list_available_sequences()
            return
        
        # Execute automation
        with_user_input = choice == '1'
        success = controller.execute_bookbolt_automation(with_user_input)
        
        if success:
            print("\nSUCCESS! V5 automation completed.")
        else:
            print("\nFAILED! Check logs above.")
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except ConfigurationError as e:
        print(f"\nConfiguration error: {e}")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        if 'controller' in locals():
            controller.cleanup()
        print("\nV5 program finished!")

if __name__ == "__main__":
    main()