"""
User Configuration Manager for BookBolt Automation
Handles user input, template selection, and configuration management
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

class UserConfigManager:
    """
    Manages user configuration including template selection,
    start numbers, batch processing settings.
    """
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.templates = self._load_templates()
        
        # User configuration variables
        self.selected_template = None
        self.start_number = None
        self.total_notebooks = None
        self.current_notebook_number = None
        
    def _load_templates(self) -> Dict[str, Any]:
        """Load templates from JSON file"""
        try:
            template_file = self.config_dir / "bookbolt_templates.json"
            if template_file.exists():
                with open(template_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('templates', {})
        except Exception as e:
            print(f"Warning: Could not load templates: {e}")
        
        # Return default templates if file not found
        return {
            "flowers": {
                "id": 1,
                "name": "Flowers Composition Notebook College Ruled 7.5 x 9.25",
                "prefix": "Flowers",
                "suffix": "Composition Notebook College Ruled 7.5 x 9.25"
            },
            "vintage": {
                "id": 2,
                "name": "Vintage illustration Composition Notebook College Ruled 7.5 x 9.25", 
                "prefix": "Vintage illustration",
                "suffix": "Composition Notebook College Ruled 7.5 x 9.25"
            },
            "cats": {
                "id": 3,
                "name": "Cats Composition Notebook College Ruled 7.5 x 9.25",
                "prefix": "Cats", 
                "suffix": "Composition Notebook College Ruled 7.5 x 9.25"
            },
            "scientific": {
                "id": 4,
                "name": "Scientific Composition Notebook College Ruled 7.5 x 9.25",
                "prefix": "Scientific",
                "suffix": "Composition Notebook College Ruled 7.5 x 9.25"
            }
        }
    
    def get_user_configuration(self) -> bool:
        """
        Collect user configuration for template, start number, and total notebooks.
        
        Returns:
            bool: True if configuration completed successfully
        """
        try:
            print("\n" + "="*60)
            print("📋 USER CONFIGURATION")
            print("="*60)
            
            # Step 1: Template selection
            print("\n📚 STEP 1: Select Template Type")
            print("Available templates:")
            
            template_list = []
            for key, template in self.templates.items():
                template_id = template.get('id', len(template_list) + 1)
                template_list.append((key, template))
                print(f"   {template_id}. {template['name']}")
            
            if not template_list:
                print("❌ No templates available")
                return False
            
            while True:
                try:
                    template_choice = input(f"\nEnter your choice (1 to {len(template_list)}): ").strip()
                    template_num = int(template_choice)
                    
                    if 1 <= template_num <= len(template_list):
                        selected_key, selected_template = template_list[template_num - 1]
                        self.selected_template = selected_template
                        print(f"✅ Selected: {self.selected_template['name']}")
                        break
                    else:
                        print(f"❌ Invalid choice. Please enter 1 to {len(template_list)}.")
                        
                except ValueError:
                    print("❌ Invalid input. Please enter a number.")
            
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
            print(f"   • End Number: {self.start_number + self.total_notebooks - 1}")
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
    
    def generate_dynamic_text(self) -> str:
        """
        Generate dynamic text based on current configuration.
        
        Returns:
            str: Generated text with template and current number
        """
        if not self.selected_template or self.current_notebook_number is None:
            return "Default Text"
        
        # Format: "Prefix" + number + "Suffix"
        dynamic_text = f"{self.selected_template['prefix']} {self.current_notebook_number} {self.selected_template['suffix']}"
        return dynamic_text
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get current configuration as dictionary"""
        return {
            'template': self.selected_template,
            'start_number': self.start_number,
            'total_notebooks': self.total_notebooks,
            'current_number': self.current_notebook_number,
            'end_number': self.start_number + self.total_notebooks - 1 if self.start_number and self.total_notebooks else None
        }