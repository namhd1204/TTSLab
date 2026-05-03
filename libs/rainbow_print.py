import sys
from colorama import Fore, Style, init

# Khởi tạo colorama, tự động reset màu sau mỗi dòng và hỗ trợ Windows tốt hơn
init(autoreset=True)

class RainbowPrint:
    def __init__(self):
        # Định nghĩa các màu mặc định cho từng loại thông báo
        self._colors = {
            "success": Fore.GREEN,
            "error": Fore.RED,
            "warning": Fore.YELLOW,
            "info": Fore.CYAN,
            "debug": Fore.MAGENTA
        }

    def _base_print(self, color_code, *args, prefix="", **kwargs):
        """Hàm lõi để xử lý việc in ấn"""
        # Tách các giá trị để in, nối thêm prefix nếu có
        message = " ".join(map(str, args))
        full_output = f"{color_code}{prefix}{message}{Style.RESET_ALL}"
        
        # Gọi hàm print gốc của hệ thống
        print(full_output, **kwargs)

    def success(self, *args, **kwargs):
        """In thông báo thành công với dấu tích"""
        self._base_print(self._colors["success"], *args, prefix="✔ ", **kwargs)

    def error(self, *args, **kwargs):
        """In thông báo lỗi với dấu X"""
        self._base_print(self._colors["error"], *args, prefix="✘ ", **kwargs)

    def warning(self, *args, **kwargs):
        """In thông báo cảnh báo"""
        self._base_print(self._colors["warning"], *args, prefix="⚠ ", **kwargs)

    def info(self, *args, **kwargs):
        """In thông báo thông tin"""
        self._base_print(self._colors["info"], *args, prefix="ℹ ", **kwargs)

    def log(self, *args, color="white", **kwargs):
        """In log với màu tùy chỉnh (ví dụ: color='blue')"""
        color_code = getattr(Fore, color.upper(), Fore.WHITE)
        self._base_print(color_code, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Để có thể gọi rprint() như hàm print bình thường"""
        print(*args, **kwargs)

# Khởi tạo một instance duy nhất để người dùng import và sử dụng ngay
rprint = RainbowPrint()