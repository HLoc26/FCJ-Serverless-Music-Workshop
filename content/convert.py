import re
import os

def replace_figure_tags(content):
    """
    Thay thế các thẻ {{<figure>}} thành định dạng markdown ![]()
    """
    # Pattern để match thẻ figure với các thuộc tính
    pattern = r'\{\{<\s*figure\s+src="([^"]+)"\s+alt="([^"]*)"\s+(?:width="[^"]*"\s*)?>\}\}'
    
    def replacement(match):
        src = match.group(1)
        alt = match.group(2)
        return f"![{alt}]({src})"
    
    # Thay thế tất cả các matches
    result = re.sub(pattern, replacement, content)
    return result

def process_file(file_path):
    """
    Xử lý một file
    """
    try:
        # Đọc nội dung file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Thay thế
        new_content = replace_figure_tags(content)
        
        # Ghi lại file nếu có thay đổi
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Đã xử lý: {file_path}")
            return True
        else:
            print(f"⏭️  Không có thay đổi: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi xử lý {file_path}: {e}")
        return False

def process_directory(directory_path, file_extensions=None):
    """
    Xử lý tất cả files trong thư mục
    """
    if file_extensions is None:
        file_extensions = ['.md', '.markdown', '.txt']
    
    processed_count = 0
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Kiểm tra extension
            if any(file.lower().endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                if process_file(file_path):
                    processed_count += 1
    
    print(f"\n🎉 Hoàn thành! Đã xử lý {processed_count} files.")

def main():
    print("🔄 Script thay thế Figure tags thành Markdown images")
    print("=" * 50)
    
    # Lựa chọn chế độ
    choice = input("Chọn chế độ:\n1. Xử lý 1 file\n2. Xử lý thư mục\nNhập lựa chọn (1/2): ").strip()
    
    if choice == "1":
        # Xử lý 1 file
        file_path = input("Nhập đường dẫn file: ").strip()
        if os.path.exists(file_path):
            process_file(file_path)
        else:
            print("❌ File không tồn tại!")
            
    elif choice == "2":
        # Xử lý thư mục
        dir_path = input("Nhập đường dẫn thư mục: ").strip()
        if not dir_path:
            dir_path = "."  # Thư mục hiện tại
            
        if os.path.exists(dir_path):
            # Tùy chọn file extensions
            extensions_input = input("Nhập các extension cần xử lý (mặc định: .md,.markdown,.txt): ").strip()
            if extensions_input:
                extensions = [ext.strip() for ext in extensions_input.split(',')]
                if not all(ext.startswith('.') for ext in extensions):
                    # Thêm dấu . nếu user quên
                    extensions = ['.' + ext if not ext.startswith('.') else ext for ext in extensions]
            else:
                extensions = None
                
            process_directory(dir_path, extensions)
        else:
            print("❌ Thư mục không tồn tại!")
    else:
        print("❌ Lựa chọn không hợp lệ!")

# Test function để demo
def test_replacement():
    """
    Hàm test để xem kết quả thay thế
    """
    test_content = '''
Đây là nội dung test:

{{<figure src="/images/3.cloudfront/3.2-create-cloudfront/3.distribution-name.png" alt="Set distribution name" width="100%" >}}

{{<figure src="/images/test.jpg" alt="Test image" width="50%" >}}

{{<figure src="/path/to/image.png" alt="" width="100%" >}}
'''
    
    print("Nội dung gốc:")
    print(test_content)
    print("\n" + "="*50)
    print("Nội dung sau khi thay thế:")
    print(replace_figure_tags(test_content))

if __name__ == "__main__":
    # Uncomment dòng này để test
    # test_replacement()
    
    # Chạy chương trình chính
    main()