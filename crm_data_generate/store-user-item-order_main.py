import csv
import os
from generators.Usergenerator import DataGenerator
from generators.Storegenerator import Datagenerator_store
from generators.Itemgenerator import Datagerator_item
from generators.Ordergenerator import Ordergenerator
from generators.OrderItemgenerator import OrderItem
from printer.Printer import Printer

def generate_u(numbers):
    u = DataGenerator(int(numbers))
    user = u.generate_users() #generate_users()에서 for문이 돌아감.
    return user      

def generate_s(numbers):
    s = Datagenerator_store(int(numbers))
    store = s.generate_stores()
    return store

def generate_i(numbers):
    i = Datagerator_item(int(numbers))
    item = i.generate_item()
    return item

def generate_o(numbers):
    l = []
    for i in range(numbers):
        o = Ordergenerator()
        b = o.order_generate()
        l.append(b)
    return l

def generate_oi(numbers):
    l = []
    for i in range(numbers):
        oi = OrderItem()
        b = oi.orderitem_generate()
        l.append(b)
    return l

if __name__ == "__main__":  
            while True:
                menu = input("[생성할 데이터(user | store | item | order | orderitem), 개수, 출력 방식]을 입력하세요\n(공백으로 구분)\n[출력 방식 옵션: 스크린/파일]\n[입력 예시: user 100 스크린]\n종료를 원하면 1을 입력하세요.\n")
                if menu == "1":
                    print("종료합니다")
                    break
                try:
                    d_type = menu.split()[0].lower()
                    if d_type not in ["user","store","item","order","orderitem"]:
                        raise ValueError("데이터가 올바르지 않습니다.")
                    n = menu.split()[1]
                    if not int(n) or int(n) <= 0:
                        raise IndexError("올바른 숫자가 아닙니다.") 
                    show = menu.split()[2]
                    if show not in ["스크린","파일"]:
                        raise ValueError("올바른 출력방식이 아닙니다.")
                    s = Printer
                    if d_type == "user":
                        ans = generate_u(int(n))

                    elif d_type == "store":
                        ans = generate_s(int(n))
                    
                    elif d_type == "item":
                        ans = generate_i(int(n))

                    elif d_type == "order":
                        if os.path.isfile("output_user.csv") and os.path.isfile("output_store.csv"):
                            ans = generate_o(int(n))
                        else:
                            raise FileNotFoundError("user or store 파일이 존재하지 않습니다")
                    elif d_type == "orderitem":
                        if os.path.isfile("output_item.csv") and os.path.isfile("output_order.csv"):
                            ans = generate_oi(int(n))
                        else:
                            raise FileNotFoundError("item or order 파일이 존재하지 않습니다")
                    if show == "스크린":
                            s.print_to_screen(d_type,ans)
                    elif show == "파일":
                            s.print_to_file(d_type,ans)
                except ValueError as e:
                    print(e,"형식에 맞게 입력하세요")
                except IndexError as e:
                    print(e,"형식에 맞게 입력하세요")
                except FileNotFoundError as e:
                    print(e,"파일 데이터를 생성하세요.")