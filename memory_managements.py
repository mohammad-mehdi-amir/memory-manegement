import matplotlib.pyplot as plt
from collections import deque

class Process:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.pages = []

class MemoryManager:
    def __init__(self, total_memory, page_size):
        self.total_memory = total_memory
        self.page_size = page_size
        self.num_pages = total_memory // page_size
        self.memory = [None] * self.num_pages
        self.page_faults = 0
        self.page_access_sequence = []

    def allocate_memory(self, process, algorithm="First Fit"):
        required_pages = -(-process.size // self.page_size) 
        
        if algorithm == "First Fit":
            self.first_fit(process, required_pages)
        elif algorithm == "Best Fit":
            self.best_fit(process, required_pages)
        elif algorithm == "Worst Fit":
            self.worst_fit(process, required_pages)

    def first_fit(self, process, required_pages):
        free_block_start = -1
        free_count = 0

        for i in range(self.num_pages):
            if self.memory[i] is None:
                if free_block_start == -1:
                    free_block_start = i
                free_count += 1
                if free_count == required_pages:
                    for j in range(free_block_start, free_block_start + required_pages):
                        self.memory[j] = process.name
                        process.pages.append(j)
                    return True
            else:
                free_block_start = -1
                free_count = 0
        print(f"Not enough memory for process {process.name}")
        return False

    def best_fit(self, process, required_pages):
        best_block_start = -1
        best_block_size = float('inf')
        current_block_start = -1
        current_block_size = 0

        for i in range(self.num_pages):
            if self.memory[i] is None:
                if current_block_start == -1:
                    current_block_start = i
                current_block_size += 1
            else:
                if current_block_size >= required_pages and current_block_size < best_block_size:
                    best_block_start = current_block_start
                    best_block_size = current_block_size
                current_block_start = -1
                current_block_size = 0

        if current_block_size >= required_pages and current_block_size < best_block_size:
            best_block_start = current_block_start

        if best_block_start != -1:
            for j in range(best_block_start, best_block_start + required_pages):
                self.memory[j] = process.name
                process.pages.append(j)
            return True

        print(f"Not enough memory for process {process.name}")
        return False

    def worst_fit(self, process, required_pages):
        worst_block_start = -1
        worst_block_size = 0
        current_block_start = -1
        current_block_size = 0

        for i in range(self.num_pages):
            if self.memory[i] is None:
                if current_block_start == -1:
                    current_block_start = i
                current_block_size += 1
            else:
                if current_block_size >= required_pages and current_block_size > worst_block_size:
                    worst_block_start = current_block_start
                    worst_block_size = current_block_size
                current_block_start = -1
                current_block_size = 0

        if current_block_size >= required_pages and current_block_size > worst_block_size:
            worst_block_start = current_block_start

        if worst_block_start != -1:
            for j in range(worst_block_start, worst_block_start + required_pages):
                self.memory[j] = process.name
                process.pages.append(j)
            return True

        print(f"Not enough memory for process {process.name}")
        return False

    def access_page(self, process_name, page_number):
        if any(self.memory[page] == process_name for page in range(len(self.memory))):
            print(f"Page {page_number} for process {process_name} is in memory.")
        else:
            print(f"Page fault occurred for process {process_name}, page {page_number}!")
            self.page_faults += 1

    def display_memory(self):
        print("Memory Status:")
        print(self.memory)

    def plot_memory(self):
        plt.figure(figsize=(10, 2))
        for i, page in enumerate(self.memory):
            color = 'blue' if page is not None else 'white'
            plt.bar(i, 1, color=color, edgecolor='black')
            plt.text(i, 0.5, page if page is not None else 'Free', ha='center', va='center')
        plt.title("Memory Allocation")
        plt.xlabel("Page Number")
        plt.ylabel("Status")
        plt.show()


memory_manager = MemoryManager(total_memory=100, page_size=10)
process_a = Process("A", 40)
process_b = Process("B", 30)
process_c = Process("C", 50)

memory_manager.allocate_memory(process_b, algorithm="Best Fit")
memory_manager.allocate_memory(process_a, algorithm="First Fit")
memory_manager.display_memory()
memory_manager.plot_memory()

memory_manager.access_page("A", 1)
memory_manager.access_page("C", 1)