import os

from config.settings.base import BOOKS_ROOT_DIR

class BookReader:
    def __init__(self, book_name, chapter):
        self.book_name = book_name
        self.chapter_num = chapter
        self.root_dir = BOOKS_ROOT_DIR

    def read_book(self):
        if "great expectations" in self.book_name: 
            chapter_path = os.path.join(BOOKS_ROOT_DIR, "great expectations", f"{self.chapter_num}.txt")

            if os.path.exists(chapter_path):
                with open (chapter_path, "r", encoding="utf-8") as f:
                    chapter = f.read()
                
                response = f"You are reading {self.book_name}, Chapter {self.chapter_num}: \n\n {chapter}"
            else:
                response = f"I'm sorry this chapter of the book {self.book_name} either does not exist or I have no access to it."
        else:
            response = f"I'm sorry the book {self.book_name} either does not exist or I have no access to it."
        
        return response