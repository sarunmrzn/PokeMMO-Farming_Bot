import pygetwindow as gw

windows = [w.title for w in gw.getAllWindows() if w.title.strip()]
for i, title in enumerate(windows, 1):
    print(f"{i}. {title}")
