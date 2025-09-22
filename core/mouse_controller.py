"""
Advanced mouse controller with anti-detection capabilities.
Provides natural mouse movements, area-based clicking, and human-like behavior patterns.
"""

import time
import random
import math
from typing import Tuple, List, Optional, Dict, Any
from dataclasses import dataclass

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️  pyautogui not available. Mouse operations will be simulated.")

from utils.coordinate_helper import CoordinateHelper, Point, Rectangle
from utils.random_helper import RandomHelper, BehaviorProfile
from utils.logger import get_logger, log_mouse, log_action, log_detection

@dataclass
class MouseState:
    """Tracks current mouse state and statistics"""
    current_position: Point = None
    last_click_time: float = 0.0
    last_move_time: float = 0.0
    total_clicks: int = 0
    total_moves: int = 0
    session_start: float = 0.0
    is_dragging: bool = False
    last_drag_end: float = 0.0

class MouseController:
    """
    Advanced mouse controller with natural movements and anti-detection features.
    Simulates human-like mouse behavior with randomization and natural patterns.
    """
    
    def __init__(self, settings, behavior_profile: Optional[BehaviorProfile] = None):
        self.settings = settings
        self.coordinate_helper = CoordinateHelper()
        self.random_helper = RandomHelper(behavior_profile)
        self.logger = get_logger("mouse")
        
        # Initialize mouse state
        self.state = MouseState()
        self.state.session_start = time.time()
        
        # Configure pyautogui if available
        if PYAUTOGUI_AVAILABLE:
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.0  # We handle our own delays
            
            # Get current mouse position
            try:
                current_pos = pyautogui.position()
                self.state.current_position = Point(current_pos.x, current_pos.y)
            except Exception:
                self.state.current_position = self.coordinate_helper.get_screen_center()
        else:
            self.state.current_position = self.coordinate_helper.get_screen_center()
        
        # Screen dimensions
        self.screen_width, self.screen_height = self.coordinate_helper.get_screen_size()
        
        log_detection("mouse_controller_init", f"Screen: {self.screen_width}x{self.screen_height}", "INFO")
        self.logger.info(f"🖱️  Mouse controller initialized - Screen: {self.screen_width}x{self.screen_height}")
    
    # Core clicking methods
    
    def click_at_coordinates(self, x: int, y: int, button: str = 'left', 
                           natural_approach: bool = True) -> bool:
        """
        Click at specific coordinates with natural movement and timing.
        
        Args:
            x: X coordinate to click
            y: Y coordinate to click
            button: Mouse button ('left', 'right', 'middle')
            natural_approach: Use natural movement to target
            
        Returns:
            bool: True if click was successful
        """
        try:
            target_point = Point(x, y)
            
            # Validate coordinates
            if not self.coordinate_helper.validate_point(target_point, margin=5):
                self.logger.error(f"❌ Invalid coordinates: {target_point}")
                return False
            
            # Move to target with natural approach
            if natural_approach:
                success = self._move_naturally_to_target(target_point)
                if not success:
                    self.logger.warning("⚠️  Natural movement failed, using direct movement")
                    self._move_directly_to_target(target_point)
            else:
                self._move_directly_to_target(target_point)
            
            # Pre-click pause and micro-adjustments
            self._pre_click_behavior(target_point)
            
            # Perform the actual click
            click_success = self._execute_click(target_point, button)
            
            # Post-click behavior
            self._post_click_behavior(click_success)
            
            # Update statistics
            self.state.total_clicks += 1
            self.state.last_click_time = time.time()
            
            # Log the action
            log_mouse("click", target_point.to_tuple(), f"{button} button")
            log_action("click", f"Clicked at {target_point} with {button} button", click_success)
            
            return click_success
            
        except Exception as e:
            self.logger.error(f"❌ Click failed at ({x}, {y}): {e}")
            log_action("click", f"Click failed at ({x}, {y}): {str(e)}", False)
            return False
    
    def click_in_area(self, x_range: Tuple[int, int], y_range: Tuple[int, int], 
                     button: str = 'left', safe_margin: int = 0) -> bool:
        """
        Click at random position within area - primary anti-detection method.
        
        Args:
            x_range: Tuple of (min_x, max_x) coordinates
            y_range: Tuple of (min_y, max_y) coordinates
            button: Mouse button to use
            safe_margin: Safety margin from area edges
            
        Returns:
            bool: True if click was successful
        """
        try:
            # Apply safety margin if requested
            if safe_margin > 0:
                adjusted_x_range, adjusted_y_range = self.coordinate_helper.apply_margin_to_area(
                    x_range, y_range, safe_margin
                )
            else:
                adjusted_x_range, adjusted_y_range = x_range, y_range
            
            # Get random point in area
            target_point = self.coordinate_helper.get_random_point_in_area(
                adjusted_x_range, adjusted_y_range
            )
            
            self.logger.info(f"🎯 Area click: {x_range}x{y_range} → target: {target_point}")
            log_detection("area_click", f"Area: {x_range}x{y_range}, Target: {target_point}", "INFO")
            
            return self.click_at_coordinates(target_point.x, target_point.y, button)
            
        except Exception as e:
            self.logger.error(f"❌ Area click failed {x_range}x{y_range}: {e}")
            log_action("area_click", f"Area click failed: {str(e)}", False)
            return False
    
    def double_click_at_coordinates(self, x: int, y: int) -> bool:
        """Perform double click with natural timing"""
        try:
            # First click
            if not self.click_at_coordinates(x, y, natural_approach=True):
                return False
            
            # Natural interval between clicks
            interval = self.random_helper.get_click_delay(0.05, 0.15)
            time.sleep(interval)
            
            # Second click (no movement, just click)
            click_success = self._execute_click(Point(x, y), 'left')
            
            log_action("double_click", f"Double-clicked at ({x}, {y})", click_success)
            return click_success
            
        except Exception as e:
            self.logger.error(f"❌ Double click failed at ({x}, {y}): {e}")
            return False
    
    def double_click_in_area(self, x_range: Tuple[int, int], y_range: Tuple[int, int]) -> bool:
        """Double click in random area"""
        try:
            # Get target point
            target_point = self.coordinate_helper.get_random_point_in_area(x_range, y_range)
            return self.double_click_at_coordinates(target_point.x, target_point.y)
        except Exception as e:
            self.logger.error(f"❌ Double click in area failed: {e}")
            return False
    
    def right_click_at_coordinates(self, x: int, y: int) -> bool:
        """Right click at coordinates"""
        return self.click_at_coordinates(x, y, button='right')
    
    def right_click_in_area(self, x_range: Tuple[int, int], y_range: Tuple[int, int]) -> bool:
        """Right click in area"""
        return self.click_in_area(x_range, y_range, button='right')
    
    # Movement methods
    
    def move_to_coordinates(self, x: int, y: int, natural: bool = True) -> bool:
        """
        Move mouse to coordinates.
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            natural: Use natural movement path
            
        Returns:
            bool: True if movement was successful
        """
        try:
            target_point = Point(x, y)
            
            if not self.coordinate_helper.validate_point(target_point):
                target_point = self.coordinate_helper.clamp_point(target_point)
                self.logger.warning(f"⚠️  Clamped coordinates to {target_point}")
            
            if natural and self.settings.automation.anti_detection:
                success = self._move_naturally_to_target(target_point)
            else:
                success = self._move_directly_to_target(target_point)
            
            log_mouse("move", target_point.to_tuple(), "Natural" if natural else "Direct")
            return success
            
        except Exception as e:
            self.logger.error(f"❌ Move to coordinates failed: {e}")
            return False
    
    def hover_over_area(self, x_range: Tuple[int, int], y_range: Tuple[int, int], 
                       duration: float = 1.0) -> bool:
        """
        Hover mouse over area for specified duration.
        
        Args:
            x_range: X coordinate range
            y_range: Y coordinate range  
            duration: Hover duration in seconds
            
        Returns:
            bool: True if successful
        """
        try:
            target_point = self.coordinate_helper.get_random_point_in_area(x_range, y_range)
            
            if not self.move_to_coordinates(target_point.x, target_point.y):
                return False
            
            # Hover with small movements
            hover_end_time = time.time() + duration
            
            while time.time() < hover_end_time:
                # Small random movement while hovering
                if random.random() < 0.3:  # 30% chance of micro-movement
                    offset_point = self.coordinate_helper.offset_coordinates(
                        target_point.x, target_point.y, max_offset=2
                    )
                    self._move_directly_to_target(offset_point)
                
                time.sleep(0.1)
            
            log_action("hover", f"Hovered over area for {duration:.1f}s", True)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Hover failed: {e}")
            return False
    
    def move_away_from_area(self, avoid_area: Tuple[Tuple[int, int], Tuple[int, int]], 
                          min_distance: int = 100) -> bool:
        """
        Move mouse away from specified area to look more natural.
        
        Args:
            avoid_area: ((x1, x2), (y1, y2)) area to avoid
            min_distance: Minimum distance to move away
            
        Returns:
            bool: True if successful
        """
        try:
            avoid_rect = Rectangle(avoid_area[0][0], avoid_area[1][0], 
                                 avoid_area[0][1], avoid_area[1][1])
            
            # Find safe position
            max_attempts = 10
            for _ in range(max_attempts):
                # Generate random position on screen
                target_x = random.randint(50, self.screen_width - 50)
                target_y = random.randint(50, self.screen_height - 50)
                target_point = Point(target_x, target_y)
                
                # Check if far enough from avoid area
                distance = avoid_rect.center.distance_to(target_point)
                if distance >= min_distance:
                    return self.move_to_coordinates(target_x, target_y)
            
            # Fallback: move to screen corner
            corner_x = self.screen_width - 100
            corner_y = self.screen_height - 100
            return self.move_to_coordinates(corner_x, corner_y)
            
        except Exception as e:
            self.logger.error(f"❌ Move away failed: {e}")
            return False
    
    # Drag and drop methods
    
    def drag_to_coordinates(self, start_x: int, start_y: int, end_x: int, end_y: int, 
                          duration: Optional[float] = None) -> bool:
        """
        Drag from start coordinates to end coordinates.
        
        Args:
            start_x, start_y: Starting position
            end_x, end_y: Ending position
            duration: Drag duration (auto-calculated if None)
            
        Returns:
            bool: True if successful
        """
        try:
            start_point = Point(start_x, start_y)
            end_point = Point(end_x, end_y)
            
            # Move to start position
            if not self.move_to_coordinates(start_x, start_y):
                return False
            
            # Calculate duration if not specified
            if duration is None:
                distance = start_point.distance_to(end_point)
                duration = self.random_helper.get_drag_duration(distance)
            
            # Start drag
            self.state.is_dragging = True
            drag_success = self._execute_drag(start_point, end_point, duration)
            self.state.is_dragging = False
            self.state.last_drag_end = time.time()
            
            log_action("drag", f"Dragged from {start_point} to {end_point}", drag_success)
            return drag_success
            
        except Exception as e:
            self.logger.error(f"❌ Drag failed: {e}")
            self.state.is_dragging = False
            return False
    
    def drag_in_areas(self, start_area: Tuple[Tuple[int, int], Tuple[int, int]], 
                     end_area: Tuple[Tuple[int, int], Tuple[int, int]]) -> bool:
        """
        Drag from random point in start area to random point in end area.
        
        Args:
            start_area: ((min_x, max_x), (min_y, max_y)) for start
            end_area: ((min_x, max_x), (min_y, max_y)) for end
            
        Returns:
            bool: True if successful
        """
        try:
            # Get random points in both areas
            start_point = self.coordinate_helper.get_random_point_in_area(
                start_area[0], start_area[1]
            )
            end_point = self.coordinate_helper.get_random_point_in_area(
                end_area[0], end_area[1]
            )
            
            return self.drag_to_coordinates(
                start_point.x, start_point.y, 
                end_point.x, end_point.y
            )
            
        except Exception as e:
            self.logger.error(f"❌ Drag in areas failed: {e}")
            return False
    
    # Scroll methods
    
    def scroll_vertical(self, amount: int, x: Optional[int] = None, 
                       y: Optional[int] = None) -> bool:
        """
        Scroll vertically at specified position.
        
        Args:
            amount: Scroll amount (positive = up, negative = down)
            x, y: Position to scroll at (current position if None)
            
        Returns:
            bool: True if successful
        """
        try:
            # Use current position if not specified
            if x is None or y is None:
                scroll_pos = self.get_current_position()
                x, y = scroll_pos.x, scroll_pos.y
            
            # Add natural variation to scroll amount
            varied_amount = self.random_helper.get_scroll_amount(abs(amount))
            if amount < 0:
                varied_amount = -varied_amount
            
            scroll_success = self._execute_scroll(x, y, varied_amount, horizontal=False)
            
            log_mouse("scroll", (x, y), f"Vertical: {varied_amount}")
            return scroll_success
            
        except Exception as e:
            self.logger.error(f"❌ Vertical scroll failed: {e}")
            return False
    
    def scroll_horizontal(self, amount: int, x: Optional[int] = None, 
                         y: Optional[int] = None) -> bool:
        """Scroll horizontally at specified position"""
        try:
            if x is None or y is None:
                scroll_pos = self.get_current_position()
                x, y = scroll_pos.x, scroll_pos.y
            
            varied_amount = self.random_helper.get_scroll_amount(abs(amount))
            if amount < 0:
                varied_amount = -varied_amount
            
            scroll_success = self._execute_scroll(x, y, varied_amount, horizontal=True)
            
            log_mouse("scroll", (x, y), f"Horizontal: {varied_amount}")
            return scroll_success
            
        except Exception as e:
            self.logger.error(f"❌ Horizontal scroll failed: {e}")
            return False
    
    def scroll_in_area(self, x_range: Tuple[int, int], y_range: Tuple[int, int], 
                      amount: int, horizontal: bool = False) -> bool:
        """Scroll at random position within area"""
        try:
            scroll_point = self.coordinate_helper.get_random_point_in_area(x_range, y_range)
            
            if horizontal:
                return self.scroll_horizontal(amount, scroll_point.x, scroll_point.y)
            else:
                return self.scroll_vertical(amount, scroll_point.x, scroll_point.y)
                
        except Exception as e:
            self.logger.error(f"❌ Scroll in area failed: {e}")
            return False
    
    def natural_scroll_pattern(self, total_amount: int, x: Optional[int] = None, 
                              y: Optional[int] = None) -> bool:
        """
        Perform natural scrolling pattern with multiple small scrolls.
        
        Args:
            total_amount: Total amount to scroll
            x, y: Position to scroll at
            
        Returns:
            bool: True if successful
        """
        try:
            if x is None or y is None:
                scroll_pos = self.get_current_position()
                x, y = scroll_pos.x, scroll_pos.y
            
            # Break total scroll into natural chunks
            remaining = abs(total_amount)
            scroll_direction = 1 if total_amount > 0 else -1
            
            while remaining > 0:
                # Random chunk size (1-5 scroll units)
                chunk_size = min(remaining, random.randint(1, 5))
                scroll_amount = chunk_size * scroll_direction
                
                # Execute scroll
                self._execute_scroll(x, y, scroll_amount, horizontal=False)
                
                remaining -= chunk_size
                
                # Random pause between scrolls
                if remaining > 0:
                    pause = self.random_helper.get_click_delay(0.1, 0.3)
                    time.sleep(pause)
            
            log_action("natural_scroll", f"Scrolled {total_amount} units naturally", True)
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Natural scroll failed: {e}")
            return False
    
    # Utility and state methods
    
    def get_current_position(self) -> Point:
        """Get current mouse position"""
        if PYAUTOGUI_AVAILABLE:
            try:
                pos = pyautogui.position()
                current_pos = Point(pos.x, pos.y)
                self.state.current_position = current_pos
                return current_pos
            except Exception:
                pass
        
        return self.state.current_position
    
    def is_position_safe(self, x: int, y: int, margin: int = 10) -> bool:
        """Check if position is safe for clicking"""
        return self.coordinate_helper.validate_coordinates(x, y, margin)
    
    def wait_for_mouse_idle(self, timeout: float = 5.0) -> bool:
        """Wait for mouse to become idle (stop moving)"""
        try:
            start_time = time.time()
            last_pos = self.get_current_position()
            
            while time.time() - start_time < timeout:
                current_pos = self.get_current_position()
                
                if last_pos.distance_to(current_pos) < 2:  # Mouse is idle
                    return True
                
                last_pos = current_pos
                time.sleep(0.1)
            
            return False  # Timeout
            
        except Exception as e:
            self.logger.error(f"❌ Wait for idle failed: {e}")
            return False
    
    def click_with_retry(self, x_range: Tuple[int, int], y_range: Tuple[int, int], 
                        max_retries: int = 3, button: str = 'left') -> bool:
        """
        Click with automatic retry on failure.
        
        Args:
            x_range: X coordinate range
            y_range: Y coordinate range
            max_retries: Maximum retry attempts
            button: Mouse button to use
            
        Returns:
            bool: True if any attempt succeeded
        """
        for attempt in range(max_retries):
            try:
                if self.click_in_area(x_range, y_range, button):
                    return True
                
                self.logger.warning(f"⚠️  Click attempt {attempt + 1} failed, retrying...")
                
                # Wait before retry with increasing delay
                retry_delay = 1.0 + (attempt * 0.5)
                time.sleep(retry_delay)
                
            except Exception as e:
                self.logger.error(f"❌ Click attempt {attempt + 1} error: {e}")
        
        self.logger.error(f"❌ All {max_retries} click attempts failed")
        log_action("click_retry", f"All {max_retries} attempts failed", False)
        return False
    
    def get_mouse_statistics(self) -> Dict[str, Any]:
        """Get mouse usage statistics"""
        session_duration = time.time() - self.state.session_start
        
        return {
            "session_duration": session_duration,
            "total_clicks": self.state.total_clicks,
            "total_moves": self.state.total_moves,
            "clicks_per_minute": (self.state.total_clicks / (session_duration / 60)) if session_duration > 0 else 0,
            "current_position": self.state.current_position.to_tuple(),
            "last_click_ago": time.time() - self.state.last_click_time,
            "is_dragging": self.state.is_dragging
        }
    
    # Private implementation methods
    
    def _move_naturally_to_target(self, target: Point) -> bool:
        """Move mouse naturally to target with curves and variation"""
        try:
            start_point = self.get_current_position()
            
            # Generate natural path
            path = self.coordinate_helper.generate_natural_path(
                start_point, target, human_like=True
            )
            
            # Execute movement along path
            total_distance = start_point.distance_to(target)
            base_speed = self.settings.mouse.movement_speed
            
            for i, point in enumerate(path):
                if PYAUTOGUI_AVAILABLE:
                    pyautogui.moveTo(point.x, point.y)
                
                self.state.current_position = point
                
                # Variable speed - slower at start/end, faster in middle
                progress = i / (len(path) - 1) if len(path) > 1 else 1
                speed_multiplier = 1 - abs(0.5 - progress)  # Parabolic speed curve
                
                move_delay = (0.01 / base_speed) * (1 + speed_multiplier)
                move_delay = max(0.005, min(0.05, move_delay))  # Clamp delays
                
                time.sleep(move_delay)
            
            self.state.total_moves += 1
            self.state.last_move_time = time.time()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Natural movement failed: {e}")
            return False
    
    def _move_directly_to_target(self, target: Point) -> bool:
        """Move mouse directly to target"""
        try:
            if PYAUTOGUI_AVAILABLE:
                pyautogui.moveTo(target.x, target.y)
            
            self.state.current_position = target
            self.state.total_moves += 1
            self.state.last_move_time = time.time()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Direct movement failed: {e}")
            return False
    
    def _pre_click_behavior(self, target: Point):
        """Execute pre-click behavior (hesitation, micro-adjustments)"""
        # Hesitation check
        if self.random_helper.should_hesitate("normal"):
            hesitation_pause = self.random_helper.get_natural_pause("hesitation")
            time.sleep(hesitation_pause)
            log_detection("pre_click_hesitation", f"Hesitated {hesitation_pause:.2f}s", "INFO")
        
        # Micro-adjustment (small final movement)
        if random.random() < 0.3 and self.settings.automation.anti_detection:
            micro_offset = self.coordinate_helper.offset_coordinates(
                target.x, target.y, max_offset=2, distribution="gaussian"
            )
            if PYAUTOGUI_AVAILABLE:
                pyautogui.moveTo(micro_offset.x, micro_offset.y)
            self.state.current_position = micro_offset
            
            log_detection("micro_adjustment", f"Micro-adjusted to {micro_offset}", "INFO")
        
        # Pre-click delay
        pre_click_delay = self.random_helper.get_click_delay(
            self.settings.mouse.click_delay_min,
            self.settings.mouse.click_delay_max
        )
        time.sleep(pre_click_delay)
    
    def _execute_click(self, point: Point, button: str) -> bool:
        """Execute the actual mouse click"""
        try:
            if PYAUTOGUI_AVAILABLE:
                pyautogui.click(point.x, point.y, button=button)
            else:
                # Simulate click for testing
                self.logger.info(f"🖱️  [SIMULATED] Clicked at {point} with {button}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Click execution failed: {e}")
            return False
    
    def _post_click_behavior(self, click_success: bool):
        """Execute post-click behavior"""
        # Post-click delay
        post_delay = self.random_helper.get_click_delay(0.05, 0.2)
        time.sleep(post_delay)
        
        # Occasional double-check (move mouse slightly away and back)
        if (click_success and self.random_helper.should_double_check() and 
            self.settings.automation.anti_detection):
            
            current_pos = self.get_current_position()
            away_point = self.coordinate_helper.offset_coordinates(
                current_pos.x, current_pos.y, max_offset=20
            )
            
            # Quick move away and back
            self._move_directly_to_target(away_point)
            time.sleep(0.1)
            self._move_directly_to_target(current_pos)
            
            log_detection("post_click_doublecheck", "Performed double-check movement", "INFO")
    
    def _execute_drag(self, start: Point, end: Point, duration: float) -> bool:
        """Execute drag operation"""
        try:
            if PYAUTOGUI_AVAILABLE:
                pyautogui.dragTo(end.x, end.y, duration=duration, button='left')
            else:
                self.logger.info(f"🖱️  [SIMULATED] Dragged from {start} to {end} in {duration:.2f}s")
            
            self.state.current_position = end
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Drag execution failed: {e}")
            return False
    
    def _execute_scroll(self, x: int, y: int, amount: int, horizontal: bool = False) -> bool:
        """Execute scroll operation"""
        try:
            if PYAUTOGUI_AVAILABLE:
                # Move to position first if not already there
                current_pos = self.get_current_position()
                if current_pos.distance_to(Point(x, y)) > 5:
                    pyautogui.moveTo(x, y)
                
                if horizontal:
                    pyautogui.hscroll(amount)
                else:
                    pyautogui.scroll(amount)
            else:
                direction = "horizontal" if horizontal else "vertical"
                self.logger.info(f"🖱️  [SIMULATED] Scrolled {direction}: {amount} at ({x}, {y})")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Scroll execution failed: {e}")
            return False
    
    def emergency_stop(self):
        """Emergency stop all mouse operations"""
        try:
            self.state.is_dragging = False
            if PYAUTOGUI_AVAILABLE:
                # Move mouse to safe corner
                pyautogui.moveTo(10, 10)
            
            self.logger.warning("🛑 Emergency stop - Mouse operations halted")
            log_action("emergency_stop", "Mouse operations emergency stopped", True)
            
        except Exception as e:
            self.logger.error(f"❌ Emergency stop failed: {e}")

