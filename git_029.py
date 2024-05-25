import requests
from collections import Counter
import warnings
import os
import time


success_counter = Counter()
failure_counter = Counter()


warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made.*")


def check_url(url, custom_content_file, success_file, failure_file):
    try:
        custom_content = ""
        with open(custom_content_file, 'r', encoding='utf-8') as f:
            custom_content = f.read().strip()

        if not url.startswith('http://') and not url.startswith('https://'):
            full_url = f"http://{url}{custom_content}"  
        else:
            full_url = f"{url}{custom_content}"
        
        response = requests.get(full_url, timeout=5, verify=False)  
        if response.status_code == 200:
            with open(success_file, 'a', encoding='utf-8') as file:
                file.write(full_url + '\n')  
            success_counter[url] += 1
            print(f"\033[32m成功访问链接：{full_url}\033[0m")  
        else:
            with open(failure_file, 'a', encoding='utf-8') as file:
                file.write(full_url + '\n')  
            failure_counter[url] += 1
            print(f"无法访问链接：{full_url}")
    except requests.RequestException as e:
        with open(failure_file, 'a', encoding='utf-8') as file:
            file.write(full_url + '\n') 
        failure_counter[url] += 1
        print(f"访问链接时发生异常：{full_url} (Exception: {e.__class__.__name__})")


def generate_statistics():
    total_success = sum(success_counter.values())
    total_failure = sum(failure_counter.values())
    print(f"成功链接数量: {total_success}")
    print(f"失败链接数量: {total_failure}")

    max_value = max(total_success, total_failure)
    success_percentage = (total_success / max_value) * 100 if max_value > 0 else 0
    failure_percentage = (total_failure / max_value) * 100 if max_value > 0 else 0

    success_bar = '█' * int(success_percentage / 2)
    failure_bar = '█' * int(failure_percentage / 2)

    print(f"成功：\033[32m{success_bar} {success_percentage:.1f}%\033[0m")  
    print(f"失败：{failure_bar} {failure_percentage:.1f}%")
    
    
    print("\nby-029制作，可以访问的链接已经导出到yes.txt里面了哦")


def show_directory_structure():
    current_directory = os.getcwd()
    print("当前脚本结构：")
    for dirpath, dirnames, filenames in os.walk(current_directory):
        level = dirpath.replace(current_directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(dirpath)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in filenames:
            if f == 'yes.txt':
                print(f"{subindent}{f} - 这里保存了可以成功访问的链接")
            elif f == 'no.txt':
                print(f"{subindent}{f} - 这里保存了无法访问的链接")
            elif f == '1.txt':
                print(f"{subindent}{f} - 这里保存了你导入的链接")
            elif f == '2.txt':
                print(f"{subindent}{f} - 这里保存了你要搜索的关键字")
            else:
                print(f"{subindent}{f}")


def main():
    
    show_directory_structure()
    print("\n")
    time.sleep(5)

    
    open('yes.txt', 'w').close()
    open('no.txt', 'w').close()


    with open('1.txt', 'r', encoding='utf-8') as file:
        links = file.readlines()

   
    for link in links:
        link = link.strip()
        check_url(link, '2.txt', 'yes.txt', 'no.txt')

   
    generate_statistics()

if __name__ == "__main__":
    main()
