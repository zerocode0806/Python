import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import ttk, messagebox
import os

class AlphabetRecognizer:
    def __init__(self):
        self.model = None
        self.alphabet_mapping = {i: chr(65 + i) for i in range(26)}  # 0:'A', 1:'B', ..., 25:'Z'
        self.load_saved_model()
        
    def load_saved_model(self):
        """Load the model - supports both .h5 and .keras files"""
        # Get the folder where this script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try both .h5 and .keras extensions for the same base filename
        for extension in ['.h5', '.keras']:
            model_path = os.path.join(base_dir, 'Best_points' + extension)
            
            if os.path.exists(model_path):
                try:
                    self.model = tf.keras.models.load_model(model_path)
                    print(f"✅ Successfully loaded alphabet model: Best_points{extension}")
                    return True
                except Exception as e:
                    print(f"⚠️ Error loading Best_points{extension}: {e}")
                    continue
        
        print("❌ No model found!")
        print("Please ensure you have 'Best_points.h5' or 'Best_points.keras' in the same folder.")
        return False
    


    def predict_letter(self, image_array):
        """Predict letter from image array"""
        if self.model is None:
            return None, []

        try:
            # Handle different input shapes
            input_shape = self.model.input_shape
            
            if len(input_shape) == 4:  # CNN model (batch, height, width, channels)
                # Reshape for CNN input (28x28x1)
                processed_image = image_array.reshape(1, 28, 28, 1).astype("float32") / 255.0
            elif len(input_shape) == 2:  # Dense model (batch, features)
                # Flatten for dense input (784,)
                processed_image = image_array.reshape(1, 784).astype("float32") / 255.0
            else:
                print(f"⚠️ Unexpected input shape: {input_shape}")
                return None, []

            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)[0]
            
            # Ensure we have 26 predictions for A-Z
            if len(predictions) != 26:
                print(f"⚠️ Model output size {len(predictions)} doesn't match alphabet size (26)")
                return None, []
            
            predicted_letter_index = np.argmax(predictions)
            predicted_letter = self.alphabet_mapping[predicted_letter_index]

            return predicted_letter, predictions
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None, []

