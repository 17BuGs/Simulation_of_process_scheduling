from PCB import PCB
from PCBQueue import PCBQueue


def read_file(file_path, type):
    """
    从文件读取进程信息，并创建相应的 PCB 对象并加入 PCB 队列中。

    参数:
    - file_path: 文件路径
    - type: 进程类型，可以是 'ready' 或 'block'

    返回值:
    - PCBQueue 对象，包含从文件读取的 PCB 对象

    异常:
    - FileNotFoundError: 如果文件路径无效或文件不存在，则引发该异常
    - ValueError: 如果文件内容格式不正确，则引发该异常
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    pcb_queue = PCBQueue()
    if type == 'ready':
        for line in lines:
            parts = line.strip().split()  # 分割字符串成多个部分
            pid = int(parts[0])
            priority = int(parts[1])
            all_time = int(parts[2])
            running2block_time = int(parts[3])
            pcb = PCB(pid,
                      priority,
                      all_time,
                      running2block_time=running2block_time,
                      state='READY')
            pcb_queue.enqueue(pcb)
    elif type == 'block':
        for line in lines:
            parts = line.strip().split()  # 分割字符串成多个部分
            pid = int(parts[0])
            priority = int(parts[1])
            all_time = int(parts[2])
            block2ready_time = int(parts[3])
            pcb = PCB(pid,
                      priority,
                      all_time,
                      block2ready_time=block2ready_time,
                      state='BLOCKED')
            pcb_queue.enqueue(pcb)
    return pcb_queue
