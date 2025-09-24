"""
Keywords Search Configuration
Defines click areas and action sequences for keyword research operations
"""

# =============================================================================
# 🎯 CLICK AREAS CONFIGURATION
# =============================================================================

CLICK_AREAS = {
    "search_input": {
        "name": "Search Input Field",
        "coordinates": (300, 200, 600, 230),
        "description": "Main search input field area"
    },
    "search_button": {
        "name": "Search Button",
        "coordinates": (610, 200, 650, 230),
        "description": "Search button area"
    },
    "first_result": {
        "name": "First Search Result",
        "coordinates": (300, 280, 700, 320),
        "description": "First search result to select"
    },
    "second_result": {
        "name": "Second Search Result",
        "coordinates": (300, 330, 700, 370),
        "description": "Second search result to select"
    },
    "third_result": {
        "name": "Third Search Result",
        "coordinates": (300, 380, 700, 420),
        "description": "Third search result to select"
    },
    "text_selection_area": {
        "name": "Text Selection Area",
        "coordinates": (300, 350, 700, 450),
        "description": "Area containing text to select and copy"
    },
    "paste_destination": {
        "name": "Paste Destination",
        "coordinates": (300, 500, 600, 530),
        "description": "Where to paste copied text"
    },
    "filter_button": {
        "name": "Filter Button",
        "coordinates": (750, 200, 800, 230),
        "description": "Filter or advanced options button"
    },
    "results_container": {
        "name": "Results Container",
        "coordinates": (250, 280, 750, 600),
        "description": "Container with search results"
    },
    "export_button": {
        "name": "Export Button",
        "coordinates": (650, 150, 720, 180),
        "description": "Export results button"
    },
    "suggestions_dropdown": {
        "name": "Search Suggestions Dropdown",
        "coordinates": (300, 230, 600, 350),
        "description": "Dropdown with search suggestions"
    },
    "tools_menu": {
        "name": "Tools Menu",
        "coordinates": (800, 150, 900, 200),
        "description": "Tools and options menu"
    },
    "sidebar_keywords": {
        "name": "Sidebar Keywords",
        "coordinates": (50, 300, 200, 600),
        "description": "Sidebar with related keywords"
    },
    "main_content": {
        "name": "Main Content Area",
        "coordinates": (250, 250, 900, 700),
        "description": "Main content area of the page"
    },
    "secondary_input": {
        "name": "Secondary Input Field",
        "coordinates": (300, 600, 600, 630),
        "description": "Secondary input field for additional terms"
    }
}

# =============================================================================
# 🎬 ACTION SEQUENCES CONFIGURATION
# =============================================================================

