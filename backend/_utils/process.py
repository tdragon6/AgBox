'''
后台进程工具
'''


import os
import signal
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path
from typing import Callable

import psutil
from core.logger import logger


class ProcessWorkerThread(threading.Thread):
    '''
    定义一个安全的进程线程
    '''
    def __init__(
        self,
        command: list[str],
        cwd: Path = Path.home(),
        env: dict = {},
        task_id: str = None,
        callback: Callable = None
    ):
        super().__init__(daemon=True)
        self.command = command
        self.cwd = cwd
        self.env = os.environ.copy()
        self.env.update(env)
        self.process = None
        self.stdout = None
        self.stderr = None
        self.returncode = None
        self.task_id = task_id
        self.callback = callback
    def run(
        self
    ):
        '''
        启动进程
        '''
        try:
            kwargs = {
                'stdout': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'text': True,
                'env': self.env,
                'cwd': self.cwd
            }
            
            # 架构设计在 linux 或 docker 中，预留兼容windows环境
            if sys.platform != 'win32':
                kwargs['preexec_fn'] = os.setsid

            self.process = subprocess.Popen(self.command, **kwargs)
            self.stdout, self.stderr = self.process.communicate()
            self.returncode = self.process.returncode
        except:
            self.returncode = -1
            logger.error(traceback.format_exc())
        finally:
            if self.callback:
                self.callback(self)


    def stop(
        self
    ):
        '''
        终止进程及其全部子进程树
        '''
        if not self.process or self.process.poll() is not None:
            return

        pid = self.process.pid

        try:
            # 架构设计在 linux 或 docker 中，预留兼容windows环境
            if sys.platform == 'win32':
                self._kill_windows_process_tree(pid)
            else:
                self._kill_unix_process_group(pid)
            
            self.process.wait(timeout=10)
            logger.info(f'Tree PID: {pid} Stopped')
        except:
            pass
        finally:
            self.returncode = -1
            if self.callback:
                self.callback(self, is_interrupted=True)


    def _kill_unix_process_group(
        self,
        pid: int
    ):
        try:
            pgid = os.getpgid(pid)
            os.killpg(pgid, signal.SIGTERM)
            time.sleep(3)
            try:
                os.killpg(pgid, signal.SIGKILL)
            except:
                pass
        except:
            pass

    def _kill_windows_process_tree(
        self,
        pid: int
    ):
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            
            for child in children:
                try:
                    child.terminate()
                except:
                    pass
            
            _, alive = psutil.wait_procs(children, timeout=3)
            
            for p in alive:
                try:
                    p.kill()
                except:
                    pass
            
            try:
                parent.terminate()
                parent.wait(timeout=2)
            except psutil.NoSuchProcess:
                pass
            except psutil.TimeoutExpired:
                parent.kill()
        except:
            pass