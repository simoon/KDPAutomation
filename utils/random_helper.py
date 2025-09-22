"""
Random behavior generation for human-like automation.
Provides functions to simulate natural human patterns, timing, and variations.
"""

import random
import time
import math
from typing import Tuple, List, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

class ActivityLevel(Enum):
    """Different levels of user activity"""
    TIRED = "tired"           # Slower, more pauses
    NORMAL = "normal"         # Standard behavior
    ENERGETIC = "energetic"   # Faster, more active
    FOCUSED = "focused"       # Consistent, fewer mistakes
    DISTRACTED = "distracted" # More pauses, inconsistent

class TypingStyle(Enum):
    """Different typing patterns"""
    HUNT_AND_PECK = "hunt_and_peck"     # Slow, inconsistent
    TOUCH_TYPING = "touch_typing"       # Fast, consistent
    CASUAL = "casual"                   # Average speed, some mistakes
    PROFESSIONAL = "professional"       # Fast, accurate
    MOBILE = "mobile"                   # Slower, more corrections

@dataclass
class BehaviorProfile:
    """Profile defining human behavior characteristics"""
    activity_level: ActivityLevel = ActivityLevel.NORMAL
    typing_style: TypingStyle = TypingStyle.CASUAL
    mistake_proneness: float = 0.0      # Probability of making mistakes (0.0-1.0)
    hesitation_tendency: float = 0.1     # Probability of hesitating (0.0-1.0)
    multitasking_level: float = 0.1      # Probability of pauses for "other tasks"
    attention_span: float = 0.8          # How focused the user is (0.0-1.0)
    fatigue_factor: float = 0.0          # How tired the user gets over time (0.0-1.0)
    consistency: float = 0.7             # How consistent the behavior is (0.0-1.0)