ACTION_SEQUENCES = {
    "basic_search": {
        "name": "Basic Keyword Search",
        "description": "Performs a basic keyword search with natural timing",
        "actions": [
            {"type": "click_area", "area": "search_input", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "clear_field", "wait_min": 0.2, "wait_max": 0.5},
            {"type": "type_text", "text": "keyword research tools", "wait_min": 0.8, "wait_max": 1.5},
            {"type": "press_key", "key": "enter", "wait_min": 1.0, "wait_max": 2.0},
            {"type": "wait", "seconds": 2, "wait_min": 1.8, "wait_max": 2.5}
        ]
    },
    
    "text_selection_copy": {
        "name": "Select and Copy Text",
        "description": "Selects text from results and copies to destination",
        "actions": [
            {"type": "click_area", "area": "text_selection_area", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "triple_click", "area": "text_selection_area", "wait_min": 0.3, "wait_max": 0.8},
            {"type": "copy_text", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "click_area", "area": "paste_destination", "wait_min": 0.8, "wait_max": 1.5},
            {"type": "paste_text", "wait_min": 0.3, "wait_max": 0.8}
        ]
    },
    
    "advanced_text_operations": {
        "name": "Advanced Text Selection and Manipulation",
        "description": "Complex text operations with multiple selections and manipulations",
        "actions": [
            {"type": "double_click", "area": "first_result", "wait_min": 0.5, "wait_max": 1.2},
            {"type": "select_word", "area": "text_selection_area", "wait_min": 0.3, "wait_max": 0.8},
            {"type": "copy_text", "wait_min": 0.2, "wait_max": 0.5},
            {"type": "click_area", "area": "search_input", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "clear_field", "wait_min": 0.2, "wait_max": 0.4},
            {"type": "paste_text", "wait_min": 0.3, "wait_max": 0.7},
            {"type": "type_text", "text": " analysis", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "press_key", "key": "enter", "wait_min": 1.0, "wait_max": 1.8}
        ]
    },
    
    "multi_keyword_research": {
        "name": "Multiple Keywords Research",
        "description": "Researches multiple keywords and collects results",
        "actions": [
            {"type": "click_area", "area": "search_input", "wait_min": 0.3, "wait_max": 0.8},
            {"type": "clear_field", "wait_min": 0.2, "wait_max": 0.4},
            {"type": "type_text", "text": "SEO tools", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "press_key", "key": "enter", "wait_min": 1.0, "wait_max": 1.5},
            {"type": "wait", "seconds": 2, "wait_min": 1.5, "wait_max": 2.5},
            {"type": "triple_click", "area": "first_result", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "copy_text", "wait_min": 0.3, "wait_max": 0.6},
            {"type": "click_area", "area": "paste_destination", "wait_min": 0.8, "wait_max": 1.2},
            {"type": "paste_text", "wait_min": 0.3, "wait_max": 0.7}
        ]
    },
    
    "competitor_analysis": {
        "name": "Competitor Keywords Analysis",
        "description": "Analyzes competitor keywords with multiple searches",
        "actions": [
            {"type": "click_area", "area": "search_input", "wait_min": 0.4, "wait_max": 0.9},
            {"type": "clear_field", "wait_min": 0.2, "wait_max": 0.5},
            {"type": "type_text", "text": "competitor analysis tools", "wait_min": 0.8, "wait_max": 1.3},
            {"type": "press_key", "key": "enter", "wait_min": 1.0, "wait_max": 1.8},
            {"type": "wait", "seconds": 3, "wait_min": 2.5, "wait_max": 3.5},
            {"type": "click_area", "area": "first_result", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "double_click", "area": "text_selection_area", "wait_min": 0.4, "wait_max": 0.8},
            {"type": "copy_text", "wait_min": 0.3, "wait_max": 0.7},
            {"type": "click_area", "area": "secondary_input", "wait_min": 0.6, "wait_max": 1.1},
            {"type": "paste_text", "wait_min": 0.3, "wait_max": 0.6}
        ]
    },
    
    "batch_keyword_collection": {
        "name": "Batch Keyword Collection",
        "description": "Collects keywords from multiple results systematically",
        "actions": [
            {"type": "click_area", "area": "search_input", "wait_min": 0.3, "wait_max": 0.7},
            {"type": "clear_field", "wait_min": 0.2, "wait_max": 0.4},
            {"type": "type_text", "text": "digital marketing keywords", "wait_min": 0.7, "wait_max": 1.2},
            {"type": "press_key", "key": "enter", "wait_min": 1.0, "wait_max": 1.6},
            {"type": "wait", "seconds": 2, "wait_min": 1.8, "wait_max": 2.3},
            
            # Collect from first result
            {"type": "triple_click", "area": "first_result", "wait_min": 0.4, "wait_max": 0.8},
            {"type": "copy_text", "wait_min": 0.3, "wait_max": 0.6},
            {"type": "click_area", "area": "paste_destination", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "paste_text", "wait_min": 0.2, "wait_max": 0.5},
            {"type": "press_key", "key": "enter", "wait_min": 0.3, "wait_max": 0.6},
            
            # Collect from second result
            {"type": "triple_click", "area": "second_result", "wait_min": 0.4, "wait_max": 0.8},
            {"type": "copy_text", "wait_min": 0.3, "wait_max": 0.6},
            {"type": "click_area", "area": "paste_destination", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "paste_text", "wait_min": 0.2, "wait_max": 0.5},
            {"type": "press_key", "key": "enter", "wait_min": 0.3, "wait_max": 0.6},
            
            # Collect from third result
            {"type": "triple_click", "area": "third_result", "wait_min": 0.4, "wait_max": 0.8},
            {"type": "copy_text", "wait_min": 0.3, "wait_max": 0.6},
            {"type": "click_area", "area": "paste_destination", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "paste_text", "wait_min": 0.2, "wait_max": 0.5}
        ]
    },
    
    "suggestion_harvesting": {
        "name": "Search Suggestions Harvesting",
        "description": "Harvests search suggestions for keyword ideas",
        "actions": [
            {"type": "click_area", "area": "search_input", "wait_min": 0.4, "wait_max": 0.8},
            {"type": "clear_field", "wait_min": 0.2, "wait_max": 0.4},
            {"type": "type_text", "text": "how to", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "wait", "seconds": 1, "wait_min": 0.8, "wait_max": 1.3},  # Wait for suggestions
            {"type": "click_area", "area": "suggestions_dropdown", "wait_min": 0.3, "wait_max": 0.7},
            {"type": "copy_text", "wait_min": 0.3, "wait_max": 0.6},
            {"type": "click_area", "area": "paste_destination", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "paste_text", "wait_min": 0.2, "wait_max": 0.5}
        ]
    },
    
    "drag_select_operation": {
        "name": "Drag Selection Operation",
        "description": "Uses mouse drag to select text across multiple lines",
        "actions": [
            {"type": "click_area", "area": "main_content", "wait_min": 0.5, "wait_max": 1.0},
            {"type": "drag_select", "start_area": "text_selection_area", "end_area": "paste_destination", "wait_min": 0.8, "wait_max": 1.5},
            {"type": "copy_text", "wait_min": 0.4, "wait_max": 0.8},
            {"type": "click_area", "area": "secondary_input", "wait_min": 0.6, "wait_max": 1.2},
            {"type": "paste_text", "wait_min": 0.3, "wait_max": 0.7}
        ]
    },
    
    "rapid_keyword_extraction": {
        "name": "Rapid Keyword Extraction",
        "description": "Quickly extracts keywords from multiple sources",
        "actions": [
            {"type": "click_area", "area": "search_input", "wait_min": 0.2, "wait_max": 0.5},
            {"type": "type_text", "text": "content marketing", "wait_min": 0.4, "wait_max": 0.8},
            {"type": "press_key", "key": "enter", "wait_min": 0.8, "wait_max": 1.2},
            {"type": "wait", "seconds": 1, "wait_min": 0.8, "wait_max": 1.3},
            
            # Rapid extraction sequence
            {"type": "double_click", "area": "first_result", "wait_min": 0.2, "wait_max": 0.4},
            {"type": "copy_text", "wait_min": 0.1, "wait_max": 0.3},
            {"type": "click_area", "area": "paste_destination", "wait_min": 0.3, "wait_max": 0.6},
            {"type": "paste_text", "wait_min": 0.1, "wait_max": 0.3},
            {"type": "type_text", "text": ", ", "wait_min": 0.1, "wait_max": 0.2},
            
            {"type": "double_click", "area": "second_result", "wait_min": 0.2, "wait_max": 0.4},
            {"type": "copy_text", "wait_min": 0.1, "wait_max": 0.3},
            {"type": "click_area", "area": "paste_destination", "wait_min": 0.3, "wait_max": 0.6},
            {"type": "paste_text", "wait_min": 0.1, "wait_max": 0.3},
            {"type": "type_text", "text": ", ", "wait_min": 0.1, "wait_max": 0.2},
            
            {"type": "double_click", "area": "third_result", "wait_min": 0.2, "wait_max": 0.4},
            {"type": "copy_text", "wait_min": 0.1, "wait_max": 0.3},
            {"type": "click_area", "area": "paste_destination", "wait_min": 0.3, "wait_max": 0.6},
            {"type": "paste_text", "wait_min": 0.1, "wait_max": 0.3}
        ]
    }
}

