import tkinter as tk
from tkinter import filedialog, messagebox
from EmbedLSB import ImageSteganography
import cv2

class StegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography App")
        self.root.geometry("600x500")  # Set window size
        self.root.resizable(False, False)  # Prevent resizing

        self.image = None
        self.key = None
        self.nonce = None

        # Create widgets for the UI
        self.create_widgets()

    def create_widgets(self):
        # Load Image Button
        self.load_image_button = tk.Button(self.root, text="Load Image", command=self.load_image, width=20, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        self.load_image_button.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Secret message input
        self.message_label = tk.Label(self.root, text="Enter secret message:", font=("Arial", 12))
        self.message_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.message_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.message_entry.grid(row=1, column=1, padx=10, pady=5)

        # Key input
        self.key_label = tk.Label(self.root, text="Enter key (Hex):", font=("Arial", 12))
        self.key_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.key_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.key_entry.grid(row=2, column=1, padx=10, pady=5)

        # Nonce input
        self.nonce_label = tk.Label(self.root, text="Enter nonce (Hex):", font=("Arial", 12))
        self.nonce_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.nonce_entry = tk.Entry(self.root, width=40, font=("Arial", 12))
        self.nonce_entry.grid(row=3, column=1, padx=10, pady=5)

        # Embed and Extract buttons
        self.embed_button = tk.Button(self.root, text="Embed Message", command=self.embed_message, width=20, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        self.embed_button.grid(row=4, column=0, padx=10, pady=20)

        self.extract_button = tk.Button(self.root, text="Extract Message", command=self.extract_message, width=20, bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
        self.extract_button.grid(row=4, column=1, padx=10, pady=20)

        # Decrypted message display
        self.decrypted_message_label = tk.Label(self.root, text="Decrypted message will appear here.", font=("Arial", 12, "italic"), fg="#555")
        self.decrypted_message_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def load_image(self):
        """ Load an image using a file dialog """
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image = cv2.imread(file_path)
            messagebox.showinfo("Image Loaded", "Image loaded successfully.")

    def embed_message(self):
        """ Embed the secret message into the image and save the stego image """
        message = self.message_entry.get()
        if not message or self.image is None:
            messagebox.showwarning("Missing Information", "Please enter a message and load an image.")
            return

        # Embed the message
        stego_image, self.key, self.nonce = ImageSteganography.embed_message(self.image, message)
        
        # Save the key and nonce to a file
        with open("key_nonce.txt", "w") as f:
            f.write(f"Key: {self.key.hex()}\n")
            f.write(f"Nonce: {self.nonce.hex()}\n")

        # Save the stego image as a PNG
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if output_path:
            cv2.imwrite(output_path, stego_image)
            messagebox.showinfo("Success", f"Message embedded and saved to {output_path}")
        
        # Display instructions to the user
        messagebox.showinfo("Key and Nonce Saved", "The key and nonce have been saved to 'key_nonce.txt'.\nPlease save this file securely.")

    def extract_message(self):
        """ Extract the secret message from the image using the key and nonce """
        if self.image is None:
            messagebox.showwarning("Missing Image", "Please load an image to extract the message.")
            return

        # Prompt the user to enter the key and nonce
        key_input = self.key_entry.get()
        nonce_input = self.nonce_entry.get()

        if not key_input or not nonce_input:
            messagebox.showwarning("Missing Information", "Please enter both key and nonce.")
            return

        try:
            # Convert the hex strings back to bytes for key and nonce
            key = bytes.fromhex(key_input)
            nonce = bytes.fromhex(nonce_input)
        except ValueError:
            messagebox.showerror("Invalid Format", "The key or nonce format is invalid. Please enter valid hex strings.")
            return

        # Extract the message
        try:
            extracted_message = ImageSteganography.extract_message(self.image, key, nonce)
            self.decrypted_message_label.config(text=f"Decrypted message: {extracted_message}")
            messagebox.showinfo("Extracted Message", f"Extracted message: {extracted_message}")
        except Exception as e:
            messagebox.showerror("Extraction Failed", f"An error occurred while extracting the message: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StegoApp(root)
    root.mainloop()
