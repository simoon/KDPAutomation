"""
Coordinate management and calculation utilities for browser automation.
Provides functions for coordinate validation, randomization, and geometric calculations.
"""

import random
import math
from typing import Tuple, List, Optional, Union
from dataclasses import dataclass
from enum import Enum

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("⚠️  pyautogui not available. Some screen detection features will be limited.")

class AreaShape(Enum):
    """Enumeration for different area shapes"""
    RECTANGLE = "rectangle"
    CIRCLE = "circle"
    ELLIPSE = "ellipse"

@dataclass
class Point:
    """Represents a 2D point with x and y coordinates"""
    x: int
    y: int
    
    def __post_init__(self):
        # Ensure coordinates are integers
        self.x = int(self.x)
        self.y = int(self.y)
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate distance to another point"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def offset(self, x_offset: int, y_offset: int) -> 'Point':
        """Create new point with offset applied"""
        return Point(self.x + x_offset, self.y + y_offset)
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to tuple representation"""
        return (self.x, self.y)
    
    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

@dataclass
class Rectangle:
    """Represents a rectangular area"""
    x1: int  # Top-left X
    y1: int  # Top-left Y
    x2: int  # Bottom-right X
    y2: int  # Bottom-right Y
    
    def __post_init__(self):
        # Ensure coordinates are integers and properly ordered
        self.x1, self.x2 = int(min(self.x1, self.x2)), int(max(self.x1, self.x2))
        self.y1, self.y2 = int(min(self.y1, self.y2)), int(max(self.y1, self.y2))
    
    @property
    def width(self) -> int:
        """Get rectangle width"""
        return self.x2 - self.x1
    
    @property
    def height(self) -> int:
        """Get rectangle height"""
        return self.y2 - self.y1
    
    @property
    def center(self) -> Point:
        """Get center point of rectangle"""
        return Point((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)
    
    @property
    def area(self) -> int:
        """Get rectangle area"""
        return self.width * self.height
    
    def contains(self, point: Point) -> bool:
        """Check if point is inside rectangle"""
        return self.x1 <= point.x <= self.x2 and self.y1 <= point.y <= self.y2
    
    def intersects(self, other: 'Rectangle') -> bool:
        """Check if this rectangle intersects with another"""
        return not (self.x2 < other.x1 or other.x2 < self.x1 or 
                   self.y2 < other.y1 or other.y2 < self.y1)
    
    def expand(self, margin: int) -> 'Rectangle':
        """Create expanded rectangle with margin"""
        return Rectangle(
            self.x1 - margin, self.y1 - margin,
            self.x2 + margin, self.y2 + margin
        )
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        """Convert to tuple representation"""
        return (self.x1, self.y1, self.x2, self.y2)
    
    def __str__(self) -> str:
        return f"Rectangle({self.x1}, {self.y1}, {self.x2}, {self.y2}) [{self.width}x{self.height}]"

@dataclass
class Circle:
    """Represents a circular area"""
    center_x: int
    center_y: int
    radius: int
    
    def __post_init__(self):
        self.center_x = int(self.center_x)
        self.center_y = int(self.center_y)
        self.radius = int(abs(self.radius))
    
    @property
    def center(self) -> Point:
        """Get center point of circle"""
        return Point(self.center_x, self.center_y)
    
    @property
    def area(self) -> float:
        """Get circle area"""
        return math.pi * self.radius ** 2
    
    def contains(self, point: Point) -> bool:
        """Check if point is inside circle"""
        distance = self.center.distance_to(point)
        return distance <= self.radius
    
    def bounding_box(self) -> Rectangle:
        """Get bounding rectangle of circle"""
        return Rectangle(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius
        )
    
    def __str__(self) -> str:
        return f"Circle({self.center_x}, {self.center_y}, r={self.radius})"

class CoordinateHelper:
    """
    Advanced coordinate management system for browser automation.
    Provides coordinate validation, randomization, and geometric calculations.
    """
    
    def __init__(self):
        self.screen_width = None
        self.screen_height = None
        self._detect_screen_size()
    
    def _detect_screen_size(self):
        """Detect screen dimensions"""
        if PYAUTOGUI_AVAILABLE:
            try:
                self.screen_width, self.screen_height = pyautogui.size()
            except Exception:
                self._set_default_screen_size()
        else:
            self._set_default_screen_size()
    
    def _set_default_screen_size(self):
        """Set default screen size when detection fails"""
        self.screen_width = 1920
        self.screen_height = 1080
        print(f"⚠️  Using default screen size: {self.screen_width}x{self.screen_height}")
    
    def set_screen_size(self, width: int, height: int):
        """Manually set screen dimensions"""
        self.screen_width = int(width)
        self.screen_height = int(height)
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get current screen dimensions"""
        return (self.screen_width, self.screen_height)
    
    def get_screen_center(self) -> Point:
        """Get screen center point"""
        return Point(self.screen_width // 2, self.screen_height // 2)
    
    def validate_coordinates(self, x: int, y: int, margin: int = 0) -> bool:
        """
        Validate if coordinates are within screen bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate
            margin: Safety margin from screen edges
            
        Returns:
            bool: True if coordinates are valid
        """
        return (margin <= x <= self.screen_width - margin and 
                margin <= y <= self.screen_height - margin)
    
    def validate_point(self, point: Point, margin: int = 0) -> bool:
        """Validate if point is within screen bounds"""
        return self.validate_coordinates(point.x, point.y, margin)
    
    def clamp_coordinates(self, x: int, y: int, margin: int = 0) -> Point:
        """
        Clamp coordinates to valid screen bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate
            margin: Safety margin from edges
            
        Returns:
            Point: Clamped coordinates
        """
        clamped_x = max(margin, min(self.screen_width - margin, x))
        clamped_y = max(margin, min(self.screen_height - margin, y))
        return Point(clamped_x, clamped_y)
    
    def clamp_point(self, point: Point, margin: int = 0) -> Point:
        """Clamp point to valid screen bounds"""
        return self.clamp_coordinates(point.x, point.y, margin)
    
    # Random coordinate generation methods
    
    def get_random_point_in_range(self, coordinate_range: Tuple[int, int]) -> int:
        """
        Get random coordinate within specified range.
        
        Args:
            coordinate_range: Tuple of (min, max) values
            
        Returns:
            int: Random coordinate within range
        """
        min_val, max_val = coordinate_range
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        return random.randint(min_val, max_val)
    
    def get_random_point_in_area(self, x_range: Tuple[int, int], 
                                y_range: Tuple[int, int]) -> Point:
        """
        Get random point within rectangular area.
        
        Args:
            x_range: Tuple of (min_x, max_x)
            y_range: Tuple of (min_y, max_y)
            
        Returns:
            Point: Random point within area
        """
        x = self.get_random_point_in_range(x_range)
        y = self.get_random_point_in_range(y_range)
        return Point(x, y)
    
    def get_random_point_in_rectangle(self, rect: Rectangle) -> Point:
        """Get random point within rectangle"""
        return self.get_random_point_in_area((rect.x1, rect.x2), (rect.y1, rect.y2))
    
    def get_random_point_in_circle(self, circle: Circle) -> Point:
        """
        Get random point within circle using uniform distribution.
        Uses rejection sampling for true uniform distribution.
        """
        max_attempts = 100
        for _ in range(max_attempts):
            # Generate random point in bounding box
            bbox = circle.bounding_box()
            point = self.get_random_point_in_rectangle(bbox)
            
            # Check if point is inside circle
            if circle.contains(point):
                return point
        
        # Fallback: return center if sampling fails
        return circle.center
    
    def get_random_point_on_circle_edge(self, circle: Circle, 
                                       thickness: int = 1) -> Point:
        """
        Get random point on circle edge with specified thickness.
        
        Args:
            circle: Circle to sample from
            thickness: Thickness of the edge band
            
        Returns:
            Point: Random point on circle edge
        """
        angle = random.uniform(0, 2 * math.pi)
        # Randomize radius within thickness band
        radius = random.uniform(circle.radius - thickness, circle.radius)
        
        x = circle.center_x + int(radius * math.cos(angle))
        y = circle.center_y + int(radius * math.sin(angle))
        
        return Point(x, y)
    
    # Coordinate transformation and offset methods
    
    def offset_coordinates(self, x: int, y: int, max_offset: int = 5, 
                          distribution: str = "uniform") -> Point:
        """
        Add random offset to coordinates for natural variation.
        
        Args:
            x: Original X coordinate
            y: Original Y coordinate
            max_offset: Maximum pixel offset in any direction
            distribution: Offset distribution ("uniform", "gaussian")
            
        Returns:
            Point: Offset coordinates
        """
        if distribution == "gaussian":
            # Gaussian distribution for more natural randomization
            std_dev = max_offset / 3  # 99.7% of values within max_offset
            offset_x = int(random.gauss(0, std_dev))
            offset_y = int(random.gauss(0, std_dev))
            
            # Clamp to max_offset
            offset_x = max(-max_offset, min(max_offset, offset_x))
            offset_y = max(-max_offset, min(max_offset, offset_y))
        else:
            # Uniform distribution
            offset_x = random.randint(-max_offset, max_offset)
            offset_y = random.randint(-max_offset, max_offset)
        
        new_x = x + offset_x
        new_y = y + offset_y
        
        # Ensure coordinates stay within screen bounds
        return self.clamp_coordinates(new_x, new_y)
    
    def offset_point(self, point: Point, max_offset: int = 5, 
                    distribution: str = "uniform") -> Point:
        """Add random offset to point"""
        return self.offset_coordinates(point.x, point.y, max_offset, distribution)
    
    def apply_margin_to_area(self, x_range: Tuple[int, int], 
                            y_range: Tuple[int, int], 
                            margin: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
        Apply margin to coordinate ranges (shrink the clickable area).
        
        Args:
            x_range: Original X range
            y_range: Original Y range
            margin: Margin to apply (pixels)
            
        Returns:
            Tuple of new coordinate ranges
        """
        new_x_range = (x_range[0] + margin, x_range[1] - margin)
        new_y_range = (y_range[0] + margin, y_range[1] - margin)
        
        # Ensure ranges are still valid
        if new_x_range[0] >= new_x_range[1]:
            new_x_range = (x_range[0], x_range[1])
        if new_y_range[0] >= new_y_range[1]:
            new_y_range = (y_range[0], y_range[1])
        
        return new_x_range, new_y_range
    
    # Distance and geometric calculations
    
    def calculate_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """Calculate Euclidean distance between two points"""
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def calculate_point_distance(self, point1: Point, point2: Point) -> float:
        """Calculate distance between two points"""
        return point1.distance_to(point2)
    
    def calculate_angle(self, from_point: Point, to_point: Point) -> float:
        """
        Calculate angle from one point to another in radians.
        
        Returns:
            float: Angle in radians (0 to 2π)
        """
        dx = to_point.x - from_point.x
        dy = to_point.y - from_point.y
        return math.atan2(dy, dx)
    
    def calculate_midpoint(self, point1: Point, point2: Point) -> Point:
        """Calculate midpoint between two points"""
        mid_x = (point1.x + point2.x) // 2
        mid_y = (point1.y + point2.y) // 2
        return Point(mid_x, mid_y)
    
    def get_center_of_area(self, x_range: Tuple[int, int], 
                          y_range: Tuple[int, int]) -> Point:
        """Get center point of rectangular area"""
        center_x = (x_range[0] + x_range[1]) // 2
        center_y = (y_range[0] + y_range[1]) // 2
        return Point(center_x, center_y)
    
    # Path generation for smooth mouse movements
    
    def generate_smooth_path(self, start: Point, end: Point, 
                           steps: int = 20, 
                           curve_intensity: float = 0.2) -> List[Point]:
        """
        Generate smooth path between two points with natural curves.
        
        Args:
            start: Starting point
            end: Ending point
            steps: Number of intermediate points
            curve_intensity: How much to curve the path (0.0 = straight, 1.0 = very curved)
            
        Returns:
            List[Point]: Path points from start to end
        """
        if steps <= 2:
            return [start, end]
        
        path = []
        
        # Calculate control points for Bezier curve
        distance = start.distance_to(end)
        
        # Generate random control points for natural curves
        mid_x = (start.x + end.x) // 2
        mid_y = (start.y + end.y) // 2
        
        # Add some randomness to the curve
        offset_range = int(distance * curve_intensity * 0.5)
        if offset_range > 0:
            control_offset_x = random.randint(-offset_range, offset_range)
            control_offset_y = random.randint(-offset_range, offset_range)
        else:
            control_offset_x = control_offset_y = 0
        
        control_point = Point(mid_x + control_offset_x, mid_y + control_offset_y)
        
        # Generate points along quadratic Bezier curve
        for i in range(steps):
            t = i / (steps - 1)  # Parameter from 0 to 1
            
            # Quadratic Bezier: P(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
            x = ((1 - t) ** 2 * start.x + 
                 2 * (1 - t) * t * control_point.x + 
                 t ** 2 * end.x)
            y = ((1 - t) ** 2 * start.y + 
                 2 * (1 - t) * t * control_point.y + 
                 t ** 2 * end.y)
            
            # Clamp coordinates to screen bounds
            point = self.clamp_coordinates(int(x), int(y))
            path.append(point)
        
        return path
    
    def generate_natural_path(self, start: Point, end: Point, 
                             human_like: bool = True) -> List[Point]:
        """
        Generate natural mouse movement path that mimics human behavior.
        
        Args:
            start: Starting point
            end: Ending point
            human_like: Whether to add human-like imperfections
            
        Returns:
            List[Point]: Natural movement path
        """
        distance = start.distance_to(end)
        
        # Calculate appropriate number of steps based on distance
        steps = max(5, int(distance / 15))  # ~15 pixels per step
        
        # Curve intensity based on distance (longer moves = more curved)
        if distance < 50:
            curve_intensity = 0.1
        elif distance < 200:
            curve_intensity = 0.2
        else:
            curve_intensity = 0.3
        
        # Generate base path
        path = self.generate_smooth_path(start, end, steps, curve_intensity)
        
        if human_like:
            # Add small random variations to simulate human imperfections
            varied_path = []
            for point in path:
                # Small random offset (1-2 pixels)
                offset_point = self.offset_coordinates(
                    point.x, point.y, 
                    max_offset=2, 
                    distribution="gaussian"
                )
                varied_path.append(offset_point)
            
            path = varied_path
        
        return path
    
    # Utility methods for common geometric operations
    
    def is_point_in_screen(self, point: Point, margin: int = 0) -> bool:
        """Check if point is within screen bounds"""
        return self.validate_point(point, margin)
    
    def get_safe_click_area(self, rect: Rectangle, safety_margin: int = 10) -> Rectangle:
        """
        Get safe clicking area within rectangle with margin from edges.
        
        Args:
            rect: Original rectangle
            safety_margin: Margin to maintain from edges
            
        Returns:
            Rectangle: Safe clicking area
        """
        safe_rect = Rectangle(
            rect.x1 + safety_margin,
            rect.y1 + safety_margin,
            rect.x2 - safety_margin,
            rect.y2 - safety_margin
        )
        
        # Ensure the safe area is still valid
        if safe_rect.width <= 0 or safe_rect.height <= 0:
            return rect  # Return original if margin too large
        
        return safe_rect
    
    def get_corner_points(self, rect: Rectangle) -> List[Point]:
        """Get all four corner points of rectangle"""
        return [
            Point(rect.x1, rect.y1),  # Top-left
            Point(rect.x2, rect.y1),  # Top-right
            Point(rect.x1, rect.y2),  # Bottom-left
            Point(rect.x2, rect.y2),  # Bottom-right
        ]
    
    def get_edge_points(self, rect: Rectangle, points_per_edge: int = 5) -> List[Point]:
        """Get points along the edges of rectangle"""
        points = []
        
        # Top edge
        for i in range(points_per_edge):
            x = rect.x1 + (rect.width * i // (points_per_edge - 1))
            points.append(Point(x, rect.y1))
        
        # Right edge (skip corner)
        for i in range(1, points_per_edge):
            y = rect.y1 + (rect.height * i // (points_per_edge - 1))
            points.append(Point(rect.x2, y))
        
        # Bottom edge (skip corner, reverse order)
        for i in range(points_per_edge - 2, -1, -1):
            x = rect.x1 + (rect.width * i // (points_per_edge - 1))
            points.append(Point(x, rect.y2))
        
        # Left edge (skip corners)
        for i in range(points_per_edge - 2, 0, -1):
            y = rect.y1 + (rect.height * i // (points_per_edge - 1))
            points.append(Point(rect.x1, y))
        
        return points

# Convenience functions for quick operations
def create_rectangle_from_ranges(x_range: Tuple[int, int], 
                                y_range: Tuple[int, int]) -> Rectangle:
    """Create Rectangle from coordinate ranges"""
    return Rectangle(x_range[0], y_range[0], x_range[1], y_range[1])

def create_circle_from_center_radius(center: Point, radius: int) -> Circle:
    """Create Circle from center point and radius"""
    return Circle(center.x, center.y, radius)

def point_from_tuple(coords: Tuple[int, int]) -> Point:
    """Create Point from tuple"""
    return Point(coords[0], coords[1])

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing coordinate helper system...")
    
    # Create coordinate helper
    coord_helper = CoordinateHelper()
    print(f"📏 Screen size: {coord_helper.get_screen_size()}")
    
    # Test point creation and validation
    test_point = Point(500, 300)
    print(f"📍 Test point: {test_point}")
    print(f"✅ Point valid: {coord_helper.validate_point(test_point)}")
    
    # Test rectangle operations
    test_rect = Rectangle(100, 100, 300, 200)
    print(f"📐 Test rectangle: {test_rect}")
    print(f"🎯 Rectangle center: {test_rect.center}")
    print(f"📏 Rectangle area: {test_rect.area}")
    
    # Test random point generation
    random_point = coord_helper.get_random_point_in_rectangle(test_rect)
    print(f"🎲 Random point in rect: {random_point}")
    print(f"✅ Point in rectangle: {test_rect.contains(random_point)}")
    
    # Test coordinate offset
    offset_point = coord_helper.offset_point(test_point, max_offset=10)
    print(f"↗️  Offset point: {offset_point}")
    
    # Test path generation
    start = Point(100, 100)
    end = Point(500, 400)
    path = coord_helper.generate_natural_path(start, end)
    print(f"🛤️  Generated path with {len(path)} points")
    
    # Test circle operations
    test_circle = Circle(400, 300, 50)
    print(f"⭕ Test circle: {test_circle}")
    circle_point = coord_helper.get_random_point_in_circle(test_circle)
    print(f"🎲 Random point in circle: {circle_point}")
    
    print("✅ Coordinate helper system test completed!")