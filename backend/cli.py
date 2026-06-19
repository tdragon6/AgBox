'''
命令行
'''


import os
import sys
import signal
import time
import typer
import subprocess
import questionary

from core.config import settings
from core.auth import hash_password
from _utils.func import desensitize
from schemas.auth import LoginRequest
from rich.console import Console
from pathlib import Path
from core.database import db_session


ROOT_DIR = Path(__file__).parent
PID_FILE_PATH = ROOT_DIR / 'pid'
SERVICE_SCRIPT_PATH = ROOT_DIR / 'main.py'


app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode='rich'
)

console = Console()


# 多语言
T = {
    'zh-CN': {
        'version': '版本信息',
        'lang': '语言配置',
        'lang_select': '选择语言',
        'lang_not_supported': '不支持的语言',
        'username': '用户名配置',
        'username_input': '请输入用户名：',
        'username_format_error': '用户名格式错误',
        'password': '密码配置',
        'password_input': '请输入密码：',
        'password_format_error': '密码格式错误',
        'start': '启动服务',
        'stop': '停止服务',
        'daemon': '后台运行',
        'service_start': '服务已启动：',
        'service_stop': '服务已停止',
        'service_stop_confirm': '存在运行或等待中的任务，确认停止服务吗?'
    },
    'en-US': {
        'version': 'Version',
        'lang': 'Language Config',
        'lang_select': 'Select Language',
        'lang_not_supported': 'Language not supported',
        'username': 'Username Config',
        'username_input': 'Please input username:',
        'username_format_error': 'Username format error',
        'password': 'Password Config',
        'password_input': 'Please input password:',
        'password_format_error': 'Password format error',
        'start': 'Start Service',
        'stop': 'Stop Service',
        'daemon': 'Daemon Service',
        'service_start': 'Service started:',
        'service_stop': 'Service stopped',
        'service_stop_confirm': 'There are running or pending tasks, confirm you want to stop the service?'
    },
}


def get_pid():
    '''
    获取服务进程ID
    '''
    with PID_FILE_PATH.open('r') as f:
        pid_str = f.read().strip()
    
    if pid_str == '':
        return None
    else:
        return int(pid_str)


def is_running(pid):
    '''
    检查服务进程是否正在运行
    '''
    try:
        os.kill(pid, 0)
        return True
    except:
        return False


@app.command(help=T[settings.LANG]['version'])
def version():
    '''
    版本信息
    '''
    console.print(f'[bold green]{settings.APP_VERSION}[/bold green]')


@app.command(help=T[settings.LANG]['lang'])
def lang(lang: str = None):
    '''
    语言配置
    '''
    if lang is None:
        lang = questionary.select(
            T[settings.LANG]['lang_select'],
            choices=list(T.keys()),
            default=settings.LANG,
        ).ask()

    if lang is None:
        return
    
    if lang not in T.keys():
        console.print(f'[red][✗][/red] {T[settings.LANG]["lang_not_supported"]}')
        return
    
    settings.LANG = lang
    console.print(f'[green][✓][/green] {lang}')


@app.command(help=T[settings.LANG]['username'])
def username(username: str = typer.Argument(None)):
    '''
    配置用户名
    '''
    if username is None:
        username = questionary.text(T[settings.LANG]['username_input']).ask()
    
    if username is None:
        return

    try:
        LoginRequest(username=username, password='x' * 8)
    except:
        console.print(f'[red][✗][/red] {T[settings.LANG]["username_format_error"]}')
        return
    
    settings.USERNAME = username
    console.print(f'[green][✓][/green] {username}')


@app.command(help=T[settings.LANG]['password'])
def password(password: str = typer.Argument(None)):
    '''
    配置密码
    '''
    if password is None:
        password = questionary.password(T[settings.LANG]['password_input']).ask()
    
    if password is None:
        return
    
    try:
        LoginRequest(username='x' * 8, password=password)
    except:
        console.print(f'[red][✗][/red] {T[settings.LANG]["password_format_error"]}')
        return
    
    settings.PASSWORD = hash_password(password)[-1]
    console.print(f'[green][✓][/green] {desensitize(password)}')


@app.command(help=T[settings.LANG]['start'])
def start(
    daemon: bool = typer.Option(False, '--daemon', '-d', help=T[settings.LANG]['daemon']),
):
    '''
    启动服务
    '''
    pid = get_pid()
    if pid is not None and is_running(pid):
        console.print(f'[yellow][⚠][/yellow] {T[settings.LANG]["service_start"]} {pid}')
        return

    cmd = [sys.executable, str(SERVICE_SCRIPT_PATH)]

    if daemon:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        pid = proc.pid

        with PID_FILE_PATH.open('w') as f:
            f.write(str(pid))
        
        console.print(f'[green][✓][/green] {T[settings.LANG]["service_start"]} {pid}')
    else:
        subprocess.run(cmd)


@app.command(help=T[settings.LANG]['stop'])
def stop():
    '''
    停止服务
    '''
    from services.tasks.task import get_tasks_items
    
    pid = get_pid()
    if pid is None or not is_running(pid):
        console.print(f'[yellow][⚠][/yellow] {T[settings.LANG]["service_stop"]}')
        return
    
    with db_session() as db:
        running_pending_tasks = get_tasks_items(
            db=db,
            page=0,
            statuses=['running', 'pending']
        )[-1]['items']

        if not running_pending_tasks:
            pass
        else:
            confirm = questionary.confirm(T[settings.LANG]['service_stop_confirm']).ask()
            if not confirm:
                return

    os.kill(pid, signal.SIGTERM)

    for _ in range(10):
        if not is_running(pid):
            break
        time.sleep(0.5)
    
    with PID_FILE_PATH.open('w') as f:
        f.write('')
    
    console.print(f'[green][✓][/green] {T[settings.LANG]["service_stop"]}')


if __name__ == '__main__':
    app(prog_name='agbox')
