import subprocess
from ..utils import ThreadedSegment, get_git_subprocess_env


def get_head_hash():
    try:
        p = subprocess.Popen(['git', 'rev-parse', '--short=12', 'HEAD'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=get_git_subprocess_env())
    except OSError:
        # Popen will throw an OSError if git is not found
        return ""

    pdata = p.communicate()
    if p.returncode != 0:
        return ""

    return pdata[0].decode("utf-8").strip()


class Segment(ThreadedSegment):
    def run(self):
        self.head_hash = get_head_hash()

    def add_to_powerline(self):
        self.join()
        if not self.head_hash:
            return

        bg = self.powerline.theme.GIT_HEAD_HASH_BG
        fg = self.powerline.theme.GIT_HEAD_HASH_FG

        hh = " " + self.head_hash + " "
        self.powerline.append(hh, fg, bg)
