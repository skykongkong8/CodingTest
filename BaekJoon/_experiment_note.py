from dataclasses import dataclass
from datetime import date

class Node:
    def __init__(self, num : int, createdDate: date, admin: bool = False) -> None:
        self.num = num
        self.createDate = createdDate
        self.admin = admin

    def __repr__(self):
        return (self.__class__.__qualname__ + f"(num={self.num!r}, createdDate={self.createDate!r}, "
        f"admin={self.admin!r})"
        )

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.num, self.createDate, self.admin) == (other.num, other.createDate, other.admin)

        return NotImplemented
    
my_node = Node(1, date(1998,4,16), admin = True)
my_node2 = Node(1, date(1998,4,16), admin = True)

print(my_node == my_node2)