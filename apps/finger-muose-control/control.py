import cv2
import mediapipe as mp
import pyautogui
import time
import math
from collections import deque
from enum import Enum

# Disable pyautogui fail-safe for smoother operation
pyautogui.FAILSAFE = False

class GestureState(Enum):
    IDLE = "Idle"
    MOVE = "Move"
    PINCH_CLOSED = "Pinch Closed"
    DRAGGING = "Dragging"

class GestureMouseController:
    def __init__(self):
        # Initialize MediaPipe hands module
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=1
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Gesture state management
        self.current_state = GestureState.IDLE
        self.previous_state = GestureState.IDLE
        
        # Pinch detection parameters
        self.pinch_threshold = 40
        self.is_pinch_closed = False
        self.was_pinch_closed = False
        self.pinch_start_time = 0
        self.pinch_close_events = deque(maxlen=10)
        
        # Mouse movement smoothing - Much more aggressive
        self.smoothing_factor = 0.02  # Very strong smoothing (was 0.1)
        self.prev_x, self.prev_y = 0, 0
        
        # Movement filtering with larger buffer
        self.movement_buffer = deque(maxlen=15)  # Increased buffer size
        self.movement_threshold = 1  # Lower threshold for more responsiveness
        
        # Multi-stage smoothing
        self.stage1_buffer = deque(maxlen=10)
        self.stage2_buffer = deque(maxlen=5)
        
        # Screen mapping margins (use only center 60% of camera view for full screen)
        self.margin_x = 0.2  # 20% margin on each side
        self.margin_y = 0.1  # 10% margin on top/bottom
        
        # Gesture timing - more lenient timing for clicks
        self.double_click_timeout = 0.8  # Increased from 0.5s
        self.triple_click_timeout = 1.2  # Increased from 0.7s
        self.drag_threshold = 0.8
        
        # Debug information
        self.current_gesture = "None"
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def is_l_shape_gesture(self, hand_landmarks):
        """
        Detect L-shape gesture: thumb and index finger extended, others folded.
        """
        # Get landmark positions
        thumb_tip = hand_landmarks.landmark[4]
        thumb_mcp = hand_landmarks.landmark[2]
        index_tip = hand_landmarks.landmark[8]
        index_pip = hand_landmarks.landmark[6]
        middle_tip = hand_landmarks.landmark[12]
        middle_pip = hand_landmarks.landmark[10]
        ring_tip = hand_landmarks.landmark[16]
        ring_pip = hand_landmarks.landmark[14]
        pinky_tip = hand_landmarks.landmark[20]
        pinky_pip = hand_landmarks.landmark[18]
        
        # Check if thumb is extended (x-coordinate comparison for horizontal extension)
        thumb_extended = abs(thumb_tip.x - thumb_mcp.x) > 0.04
        
        # Check if index finger is extended (y-coordinate comparison for vertical extension)
        index_extended = index_tip.y < index_pip.y
        
        # Check if other fingers are folded
        middle_folded = middle_tip.y > middle_pip.y
        ring_folded = ring_tip.y > ring_pip.y
        pinky_folded = pinky_tip.y > pinky_pip.y
        
        return thumb_extended and index_extended and middle_folded and ring_folded and pinky_folded
    
    def detect_pinch(self, hand_landmarks, frame_width, frame_height):
        """
        Detect pinch gesture between thumb and index finger.
        """
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        
        # Convert normalized coordinates to pixel coordinates
        thumb_x = int(thumb_tip.x * frame_width)
        thumb_y = int(thumb_tip.y * frame_height)
        index_x = int(index_tip.x * frame_width)
        index_y = int(index_tip.y * frame_height)
        
        # Calculate distance in pixels
        distance = math.sqrt((thumb_x - index_x)**2 + (thumb_y - index_y)**2)
        
        return distance < self.pinch_threshold, distance
    
    def detect_gesture(self, hand_landmarks, frame_width, frame_height):
        """
        Main gesture detection function.
        """
        current_time = time.time()
        
        # Check for L-shape gesture
        l_shape = self.is_l_shape_gesture(hand_landmarks)
        
        # Check for pinch
        is_pinched, pinch_distance = self.detect_pinch(hand_landmarks, frame_width, frame_height)
        
        # Update pinch state
        self.was_pinch_closed = self.is_pinch_closed
        self.is_pinch_closed = is_pinched
        
        # Detect pinch close event (transition from open to closed)
        if self.is_pinch_closed and not self.was_pinch_closed:
            self.pinch_close_events.append(current_time)
            self.pinch_start_time = current_time
        
        # State machine logic
        if l_shape and not self.is_pinch_closed:
            self.current_state = GestureState.MOVE
            self.current_gesture = "Move"
            
        elif l_shape and self.is_pinch_closed:
            # Check if this is a drag operation (pinch held for more than drag_threshold)
            if current_time - self.pinch_start_time > self.drag_threshold:
                if self.current_state != GestureState.DRAGGING:
                    self.current_state = GestureState.DRAGGING
                    self.current_gesture = "Dragging"
            else:
                self.current_state = GestureState.PINCH_CLOSED
                self.current_gesture = "Pinch Closed"
                
        else:
            # Check for click gestures when transitioning from pinch to non-pinch
            if self.was_pinch_closed and not self.is_pinch_closed:
                # Don't process immediately - let process_pending_clicks handle it
                pass
            
            self.current_state = GestureState.IDLE
            if not self.pinch_close_events:
                self.current_gesture = "Idle"
        
        return l_shape, is_pinched, pinch_distance
    
    def handle_click_gestures(self, current_time):
        """
        Handle different types of click gestures based on timing.
        """
        # Don't process clicks immediately - wait for potential additional clicks
        return
    
    def process_pending_clicks(self, current_time):
        """
        Process clicks after a delay to allow for multiple click detection.
        """
        if not self.pinch_close_events:
            return
            
        # Get the most recent event
        last_event = self.pinch_close_events[-1]
        
        # Wait a bit after the last event to see if more clicks come
        if current_time - last_event < 0.3:
            return
            
        # Count recent events within the timeout window
        recent_events = [t for t in self.pinch_close_events if current_time - t < self.triple_click_timeout]
        
        if len(recent_events) >= 3:
            # Triple click -> Right click
            self.current_gesture = "Right Click"
            self.perform_action("right_click")
            print("Right click performed!")
            
        elif len(recent_events) >= 2:
            # Double click
            self.current_gesture = "Double Click" 
            self.perform_action("double_click")
            print("Double click performed!")
            
        elif len(recent_events) >= 1:
            # Single click
            self.current_gesture = "Single Click"
            self.perform_action("single_click")
            print("Single click performed!")
        
        # Clear events after processing
        self.pinch_close_events.clear()
    
    def perform_action(self, action_type, x=None, y=None):
        """
        Perform the specified mouse action.
        """
        try:
            if action_type == "move" and x is not None and y is not None:
                pyautogui.moveTo(x, y)
                
            elif action_type == "single_click":
                pyautogui.click()
                
            elif action_type == "double_click":
                pyautogui.doubleClick()
                
            elif action_type == "right_click":
                pyautogui.rightClick()
                
            elif action_type == "drag_start":
                pyautogui.mouseDown()
                
            elif action_type == "drag_end":
                pyautogui.mouseUp()
                
        except Exception as e:
            print(f"Error performing action {action_type}: {e}")
    
    def smooth_movement(self, new_x, new_y):
        """
        Apply multi-stage ultra-smooth filtering to eliminate all jitter.
        """
        # Stage 1: Raw coordinate smoothing with large buffer
        self.stage1_buffer.append((new_x, new_y))
        
        if len(self.stage1_buffer) < 5:
            return int(new_x), int(new_y)
        
        # Calculate median to remove outliers
        x_values = [pos[0] for pos in self.stage1_buffer]
        y_values = [pos[1] for pos in self.stage1_buffer]
        x_values.sort()
        y_values.sort()
        
        median_x = x_values[len(x_values) // 2]
        median_y = y_values[len(y_values) // 2]
        
        # Stage 2: Weighted moving average
        self.stage2_buffer.append((median_x, median_y))
        
        if len(self.stage2_buffer) < 3:
            return int(median_x), int(median_y)
        
        # Calculate weighted average with exponential decay
        total_weight = 0
        weighted_x = 0
        weighted_y = 0
        
        for i, (x, y) in enumerate(self.stage2_buffer):
            # Exponential weight - recent positions much more important
            weight = (2 ** i)
            weighted_x += x * weight
            weighted_y += y * weight
            total_weight += weight
        
        avg_x = weighted_x / total_weight
        avg_y = weighted_y / total_weight
        
        # Stage 3: Final exponential smoothing with previous cursor position
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = avg_x, avg_y
            return int(avg_x), int(avg_y)
        
        # Ultra-smooth exponential filter
        smooth_x = self.prev_x * self.smoothing_factor + avg_x * (1 - self.smoothing_factor)
        smooth_y = self.prev_y * self.smoothing_factor + avg_y * (1 - self.smoothing_factor)
        
        # Only update if movement is meaningful (but very low threshold)
        movement_distance = math.sqrt((smooth_x - self.prev_x)**2 + (smooth_y - self.prev_y)**2)
        if movement_distance > self.movement_threshold:
            self.prev_x, self.prev_y = smooth_x, smooth_y
        
        return int(self.prev_x), int(self.prev_y)
    
    def map_to_screen(self, hand_landmarks, frame_width, frame_height):
        """
        Map hand coordinates to screen coordinates with expanded range.
        Uses only center portion of camera view to map to full screen.
        """
        index_tip = hand_landmarks.landmark[8]
        
        # Normalize coordinates to usable range (exclude margins)
        # Map the center 60%x80% of camera view to full screen
        normalized_x = (index_tip.x - self.margin_x) / (1 - 2 * self.margin_x)
        normalized_y = (index_tip.y - self.margin_y) / (1 - 2 * self.margin_y)
        
        # Clamp to [0,1] range
        normalized_x = max(0, min(1, normalized_x))
        normalized_y = max(0, min(1, normalized_y))
        
        # Convert to screen coordinates
        screen_x = int(normalized_x * self.screen_width)
        screen_y = int(normalized_y * self.screen_height)
        
        # Apply bounds checking
        screen_x = max(0, min(screen_x, self.screen_width - 1))
        screen_y = max(0, min(screen_y, self.screen_height - 1))
        
        return screen_x, screen_y
    
    def draw_debug_info(self, frame, hand_landmarks, l_shape, is_pinched, pinch_distance):
        """
        Draw debug information on the frame.
        """
        height, width, _ = frame.shape
        
        # Draw hand landmarks
        self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        # Draw pinch detection line
        if l_shape:
            thumb_tip = hand_landmarks.landmark[4]
            index_tip = hand_landmarks.landmark[8]
            
            thumb_x = int(thumb_tip.x * width)
            thumb_y = int(thumb_tip.y * height)
            index_x = int(index_tip.x * width)
            index_y = int(index_tip.y * height)
            
            # Color based on pinch state
            color = (0, 0, 255) if is_pinched else (0, 255, 0)
            cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), color, 2)
            
            # Draw distance text
            cv2.putText(frame, f'Distance: {pinch_distance:.1f}', 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Draw gesture information
        cv2.putText(frame, f'State: {self.current_state.value}', 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f'Gesture: {self.current_gesture}', 
                   (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        # Draw L-shape detection
        l_status = "YES" if l_shape else "NO"
        cv2.putText(frame, f'L-Shape: {l_status}', 
                   (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        
        # Draw screen mapping zone visualization
        overlay_color = (0, 255, 255, 50)  # Semi-transparent yellow
        margin_x_px = int(self.margin_x * width)
        margin_y_px = int(self.margin_y * height)
        
        # Draw the active control zone
        cv2.rectangle(frame, (margin_x_px, margin_y_px), 
                     (width - margin_x_px, height - margin_y_px), (0, 255, 255), 2)
        cv2.putText(frame, 'Control Zone', (margin_x_px + 5, margin_y_px + 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    def run(self):
        """
        Main execution loop.
        """
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        print("Gesture Mouse Controller Started!")
        print("Controls:")
        print("- L-shape (thumb + index extended): Move cursor")
        print("- Pinch (in L-shape): Click/Drag")
        print("- Single pinch: Left click")
        print("- Double pinch: Double click")
        print("- Triple pinch: Right click")
        print("- Hold pinch: Drag")
        print("- Press 'q' to quit")
        
        drag_active = False
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame. Exiting...")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            # Process hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Detect gestures
                    l_shape, is_pinched, pinch_distance = self.detect_gesture(hand_landmarks, width, height)
                    
                    # Handle mouse control with reduced update frequency for smoothness
                    if self.current_state == GestureState.MOVE:
                        # Move cursor with ultra-smooth filtering
                        screen_x, screen_y = self.map_to_screen(hand_landmarks, width, height)
                        smooth_x, smooth_y = self.smooth_movement(screen_x, screen_y)
                        
                        # Only update cursor every few frames to reduce system load
                        if hasattr(self, 'frame_count'):
                            self.frame_count += 1
                        else:
                            self.frame_count = 0
                            
                        if self.frame_count % 2 == 0:  # Update every 2nd frame
                            self.perform_action("move", smooth_x, smooth_y)
                        
                    elif self.current_state == GestureState.DRAGGING:
                        # Handle drag operations
                        if not drag_active:
                            self.perform_action("drag_start")
                            drag_active = True
                        
                        # Continue moving while dragging with same smoothing
                        screen_x, screen_y = self.map_to_screen(hand_landmarks, width, height)
                        smooth_x, smooth_y = self.smooth_movement(screen_x, screen_y)
                        
                        if self.frame_count % 2 == 0:  # Same frame limiting for drag
                            self.perform_action("move", smooth_x, smooth_y)
                        
                    elif self.previous_state == GestureState.DRAGGING and drag_active:
                        # End drag operation
                        self.perform_action("drag_end")
                        drag_active = False
                    
                    # Update previous state
                    self.previous_state = self.current_state
                    
                    # Process any pending clicks
                    self.process_pending_clicks(time.time())
                    
                    # Draw debug information
                    self.draw_debug_info(frame, hand_landmarks, l_shape, is_pinched, pinch_distance)
            else:
                # No hands detected
                self.current_state = GestureState.IDLE
                self.current_gesture = "No Hand Detected"
                cv2.putText(frame, self.current_gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Display the frame
            cv2.imshow('Gesture Mouse Controller', frame)
            
            # Break on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    controller = GestureMouseController()
    controller.run()