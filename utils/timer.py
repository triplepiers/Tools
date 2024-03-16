# 自定义装饰器：函数运行计时

import time
import math

def timer(func):
    def wrapper(*args):   # 接受被包裹函数的变长参数
        t1  = time.time()
        res = func(*args)
        t2  = time.time()
        print('Used time :{:.4}s'.format(t2-t1))
        return res        # 返回被包裹函数的执行结果
    return wrapper

def is_prime(num: int) -> bool:
    if num < 2:
        return False
    elif num == 2:
        return True
    else:
        for i in range(2, math.ceil(math.sqrt(num))):
            if num % i == 0:
                return False
        return True

@timer # use decorator 进行计时
def cnt_prime_nums(n: int):
    cnt = 0
    for i in range(1, n+1):
        if is_prime(i): cnt += 1
    return cnt

if __name__ == '__main__':
    n = int(input("Please input upper bound: "))
    print(f'There are [{cnt_prime_nums(n)}] prime nums in range [1, {n}].')