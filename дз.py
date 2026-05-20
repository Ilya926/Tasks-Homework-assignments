import heapq
from typing import Generic, TypeVar, List, Callable, Iterator
from collections import deque
from dataclasses import dataclass

# 1. PriorityQueue

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    def __init__(self, priority_func: Callable[[T], int]):
        self.priority_func = priority_func
        self.counter = 0
        self.heap = []

    def push(self, item: T) -> None:
        priority = self.priority_func(item)
        heapq.heappush(self.heap, (-priority, self.counter, item))
        self.counter += 1

    def pop(self) -> T:
        if not self.heap:
            raise IndexError("pop from empty queue")
        _, _, item = heapq.heappop(self.heap)
        return item

    def peek(self) -> T:
        if not self.heap:
            raise IndexError("peek from empty queue")
        return self.heap[0][2]

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def size(self) -> int:
        return len(self.heap)

    def __len__(self) -> int:
        return self.size()

    def __iter__(self) -> Iterator[T]:
        temp = self.heap.copy()
        while temp:
            _, _, item = heapq.heappop(temp)
            yield item


# 2. Иерархия Animal/Dog/Cat

class Animal:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"


class Dog(Animal):
    def bark(self):
        print(f"{self.name} says: Woof!")

    def __repr__(self):
        return f"Dog({self.name!r})"


class Cat(Animal):
    def meow(self):
        print(f"{self.name} says: Meow!")

    def __repr__(self):
        return f"Cat({self.name!r})"


# 3. Дженерик-функции

# Функция 1: copyAnimals
def copyAnimals(src: List[Dog], dst: List[Animal]) -> None:
    dst.extend(src)


# Функция 2: fillWithCats
def fillWithCats(dst: List[Animal]) -> None:
    dst.clear()
    dst.extend([Cat("Cat1"), Cat("Cat2"), Cat("Cat3")])


# Типы для safeTransfer
S = TypeVar('S')  # для src
D = TypeVar('D')  # для dst


def safeTransfer(src: List[S], dst: List[D]) -> None:
    dst.extend(src)
    src.clear()


# Примеры использования

if __name__ == "__main__":
    # Тест PriorityQueue
    print("=== Тест PriorityQueue ===")


    def priority_func(x: str) -> int:
        return {"high": 3, "medium": 2, "low": 1}.get(x, 0)


    pq = PriorityQueue(priority_func)

    pq.push("medium")
    pq.push("high")
    pq.push("low")
    pq.push("high")
    pq.push("medium")

    while not pq.is_empty():
        print(f"Извлечено: {pq.pop()}")

    # Тест copyAnimals
    print("\n=== Тест copyAnimals ===")
    dogs = [Dog("Buddy"), Dog("Max")]
    animals = [Cat("Whiskers")]

    print(f"До: {animals}")
    copyAnimals(dogs, animals)
    print(f"После: {animals}")

    # Тест fillWithCats
    print("\n=== Тест fillWithCats ===")
    animals2 = [Dog("Rex")]
    print(f"До: {animals2}")
    fillWithCats(animals2)
    print(f"После: {animals2}")

    # Проверка с List[Cat]
    cats_list = [Cat("Old Cat")]
    print(f"До (List[Cat]): {cats_list}")
    fillWithCats(cats_list)  # Работает благодаря ковариантности
    print(f"После (List[Cat]): {cats_list}")

    # Тест safeTransfer
    print("\n=== Тест safeTransfer ===")

    # Сценарий 1: Dog -> Animal
    dog_list = [Dog("Rex"), Dog("Charlie")]
    animal_list: List[Animal] = [Cat("Tom")]

    print(f"До: dogs={dog_list}, animals={animal_list}")
    safeTransfer(dog_list, animal_list)
    print(f"После: dogs={dog_list}, animals={animal_list}")

    # Сценарий 2: Cat -> Animal
    cat_list = [Cat("Felix"), Cat("Luna")]
    animal_list2: List[Animal] = [Dog("Spike")]

    print(f"\nДо: cats={cat_list}, animals={animal_list2}")
    safeTransfer(cat_list, animal_list2)
    print(f"После: cats={cat_list}, animals={animal_list2}")

    # Сценарий 3: Dog -> List[object]
    dogs3 = [Dog("Oscar")]
    objects_list: List[object] = ["string", 123]

    print(f"\nДо: dogs={dogs3}, objects={objects_list}")
    safeTransfer(dogs3, objects_list)
    print(f"После: dogs={dogs3}, objects={objects_list}")