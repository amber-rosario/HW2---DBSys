import os
import re
from pymongo import MongoClient
from datetime import datetime


# Validation functions
def validate_name(name):
    return bool(name)


def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def validate_phone(phone):
    return phone.isdigit() and len(phone) >= 10


def validate_address(address):
    return bool(address)


# CRUD operations
def create_document(collection):
    while True:
        name = input("Enter name: ")
        if validate_name(name):
            break
        print("Name cannot be empty.")

    while True:
        email = input("Enter email: ")
        if validate_email(email):
            break
        print("Invalid email format. Please try again.")

    while True:
        phone = input("Enter phone (digits only, at least 10 characters): ")
        if validate_phone(phone):
            break
        print("Invalid phone number. Must contain only digits and be at least 10 characters long.")

    while True:
        address = input("Enter address: ")
        if validate_address(address):
            break
        print("Address cannot be empty.")

    document = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "created_at": datetime.now()
    }

    try:
        collection.insert_one(document)
        print("Document created successfully.")
    except Exception as e:
        print(f"Error creating document: {e}")


def read_documents(collection):
    try:
        documents = list(collection.find())
        if not documents:
            print("No documents found.")
            return

        print(f"{'Name':<20} {'Email':<30} {'Phone':<15} {'Address':<50} {'Created At':<20}")
        print("-" * 145)

        for doc in documents:
            print(
                f"{doc['name']:<20} {doc['email']:<30} {doc['phone']:<15} {doc['address']:<50} {doc['created_at']:<20}")
    except Exception as e:
        print(f"Error reading documents: {e}")


def update_document(collection):
    name = input("Enter the name of the person to update: ")
    document = collection.find_one({"name": name})
    if document:
        print(f"Found document: {document}")
        # Proceed to update, similar to create_document
    else:
        print(f"No document found with the name '{name}'.")


def delete_document(collection):
    name = input("Enter the name of the person to delete: ")
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print("Delete Successful!")
        else:
            print("No document found with that name!")
    except Exception as e:
        print(f"Error deleting document: {e}")


def main():
    # Create a MongoClient instance
    client = MongoClient("mongodb://localhost:27017")

    # Access the database and collection
    database = client['testdb']
    collection = database['testcollection']

    while True:
        print("\nChoose an operation:")
        print("1. Create a document")
        print("2. Read documents")
        print("3. Update a document")
        print("4. Delete a document")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_document(collection)
        elif choice == "2":
            read_documents(collection)
        elif choice == "3":
            update_document(collection)
        elif choice == "4":
            delete_document(collection)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

    client.close()


if __name__ == "__main__":
    main()
