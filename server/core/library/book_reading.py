import os

from config.settings.base import BOOKS_ROOT_DIR
from core.models import BookReader as BookDB


class BookReader:
    def __init__(self, book_name, chapter, user):
        self.book_name = book_name
        self.chapter_num = chapter
        self.user = user
        self.response = str()
        last_read_book = BookDB.objects.filter(user=user)
        self.template = "{}, Chapter {}:\n\n\n{}"

        if "none" in self.book_name.lower():
            self.book_name = "Great Expectations"

        if self.__check_availabilty():

            if self.chapter_num == -1:
                if last_read_book.exists():
                    self.chapter_num = last_read_book[0].chapter + 1
                else:
                    self.chapter_num = 1

    def __get_available_books(self):
        return ["great expectations"]

    def __check_availabilty(self):
        available_books = self.__get_available_books()

        for book in available_books:
            if book in self.book_name.lower():
                return book
        return None

    def read_book(self):
        libray_book_name = self.__check_availabilty()
        print(self.book_name, libray_book_name, self.chapter_num)
        if libray_book_name:
            chapter_path = os.path.join(
                BOOKS_ROOT_DIR, libray_book_name, f"{self.chapter_num}.txt"
            )

            if os.path.exists(chapter_path):
                with open(chapter_path, "r", encoding="utf-8") as f:
                    chapter = f.read()

                response = self.template.format(
                    self.book_name, self.chapter_num, chapter
                )
                if BookDB.objects.filter(user=self.user).exists():
                    obj = BookDB.objects.get(user=self.user)
                    obj.last_book_read = self.book_name
                    obj.chapter = self.chapter_num
                    obj.save()
                else:
                    BookDB.objects.create(
                        user=self.user,
                        last_book_read=self.book_name,
                        chapter=self.chapter_num,
                    )
            else:
                response = f"I'm sorry this chapter of the book {self.book_name} either does not exist or I have no access to it."
        else:
            book_list = "\n".join(self.__get_available_books())
            response = f"I only have access to these books:\n{book_list}"

        return response