# =============================================================================
# 🔧 CONFIGURATION SETTINGS
# =============================================================================

# Default URL for keyword research
DEFAULT_URL = "https://www.google.com"

# Alternative URLs for different keyword research tools
KEYWORD_RESEARCH_URLS = {
    "google": "https://www.google.com",
    "google_trends": "https://trends.google.com",
    "answer_the_public": "https://answerthepublic.com",
    "ubersuggest": "https://app.neilpatel.com/ubersuggest",
    "keyword_tool": "https://keywordtool.io",
    "semrush": "https://www.semrush.com",
    "ahrefs": "https://ahrefs.com"
}

# Browser configuration
BROWSER_CONFIG = {
    "position": "left",         # Browser position: left, right, center
    "width_fraction": 2/3,      # Fraction of screen width
    "height_fraction": 1.0,     # Fraction of screen height
    "page_load_timeout": 8      # Seconds to wait for page load
}

# Default search terms for testing
DEFAULT_SEARCH_TERMS = [
    "keyword research tools",
    "SEO optimization",
    "content marketing strategies",
    "digital marketing trends",
    "competitor analysis",
    "search engine optimization",
    "online marketing tools",
    "website traffic analysis"
]

# =============================================================================
# 🎯 VALIDATION AND UTILITY FUNCTIONS
# =============================================================================

def get_available_sequences():
    """Return list of available sequence names"""
    return list(ACTION_SEQUENCES.keys())

def get_available_areas():
    """Return list of available click area names"""
    return list(CLICK_AREAS.keys())

