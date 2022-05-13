from dataclasses import dataclass
from datetime import date

class Node:
    def __init__(self, num : int, createdDate: date, admin: bool = False) -> None:
        self.num = num
        self.createDate = createdDate
        self.admin = admin

    # print(Node)를 했을 때, 뜨게 하는 것:
    def __repr__(self):
        return (self.__class__.__qualname__ + f"(num={self.num!r}, createdDate={self.createDate!r}, "
        f"admin={self.admin!r})"
        )

    # 서로 다른 Node를 boolean으로 비교하는데, 저장된 주소가 다르더라도 내부 값이 같으면 같도록 하는 것
    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.num, self.createDate, self.admin) == (other.num, other.createDate, other.admin)

        return NotImplemented
    
my_node = Node(1, date(1998,4,16), admin = True)
my_node2 = Node(1, date(1998,4,16), admin = True)

print(my_node == my_node2)

# 이처럼, print와 기본 비교 등 data로서 사용하려면 조금 더 많은 특성들이 개별 설정될 필요가 있는데,

# dataclass 데코레이터를 사용하면 이것이 한 번에 된다
from dataclasses import field
from typing import List

@dataclass
class DataNode:
    num : int
    createdDate : date
    admin : bool
    # randomList = []
    friends: List[int] = field(default_factory=list)

# 그러나 주의할 점: 클래스 애트리뷰트로 리스트같은걸 생성해버리면, 동일 클래스 인스턴스 간에 공유가 되기 때문에,
# dataclass 상에서는 아예 기본값 할당 허용이 되지가 않는다.

# 따라서, field의 default_factory를 사용해서 매번 새로운 리스트가 생성될 수 있도록 해주어야 한다.

dataNode = DataNode(1, date(1998,4,16), False)
dataNode.friends.append(1)
print(dataNode)