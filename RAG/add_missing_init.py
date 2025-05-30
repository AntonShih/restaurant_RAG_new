# import os

# def add_missing_init_files(root_dir="."):
#     for dirpath, dirnames, filenames in os.walk(root_dir):
#         if "__pycache__" in dirpath or ".venv" in dirpath:
#             continue
#         if "__init__.py" not in filenames:
#             init_path = os.path.join(dirpath, "__init__.py")
#             open(init_path, "a").close()
#             print(f"✅ Created: {init_path}")

# if __name__ == "__main__":
#     add_missing_init_files()


import os

# 不該加入 __init__.py 的目錄關鍵字（可擴充）
skip_prefixes = [".git", ".github", ".pytest_cache", ".venv", "htmlcov", "data"]
deleted = 0

for dirpath, _, filenames in os.walk("."):
    if any(dirpath.startswith(f".\\{prefix}") or f"\\{prefix}\\" in dirpath for prefix in skip_prefixes):
        for file in filenames:
            if file == "__init__.py":
                full_path = os.path.join(dirpath, file)
                try:
                    os.remove(full_path)
                    print(f"🗑️ Deleted: {full_path}")
                    deleted += 1
                except Exception as e:
                    print(f"❌ Failed to delete {full_path}: {e}")

print(f"\n✅ Done. Total deleted: {deleted}")
