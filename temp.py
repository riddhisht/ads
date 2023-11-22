import sys
from redblacktree import RedBlackTree, Node, Book
from binaryminheap import MinHeap


class GatorLibrary:
    def __init__(self):
        self.books_rb_tree = RedBlackTree()
        self.reservation_heap = MinHeap()

    #Method to print book details
    def PrintBook(self, book_id):
        # Search for the book in the Red-Black tree
        node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)

        if node != self.books_rb_tree.TNULL:
            print(f"BookID: '{node.book.book_id}' \nTitle: '{node.book.book_name}' \nAuthor: '{node.book.author_name}' \n"
                  f"Availability: '{'Yes' if node.book.availability_status else 'No'}'")
            if node.book.borrowed_by:
                print(f"Borrowed by: {', '.join(str(patron_id) for patron_id in node.book.borrowed_by)}")
            else:
                print("Borrowed by : None")
            print(f"Reservations: {node.book.reservation_heap.get_heap_elements()}\n\n")
        else:
            print(f"Book {book_id} not found in the Library \n")

    #Method to print books in a range
    def PrintBooks(self, book_id1, book_id2):
        # Iterate through the Red-Black tree and print books within the specified range
        self._print_books_range_helper(self.books_rb_tree.root, book_id1, book_id2)

    #Method to help print books in a range
    def _print_books_range_helper(self, node, book_id1, book_id2):
        if node != self.books_rb_tree.TNULL:
            if book_id1 < node.book.book_id:
                self._print_books_range_helper(node.left, book_id1, book_id2)

            if book_id1 <= node.book.book_id <= book_id2:
                print(f"BookID: '{node.book.book_id}' \nTitle: '{node.book.book_name}' \nAuthor: '{node.book.author_name}' \n"
                    f"Availability: '{'Yes' if node.book.availability_status else 'No'}'")
                if node.book.borrowed_by:
                    print(f"Borrowed by: {', '.join(str(patron_id) for patron_id in node.book.borrowed_by)}")
                else:
                    print("Borrowed by : None")
                print(f"Reservations: {node.book.reservation_heap.get_heap_elements()}\n\n")
            if book_id2 > node.book.book_id:
                self._print_books_range_helper(node.right, book_id1, book_id2)

    #Method to insert a book
    def InsertBook(self, book_id, book_name, author_name, availability_status=True, borrowed_by=None, reservation_heap=None):
        # Check if the book with the given ID already exists
        existing_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)
        if existing_node != self.books_rb_tree.TNULL:
            return

        # If not, create a new book and insert it into the Red-Black tree
        new_book = Book(book_id, book_name, author_name, availability_status, borrowed_by, reservation_heap)
        self.books_rb_tree.insert(book_id, new_book)

    #Method to borrow a book
    def BorrowBook(self, p_id, book_id, patron_priority):
        # Search for the book in the Red-Black tree
        book_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)

        if book_node == self.books_rb_tree.TNULL:
            print(f"Book {book_id} not found in the Library")
            return

        # Check if the book is available
        if book_node.book.availability_status:
            # Check if the patron already has the book in possession
            if p_id in book_node.book.borrowed_by:
                return

            # Update book status and borrower information
            book_node.book.availability_status = False
            book_node.book.borrowed_by.append(p_id)
            print(f"Book {book_id} Borrowed by Patron {p_id}\n")
        else:
            # Book is not available, create a reservation node in the heap
            reservation_heap = book_node.book.reservation_heap
            reservation_heap.insert(patron_priority, p_id)
            print(f"Book {book_id} Reserved by Patron {p_id}\n")

    #Method to count the number of flips in color
    def ColorFlipCount(self):
        count = self.books_rb_tree.color_flip_count
        print("Colour Flip Count: ",count, "\n")
        return count
    
    # Original method to delete a book
    def DeleteBook(self, book_id):
        # Search for the book in the Red-Black tree
        book_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)

        if book_node == self.books_rb_tree.TNULL:
            print(f"Book {book_id} not found in the Library")
            return

        # Notify patrons in the reservation list that the book is no longer available
        reservation_heap = book_node.book.reservation_heap
        if reservation_heap.is_empty():
            print(f"Book {book_id} is no longer available\n")
        else:
            print(f"Book {book_id} is no longer available. Reservations made by Patrons ", end="")
            while not reservation_heap.is_empty():
                reservation_node = reservation_heap.extract_min()
                p_id = reservation_node.value
                print(p_id, ", ", end="")
            print("have been cancelled! \n")
        
        # Delete the book from the Red-Black tree
        self.books_rb_tree.delete_node(book_id)

    # New function to handle the notification logic
    def notify_patrons(self, book_id):
        # Search for the book in the Red-Black tree
        book_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)

        if book_node == self.books_rb_tree.TNULL:
            print(f"Book {book_id} not found in the Library")
            return

        # Notify patrons in the reservation list that the book is no longer available
        reservation_heap = book_node.book.reservation_heap
        if reservation_heap.is_empty():
            print(f"Book {book_id} is no longer available\n")
        else:
            print(f"Book {book_id} is no longer available. Reservations made by Patrons ", end="")
            while not reservation_heap.is_empty():
                reservation_node = reservation_heap.extract_min()
                p_id = reservation_node.value
                print(p_id, ", ", end="")
            print("have been cancelled! \n")

    # Method to find the closest book
    def FindClosestBook(self, target_id):
        # Call the corresponding method in the Red-Black tree class
        closest_books = self.books_rb_tree.find_closest_books(target_id)

        if closest_books:
            book_count = list(closest_books.keys())
            actual_close = self.determine_actual_close(target_id, book_count)
            
            for book_id in actual_close:
                self.PrintBook(book_id)
        else:
            print("No books found in the Library.")

    # Helper method to determine the actual closest books
    def determine_actual_close(self, target_id, book_count):
        actual_close = []
        
        if len(book_count) > 1:
            small = abs(target_id - book_count[0])
            large = abs(book_count[1] - target_id)
            
            if small!=large:
                if small<large:
                    actual_close = [book_count[0]]
                else:
                    actual_close = [book_count[1]]
            else:
                actual_close = [book_count[0], book_count[1]]

        if len(book_count)==1:
            actual_close = [book_count[0]]

        return actual_close

    #Method to Quit the program
    def Quit(self):
        print("Program Terminated!!")
        exit()

    #Method to read the input
    def readInput(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                return lines

        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # #Method to return a book
    def ReturnBook(self, p_id, book_id):
        # Search for the book in the Red-Black tree
        book_node = self.books_rb_tree.search_tree_helper(self.books_rb_tree.root, book_id)

        if book_node == self.books_rb_tree.TNULL:
            print(f"Book {book_id} not found in the Library")
            return

        # Check if the patron has borrowed the book
        if p_id not in book_node.book.borrowed_by:
            return

        # Update book status and borrower information
        book_node.book.availability_status = True
        book_node.book.borrowed_by.remove(p_id)

        # Assign the book to the patron with the highest priority in the reservation heap (if available)
        reservation_heap = book_node.book.reservation_heap
        if not reservation_heap.is_empty():
            reservation_node = reservation_heap.extract_min()
            next_p_id = reservation_node.value
            book_node.book.availability_status = False
            book_node.book.borrowed_by.append(next_p_id)
            print(f"Book {book_id} Returned by Patron {p_id}\n")
            print(f"Book {book_id} Allotted to Patron {next_p_id}\n")

        else:
            print(f"Book {book_id} Returned by Patron {p_id}\n")

# Main function
if __name__ == "__main__":
    library = GatorLibrary()

    filepath = sys.argv[1]
    name = filepath.split('.')[0]
    lines = library.readInput(filepath)
    with open(f'{name}_output_file.txt', 'w') as file:

        import sys
        sys.stdout = file
        for line in lines:
            line = 'library.'+line
            
            exec(line)
