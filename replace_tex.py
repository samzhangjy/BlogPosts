import os
import sys
import re
import shutil

interline_tag = '\n<img src="https://www.zhihu.com/equation?tex={}" alt="{}\\\\" class="ee_img tr_noresize" eeimg="1">\n'
interline_pattern = '\$\$\n*(.*?)\n*\$\$'
inline_tag = '<img src="https://www.zhihu.com/equation?tex={}" alt="{}" class="ee_img tr_noresize" eeimg="1">'
inline_pattern = '\$\n*(.*?)\n*\$'

def replace_tex(content):
	def dashrepl(matchobj, tag):
		formulas = matchobj.group(1)
		return tag.format(formulas, formulas)

	content = re.sub(interline_pattern, lambda mo: dashrepl(mo, interline_tag), content)
	content = re.sub(inline_pattern, lambda mo: dashrepl(mo, inline_tag), content)

	return content

def un_replace_tex(content):
	def dashrepl(matchobj, tag):
		formulas = matchobj.group(1)
		return tag.format(formulas, formulas)

	content = re.sub(interline_pattern, lambda mo: dashrepl(mo, interline_tag), content)
	content = re.sub(inline_pattern, lambda mo: dashrepl(mo, inline_tag), content)

	return content


def get_filename(path, filetype):
    name = []
    root_folder = "posts-generated"
    try:
        shutil.rmtree(root_folder)
    except:
        pass
    os.mkdir(root_folder)
    for root, dirs, files in os.walk(path):
        for d in dirs:
            os.mkdir(os.path.join(root_folder, d))
        for i in files:
            if os.path.splitext(i)[1] == filetype:
                with open(os.path.join(root, i), "r", encoding="utf-8") as f:
                    replaced = replace_tex(f.read())
                with open(os.path.join(".", root_folder, os.path.join(root.split("\\", 2)[-1], i)), "w", encoding="utf-8") as f:
                    f.write(replaced)
                    print("Generated file", os.path.join(".", root_folder, os.path.join(root.split("\\", 2)[-1], i)))
    return name

if __name__=='__main__':
    get_filename(".\\posts\\", ".md")