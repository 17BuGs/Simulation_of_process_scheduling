class PCBQueue:
    """
    PCBQueue是一个队列，用于存储PCB对象，PCB代表进程控制块，是操作系统中进程管理的基本数据结构。

    属性:
    - front: 链队的队首
    - rear: 链队的队尾
    """

    def __init__(self):
        """
        构造函数，初始化队列，front和rear都初始化为None。
        """
        self.front = None
        self.rear = None

    def is_empty(self):
        """
        检查队列是否为空，如果front为None，则队列为空。
        """
        return self.front == None

    def enqueue(self, pcb):
        """
        将PCB对象添加到队列尾部。如果队列为空，则将front和rear都设置为pcb。
        """
        if self.rear == None:
            self.front = self.rear = pcb
            return
        self.rear.next = pcb
        self.rear = pcb

    def dequeue(self):
        """
        从队列头部移除PCB对象并返回它。如果队列为空，则返回None。
        """
        if self.is_empty():
            return None
        temp = self.front
        self.front = temp.next
        if self.front == None:
            self.rear = None
        temp.next = None
        return temp

    def size(self):
        """
        返回队列中PCB对象的数量。从头节点开始计数，循环到尾节点，将每个PCB的next属性都加一。最后返回总数。
        """
        temp = self.front
        count = 0
        while temp != None:
            count += 1
            temp = temp.next
        return count

    def display(self):
        """
        打印队列中的所有PCB对象。从头节点开始循环到尾节点，打印每个PCB对象并打印一个换行符。
        """
        temp = self.front
        cnt = 0
        while temp != None:
            if temp.state != 'RUNNING':
                print(temp)
                cnt += 1
            temp = temp.next
        if cnt == 0:
            print("Empty")
        print()

    def del_PCB(self, pcb):
        """
        从队列中删除指定的PCB对象。

        Parameters:
        - pcb: 要删除的PCB对象

        如果找到了对应的PCB对象，则删除它。如果该PCB对象是队列中的第一个对象，则更新队列的front指针。如果该PCB对象是队列中的最后一个对象，则更新队列的rear指针。在删除操作之后，将该PCB对象的next指针设置为None。
        """
        curr = self.front
        prev = None
        found = False
        while curr:
            if curr == pcb:
                found = True
                break
            prev = curr
            curr = curr.next
        if found:
            if prev is None:
                self.front = curr.next
            else:
                prev.next = curr.next
            if curr == self.rear:
                self.rear = prev
        pcb.next = None

    def find_shortest(self):
        """
        在队列中查找等待时间最短的PCB对象并返回它。

        Returns:
        - shortestP: 等待时间最短的PCB对象

        从队列头部开始到尾部，查找等待时间最短的PCB对象。使用变量shortestT来记录当前找到的最短时间的PCB对象的等待时间，并使用变量shortestP来记录对应的PCB对象。
        """
        shortestT = 99999
        temp = self.front
        shortestP = temp
        while temp != None:
            if (temp.all_time - temp.cpu_time) < shortestT:
                shortestT = (temp.all_time - temp.cpu_time)
                shortestP = temp
            temp = temp.next
        return shortestP

    def pri_change(self, change_num):
        """
        改变队列中所有PCB对象的优先级。

        Parameters:
        - change_num: 用于改变优先级的数值

        对队列中的每个PCB对象的优先级进行改变，同时限制优先级不低于0。
        """
        temp = self.front
        while temp != None:
            temp.priority += change_num
            if temp.priority < 0:
                temp.priority = 0
            temp = temp.next

    def minus_blocked_time(self):
        """
        减少队列中所有PCB对象的阻塞时间。

        将队列中的每个PCB对象的阻塞时间减1。
        """
        temp = self.front
        while temp != None:
            temp.block2ready_time -= 1
            temp = temp.next

    def add_wait_time(self):
        """
        增加队列中所有PCB对象的等待时间。

        将队列中的每个PCB对象的等待时间加1。
        """
        temp = self.front
        while temp != None:
            temp.wait_time += 1
            temp = temp.next

    def find_highest_Response_Ratio(self):
        """
        在队列中查找响应比最高的PCB对象并返回它。

        Returns:
        - highestP: 等待响应比最高的PCB对象

        从队列头部开始到尾部，查找响应比最高的PCB对象。使用变量highestRR来记录当前找到的响应比最高的PCB对象的等待时间，并使用变量highestP来记录对应的PCB对象。
        """
        highestRR = 0
        temp = self.front
        highestP = temp
        while temp != None:
            t = temp.wait_time
            if t == 0:
                t = 0.01
            if (1 + t / (temp.all_time - temp.cpu_time)) > highestRR:
                highestRR = (1 + t / (temp.all_time - temp.cpu_time))
                highestP = temp
            temp = temp.next
        return highestP

    def find_highest_priority(self):
        """
        在队列中查找优先级最高的PCB对象并返回它。

        Returns:
        - highestP: 优先级最高的PCB对象

        从队列头部开始到尾部，查找优先级最高的PCB对象。使用变量highestPri来记录当前找到的优先级最高的PCB对象的优先级，并使用变量highestP来记录对应的PCB对象。
        """
        highestPri = -1
        temp = self.front
        highestP = temp
        while temp != None:
            if (temp.priority) > highestPri:
                highestPri = temp.priority
                highestP = temp
            temp = temp.next
        return highestP
