# -*- coding: utf-8 -*-
"""
将当前目录下的文件结构及代码整合到Markdown文件
支持文件类型: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css
"""

import os
import sys
from pathlib import Path
import fnmatch

def get_directory_tree(start_path, ignore_patterns=None):
    """
    获取目录树结构
    """
    if ignore_patterns is None:
        ignore_patterns = ['.git', '__pycache__', '*.pyc', '.idea', 'build', 'dist', 'node_modules']
    
    tree_lines = []
    
    def _walk(dir_path, prefix=""):
        # 获取当前目录下的所有项目
        try:
            items = sorted(os.listdir(dir_path))
        except PermissionError:
            return
        
        # 过滤掉忽略的项目
        items = [item for item in items 
                if not any(fnmatch.fnmatch(item, pattern) 
                          for pattern in ignore_patterns)]
        
        for i, item in enumerate(items):
            item_path = os.path.join(dir_path, item)
            is_last = (i == len(items) - 1)
            
            # 选择适当的前缀符号
            if is_last:
                tree_lines.append(f"{prefix}└── {item}")
                new_prefix = prefix + "    "
            else:
                tree_lines.append(f"{prefix}├── {item}")
                new_prefix = prefix + "│   "
            
            # 如果是目录，递归遍历
            if os.path.isdir(item_path):
                _walk(item_path, new_prefix)
    
    # 添加根目录名称
    root_name = os.path.basename(os.path.abspath(start_path))
    tree_lines.append(f"{root_name}/")
    _walk(start_path)
    
    return "\n".join(tree_lines)

def should_process_file(filename):
    """
    判断文件是否需要处理
    支持的扩展名: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css
    """
    valid_extensions = [
        '.h', '.cpp', '.pro', '.vue', '.js', '.ts', '.jsx', '.tsx',
        '.yml', '.yaml', '.xml', '.html', '.htm', '.py', '.css'   # <--- 添加 .css
    ]
    return any(filename.endswith(ext) for ext in valid_extensions)

