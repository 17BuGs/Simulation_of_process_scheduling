class PCB:
    """
    进程控制块（PCB）类，用于表示一个进程的相关信息和状态。

    属性:
    - pid: 进程ID
    - priority: 进程优先级
    - all_time: 进程运行所需CPU总时间片数
    - cpu_time: 进程已执行的CPU时间
    - running2block_time: 进程从运行状态转换为阻塞状态所需的时间
    - time_slice: 进程的时间片，默认为 99999
    - block2ready_time: 进程从阻塞状态转换为就绪状态所需的时间
    - state: 进程当前状态，可以是"CREATED", "READY", "BLOCKED", "RUNNING", "FINISHED"
    - next: 指向下一个PCB对象的指针
    - processing_time: 时间片中已消耗的时间
    - wait_time: 进程的等待时间
    """

    def __init__(self,
                 pid,
                 priority,
                 all_time,
                 block2ready_time=99999,
                 running2block_time=99999,
                 state="CREATED"):
        """
        初始化
        
        参数:
        - pid: 进程ID
        - priority: 进程优先级
        - all_time: 进程运行所需CPU总时间片数
        - block2ready_time: 进程从阻塞状态转换为就绪状态所需的时间，默认为 99999
        - running2block_time: 进程从运行状态转换为阻塞状态所需的时间，默认为 99999
        - state: 进程当前状态，默认为 "CREATED"
        """
        self.pid = pid
        self.priority = priority
        self.all_time = all_time
        self.cpu_time = 0
        self.running2block_time = running2block_time
        self.time_slice = 99999
        self.block2ready_time = block2ready_time
        self.state = state
        self.next = None
        self.processing_time = 0
        self.wait_time = 0

    def __str__(self):
        """
        返回进程的字符串表示形式，包括进程ID，优先级，CPU时间，所需CPU总时间片数和状态。

        返回值:
        - 字符串，表示该进程的信息
        """
        if self.state == 'BLOCKED':
            return f"PCB{self.pid} - Priority: {self.priority} - CPU Time: {self.cpu_time} / All Time: {self.all_time} - State: {self.state} - Blocked to Ready Time: {self.block2ready_time} - Wait Time(HRRN): {self.wait_time} - Used Slice(RR): {self.processing_time} / Time Slice(RR): {self.time_slice}"
        elif self.state == 'RUNNING' or self.state == 'READY':
            return f"PCB{self.pid} - Priority: {self.priority} - CPU Time: {self.cpu_time} / All Time: {self.all_time} - State: {self.state} - Running to Blocked Time: {self.running2block_time} - Wait Time(HRRN):{self.wait_time} - Used Slice(RR): {self.processing_time} / Time Slice(RR): {self.time_slice}"
        else:
            return f"PCB{self.pid} - Priority: {self.priority} - CPU Time: {self.cpu_time} / All Time: {self.all_time} - State: {self.state} - Wait Time(HRRN):{self.wait_time} - Used Slice(RR): {self.processing_time} / Time Slice(RR): {self.time_slice}"
