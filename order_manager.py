import json
import os
from pprint import PrettyPrinter

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"
pp = PrettyPrinter()

def load_orders() -> list:
    """讀取待處理訂單檔案，若檔案不存在則回傳空列表"""
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_orders(orders: list) -> None:
    """將待處理訂單儲存至檔案"""
    with open(INPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(orders, file, ensure_ascii=False, indent=4)

def load_output_orders() -> list:
    """讀取已出餐訂單檔案，若檔案不存在則回傳空列表"""
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_output_orders(output_orders: list) -> None:
    """將已出餐訂單儲存至檔案"""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(output_orders, file, ensure_ascii=False, indent=4)

def print_menu() -> None:
    """顯示主選單"""
    print("***************選單***************")
    print("1. 新增訂單")
    print("2. 顯示訂單報表")
    print("3. 出餐處理")
    print("4. 離開")
    print("**********************************")

def add_order() -> None:
    """新增訂單，包含訂單編號、顧客姓名及至少一項訂單項目"""
    orders = load_orders()
    order_id = input("請輸入訂單編號：").strip().upper()
    if any(order["order_id"] == order_id for order in orders):
        print(f"=> 錯誤：訂單編號 {order_id} 已存在！")
        return
    customer_name = input("請輸入顧客姓名：").strip()
    items = []
    while True:
        item_name = input("請輸入訂單項目名稱（輸入空白結束）：").strip()
        if not item_name:
            break
        try:
            price = int(input("請輸入價格：").strip())
            if price < 0:
                print("=> 錯誤：價格不能為負數，請重新輸入")
                continue
            quantity = int(input("請輸入數量：").strip())
            if quantity <= 0:
                print("=> 錯誤：數量必須為正整數，請重新輸入")
                continue
        except ValueError:
            print("=> 錯誤：價格或數量必須為整數，請重新輸入")
            continue
        items.append({"name": item_name, "price": price, "quantity": quantity})
    if not items:
        print("=> 至少需要一個訂單項目")
        return
    orders.append({"order_id": order_id, "customer": customer_name, "items": items})
    save_orders(orders)
    print(f"=> 訂單 {order_id} 已新增！")

def show_orders() -> None:
    """顯示所有待處理訂單報表"""
    orders = load_orders()
    if not orders:
        print("=> 目前沒有訂單")
        return
    print("\n==================== 訂單報表 ====================")
    for i, order in enumerate(orders, 1):
        print(f"訂單 #{i}\n訂單編號: {order['order_id']}\n客戶姓名: {order['customer']}")
        print("-" * 50)
        print("商品名稱\t單價\t數量\t小計")
        print("-" * 50)
        total = 0
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            print(f"{item['name']}\t{item['price']:,}\t{item['quantity']}\t{subtotal:,}")
        print("-" * 50)
        print(f"訂單總額: {total:,}")
        print("=" * 50)

def process_order() -> None:
    """出餐處理，將選定的訂單移至已出餐清單"""
    orders = load_orders()
    if not orders:
        print("=> 目前沒有可處理的訂單")
        return
    print("\n======== 待處理訂單列表 ========")
    for i, order in enumerate(orders, 1):
        print(f"{i}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("=" * 30)
    try:
        choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ").strip()
        if not choice:
            return
        index = int(choice) - 1
        if index < 0 or index >= len(orders):
            raise ValueError
    except ValueError:
        print("=> 錯誤：請輸入有效的數字")
        return
    output_orders = load_output_orders()
    processed_order = orders.pop(index)
    save_orders(orders)
    output_orders.append(processed_order)
    save_output_orders(output_orders)
    pp.pprint(processed_order)

def main() -> None:
    """主選單迴圈，處理使用者輸入"""
    while True:
        print_menu()
        choice = input("請選擇操作項目(Enter 離開)：").strip()
        if not choice:
            break
        if choice == "1":
            add_order()
        elif choice == "2":
            show_orders()
        elif choice == "3":
            process_order()
        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項（1-4）")

if __name__ == "__main__":
    main()