# Example usage and testing
if __name__ == "__main__":
    from config.settings import Settings
    from utils.random_helper import create_casual_profile
    
    print("🧪 Testing mouse controller...")
    
    # Create settings and mouse controller
    settings = Settings()
    profile = create_casual_profile()
    mouse = MouseController(settings, profile)
    
    # Test basic operations
    print(f"📍 Current position: {mouse.get_current_position()}")
    
    # Test area clicking
    test_area = ((100, 300), (200, 400))
    print(f"🎯 Testing area click: {test_area}")
    success = mouse.click_in_area(test_area[0], test_area[1])
    print(f"✅ Area click success: {success}")
    
    # Test natural movement
    print("🌊 Testing natural movement...")
    success = mouse.move_to_coordinates(500, 300, natural=True)
    print(f"✅ Natural movement success: {success}")
    
    # Test hover
    print("⏸️  Testing hover...")
    hover_area = ((400, 600), (250, 350))
    success = mouse.hover_over_area(hover_area[0], hover_area[1], duration=2.0)
    print(f"✅ Hover success: {success}")
    
    # Test drag
    print("🔄 Testing drag operation...")
    start_area = ((100, 200), (100, 200))
    end_area = ((400, 500), (300, 400))
    success = mouse.drag_in_areas(start_area, end_area)
    print(f"✅ Drag success: {success}")
    
    # Test scroll
    print("📜 Testing scroll...")
    success = mouse.scroll_vertical(-3)
    print(f"✅ Scroll success: {success}")
    
    # Test natural scroll pattern
    print("📜 Testing natural scroll pattern...")
    success = mouse.natural_scroll_pattern(-10)
    print(f"✅ Natural scroll success: {success}")
    
    # Test retry mechanism
    print("🔄 Testing retry mechanism...")
    retry_area = ((200, 400), (200, 400))
    success = mouse.click_with_retry(retry_area[0], retry_area[1], max_retries=2)
    print(f"✅ Retry click success: {success}")
    
    # Show statistics
    stats = mouse.get_mouse_statistics()
    print(f"\n📊 Mouse Statistics:")
    print(f"  • Total clicks: {stats['total_clicks']}")
    print(f"  • Total moves: {stats['total_moves']}")
    print(f"  • Session duration: {stats['session_duration']:.1f}s")
    print(f"  • Clicks per minute: {stats['clicks_per_minute']:.1f}")
    print(f"  • Current position: {stats['current_position']}")
    print(f"  • Last click ago: {stats['last_click_ago']:.1f}s")
    
    # Test move away from area
    print("↩️  Testing move away from area...")
    avoid_area = ((100, 300), (100, 300))
    success = mouse.move_away_from_area(avoid_area, min_distance=150)
    print(f"✅ Move away success: {success}")
    
    # Test double click
    print("👆👆 Testing double click...")
    success = mouse.double_click_in_area((200, 400), (200, 400))
    print(f"✅ Double click success: {success}")
    
    # Test right click
    print("👆➡️  Testing right click...")
    success = mouse.right_click_in_area((300, 500), (300, 500))
    print(f"✅ Right click success: {success}")
    
    print("\n✅ Mouse controller test completed!")
    print(f"🎯 Final position: {mouse.get_current_position()}")