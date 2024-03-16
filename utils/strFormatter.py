from datetime import datetime

# 千分位分隔符
def thousandsSeparator(n: int, dash: bool = True) -> str:
    if dash:
        return f'{n:_}' # 1_000_023_475
    else:
        return f'{n:,}' # 1,000,023,475

# align: 0-left, 1-mid, r-right
def textAligned(s: str, align: int = 0) -> str:
    # 其实还可以通过 :{symbol}<10 定义填充符号
    if align == 0:
        return f'{s:<10}|' # 左对齐
    elif align == 1:
        return f'{s:^10}|' # 水平居中
    else:
        return f'{s:>10}|' # 右对齐

# 格式化日期
def now(choice: int = 0) -> str:
    now = datetime.now()
    if choice == 0:
        return f'{now:%y.%m.%d (%H:%M:%S)}' # YY.MM.DD (hh:mm:ss)
    elif choice == 1:
        return f'{now:%c}'                  # LocalTime: Sat Mar 16 20:03:02 2024
    elif choice == 2:
        return f'{now:%I%p}'                # {hh}AM/PM

# 保留小数
def rounded(num: float, choice: int=0) -> str:
    if choice == 0:
        return f'{num:.0f}'  # 保留整数
    elif choice == 1:
        return f'{num:.2f}'  # 保留两位整数
    elif choice == 2:
        return f'{num:.3f}'  # 整数部分使用千分位分隔符

def plus_debug(a:int, b: int) -> None:
    print(f'{a + b = }')     # 会出现 a + b = {res}，很神奇吧
                             # f'{var = }' 与 f'var = {var}' 等价，更神奇了