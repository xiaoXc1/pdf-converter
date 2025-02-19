import os
import fitz
import re

def 提取中文名(文件名):
    return ''.join(re.findall(r'[\u4e00-\u9fff]+', 文件名)) or "未命名"

def 转换PDF():
    pdf文件夹 = os.path.join(os.getcwd(), "准备转换的PDF")
    导出文件夹 = os.path.join(os.getcwd(), "生成的图片")
    
    if not os.path.exists(导出文件夹):
        os.makedirs(导出文件夹)
    
    名称计数器 = {}
    # 新增统计变量
    total_pdfs = 0
    success_count = 0
    fail_count = 0
    failures = []

    for 文件名 in os.listdir(pdf文件夹):
        if 文件名.lower().endswith(".pdf"):
            total_pdfs += 1  # 统计总数
            文件路径 = os.path.join(pdf文件夹, 文件名)
            中文前缀 = 提取中文名(文件名)
            
            当前计数 = 名称计数器.get(中文前缀, 0) + 1
            名称计数器[中文前缀] = 当前计数
            实际前缀 = 中文前缀 if 当前计数 == 1 else f"{中文前缀}-{当前计数 - 1}"
            
            try:
                pdf文档 = fitz.open(文件路径)
                for 页码 in range(len(pdf文档)):
                    页 = pdf文档.load_page(页码)
                    图片 = 页.get_pixmap(dpi=200)
                    保存路径 = os.path.join(导出文件夹, f"{实际前缀}_page{页码+1}.png")
                    图片.save(保存路径)
                success_count += 1  # 记录成功
                print(f"✔ {文件名}已转换完成")
            except Exception as 错误:
                fail_count += 1  # 记录失败
                failures.append((文件名, str(错误)))
                print(f"✘ 转换失败：{文件名} → {str(错误)}")

    # 输出总结报告
    print("\n==== 转换总结 ====")
    print(f"总PDF数量: {total_pdfs}")
    print(f"转换成功: {success_count}")
    print(f"转换失败: {fail_count}")
    if failures:
        print("\n失败列表:")
        for 文件名, 原因 in failures:
            print(f"  - 文件: {文件名}\n    原因: {原因}")

if __name__ == "__main__":
    转换PDF()
    input("\n按回车键退出程序...")