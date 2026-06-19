'''
Agbox Sync Assign Task Script
'''


import argparse
import os
import sys
import subprocess
from pathlib import Path

import json_repair
from hermes_state import SessionDB


def find_child_session_ids(
    all_session_ids: list[dict],
    session_id: str,
    child_session_ids: list[str] = []
) -> list[str]:
    '''
    recursive search for sub session ID
    '''
    for item in all_session_ids:
        if item['parent_session_id'] == session_id:
            child_session_ids.append(item['id'])

            return find_child_session_ids(
                all_session_ids=all_session_ids,
                session_id=item['id'],
                child_session_ids=child_session_ids
            )
    
    return child_session_ids


def get_tasks_results(
    robots_dir: Path,
    session_id: str,
    name: str = None
):
    '''
    get tasks results
    '''
    if name is not None:
        db_path = robots_dir / name / 'state.db'
    else:
        db_path = robots_dir.parent / 'coordinator' / 'agbox-coordinator-sync' / 'state.db'
    
    session_db = SessionDB(
        db_path=db_path
    )

    items = session_db.get_messages(session_id)

    all_session_ids = session_db.list_sessions_rich(
        limit=999999,
        offset=0,
        include_children=True
    )

    child_session_ids = find_child_session_ids(
        all_session_ids=all_session_ids,
        session_id=session_id
    )

    for child_session_id in child_session_ids:
        items += session_db.get_messages(child_session_id)
    
    result = items[-1]['content']

    return result


def run_chat_process(
    robots_dir: Path,
    task_description: str,
    work_dir: Path,
    session_id: str,
    name: str = None
):
    '''
    run chat process
    '''
    if name is not None:
        hermes_home = str(robots_dir / name)
        task_description += f'\n\nNote: All output must be in the current working directory: {work_dir}.'
    else:
        hermes_home = str(robots_dir.parent / 'coordinator' / 'agbox-coordinator-sync')
    
    env = os.environ.copy()
    env.update({'HERMES_HOME': hermes_home})

    result = subprocess.run(
        [str(Path(sys.executable).parent / 'hermes'), 'chat', '--yolo', '-r', session_id, '-Q', '-q', task_description],
        cwd=work_dir,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True
    )

    return result.returncode, result.stdout.strip(), result.stderr.strip()


def run_robots_loop(
    robots_dir: Path,
    task_description: str,
    work_dir: Path,
    session_id: str,
    name: str = None
):
    '''
    run robots loop
    '''
    returncode, _, _ = run_chat_process(
        robots_dir=robots_dir,
        task_description=task_description,
        work_dir=work_dir,
        session_id=session_id,
        name=name
    )

    if returncode != 0:
        if name is not None:
            result = f'{{"name":"{name}","message": "Task execution failed"}}'
        else:
            result = f'{{"name":null,"message": "Task execution failed"}}'
        
        return run_robots_loop(
            robots_dir=robots_dir,
            task_description=result,
            work_dir=work_dir,
            session_id=session_id,
            name=None
        )

    result = get_tasks_results(
        robots_dir=robots_dir,
        session_id=session_id,
        name=name
    )

    if name is None:
        try:
            data = json_repair.loads(result)
            if any(
                [
                    'name' not in data.keys(),
                    'message' not in data.keys(),
                    'finished' not in data.keys()
                ]
            ):
                raise ValueError('JSON format is incorrect')
        except:            
            message = f'{{"name":null, "message": "The JSON format is incorrect, please check."}}'
            return run_robots_loop(
                robots_dir=robots_dir,
                task_description=message,
                work_dir=work_dir,
                session_id=session_id,
                name=None
            )
        
        if data['finished']:
            return
        
        next_name = data['name']
        next_message = data['message']
    else:
        next_name = None
        next_message = f'{{"name":"{name}","message":"{result}"}}'
    
    return run_robots_loop(
        robots_dir=robots_dir,
        task_description=next_message,
        work_dir=work_dir,
        session_id=session_id,
        name=next_name
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Agbox Sync Assign Task Script',
        epilog='Usage Example: <python executable> loop.py --robots_dir <robots_dir> --task_description <task_description> --work_dir <work_dir> --session_id <session_id>'
    )

    parser.add_argument('--robots_dir', required=True, help='All Digital employees home directory')
    parser.add_argument('--task_description', required=True, help='Task description to assign to the digital employee')
    parser.add_argument('--work_dir', required=True, help='Work directory')
    parser.add_argument('--session_id', required=True, help='Session ID')
    args = parser.parse_args()

    result = run_robots_loop(
        robots_dir=Path(args.robots_dir),
        task_description=args.task_description,
        work_dir=Path(args.work_dir),
        session_id=args.session_id
    )