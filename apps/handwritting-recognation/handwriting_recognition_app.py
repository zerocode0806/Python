import torch
import torch.nn as nn
import numpy as np
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import ttk, messagebox
import os

class FastCNN(nn.Module):
    """Same architecture as training script"""
    def __init__(self, num_classes=26):
        super(FastCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        
        self.pool = nn.MaxPool2d(2, 2)
        self.dropout = nn.Dropout(0.3)
        
        self.fc1 = nn.Linear(128 * 3 * 3, 256)
        self.fc2 = nn.Linear(256, num_classes)
    
    def forward(self, x):
        x = self.pool(torch.relu(self.bn1(self.conv1(x))))
        x = self.pool(torch.relu(self.bn2(self.conv2(x))))
        x = self.pool(torch.relu(self.bn3(self.conv3(x))))
        
        x = x.view(x.size(0), -1)
        x = self.dropout(torch.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

class AlphabetRecognizer:
    def __init__(self):
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.alphabet_mapping = {i: chr(65 + i) for i in range(26)}  # 0:'A', 1:'B', ..., 25:'Z'
        self.load_saved_model()
        
    def load_saved_model(self):
        """Load the PyTorch model"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'best_alphabet_model.pth')
        
        if os.path.exists(model_path):
            try:
                # Create model architecture
                self.model = FastCNN(num_classes=26)
                
                # Load weights
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                self.model.to(self.device)
                self.model.eval()  # Set to evaluation mode
                
                print(f"✅ Successfully loaded PyTorch model: best_alphabet_model.pth")
                print(f"🔥 Device: {self.device}")
                return True
            except Exception as e:
                print(f"❌ Error loading model: {e}")
                return False
        else:
            print("❌ Model file not found: best_alphabet_model.pth")
            print("Please ensure you have trained the model first!")
            return False

    def predict_letter(self, image_array):
        """Predict letter from image array (28x28 grayscale)"""
        if self.model is None:
            return None, []

        try:
            # Preprocess image
            # Convert to RGB (repeat grayscale 3 times)
            img_rgb = np.repeat(image_array[:, :, np.newaxis], 3, axis=2)
            
            # Normalize to [-1, 1] range (same as training)
            img_normalized = (img_rgb.astype(np.float32) / 255.0 - 0.5) / 0.5
            
            # Convert to PyTorch tensor (CHW format)
            img_tensor = torch.from_numpy(img_normalized).permute(2, 0, 1).unsqueeze(0)
            img_tensor = img_tensor.to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilities = torch.softmax(outputs, dim=1)[0].cpu().numpy()
            
            predicted_letter_index = np.argmax(probabilities)
            predicted_letter = self.alphabet_mapping[predicted_letter_index]

            return predicted_letter, probabilities
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            import traceback
            traceback.print_exc()
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
            "Please train the model first using the training script!\n" +
            "Make sure 'best_alphabet_model.pth' exists in the same folder."
        )
        root.destroy()
        
    def setup_gui(self):
        """Setup the GUI"""
        self.root = tk.Tk()
        self.root.title("PyTorch Alphabet Recognition - Fast CNN Model")
        self.root.geometry("800x600")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🔥 PyTorch Alphabet Recognition (A-Z)", 
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
        ttk.Button(draw_frame, text="🚀 Predict", 
                  command=self.predict_drawing).grid(row=1, column=1, padx=(5, 0))
        
        # Neural network output section
        neural_frame = ttk.LabelFrame(main_frame, text="Neural Network Output (26 Letters)", padding="15")
        neural_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Create letter display
        self.letter_frames = []
        self.letter_labels = []
        self.prediction_labels = []
        
        # Arrange 26 letters in rows
        letters_per_row = [6, 6, 6, 4, 4]
        current_letter = 0
        
        for row_idx, letters_in_row in enumerate(letters_per_row):
            for col_idx in range(letters_in_row):
                if current_letter >= 26:
                    break
                    
                letter = chr(65 + current_letter)
                
                # Frame for each letter
                letter_frame = ttk.Frame(neural_frame, relief='solid', borderwidth=1, padding="4")
                letter_frame.grid(row=row_idx, column=col_idx, padx=1, pady=1, sticky=(tk.W, tk.E))
                self.letter_frames.append(letter_frame)
                
                # Letter label
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
            for i in range(26):
                self.prediction_labels[i].config(text="0.0%", foreground='gray')
                self.letter_labels[i].config(foreground='gray')
                self.letter_frames[i].config(relief='solid', borderwidth=1)
        else:
            max_letter_index = np.argmax(predictions)
            max_confidence = predictions[max_letter_index]
            predicted_letter = chr(65 + max_letter_index)
            
            # Get top 3 predictions
            top_3_indices = np.argsort(predictions)[-3:][::-1]
            top_3_text = " | ".join([f"{chr(65+i)}({predictions[i]*100:.1f}%)" for i in top_3_indices])
            print(f"🎯 Prediction: {predicted_letter} | Top 3: {top_3_text}")
            
            # Update each letter's display
            for i in range(26):
                confidence = predictions[i] * 100
                self.prediction_labels[i].config(text=f"{confidence:.1f}%")
                
                if i == max_letter_index:
                    self.letter_labels[i].config(foreground='green')
                    self.prediction_labels[i].config(foreground='green')
                    self.letter_frames[i].config(relief='solid', borderwidth=3)
                else:
                    if confidence < 0.5:
                        color = 'lightgray'
                    elif confidence < 5.0:
                        color = 'gray'
                    else:
                        color = 'black'
                    self.letter_labels[i].config(foreground=color)
                    self.prediction_labels[i].config(foreground=color)
                    self.letter_frames[i].config(relief='solid', borderwidth=1)
            
            self.result_label.config(text=f"🎯 Prediction: {predicted_letter} (Confidence: {max_confidence*100:.1f}%)")
        
    def paint(self, event):
        """Handle drawing on canvas"""
        x, y = event.x, event.y
        r = 15
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='white', outline='white')
    
    def clear_canvas(self):
        """Clear the drawing canvas"""
        self.canvas.delete("all")
        self.result_label.config(text="Canvas cleared - draw a new letter")
        self.update_neural_display(None)
    
    def predict_drawing(self):
        """Predict the drawn letter"""
        try:
            canvas_items = self.canvas.find_all()
            if not canvas_items:
                self.result_label.config(text="Please draw something first!")
                self.update_neural_display(None)
                return
            
            # Create image from canvas
            img = Image.new('L', (250, 250), 0)
            draw = ImageDraw.Draw(img)
            
            for item in canvas_items:
                coords = self.canvas.coords(item)
                if len(coords) == 4:
                    draw.ellipse(coords, fill=255)
            
            # Resize to 28x28
            img = img.resize((28, 28), Image.Resampling.LANCZOS)
            img_array = np.array(img)
            
            # Predict
            letter, predictions = self.recognizer.predict_letter(img_array)
            if letter is not None and predictions is not None:
                self.update_neural_display(predictions)
            else:
                self.result_label.config(text="Could not make prediction")
                self.update_neural_display(None)
                
        except Exception as e:
            print(f"❌ Error in prediction: {e}")
            import traceback
            traceback.print_exc()
            self.result_label.config(text="Error - try redrawing")
            self.update_neural_display(None)
    
    def run(self):
        """Start the GUI"""
        if hasattr(self, 'root'):
            self.root.mainloop()

if __name__ == "__main__":
    print("🔥 Loading PyTorch Alphabet Recognition App...")
    print("🔍 Looking for trained model (best_alphabet_model.pth)...")
    
    app = AlphabetRecognitionGUI()
    if hasattr(app, 'root'):
        app.run()