import os
import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class EloRankingSystem:
    def __init__(self, k=32):
        self.k = k
        self.players = {}
        self.rankings_file = ""
        
    def load_rankings(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    player, rating = line.strip().split(':')
                    self.players[player.strip()] = int(rating.strip())
            print("Rankings loaded from", file_path)
            self.rankings_file = file_path
        else:
            print("No existing rankings file found at", file_path)

    def add_player(self, player_id, rating=1500):
        self.players[player_id] = rating

    def get_rating(self, player_id):
        return self.players.get(player_id, 1500)

    def update_rating(self, winner_id, loser_id):
        print("Updating rating")  # Debugging statement
        winner_rating = self.get_rating(winner_id)
        loser_rating = self.get_rating(loser_id)

        expected_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
        expected_loser = 1 / (1 + 10 ** ((winner_rating - loser_rating) / 400))

        self.players[winner_id] = round(winner_rating + self.k * (1 - expected_winner))
        self.players[loser_id] = round(loser_rating + self.k * (0 - expected_loser))

    def save_rankings(self):
        if self.rankings_file:
            print("Saving rankings to", self.rankings_file)  # Debugging statement
            with open(self.rankings_file, 'w') as file:
                for player, rating in self.players.items():
                    file.write(f"{player}: {rating}\n")
        else:
            print("No rankings file path specified.")

class ImageComparisonTool:
    def __init__(self, root):
        self.root = root
        self.images_folder = ""
        self.image_list = []
        self.current_pair = []
        self.elo_system = EloRankingSystem()

        self.label = tk.Label(root, text="Image Comparison Tool")
        self.label.pack()

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_images)
        self.browse_button.pack()

        self.start_button = tk.Button(root, text="Start Comparison", command=self.run_comparison)
        self.start_button.pack(pady=10)

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

    def browse_images(self):
        folder_path = filedialog.askdirectory(title="Select Image Folder")
        if folder_path:
            self.images_folder = folder_path
            rankings_file = os.path.join(self.images_folder, "elo_rankings.txt") 
            self.elo_system.load_rankings(rankings_file)
            self.image_list = os.listdir(self.images_folder)
            self.label.config(text=f"Selected folder: {self.images_folder}")

    def get_random_image_pair(self):
        random.shuffle(self.image_list)
        self.current_pair = self.image_list[:2]
        print("Current pair:", self.current_pair)  # Debugging statement
        return self.current_pair

    def compare_images(self, winner_id):
        print("Winner ID:", winner_id)  # Debugging statement
        loser_id = self.current_pair[1] if winner_id == self.current_pair[0] else self.current_pair[0]
        print("Loser ID:", loser_id)  # Debugging statement
        self.elo_system.update_rating(winner_id, loser_id)
        self.elo_system.save_rankings()
        self.get_random_image_pair()
        self.show_images()

    def show_images(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()
        max_width = 600
        max_height = 600

        for i, image_id in enumerate(self.current_pair):
            image_path = os.path.join(self.images_folder, image_id)

            try:
                image = Image.open(image_path)
                width, height = image.size
                aspect_ratio = width / height

                if width > max_width or height > max_height:
                    if aspect_ratio > 1:
                        width = max_width
                        height = int(width / aspect_ratio)
                    else:
                        height = max_height
                        width = int(height * aspect_ratio)

                image = image.resize((width, height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
                continue

            label = tk.Label(self.canvas, image=photo)
            label.image = photo
            label.grid(row=0, column=i)

            button = tk.Button(self.canvas, text=f"Select {image_id}", command=lambda i=i: self.compare_images(self.current_pair[i]))
            button.grid(row=1, column=i)  
        self.canvas.update()
        self.root.bind("<Left>", lambda event: self.compare_images(self.current_pair[0]))
        self.root.bind("<Right>", lambda event: self.compare_images(self.current_pair[1]))


    def run_comparison(self):
        print("Run comparison called")  # Debugging statement
        if not self.image_list or len(self.image_list) < 2:
            messagebox.showinfo("Error", "Please select at least two images in the folder.")
            return

        self.get_random_image_pair()
        self.show_images()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Comparison Tool")
    root.geometry("400x300")

    comparison_tool = ImageComparisonTool(root)

    root.mainloop()
