'''
脚本工具：转换 hermes 原生技能目录结构
'''


import json
import yaml
import re
import shutil
from pathlib import Path


def find_file_dirs(
    path: Path,
    file_name: str
) -> tuple[bool, str, list[Path]]:
    '''
    查找目录下指定文件所在目录路径
    '''
    result = [ file.parent for file in list(path.rglob(file_name)) ]

    return True, 'success', result


def get_skills_info(
    path: Path
) -> tuple[bool, str, str | None]:
    '''
    获取 skills 的 name
    '''
    with (path / 'SKILL.md').open('r', encoding='utf-8') as f:
        lines = []
        for line_num in range(30):
            line = f.readline()
            if line is None:
                break
            if line.strip() == '---':
                if line_num == 0:
                    continue
                else:
                    break
            lines.append(line)
        
        skills_content = ''.join(lines)
    
    try:
        skills_content_dict = yaml.safe_load(skills_content)
    except:
        skills_content_dict = {}
    
    name = skills_content_dict.get('name', '').strip().strip('"\'')
    if re.match(r'^[a-zA-Z0-9_-]+$', name):
        return True, 'success', name
    else:
        return False, 'skills_name_format_error', None


def merge_second_last_to_third_last(path: Path):
    '''
    合并倒数第二级目录的所有内容到倒数第三级目录，并删除空的倒数第二级目录
    '''
    source_dir = path.parents[0]
    if not source_dir.exists():
        return False, 'source_dir_not_exist', None

    target_dir = path.parents[1]

    for item in source_dir.iterdir():
        target_path = target_dir / item.name
        item.replace(target_path)

    source_dir.rmdir()

    return True, 'success', None


if __name__ == '__main__':
    STORE_PATH = Path(__file__).parent.parent / 'store'
    SKILLS_PATH = STORE_PATH / 'skills'

    source_hermes_self_skills_path_list = find_file_dirs(SKILLS_PATH, 'SKILL.md')[-1]

    # 合并倒数第二级目录的所有内容到倒数第三级目录，并删除空的倒数第二级目录
    for path in source_hermes_self_skills_path_list:
        source_skill_dir_structure = path.relative_to(SKILLS_PATH).parts

        if len(source_skill_dir_structure) >= 3:
            merge_second_last_to_third_last(path)

    # 建立技能索引
    result = []

    hermes_self_skills_path_list = find_file_dirs(SKILLS_PATH, 'SKILL.md')[-1]
    for path in hermes_self_skills_path_list:
        skill_dir_structure = path.relative_to(SKILLS_PATH).parts

        status, msg, data = get_skills_info(path)
        if not status:
            continue
        
        if skill_dir_structure[-1] != data:
            path.replace(path.parent / data)
        
        result.append(
            {
                'category': skill_dir_structure[0] if len(skill_dir_structure) != 1 else '',
                'name': data,
            }
        )
    
    for item in result:
        print(item)

    with (STORE_PATH / 'hermes_self_skills.json').open('w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=4))
