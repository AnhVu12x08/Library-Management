
import requests
import json

cate = input("Enter Category name: ")
# URL của trang web cần lấy dữ liệu từ API
url = f"http://openlibrary.org/subjects/{cate}.json"

# Gửi yêu cầu GET đến URL và lấy dữ liệu về
response = requests.get(url)

# Kiểm tra xem yêu cầu có thành công hay không (status code 200 là thành công)
if response.status_code == 200:
    # Lấy nội dung JSON từ phản hồi
    data = response.json()

    # Lưu dữ liệu vào một tệp JSON
    with open("category.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print("Success")
else:
    print("Error.")




