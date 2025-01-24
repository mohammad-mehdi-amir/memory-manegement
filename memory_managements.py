class MemoryManagementSimulator:
    def __init__(self, total_memory_size, page_size, allocation_algo, replacement_algo):
        self.total_memory_size = total_memory_size
        self.page_size = page_size
        self.allocation_algo = allocation_algo
        self.replacement_algo = replacement_algo
        self.memory = []  
        self.process_pages = {}  
        self.page_faults = {}  

    def allocate_memory(self, processes):
        remaining_memory = self.total_memory_size
        print("Initial Memory Allocation:")
        print(f"- Total Memory Size: {self.total_memory_size} MB")

        for process, size in processes.items():
            num_pages = -(-size // self.page_size)  # Calculate number of pages

            if remaining_memory >= size:
                self.process_pages[process] = [f"{process}{i+1}" for i in range(num_pages)]
                remaining_memory -= size
                print(f"- Allocated to {process}: {size} MB ({num_pages} pages)")
            else:
                self.process_pages[process] = []
                print(f"- Remaining Memory for {process}: {remaining_memory} MB")

        print()

    def simulate_page_access(self, page_access_sequence):
        print("Starting Page Access Sequence...\n")
        
        for step, (process, page_num) in enumerate(page_access_sequence, start=1):
            page = f"{process}{page_num}"

            if page in self.memory:
                print(f"{step}. Accessing {process}, Page {page_num}")
                print("   - Page already in memory (no page fault)")
            else:
                print(f"{step}. Accessing {process}, Page {page_num}")
                print("   - Page fault! Page not in memory")

                if len(self.memory) < self.total_memory_size // self.page_size:
                    self.memory.append(page)
                else:
                    replaced_page = self.replace_page(page)
                    print(f"   - Applying {self.replacement_algo} replacement")
                    print(f"   - Replaced {replaced_page} with {page}")
                    
                if process not in self.page_faults:
                    self.page_faults[process] = 0

                self.page_faults[process] += 1

            print(f"   - Memory Status: {self.memory}\n")

    def replace_page(self, new_page):
        if self.replacement_algo == "FIFO":
            replaced_page = self.memory.pop(0)
        elif self.replacement_algo == "LRU":
            replaced_page = self.memory.pop(0)  
        elif self.replacement_algo == "Optimal":
            replaced_page = self.memory.pop(-1)  
        elif self.replacement_algo == "Clock":
            replaced_page = self.memory.pop(0)  
        elif self.replacement_algo == "NRU":
            replaced_page = self.memory.pop(0)  
        
        self.memory.append(new_page)
        return replaced_page

    def print_statistics(self):
        print("Final Statistics:")
        print(f"- Total Page Faults: {sum(self.page_faults.values())}")
        print(f"- Final Memory Status: {self.memory}")

        print("- Page Faults by Process:")
        for process, faults in self.page_faults.items():
            print(f"  {process} = {faults}")



total_memory_size = 100
page_size = 10
allocation_algo = "First Fit"
replacement_algo = "LRU"
processes = {
    "Process A": 40,
    "Process B": 30,
    "Process C": 50
}
page_access_sequence = [
    ["Process A", 1],
    ["Process B", 1],
    ["Process A", 2],
    ["Process C", 1],
    ["Process A", 3],
    ["Process C", 2],
    ["Process B", 2],
    ["Process C", 3],
    ["Process A", 4],
    ["Process C", 4],
    ["Process B", 3],
    ["Process C", 5]
]

simulator = MemoryManagementSimulator(total_memory_size, page_size, allocation_algo, replacement_algo)
simulator.allocate_memory(processes)
simulator.simulate_page_access(page_access_sequence)
simulator.print_statistics()
