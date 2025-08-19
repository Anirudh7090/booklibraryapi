import logging
from fastapi import FastAPI, HTTPException


logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI(
    title="Book Library Management API",
    description="API for managing a digital book library"
)


books_db = [
    {"id": 1, "title": "Book One", "author": "Alice", "description": "First book", "published_year": 2021},
    {"id": 2, "title": "Book Two", "author": "Bob", "description": "Second book", "published_year": 2020},
    {"id": 3, "title": "Book Three", "author": "Alice", "description": "Third book", "published_year": 2022}
]


def get_next_id():
    if books_db:
        return max(book["id"] for book in books_db) + 1
    return 1



@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    logging.info(f"GET /books/{book_id}")
    for book in books_db:
        if book["id"] == book_id:
            return book
    logging.error(f"Book with id {book_id} not found")
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/author/{author_name}")
def get_books_by_author(author_name: str):
    logging.info(f"GET /books/author/{author_name}")
    result = [book for book in books_db if book["author"].lower() == author_name.lower()]
    return result

@app.post("/books")
def create_book(book: dict):
    logging.info(f"POST /books - Creating book: {book}")
    book["id"] = get_next_id()
    books_db.append(book)
    return book

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: dict):
    logging.info(f"PUT /books/{book_id} - Updating book")
    for idx, book in enumerate(books_db):
        if book["id"] == book_id:
            updated_book["id"] = book_id
            books_db[idx] = updated_book
            return updated_book
    logging.error(f"Book with id {book_id} not found for update")
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    logging.info(f"DELETE /books/{book_id}")
    for idx, book in enumerate(books_db):
        if book["id"] == book_id:
            removed_book = books_db.pop(idx)
            return {"message": "Book deleted", "book": removed_book}
    logging.error(f"Book with id {book_id} not found for deletion")
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/")
def root():
    return {"message": "Book Library Management API is running!"}