def validate_sequence(sequence_name):
    """Validate if sequence exists and has valid structure"""
    if sequence_name not in ACTION_SEQUENCES:
        return False, f"Sequence '{sequence_name}' not found"
    
    sequence = ACTION_SEQUENCES[sequence_name]
    
    if 'actions' not in sequence:
        return False, f"Sequence '{sequence_name}' missing 'actions' key"
    
    if not isinstance(sequence['actions'], list):
        return False, f"Sequence '{sequence_name}' actions must be a list"
    
    if len(sequence['actions']) == 0:
        return False, f"Sequence '{sequence_name}' has no actions"
    
    return True, "Valid sequence"

def validate_area(area_name):
    """Validate if click area exists and has valid coordinates"""
    if area_name not in CLICK_AREAS:
        return False, f"Area '{area_name}' not found"
    
    area = CLICK_AREAS[area_name]
    
    if 'coordinates' not in area:
        return False, f"Area '{area_name}' missing 'coordinates' key"
    
    coords = area['coordinates']
    if not isinstance(coords, (tuple, list)) or len(coords) != 4:
        return False, f"Area '{area_name}' coordinates must be tuple/list of 4 values"
    
    x1, y1, x2, y2 = coords
    if x1 >= x2 or y1 >= y2:
        return False, f"Area '{area_name}' has invalid coordinate order"
    
    return True, "Valid area"

def get_sequence_info(sequence_name):
    """Get detailed information about a sequence"""
    if sequence_name not in ACTION_SEQUENCES:
        return None
    
    sequence = ACTION_SEQUENCES[sequence_name]
    return {
        'name': sequence.get('name', sequence_name),
        'description': sequence.get('description', 'No description available'),
        'action_count': len(sequence['actions']),
        'actions': sequence['actions']
    }

def get_area_info(area_name):
    """Get detailed information about a click area"""
    if area_name not in CLICK_AREAS:
        return None
    
    area = CLICK_AREAS[area_name]
    coords = area['coordinates']
    
    return {
        'name': area.get('name', area_name),
        'description': area.get('description', 'No description available'),
        'coordinates': coords,
        'width': coords[2] - coords[0],
        'height': coords[3] - coords[1],
        'area_size': (coords[2] - coords[0]) * (coords[3] - coords[1])
    }

def list_sequences_by_category():
    """Organize sequences by functionality category"""
    categories = {
        'basic': ['basic_search'],
        'text_operations': ['text_selection_copy', 'advanced_text_operations', 'drag_select_operation'],
        'research': ['multi_keyword_research', 'competitor_analysis', 'suggestion_harvesting'],
        'batch_operations': ['batch_keyword_collection', 'rapid_keyword_extraction']
    }
    
    return categories

# =============================================================================
# 🧪 TESTING AND VALIDATION
# =============================================================================

def validate_all_configurations():
    """Validate all sequences and areas"""
    results = {
        'sequences': {},
        'areas': {},
        'summary': {'sequences_valid': 0, 'areas_valid': 0, 'total_sequences': len(ACTION_SEQUENCES), 'total_areas': len(CLICK_AREAS)}
    }
    
    # Validate sequences
    for seq_name in ACTION_SEQUENCES:
        is_valid, message = validate_sequence(seq_name)
        results['sequences'][seq_name] = {'valid': is_valid, 'message': message}
        if is_valid:
            results['summary']['sequences_valid'] += 1
    
    # Validate areas
    for area_name in CLICK_AREAS:
        is_valid, message = validate_area(area_name)
        results['areas'][area_name] = {'valid': is_valid, 'message': message}
        if is_valid:
            results['summary']['areas_valid'] += 1
    
    return results

if __name__ == "__main__":
    # Test configuration when run directly
    print("🧪 Testing Keywords Search Configuration...")
    print("="*60)
    
    # Validate all configurations
    validation_results = validate_all_configurations()
    
    print(f"📊 Validation Summary:")
    print(f"   • Sequences: {validation_results['summary']['sequences_valid']}/{validation_results['summary']['total_sequences']} valid")
    print(f"   • Areas: {validation_results['summary']['areas_valid']}/{validation_results['summary']['total_areas']} valid")
    
    print(f"\n🎬 Available Sequences:")
    for seq_name in get_available_sequences():
        info = get_sequence_info(seq_name)
        print(f"   • {seq_name}: {info['name']} ({info['action_count']} actions)")
    
    print(f"\n🎯 Available Click Areas:")
    for area_name in get_available_areas():
        info = get_area_info(area_name)
        print(f"   • {area_name}: {info['name']} [{info['width']}x{info['height']}]")
    
    print("\n✅ Configuration test completed!")