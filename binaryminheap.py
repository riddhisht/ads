class MinHeapNode:
    def __init__(self, priority, value):
        self.priority = priority
        self.value = value

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, priority, value):
        node = MinHeapNode(priority, value)
        self.heap.append(node)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def is_empty(self):
        return len(self.heap) == 0

    def _heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index].priority < self.heap[parent_index].priority:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def _heapify_down(self, index):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest = index

        if left_child_index < len(self.heap) and self.heap[left_child_index].priority < self.heap[smallest].priority:
            smallest = left_child_index

        if right_child_index < len(self.heap) and self.heap[right_child_index].priority < self.heap[smallest].priority:
            smallest = right_child_index

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)
    
    def get_heap_elements(self):
        return [node.value for node in self.heap]

