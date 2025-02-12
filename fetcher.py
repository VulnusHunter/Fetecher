import os
import threading
import requests
import json
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import exifread

class Fetcher:
    def __init__(self):
        self.supported_sites = [
            "https://twitter.com/{}",
            "https://instagram.com/{}",
            "https://github.com/{}",
            "https://www.reddit.com/user/{}"
            
        ]
    
    def extract_metadata(self, image_path):
        metadata = {}
        with open(image_path, 'rb') as img_file:
            tags = exifread.process_file(img_file)
            for tag, value in tags.items():
                metadata[tag] = str(value)
        return metadata
    
    def check_username(self, username):
        results = {}
        threads = []

        def fetch(site):
            url = site.format(username)
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    results[url] = "Found"
                else:
                    results[url] = "Not Found"
            except requests.RequestException:
                results[url] = "Error"

        for site in self.supported_sites:
            thread = threading.Thread(target=fetch, args=(site,))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()
        
        return results
    
    def export_metadata(self, metadata, export_path, filetype="json"):
        if filetype == "json":
            with open(export_path, 'w') as json_file:
                json.dump(metadata, json_file, indent=4)
        elif filetype == "csv":
            with open(export_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                for key, value in metadata.items():
                    writer.writerow([key, value])

class FetcherGUI:
    def __init__(self, root):
        self.fetcher = Fetcher()
        self.root = root
        self.root.title("Fetcher - Metadata Extractor & Username Crawler")
        
        self.label = tk.Label(root, text="Select an Image:")
        self.label.pack()
        
        self.button = tk.Button(root, text="Browse", command=self.load_image)
        self.button.pack()
        
        self.text = tk.Text(root, height=10, width=50)
        self.text.pack()
        
        self.export_button = tk.Button(root, text="Export Metadata", command=self.export_metadata)
        self.export_button.pack()
        
        self.username_label = tk.Label(root, text="Enter Username:")
        self.username_label.pack()
        
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()
        
        self.username_button = tk.Button(root, text="Check Username", command=self.check_username)
        self.username_button.pack()
        
        self.result_text = tk.Text(root, height=5, width=50)
        self.result_text.pack()
    
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            metadata = self.fetcher.extract_metadata(file_path)
            self.text.delete(1.0, tk.END)
            for key, value in metadata.items():
                self.text.insert(tk.END, f"{key}: {value}\n")
            self.current_metadata = metadata
    
    def export_metadata(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("CSV", "*.csv")])
        if file_path:
            filetype = "json" if file_path.endswith(".json") else "csv"
            self.fetcher.export_metadata(self.current_metadata, file_path, filetype)
            messagebox.showinfo("Success", "Metadata exported successfully!")
    
    def check_username(self):
        username = self.username_entry.get().strip()
        if username:
            results = self.fetcher.check_username(username)
            self.result_text.delete(1.0, tk.END)
            for site, status in results.items():
                self.result_text.insert(tk.END, f"{site}: {status}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = FetcherGUI(root)
    root.mainloop()
