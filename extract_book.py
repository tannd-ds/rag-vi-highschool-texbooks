import requests
import os
import json

def get_book_save_dir(book_id, book_name):
    """ Get the save directory for the book """
    save_dir = f"data/{book_id}_{book_name}"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"{book_id}_{book_name}.json")
    return file_path

def save_book(data, book_id, book_name):
    file_path = get_book_save_dir(book_id, book_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data["data"], f, sort_keys=True, ensure_ascii=False, indent=4)


def extract_book_from_hoc10_scheme(book_id, page, book_name, limit, status, app_id):
    if os.path.exists(get_book_save_dir(book_id, book_name)):
        file_path = get_book_save_dir(book_id, book_name)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    url = f"https://api.hoc10.vn/api/get-detail-page?book_id={book_id}&page={page}&book_name={book_name}&limit={limit}&status={status}&app_id={app_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        save_book(data, book_id, book_name)

        return data["data"]
    else:
        print("Error: ", response.status_code)
        return None

if __name__ == "__main__":
    book_info = {
        "book_id": 154,
        "page": 0,
        "book_name": "ngu-van-10-tap-2",
        "limit": 0,
        "status": "",
        "app_id": 68,
    }
    data = extract_book_from_hoc10_scheme(**book_info)

    if data:
        # Download and save all pages
        pages_dir = os.path.join('data', f"{book_info['book_id']}_{book_info['book_name']}", 'pages')
        for page in data["list_page"]:
            img_url = 'https://hoc10.monkeyuni.net/' + page['background']
            print(f"Page {page['index']}: {img_url}")

            # Download the page image
            image_response = requests.get(img_url)
            if image_response.status_code == 200:
                image_path = os.path.join(pages_dir, f"{page['index']}.jpg")
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_response.content)
            else:
                print(f"Failed to download image for page {page['index']}")