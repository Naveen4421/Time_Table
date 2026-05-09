import sys

def make_logout_vibrant(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Make the button more vibrant
    old_style = 'style="padding: 8px 15px; margin-right: 10px; font-size: 0.8rem; background: rgba(255,126,126,0.1); border-color: rgba(255,126,126,0.3); color: #ff7e7e;"'
    new_style = 'style="padding: 10px 20px; margin-right: 15px; font-size: 0.85rem; background: #ff7e7e; color: #fff; border: none; border-radius: 12px; font-weight: 800; cursor: pointer; box-shadow: 0 4px 12px rgba(255,126,126,0.3);"'
    
    if old_style in content:
        content = content.replace(old_style, new_style)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

make_logout_vibrant('study_timetable.html')
make_logout_vibrant('index.html')
print("Made Logout button vibrant.")
