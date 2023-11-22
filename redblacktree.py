
from binaryminheap import MinHeap, MinHeapNode
class Node:
    def __init__(self, book):
        self.book = book
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1  # 1 for red, 0 for black

class Book:
    def __init__(self, book_id, book_name, author_name, availability_status=True, borrowed_by=None, reservation_heap=None):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = borrowed_by or []
        self.reservation_heap = MinHeap() if reservation_heap is None else reservation_heap

    def __str__(self):
        return f"Book ID: {self.book_id}, Title: {self.book_name}, Author: {self.author_name}, Available: {self.availability_status}"
    
class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(None)
        self.TNULL.color = 0  # Set color of TNULL to black
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.color_flip_count = 0

    # Search the tree
    def search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.book.book_id:
            return node

        if key < node.book.book_id:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    # Balance the tree after deletion
    def fix_delete(self, x):
        while x != self.root and x.color == 0:
            # self.color_flip_count +=1
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.color_flip_count +=1
                    self.left_rotate(x.parent)
                    s = x.parent.right
                    
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.color_flip_count +=1
                        self.right_rotate(s)
                        s = x.parent.right
                        

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.color_flip_count +=1
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.color_flip_count +=1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.color_flip_count +=1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.color_flip_count +=1
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 0

    # Balance the tree after insertion of a node
    def fix_insert(self, k):
        while k.parent.color == 1:
            
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # uncle
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                    self.color_flip_count +=1
                    self.color_flip_count +=1
                    
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.color_flip_count +=1
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1 
                    self.color_flip_count +=1    
                    self.color_flip_count +=1 
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # uncle
                
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent  # move x up
                    self.color_flip_count += 1
                    self.color_flip_count +=1
                    self.color_flip_count +=1 
                    
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.color_flip_count +=1
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.color_flip_count += 1
                    self.color_flip_count +=1
                    self.right_rotate(k.parent.parent)

            if k == self.root:
                break
        self.root.color = 0

    #Left rotate the tree
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    #Right rotate the tree
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    #Insert a node
    def insert(self, key, book):
        node = Node(book)
        node.parent = None
        node.book = book
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1  # new node must be red

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.book.book_id < x.book.book_id:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == None:
            self.root = node
        elif node.book.book_id < y.book.book_id:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return
        
        self.fix_insert(node)

    #Get min value node
    def get_min_value_node(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    #Get max value node
    def get_max_value_node(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    #Delete a node
    def delete_node(self, key):
        self.delete_node_helper(self.root, key)

    #Helper method to delete a node
    def delete_node_helper(self, root, key):
        z = self.TNULL
        while root != self.TNULL:
            if root.book.book_id == key:
                z = root

            if root.book.book_id <= key:
                root = root.right
            else:
                root = root.left

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.get_min_value_node(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 0:
            self.fix_delete(x)

    #Transplant a node
    def transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    #Method to find the closest book
    def find_closest_books(self, target_id):
        closest_books = {}
        closest_lower = self.find_closest_lower(self.root, target_id)
        closest_higher = self.find_closest_higher(self.root, target_id)
        if closest_lower is not None:
            closest_books[closest_lower.book.book_id] = {
                'book_name': closest_lower.book.book_name,
                'author_name': closest_lower.book.author_name,
                'availability_status': closest_lower.book.availability_status
            }

        if closest_higher is not None:
            closest_books[closest_higher.book.book_id] = {
                'book_name': closest_higher.book.book_name,
                'author_name': closest_higher.book.author_name,
                'availability_status': closest_higher.book.availability_status
            }

        return closest_books

    #Find the closest lower node
    def find_closest_lower(self, node, target_id):
        current_closest = None

        while node != self.TNULL:
            if node.book.book_id == target_id:
                return node
            elif node.book.book_id < target_id:
                current_closest = node
                node = node.right
            else:
                node = node.left

        return current_closest

    #Find the closest higher node
    def find_closest_higher(self, node, target_id):
        current_closest = None

        while node != self.TNULL:
            if node.book.book_id == target_id:
                return node
            elif node.book.book_id > target_id:
                current_closest = node
                node = node.left
            else:
                node = node.right

        return current_closest

