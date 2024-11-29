import tkinter as tk
from tkinter import messagebox
import subprocess
import threading


class RaftManager:
    def __init__(self, root):
        self.root = root
        self.root.title("RAFT Node Manager")
        self.nodes = {}  # Lưu trạng thái của các nút
        self.node_processes = {}  # Lưu các tiến trình node đang chạy
        self.node_id_counter = 0  # ID tự động tăng cho các nút

        # Tạo giao diện chính
        self.setup_ui()

    def setup_ui(self):
        # Frame cho danh sách nút
        self.node_frame = tk.Frame(self.root)
        self.node_frame.pack(pady=10)

        self.node_list = tk.Listbox(self.node_frame, width=50, height=10)
        self.node_list.pack(side=tk.LEFT, padx=10)

        self.scrollbar = tk.Scrollbar(self.node_frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.node_list.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.node_list.config(yscrollcommand=self.scrollbar.set)

        # Frame cho các nút điều khiển
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.add_button = tk.Button(
            self.control_frame, text="Add Node", command=self.add_node
        )
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(
            self.control_frame, text="Remove Node", command=self.remove_node
        )
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.toggle_button = tk.Button(
            self.control_frame, text="Toggle Node", command=self.toggle_node
        )
        self.toggle_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = tk.Button(
            self.control_frame, text="Restart All", command=self.restart_all
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(
            self.control_frame, text="Stop All", command=self.stop_all
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Frame cho thông tin trạng thái
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(pady=10)

        self.status_label = tk.Label(
            self.status_frame, text="Status: No nodes running", fg="blue"
        )
        self.status_label.pack()

    def add_node(self):
        """Thêm một nút mới."""
        node_id = self.node_id_counter
        port = 50050 + node_id
        self.nodes[node_id] = {"port": port, "status": "active"}

        # Chạy tiến trình nút
        process = subprocess.Popen(
            ["python", "raft_node.py", str(node_id)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.node_processes[node_id] = process

        # Cập nhật danh sách
        self.node_list.insert(tk.END, f"Node {node_id} (Port: {port}) - Active")
        self.node_id_counter += 1
        self.update_status()

    def remove_node(self):
        """Xóa một nút."""
        selected = self.node_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a node to remove.")
            return

        node_index = selected[0]
        node_info = self.node_list.get(node_index)
        node_id = int(node_info.split()[1])

        # Dừng tiến trình nút
        if node_id in self.node_processes:
            self.node_processes[node_id].terminate()
            del self.node_processes[node_id]

        # Cập nhật danh sách
        del self.nodes[node_id]
        self.node_list.delete(node_index)
        self.update_status()

    def toggle_node(self):
        """Bật hoặc tắt một nút."""
        selected = self.node_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a node to toggle.")
            return

        node_index = selected[0]
        node_info = self.node_list.get(node_index)
        node_id = int(node_info.split()[1])

        if self.nodes[node_id]["status"] == "active":
            self.nodes[node_id]["status"] = "inactive"
            self.node_list.delete(node_index)
            self.node_list.insert(
                node_index,
                f"Node {node_id} (Port: {self.nodes[node_id]['port']}) - Inactive",
            )
        else:
            self.nodes[node_id]["status"] = "active"
            self.node_list.delete(node_index)
            self.node_list.insert(
                node_index,
                f"Node {node_id} (Port: {self.nodes[node_id]['port']}) - Active",
            )

        self.update_status()

    def restart_all(self):
        """Khởi động lại tất cả các nút."""
        self.stop_all()
        for _ in range(len(self.nodes)):
            self.add_node()

    def stop_all(self):
        """Dừng tất cả các nút."""
        for node_id, process in self.node_processes.items():
            process.terminate()

        self.node_processes.clear()
        self.nodes.clear()
        self.node_list.delete(0, tk.END)
        self.update_status()

    def update_status(self):
        """Cập nhật trạng thái."""
        if not self.nodes:
            self.status_label.config(text="Status: No nodes running", fg="red")
        else:
            self.status_label.config(
                text=f"Status: {len(self.nodes)} nodes running", fg="green"
            )


def main():
    root = tk.Tk()
    app = RaftManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
