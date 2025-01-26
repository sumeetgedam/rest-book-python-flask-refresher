from flask import Flask
import pytest
from books.app import app, fake_db

isbn = "234355"

book = {
    "author" : "Elements of Programming Interviews",
    "isbn": isbn,
    "title": "Tsung-Hsien Lee"

}

@pytest.fixture()
def test_app():

    app.config.update({
        "TESTING": True,
    })

    fake_db.clear()

    yield app


@pytest.fixture()
def client(test_app: Flask):
    return test_app.test_client()

@pytest.fixture()
def runner(test_app: Flask):
    return test_app.test_cli_runner()


def test_create_book_return_http_201_created(client):
    response = _put_book(client, isbn , book)

    assert response.status_code == 201

def _put_book(client, isbn, book):
    return client.put(
        f"/books/{isbn}",
        json=book
    )

def test_read_retrieve_not_exists_returns_http_404(client):
    response = _get_book(client, isbn)

    assert response.status_code == 404

def _get_book(client, isbn):
    return client.get(
        f"/books/{isbn}"
    )

def test_read_retrieve_exists_returns_book_http_200(client):

    _put_book(client, isbn, book)

    response = client.get(
        f"/books/{isbn}"
    )

    assert response.status_code == 200
    assert response.json == book

def test_read_list_empty_returns_https_200(client):
   
    response = client.get(
        f"/books"
    )

    assert response.status_code == 200
    assert response.json == []



def test_read_list_returns_books_https_200(client):
   
   _put_book(client, isbn, book)
   
   response = client.get(
        f"/books"
   )

   assert response.status_code == 200
   assert response.json == [book]

def test_update_returns_http_200(client):
    response = _put_book(client, isbn, book)

    assert response.status_code == 201

    response = _get_book(client, isbn)
    assert response.json == book

    updated_book = book.copy()
    updated_book['title'] = 'Interview Book'

    response = _put_book(client, isbn, updated_book)
    assert response.status_code == 200

    response = _get_book(client, isbn)
    assert response.json == updated_book


def test_delete_returns_http_404_book_not_exists(client):

    response = client.delete(
        f"/books/{isbn}"
    )

    assert response.status_code == 404
    
def test_delete_returns_http_204_book_exists(client):

    _put_book(client, isbn, book)

    response = client.delete(
        f"/books/{isbn}"
    )

    assert response.status_code == 204

    response = _get_book(client, isbn)
    assert response.status_code == 404