class AlphabetRecognitionGUI:
    def __init__(self):
        self.recognizer = AlphabetRecognizer()
        if self.recognizer.model is not None:
            self.setup_gui()
        else:
            self.show_error_message()
            
    def show_error_message(self):
        """Show error if no model found"""
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "No Model Found", 
            "Please ensure you have 'Best_points.h5' or 'Best_points.keras' in the same folder!"
        )
        root.destroy()
        
    def setup_gui(self):
        """Setup the minimalist GUI"""
        self.root = tk.Tk()
        self.root.title("Alphabet Recognition - Neural Network Output (.h5 Support)")
        self.root.geometry("800x600")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Handwritten Alphabet Recognition (A-Z)", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Drawing section
        draw_frame = ttk.LabelFrame(main_frame, text="Draw a Letter (A-Z)", padding="15")
        draw_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Canvas for drawing
        self.canvas = tk.Canvas(draw_frame, width=250, height=250, bg='black', cursor='pencil')
        self.canvas.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)
        
        # Drawing controls
        ttk.Button(draw_frame, text="Clear", 
                  command=self.clear_canvas).grid(row=1, column=0, padx=(0, 5))
        ttk.Button(draw_frame, text="Predict", 
                  command=self.predict_drawing).grid(row=1, column=1, padx=(5, 0))
        
        # Neural network output section
        neural_frame = ttk.LabelFrame(main_frame, text="Neural Network Output (26 Letters)", padding="15")
        neural_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Create letter display in a more compact grid
        self.letter_frames = []
        self.letter_labels = []
        self.prediction_labels = []
        
        # Arrange 26 letters in 5 rows (6,6,6,4,4) for better layout
        letters_per_row = [6, 6, 6, 4, 4]
        current_letter = 0
        
        for row_idx, letters_in_row in enumerate(letters_per_row):
            for col_idx in range(letters_in_row):
                if current_letter >= 26:
                    break
                    
                letter = chr(65 + current_letter)  # Convert index to letter
                
                # Frame for each letter
                letter_frame = ttk.Frame(neural_frame, relief='solid', borderwidth=1, padding="4")
                letter_frame.grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky=(tk.W, tk.E))
                self.letter_frames.append(letter_frame)
                
                # Letter (medium size for better fit)
                letter_label = ttk.Label(letter_frame, text=letter, 
                                       font=('Arial', 12, 'bold'), 
                                       anchor='center')
                letter_label.grid(row=0, column=0, pady=(0, 2))
                self.letter_labels.append(letter_label)
                
                # Prediction percentage
                pred_label = ttk.Label(letter_frame, text="0.0%", 
                                      font=('Arial', 7), 
                                      anchor='center')
                pred_label.grid(row=1, column=0)
                self.prediction_labels.append(pred_label)
                
                # Configure column weight
                letter_frame.columnconfigure(0, weight=1)
                current_letter += 1
        
        # Result display
        self.result_label = ttk.Label(main_frame, 
                                     text="Draw a letter above and click Predict", 
                                     font=('Arial', 14), 
                                     anchor='center')
        self.result_label.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Initialize display
        self.update_neural_display(None)
        
    def update_neural_display(self, predictions):
        """Update the neural network output display"""
        if predictions is None:
            # Reset all displays
            for i in range(26):
                self.prediction_labels[i].config(text="0.0%", foreground='gray')
                self.letter_labels[i].config(foreground='gray')
                self.letter_frames[i].config(relief='solid', borderwidth=1)
        else:
            # Find the highest prediction
            max_letter_index = np.argmax(predictions)
            max_confidence = predictions[max_letter_index]
            predicted_letter = chr(65 + max_letter_index)
            
            # Get top 3 predictions for console output
            top_3_indices = np.argsort(predictions)[-3:][::-1]
            top_3_text = " | ".join([f"{chr(65+i)}({predictions[i]*100:.1f}%)" for i in top_3_indices])
            print(f"🎯 Prediction: {predicted_letter} | Top 3: {top_3_text}")
            
            # Update each letter's display
            for i in range(26):
                confidence = predictions[i] * 100
                self.prediction_labels[i].config(text=f"{confidence:.1f}%")
                
                # Highlight the winning letter
                if i == max_letter_index:
                    self.letter_labels[i].config(foreground='green')
                    self.prediction_labels[i].config(foreground='green')
                    self.letter_frames[i].config(relief='solid', borderwidth=3)
                else:
                    # Color based on confidence level
                    if confidence < 0.5:
                        color = 'lightgray'
                    elif confidence < 5.0:
                        color = 'gray'
                    else:
                        color = 'black'
                    self.letter_labels[i].config(foreground=color)
                    self.prediction_labels[i].config(foreground=color)
                    self.letter_frames[i].config(relief='solid', borderwidth=1)
            
            # Update result
            self.result_label.config(text=f"Prediction: {predicted_letter} (Confidence: {max_confidence*100:.1f}%)")
        
    def paint(self, event):
        """Handle drawing on canvas"""
        x, y = event.x, event.y
        r = 15  # Brush radius
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='white', outline='white')
    
    def clear_canvas(self):
        """Clear the drawing canvas"""
        self.canvas.delete("all")
        self.result_label.config(text="Canvas cleared - draw a new letter")
        self.update_neural_display(None)
    
    def predict_drawing(self):
        """Predict the drawn letter"""
        try:
            # Convert canvas to image
            canvas_items = self.canvas.find_all()
            if not canvas_items:
                self.result_label.config(text="Please draw something first!")
                self.update_neural_display(None)
                return
            
            # Create image from canvas
            img = Image.new('L', (250, 250), 0)  # Black background
            draw = ImageDraw.Draw(img)
            
            # Draw all canvas items
            for item in canvas_items:
                coords = self.canvas.coords(item)
                if len(coords) == 4:  # oval
                    draw.ellipse(coords, fill=255)  # White fill
            
            # Resize to 28x28
            img = img.resize((28, 28), Image.Resampling.LANCZOS)
            img_array = np.array(img)
            
            # Predict
            letter, predictions = self.recognizer.predict_letter(img_array)
            if letter is not None and predictions is not None:
                # Update neural network display
                self.update_neural_display(predictions)
            else:
                self.result_label.config(text="Could not make prediction")
                self.update_neural_display(None)
                
        except Exception as e:
            print(f"❌ Error in prediction: {e}")
            self.result_label.config(text="Error - try redrawing")
            self.update_neural_display(None)
    
    def run(self):
        """Start the GUI"""
        if hasattr(self, 'root'):
            self.root.mainloop()

if __name__ == "__main__":
    print("🔤 Loading Alphabet Recognition App with .h5 Support...")
    print("🔍 Looking for trained alphabet model...")
    
    app = AlphabetRecognitionGUI()
    if hasattr(app, 'root'):
        app.run()