# 目标是：可以交互菜单
# requirements: getch
import getch
import os

class Menu:

    # items[i] = (descriptionStr, function)
    def __init__(self, items: list, pageSize: int = 3, prompt: str = "Pages: LR, Items: UD") -> None:
        l = len(items)
        self.prompt = prompt
        self.items  = items
        self.len    = l
        
        self.pageSize = min(9, l, pageSize)
        self.maxPage  = (l-1)//pageSize + 1
        
        self.page     = 0
        self.hilight  = 0

    def __erase(self) -> None:
        print(f'\033[{self.pageSize+6}A', end='')  # cursor up 5 lines
        print('\r', end='')  # cursor back to start
        print('\033[0J', end='')  # erase from cursor to end
    
    def __next_page(self) -> None:
        if self.page < self.maxPage-1:
            self.page += 1
            self.hilight = 0
            self.__render()
    
    def __prev_page(self) -> None:
        # render
        if self.page > 0:
            self.page -= 1
            self.hilight = 0
            self.__render()

    def __next_item(self) -> None:
        if self.hilight < self.pageSize:
            self.hilight += 1
            self.__render()
    
    def __prev_item(self) -> None:
        if self.hilight > 0:
            self.hilight -= 1
            self.__render()

    def __set_item(self, n:int) -> None:
        self.hilight = min(n, self.pageSize)
        self.__render()
    
    def __render(self, clear=True):
        # erase
        if clear: self.__erase()
        # render
        print(f'\n{self.prompt}\n')
        base = self.page * self.pageSize
        for i in range(self.pageSize):
            print(f'{ "*" if i == self.hilight else " "}', end='')
            if base+i >= self.len:
                print(f'[{i+1:^3}]')
            else:
                print(f'[{i+1:^3}] {self.items[base+i][0]}')
        
        print(f'{"*" if self.hilight == self.pageSize else " "}[ # ] Exit')
        print(f'\n Page: {self.page+1}/{self.maxPage}')

    def __choose(self, option: int) -> bool:
        if option == self.pageSize:
            return False
        # check valid
        idx = self.pageSize*self.page + option
        if idx < self.len:
            self.items[idx][1]()
            self.__render(clear=False)
        return True

    def start(self):
        # clear
        self.page    = 0
        self.hilight = 0
        self.__render()

        flag = True
        while flag:
            c = getch.getch()
            if c == '[':
                c = getch.getch()
                if c in ['A', 'B', 'C', 'D']:
                    if c == 'D':   # left
                        self.__prev_page()
                    elif c == 'C': # right
                        self.__next_page()
                    elif c == 'A': # up
                        self.__prev_item()
                    elif c == 'B': # down
                        self.__next_item()
            else:
                asc = ord(c)
                if asc >= 49 and asc <= 57: # nums
                    self.__set_item(asc-49)
                elif asc == 10:             # enter
                    flag = self.__choose(self.hilight)
            
        print('\n Bye!')

def sayHi():
    print("hi")

if __name__ == '__main__':
    os.system('') # enable VT-100

    # init Item
    menu_items = [('c0', sayHi), ('c1', sayHi), ('c2', sayHi), ('c3', sayHi), ('c4', sayHi)]
    m = Menu(menu_items)
    m.start()