class RandomHelper:
    """
    Advanced random behavior generator for human-like automation.
    Simulates natural human patterns, timing variations, and realistic interactions.
    """
    
    def __init__(self, behavior_profile: Optional[BehaviorProfile] = None):
        self.behavior_profile = behavior_profile or BehaviorProfile()
        self.session_start = datetime.now()
        self.action_count = 0
        self.last_action_time = time.time()
        
        # Initialize random seed for reproducibility in testing
        # random.seed() - Uncomment for testing with consistent results
    
    def set_behavior_profile(self, profile: BehaviorProfile):
        """Update the current behavior profile"""
        self.behavior_profile = profile
    
    def get_current_fatigue(self) -> float:
        """Calculate current fatigue level based on session duration"""
        session_duration = (datetime.now() - self.session_start).total_seconds()
        session_hours = session_duration / 3600
        
        # Fatigue increases over time
        base_fatigue = self.behavior_profile.fatigue_factor
        time_fatigue = min(0.3, session_hours * 0.1)  # Max 30% additional fatigue
        
        return min(1.0, base_fatigue + time_fatigue)
    
    def get_attention_level(self) -> float:
        """Get current attention level (decreases with fatigue)"""
        fatigue = self.get_current_fatigue()
        base_attention = self.behavior_profile.attention_span
        
        # Attention decreases with fatigue
        current_attention = base_attention * (1 - fatigue * 0.5)
        return max(0.1, current_attention)  # Minimum 10% attention
    
    # Timing-related random functions
    
    def get_click_delay(self, min_delay: float, max_delay: float, 
                       contextual: bool = True) -> float:
        """
        Get random delay between clicks with human-like variation.
        
        Args:
            min_delay: Minimum delay in seconds
            max_delay: Maximum delay in seconds
            contextual: Whether to apply contextual modifications
            
        Returns:
            float: Delay in seconds
        """
        base_delay = random.uniform(min_delay, max_delay)
        
        if not contextual:
            return base_delay
        
        # Apply activity level modifications
        activity_multiplier = self._get_activity_multiplier()
        
        # Apply fatigue effect (tired users are slower)
        fatigue = self.get_current_fatigue()
        fatigue_multiplier = 1 + (fatigue * 0.5)  # Up to 50% slower when tired
        
        # Apply consistency variation
        if self.behavior_profile.consistency < random.random():
            # Inconsistent behavior - add more variation
            variation = random.uniform(0.5, 1.5)
            base_delay *= variation
        
        final_delay = base_delay * activity_multiplier * fatigue_multiplier
        
        # Ensure minimum and maximum bounds
        return max(min_delay, min(max_delay * 2, final_delay))
    
    def get_typing_delay(self, base_min: float = 0.05, base_max: float = 0.15, 
                        char: Optional[str] = None) -> float:
        """
        Get random delay between keystrokes with typing style consideration.
        
        Args:
            base_min: Base minimum delay
            base_max: Base maximum delay
            char: Current character being typed (for context)
            
        Returns:
            float: Delay in seconds
        """
        # Get base delay range based on typing style
        min_delay, max_delay = self._get_typing_style_delays(base_min, base_max)
        
        # Character-specific adjustments
        if char:
            if char in ' \n\t':  # Space or newlines
                max_delay *= 1.5  # Slight pause at word boundaries
            elif char in '.,!?;:':  # Punctuation
                max_delay *= 1.3  # Pause at punctuation
            elif char.isupper():  # Capital letters
                max_delay *= 1.1  # Slight pause for shift key
            elif char.isdigit():  # Numbers
                max_delay *= 1.2  # Numbers often require more thought
        
        base_delay = random.uniform(min_delay, max_delay)
        
        # Apply activity and fatigue effects
        activity_multiplier = self._get_activity_multiplier()
        fatigue = self.get_current_fatigue()
        fatigue_multiplier = 1 + (fatigue * 0.7)  # Typing is more affected by fatigue
        
        return base_delay * activity_multiplier * fatigue_multiplier
    
    def get_word_pause(self, word_length: int = 5) -> float:
        """
        Get pause duration between words based on word complexity.
        
        Args:
            word_length: Length of the word (affects thinking time)
            
        Returns:
            float: Pause duration in seconds
        """
        # Base pause increases with word length
        base_pause = 0.1 + (word_length * 0.02)
        
        # Random variation
        pause_variation = random.uniform(0.8, 1.5)
        
        # Activity level effect
        activity_multiplier = self._get_activity_multiplier()
        
        # Attention level effect (distracted users pause more)
        attention = self.get_attention_level()
        attention_multiplier = 2 - attention  # Less attention = more pauses
        
        final_pause = base_pause * pause_variation * activity_multiplier * attention_multiplier
        
        return max(0.05, min(1.0, final_pause))  # Clamp between 50ms and 1s
    
    def get_reading_pause(self, text_length: int) -> float:
        """
        Get pause duration for "reading" text before interacting.
        
        Args:
            text_length: Length of text to "read"
            
        Returns:
            float: Reading pause in seconds
        """
        # Average reading speed: 200-300 words per minute
        # Assume average word length of 5 characters
        words = max(1, text_length // 5)
        
        # Base reading time (250 words per minute)
        base_reading_time = (words / 250) * 60
        
        # Add human variation and scanning time
        scanning_time = random.uniform(0.5, 2.0)  # Initial scan
        variation_multiplier = random.uniform(0.5, 1.5)
        
        # Activity and attention effects
        activity_multiplier = self._get_activity_multiplier()
        attention = self.get_attention_level()
        
        # Lower attention = longer reading time
        attention_multiplier = 1.5 - (attention * 0.5)
        
        total_time = (base_reading_time + scanning_time) * variation_multiplier
        total_time *= activity_multiplier * attention_multiplier
        
        return max(1.0, min(30.0, total_time))  # Clamp between 1s and 30s
    
    def get_natural_pause(self, context: str = "general") -> float:
        """
        Get natural pause duration that humans might make.
        
        Args:
            context: Context for the pause (thinking, distracted, etc.)
            
        Returns:
            float: Pause duration in seconds
        """
        base_pauses = {
            "thinking": (1.0, 4.0),
            "distracted": (2.0, 8.0),
            "hesitation": (0.5, 2.0),
            "multitask": (3.0, 15.0),
            "fatigue": (1.0, 5.0),
            "general": (0.5, 2.0)
        }
        
        min_pause, max_pause = base_pauses.get(context, base_pauses["general"])
        base_pause = random.uniform(min_pause, max_pause)
        
        # Apply behavior modifiers
        activity_multiplier = self._get_activity_multiplier()
        
        # Fatigue makes pauses longer
        fatigue = self.get_current_fatigue()
        if context == "fatigue":
            fatigue_multiplier = 1 + fatigue
        else:
            fatigue_multiplier = 1 + (fatigue * 0.3)
        
        return base_pause * activity_multiplier * fatigue_multiplier
    
    # Decision-making random functions
    
    def should_make_typing_mistake(self, difficulty_factor: float = 1.0) -> bool:
        """
        Decide if a typing mistake should occur.
        
        Args:
            difficulty_factor: Multiplier for mistake probability
            
        Returns:
            bool: True if mistake should be made
        """
        base_probability = self.behavior_profile.mistake_proneness
        
        # Adjust for fatigue (tired users make more mistakes)
        fatigue = self.get_current_fatigue()
        fatigue_factor = 1 + (fatigue * 2)  # Up to 3x more mistakes when tired
        
        # Adjust for attention (distracted users make more mistakes)
        attention = self.get_attention_level()
        attention_factor = 1.5 - (attention * 0.5)
        
        # Typing style factor
        style_factor = self._get_typing_style_mistake_factor()
        
        final_probability = (base_probability * difficulty_factor * 
                           fatigue_factor * attention_factor * style_factor)
        
        return random.random() < min(0.2, final_probability)  # Cap at 20%
    
    def should_hesitate(self, complexity: str = "normal") -> bool:
        """
        Decide if user should hesitate before action.
        
        Args:
            complexity: Action complexity (simple, normal, complex)
            
        Returns:
            bool: True if hesitation should occur
        """
        base_probability = self.behavior_profile.hesitation_tendency
        
        complexity_multipliers = {
            "simple": 0.5,
            "normal": 1.0,
            "complex": 2.0,
            "very_complex": 3.0
        }
        
        complexity_factor = complexity_multipliers.get(complexity, 1.0)
        
        # Fatigue increases hesitation
        fatigue = self.get_current_fatigue()
        fatigue_factor = 1 + fatigue
        
        # Lower attention increases hesitation
        attention = self.get_attention_level()
        attention_factor = 1.5 - (attention * 0.5)
        
        final_probability = (base_probability * complexity_factor * 
                           fatigue_factor * attention_factor)
        
        return random.random() < min(0.4, final_probability)  # Cap at 40%
    
    def should_take_break(self) -> bool:
        """
        Decide if user should take a multitasking break.
        
        Returns:
            bool: True if break should be taken
        """
        base_probability = self.behavior_profile.multitasking_level
        
        # Increase probability with session duration
        session_minutes = (datetime.now() - self.session_start).total_seconds() / 60
        time_factor = 1 + (session_minutes / 60)  # Increases every hour
        
        # Activity level effect
        activity_multiplier = self._get_activity_multiplier()
        if self.behavior_profile.activity_level == ActivityLevel.DISTRACTED:
            activity_multiplier *= 3
        
        final_probability = base_probability * time_factor * activity_multiplier
        
        return random.random() < min(0.3, final_probability)  # Cap at 30%
    
    def should_double_check(self) -> bool:
        """Decide if user should double-check their action"""
        # Focused users double-check more often
        if self.behavior_profile.activity_level == ActivityLevel.FOCUSED:
            return random.random() < 0.3
        elif self.behavior_profile.activity_level == ActivityLevel.DISTRACTED:
            return random.random() < 0.05
        else:
            return random.random() < 0.15
    
    # Movement and interaction randomization
    
    def get_mouse_movement_variation(self, base_x: int, base_y: int, 
                                   max_variation: int = 3) -> Tuple[int, int]:
        """
        Add small random variation to mouse coordinates.
        
        Args:
            base_x: Base X coordinate
            base_y: Base Y coordinate
            max_variation: Maximum pixel variation
            
        Returns:
            Tuple[int, int]: Varied coordinates
        """
        # Use Gaussian distribution for more natural variation
        std_dev = max_variation / 3  # 99.7% within max_variation
        
        var_x = int(random.gauss(0, std_dev))
        var_y = int(random.gauss(0, std_dev))
        
        # Clamp to max_variation
        var_x = max(-max_variation, min(max_variation, var_x))
        var_y = max(-max_variation, min(max_variation, var_y))
        
        # Apply consistency factor
        if self.behavior_profile.consistency < random.random():
            # Inconsistent user - larger variation
            var_x = int(var_x * random.uniform(1.5, 2.0))
            var_y = int(var_y * random.uniform(1.5, 2.0))
        
        return base_x + var_x, base_y + var_y
    
    def get_scroll_amount(self, base_amount: int = 3) -> int:
        """
        Get random scroll amount with human-like variation.
        
        Args:
            base_amount: Base scroll amount
            
        Returns:
            int: Varied scroll amount
        """
        # Random variation
        variation = random.choice([-1, 0, 1])
        varied_amount = base_amount + variation
        
        # Activity level effect
        if self.behavior_profile.activity_level == ActivityLevel.ENERGETIC:
            varied_amount = int(varied_amount * random.uniform(1.2, 1.8))
        elif self.behavior_profile.activity_level == ActivityLevel.TIRED:
            varied_amount = max(1, int(varied_amount * random.uniform(0.5, 0.8)))
        
        return max(1, varied_amount)
    
    def get_drag_duration(self, distance: float) -> float:
        """
        Get drag duration based on distance and user behavior.
        
        Args:
            distance: Distance to drag in pixels
            
        Returns:
            float: Drag duration in seconds
        """
        # Base duration: longer distances take more time
        base_duration = 0.5 + (distance / 500)  # ~500 pixels per second
        
        # Activity level adjustments
        activity_multiplier = self._get_activity_multiplier()
        
        # Add natural variation
        variation = random.uniform(0.8, 1.3)
        
        final_duration = base_duration * activity_multiplier * variation
        
        return max(0.2, min(5.0, final_duration))  # Clamp between 0.2s and 5s
    
    # Helper methods for internal calculations
    
    def _get_activity_multiplier(self) -> float:
        """Get timing multiplier based on activity level"""
        multipliers = {
            ActivityLevel.TIRED: random.uniform(1.3, 1.8),      # 30-80% slower
            ActivityLevel.NORMAL: random.uniform(0.9, 1.1),     # ±10% variation
            ActivityLevel.ENERGETIC: random.uniform(0.6, 0.9),  # 10-40% faster
            ActivityLevel.FOCUSED: random.uniform(0.8, 1.0),    # Slightly faster
            ActivityLevel.DISTRACTED: random.uniform(1.1, 1.6)  # 10-60% slower
        }
        
        return multipliers.get(self.behavior_profile.activity_level, 1.0)
    
    def _get_typing_style_delays(self, base_min: float, base_max: float) -> Tuple[float, float]:
        """Get typing delays based on typing style"""
        style_multipliers = {
            TypingStyle.HUNT_AND_PECK: (2.0, 3.0),    # Much slower
            TypingStyle.TOUCH_TYPING: (0.3, 0.6),     # Much faster
            TypingStyle.CASUAL: (1.0, 1.0),           # Base speed
            TypingStyle.PROFESSIONAL: (0.4, 0.7),     # Fast and consistent
            TypingStyle.MOBILE: (1.5, 2.2)            # Slower, like mobile typing
        }
        
        min_mult, max_mult = style_multipliers.get(
            self.behavior_profile.typing_style, (1.0, 1.0)
        )
        
        return base_min * min_mult, base_max * max_mult
    
    def _get_typing_style_mistake_factor(self) -> float:
        """Get mistake probability multiplier based on typing style"""
        style_factors = {
            TypingStyle.HUNT_AND_PECK: 2.0,      # More mistakes
            TypingStyle.TOUCH_TYPING: 0.3,       # Fewer mistakes
            TypingStyle.CASUAL: 1.0,             # Base rate
            TypingStyle.PROFESSIONAL: 0.2,       # Very few mistakes
            TypingStyle.MOBILE: 1.5               # More mistakes on mobile
        }
        
        return style_factors.get(self.behavior_profile.typing_style, 1.0)
    
    # Session and usage pattern methods
    
    def update_session_stats(self):
        """Update session statistics (call after each action)"""
        self.action_count += 1
        self.last_action_time = time.time()
    
    def get_session_duration(self) -> float:
        """Get current session duration in seconds"""
        return (datetime.now() - self.session_start).total_seconds()
    
    def get_actions_per_minute(self) -> float:
        """Get current actions per minute rate"""
        duration_minutes = self.get_session_duration() / 60
        if duration_minutes == 0:
            return 0
        return self.action_count / duration_minutes
    
    def simulate_human_error_correction(self) -> Dict[str, Any]:
        """
        Simulate human error correction behavior.
        
        Returns:
            Dict with error correction details
        """
        correction_types = [
            "backspace_correction",  # Delete and retype
            "select_correction",     # Select text and replace
            "click_correction",      # Click to position cursor
            "ignore_error"           # Leave the error
        ]
        
        # Probability weights based on behavior profile
        if self.behavior_profile.typing_style == TypingStyle.PROFESSIONAL:
            weights = [0.6, 0.3, 0.05, 0.05]  # Professionals correct more
        elif self.behavior_profile.typing_style == TypingStyle.HUNT_AND_PECK:
            weights = [0.8, 0.1, 0.05, 0.05]  # Hunt-and-peck users backspace more
        else:
            weights = [0.5, 0.2, 0.1, 0.2]    # Default distribution
        
        correction_type = random.choices(correction_types, weights=weights)[0]
        
        return {
            "type": correction_type,
            "delay_before": self.get_typing_delay() * random.uniform(1.5, 3.0),
            "correction_speed": random.uniform(0.8, 1.2),
            "hesitation": self.should_hesitate("simple")
        }
    
    def get_break_duration(self, break_type: str = "short") -> float:
        """
        Get duration for different types of breaks.
        
        Args:
            break_type: Type of break (short, medium, long, distraction)
            
        Returns:
            float: Break duration in seconds
        """
        break_durations = {
            "micro": (1, 5),        # Quick pause
            "short": (5, 15),       # Brief distraction
            "medium": (15, 60),     # Moderate break
            "long": (60, 300),      # Extended break
            "distraction": (2, 30)  # Random distraction
        }
        
        min_dur, max_dur = break_durations.get(break_type, break_durations["short"])
        base_duration = random.uniform(min_dur, max_dur)
        
        # Activity level adjustments
        if self.behavior_profile.activity_level == ActivityLevel.DISTRACTED:
            base_duration *= random.uniform(1.5, 2.0)
        elif self.behavior_profile.activity_level == ActivityLevel.FOCUSED:
            base_duration *= random.uniform(0.3, 0.7)
        
        return base_duration

# Convenience functions for common operations
def create_tired_profile() -> BehaviorProfile:
    """Create behavior profile for a tired user"""
    return BehaviorProfile(
        activity_level=ActivityLevel.TIRED,
        typing_style=TypingStyle.CASUAL,
        mistake_proneness=0.0,
        hesitation_tendency=0.2,
        multitasking_level=0.15,
        attention_span=0.6,
        fatigue_factor=0.3,
        consistency=0.5
    )

def create_focused_profile() -> BehaviorProfile:
    """Create behavior profile for a focused user"""
    return BehaviorProfile(
        activity_level=ActivityLevel.FOCUSED,
        typing_style=TypingStyle.PROFESSIONAL,
        mistake_proneness=0.0,
        hesitation_tendency=0.05,
        multitasking_level=0.02,
        attention_span=0.95,
        fatigue_factor=0.1,
        consistency=0.9
    )

def create_casual_profile() -> BehaviorProfile:
    """Create behavior profile for a casual user"""
    return BehaviorProfile(
        activity_level=ActivityLevel.NORMAL,
        typing_style=TypingStyle.CASUAL,
        mistake_proneness=0.0,
        hesitation_tendency=0.1,
        multitasking_level=0.1,
        attention_span=0.8,
        fatigue_factor=0.15,
        consistency=0.7
    )

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing random helper system...")
    
    # Test different behavior profiles
    profiles = {
        "Tired User": create_tired_profile(),
        "Focused User": create_focused_profile(),
        "Casual User": create_casual_profile()
    }
    
    for profile_name, profile in profiles.items():
        print(f"\n👤 Testing {profile_name}:")
        helper = RandomHelper(profile)
        
        # Test timing functions
        click_delay = helper.get_click_delay(0.1, 0.5)
        typing_delay = helper.get_typing_delay(char='a')
        reading_pause = helper.get_reading_pause(50)
        
        print(f"  🖱️  Click delay: {click_delay:.3f}s")
        print(f"  ⌨️  Typing delay: {typing_delay:.3f}s")
        print(f"  📖 Reading pause: {reading_pause:.1f}s")
        
        # Test decision functions
        make_mistake = helper.should_make_typing_mistake()
        should_hesitate = helper.should_hesitate("complex")
        take_break = helper.should_take_break()
        
        print(f"  ❌ Make mistake: {make_mistake}")
        print(f"  🤔 Should hesitate: {should_hesitate}")
        print(f"  ⏸️  Take break: {take_break}")
        
        # Test coordinate variation
        varied_coords = helper.get_mouse_movement_variation(500, 300, 5)
        print(f"  🎯 Coordinate variation: {varied_coords}")
    
    print("\n✅ Random helper system test completed!")