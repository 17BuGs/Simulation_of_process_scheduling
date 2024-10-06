def first_come_first_served(pcb_queue, pcb):
    """
    先来先服务调度算法（First-Come, First-Served）
    """
    pcb = pcb_queue.front
    if pcb == None:
        # print("Process Finished!")
        return None
    pcb.state = "RUNNING"
    pcb.cpu_time += 1
    # pcb.processing_time += 1
    pcb.running2block_time -= 1
    if pcb.cpu_time >= pcb.all_time:
        pcb.state = 'FINISHED'
        pcb_queue.dequeue()
    elif pcb.running2block_time <= 0:
        pcb.state = 'BLOCKED'
    return pcb


def round_robin(pcb_queue, quantum):
    """
    时间片轮转调度算法（Round Robin）
    """
    pcb = pcb_queue.front
    if pcb == None:
        # print("Process Finished!")
        return None
    pcb.state = "RUNNING"
    pcb.time_slice = quantum
    pcb.cpu_time += 1
    pcb.processing_time += 1
    pcb.running2block_time -= 1
    if pcb.cpu_time >= pcb.all_time:
        pcb.state = 'FINISHED'
        pcb_queue.dequeue()
    elif pcb.running2block_time <= 0:
        pcb.state = 'BLOCKED'
    elif pcb.processing_time >= pcb.time_slice:
        pcb.state = 'READY'
        pcb.processing_time = 0
        # 加到队尾
        pcb_queue.enqueue(pcb_queue.dequeue())
    return pcb


def shortest_process_first(pcb_queue, pcb):
    """
    短进程优先调度算法（Shortest Process First）
    """
    if pcb == None or pcb.state == 'FINISHED' or pcb.state == 'BLOCKED':
        pcb = pcb_queue.find_shortest()
    if pcb == None:
        # print("Process Finished!")
        return None
    pcb.state = "RUNNING"
    pcb.cpu_time += 1
    # pcb.processing_time += 1
    pcb.running2block_time -= 1
    if pcb.cpu_time >= pcb.all_time:
        pcb.state = 'FINISHED'
        pcb_queue.del_PCB(pcb)
    elif pcb.running2block_time <= 0:
        pcb.state = 'BLOCKED'
    return pcb


def highest_response_ratio(pcb_queue, pcb):
    """
    高响应比优先调度算法（Highest Response Ratio Next）
    """
    if pcb == None or pcb.state == 'FINISHED' or pcb.state == 'BLOCKED':
        pcb = pcb_queue.find_highest_Response_Ratio()
    if pcb == None:
        # print("Process Finished!")
        return None
    pcb.state = "RUNNING"
    pcb.cpu_time += 1
    # pcb.processing_time += 1
    pcb.running2block_time -= 1
    if pcb.cpu_time >= pcb.all_time:
        pcb.state = 'FINISHED'
        pcb_queue.del_PCB(pcb)
    elif pcb.running2block_time <= 0:
        pcb.state = 'BLOCKED'
    pcb_queue.add_wait_time()
    # 执行中的进程，认为不增加其等待时间
    if pcb.state != 'FINISHED':
        pcb.wait_time -= 1
    return pcb


def static_priority(pcb_queue, pcb):
    """
    静态优先级调度算法（Static Priority Scheduling）--非抢占式
    """
    if pcb == None or pcb.state == 'FINISHED' or pcb.state == 'BLOCKED':
        pcb = pcb_queue.find_highest_priority()
    if pcb == None:
        # print("Process Finished!")
        return None
    pcb.state = "RUNNING"
    pcb.cpu_time += 1
    # pcb.processing_time += 1
    pcb.running2block_time -= 1
    if pcb.cpu_time >= pcb.all_time:
        pcb.state = 'FINISHED'
        pcb_queue.del_PCB(pcb)
    elif pcb.running2block_time <= 0:
        pcb.state = 'BLOCKED'
    return pcb


def static_priority_preemptive(pcb_queue, pcb):
    """
    静态优先级调度算法（Static Priority Scheduling）--抢占式
    """
    pcb = pcb_queue.find_highest_priority()
    if pcb == None:
        # print("Process Finished!")
        return None
    pcb.state = "RUNNING"
    pcb.cpu_time += 1
    # pcb.processing_time += 1
    pcb.running2block_time -= 1
    if pcb.cpu_time >= pcb.all_time:
        pcb.state = 'FINISHED'
        pcb_queue.del_PCB(pcb)
    elif pcb.running2block_time <= 0:
        pcb.state = 'BLOCKED'
    return pcb


def dynamic_priority(pcb_queue, pcb):
    """
    动态优先级调度算法（Dynamic Priority Scheduling）--非抢占式
    """
    if pcb == None or pcb.state == 'FINISHED' or pcb.state == 'BLOCKED':
        pcb = pcb_queue.find_highest_priority()
    if pcb == None:
        # print("Process Finished!")
        return None
    pcb.state = "RUNNING"
    pcb.cpu_time += 1
    # pcb.processing_time += 1
    pcb.running2block_time -= 1
    # 等待中的pcb优先级+1
    pcb_queue.pri_change(1)
    # 运行中的pcb优先级-3
    pcb.priority -= 4  # -1-3
    if pcb.priority < 0:
        pcb.priority = 0
    if pcb.cpu_time >= pcb.all_time:
        pcb.state = 'FINISHED'
        pcb_queue.del_PCB(pcb)
    elif pcb.running2block_time <= 0:
        pcb.state = 'BLOCKED'
    return pcb


def dynamic_priority_preemptive(pcb_queue, pcb):
    """
    动态优先级调度算法（Dynamic Priority Scheduling）--抢占式
    """
    pcb = pcb_queue.find_highest_priority()
    if pcb == None:
        # print("Process Finished!")
        return None
    pcb.state = "RUNNING"
    pcb.cpu_time += 1
    # pcb.processing_time += 1
    pcb.running2block_time -= 1
    # 等待中的pcb优先级+1
    pcb_queue.pri_change(1)
    # 运行中的pcb优先级-3
    pcb.priority -= 4  # -1-3
    if pcb.priority < 0:
        pcb.priority = 0
    if pcb.cpu_time >= pcb.all_time:
        pcb.state = 'FINISHED'
        pcb_queue.del_PCB(pcb)
    elif pcb.running2block_time <= 0:
        pcb.state = 'BLOCKED'
    return pcb