def read_file_content(filepath):
    """
    读取文件内容
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，尝试使用其他编码
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                return f.read()
        except:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    return f.read()
            except:
                return f"[无法读取文件: 编码不支持]"
    except Exception as e:
        return f"[读取文件时出错: {str(e)}]"

def generate_markdown(output_file="project_documentation.md"):
    """
    生成Markdown文档
    """
    current_dir = os.getcwd()
    dir_name = os.path.basename(current_dir)
    
    with open(output_file, 'w', encoding='utf-8') as md_file:
        # 写入标题
        md_file.write(f"# {dir_name} 项目文档\n\n")
        
        # 写入生成时间
        from datetime import datetime
        md_file.write(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        # 写入目录树
        md_file.write("## 目录结构\n\n")
        md_file.write("```\n")
        md_file.write(get_directory_tree(current_dir))
        md_file.write("\n```\n\n")
        
        # 收集所有需要处理的文件
        files_to_process = []
        for root, dirs, files in os.walk(current_dir):
            # 忽略一些目录
            dirs[:] = [d for d in dirs if not d.startswith('.') 
                      and d not in ['__pycache__', 'build', 'dist', 'node_modules']]
            
            for file in files:
                if should_process_file(file):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, current_dir)
                    files_to_process.append((rel_path, full_path))
        
        # 按文件类型和路径排序
        files_to_process.sort(key=lambda x: (os.path.splitext(x[0])[1], x[0]))
        
        # 写入文件内容
        md_file.write("## 源代码\n\n")
        
        if not files_to_process:
            md_file.write("*没有找到支持的文件类型*\n")
            md_file.write("*支持的文件类型: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css*\n")
        else:
            # 按文件类型分组
            file_types = {
                '.pro': 'Qt项目文件',
                '.h': '头文件',
                '.cpp': 'C++源文件',
                '.vue': 'Vue组件',
                '.js': 'JavaScript文件',
                '.ts': 'TypeScript文件',
                '.jsx': 'React JSX文件',
                '.tsx': 'React TSX文件',
                '.yml': 'YAML配置文件',
                '.yaml': 'YAML配置文件',
                '.xml': 'XML文件',
                '.html': 'HTML文件',
                '.htm': 'HTML文件',
                '.py': 'Python文件',
                '.css': 'CSS样式文件'   # <--- 添加 .css 描述
            }
            
            # 定义分组顺序
            extensions_order = [
                '.pro', '.h', '.cpp', 
                '.vue', '.ts', '.tsx', '.js', '.jsx',
                '.yml', '.yaml', '.xml', 
                '.css',                     # <--- 添加 .css，放在 HTML 之前或之后均可
                '.html', '.htm',
                '.py'
            ]
            
            for ext in extensions_order:
                type_files = [(rel, full) for rel, full in files_to_process if rel.endswith(ext)]
                if type_files:
                    md_file.write(f"### {file_types.get(ext, ext)}文件\n\n")
                    
                    for rel_path, full_path in type_files:
                        # 写入文件名作为子标题
                        md_file.write(f"#### {rel_path}\n\n")
                        
                        # 写入文件内容
                        content = read_file_content(full_path)
                        
                        # 根据文件扩展名设置代码块语言
                        lang_map = {
                            '.h': 'cpp',
                            '.cpp': 'cpp',
                            '.pro': 'makefile',
                            '.vue': 'vue',
                            '.js': 'javascript',
                            '.ts': 'typescript',
                            '.jsx': 'jsx',
                            '.tsx': 'tsx',
                            '.yml': 'yaml',
                            '.yaml': 'yaml',
                            '.xml': 'xml',
                            '.html': 'html',
                            '.htm': 'html',
                            '.py': 'python',
                            '.css': 'css'      # <--- 添加 .css 对应的语言标识
                        }
                        lang = lang_map.get(ext, '')
                        
                        md_file.write(f"```{lang}\n")
                        md_file.write(content)
                        if content and not content.endswith('\n'):
                            md_file.write('\n')
                        md_file.write("```\n\n")
        
        # 写入统计信息
        md_file.write("## 统计信息\n\n")
        md_file.write(f"- 总文件数: {len(files_to_process)}\n")
        
        # 按扩展名统计
        ext_counts = {}
        for rel_path, _ in files_to_process:
            ext = os.path.splitext(rel_path)[1]
            ext_counts[ext] = ext_counts.get(ext, 0) + 1
        
        # 显示统计信息
        ext_names = {
            '.pro': 'Qt项目',
            '.h': '头文件',
            '.cpp': 'C++源文件',
            '.vue': 'Vue组件',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React JSX',
            '.tsx': 'React TSX',
            '.yml': 'YAML',
            '.yaml': 'YAML',
            '.xml': 'XML',
            '.html': 'HTML',
            '.htm': 'HTML',
            '.py': 'Python',
            '.css': 'CSS样式'    # <--- 添加 .css 统计名称
        }
        
        for ext, count in ext_counts.items():
            name = ext_names.get(ext, ext)
            md_file.write(f"- {name}文件 ({ext}): {count}个\n")
    
    print(f"文档已生成: {output_file}")
    print(f"共处理了 {len(files_to_process)} 个文件")
    print(f"支持的文件类型: .h, .cpp, .pro, .vue, .js, .ts, .jsx, .tsx, .yml, .yaml, .xml, .html, .py, .css")

def main():
    """
    主函数
    """
    print("项目文档生成器 (支持C/C++/Qt/Vue/JavaScript/TypeScript/YAML/XML/HTML/Python/CSS)")
    print("=" * 80)
    
    # 可以自定义输出文件名
    output_filename = "project_documentation.md"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    
    generate_markdown(output_filename)

if __name__ == "__main__":
    main()