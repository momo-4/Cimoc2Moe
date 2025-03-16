"""Cimoc to Moe"""
import contextlib
import json
import os
import re
import shutil
import zipfile


class Cimoc2Mox:
    def __init__(self, source: str):
        self.dir = os.path.abspath(source)

        self.cimoc_config = None
        self.chapters = None
        self.group = None

    def read(self):
        os.chdir(self.dir)
        with open("index.cdif", encoding="utf-8") as f:
            a = re.search(r"(?<=cimoc).*", f.readline()).group()
            b = json.loads(a)

            self.cimoc_config = b

        c1 = [i["title"] for i in self.cimoc_config["list"]]
        c2 = [i["path"] for i in self.cimoc_config["list"]]

        lists = {}
        for title, path in zip(c1, c2):
            lists[path] = title

        self.cimoc_config["list"] = lists
        self._detect_source()

    def _detect_source(self):
        a = os.listdir(self.dir)

        chapters = []
        for dir in a:
            for k1 in self.cimoc_config["list"]:
                k2 = self._detect_word(k1)
                if dir == k2:
                    chapters.extend([self.cimoc_config["list"][k1]])
        self.chapters = chapters

    @staticmethod
    def _detect_word(word: str) -> str:
        reg = '[\\\\/:*?"<>|]'
        if "/" in word or "?" in word:
            word = re.sub(reg, "-", word)
        return word

    def copy(self):
        os.chdir(self.dir)
        self._init_chapters()
        a = os.listdir(self.dir)
        a.remove(self.cimoc_config["title"])
        for path in a:
            if os.path.isdir(path):
                with open(f"{path}/index.cdif") as f:
                    config = json.loads(re.search(r"(?<=cimoc).*", f.readline()).group())
                    title = config["title"]
                figs = os.listdir(f"{self.dir}/{path}")
                figs.remove("index.cdif")

                for fig in figs:
                    f1 = f"{path}/{fig}"
                    f2 = f"{self.cimoc_config['title']}/{title}/{fig}"
                    shutil.copyfile(f1, f2)
                print(f"{self.cimoc_config['title']}: {title} 完成")
        # self._rename_dir()

    def _init_chapters(self):
        os.chdir(self.dir)
        with contextlib.suppress(FileExistsError):
            os.mkdir(f"{self.cimoc_config['title']}")

        os.chdir(self.cimoc_config["title"])
        for i in self.chapters:
            try:
                os.mkdir(i)
            except FileExistsError:
                continue
        os.chdir("..")

    def _rename_dir(self):

        for c in self.chapters:
            os.rename(f"{self.cimoc_config['title']}/{c}", c.zfill(3))

        chapters = self.chapters
        chapters = [i.zfill(3) for i in chapters]
        self.chapters = chapters

    def zipping(self):
        self._grouping()
        dirs = os.path.abspath(f"{self.dir}\\{self.cimoc_config['title']}")

        for g in self.group:
            with zipfile.ZipFile(f"{dirs}\\{min(g)}-{max(g)}.zip", "w") as myzip:
                for chapter in g:
                    figs = os.listdir(f"{dirs}\\{chapter}")
                    for fig in figs:
                        myzip.write(f"{dirs}/{chapter}\\{fig}", f"{chapter}\\{fig}")
            print(f"{min(g)}-{max(g)}.zip 完成")

    def _grouping(self):
        a = list(range(0, len(self.chapters), 5))

        n = 0
        chapters = sorted(self.chapters)
        group = []
        while n < len(a):
            try:
                group.append(chapters[a[n]:a[n + 1]])
            except IndexError:
                group.append(chapters[a[n]:])
            finally:
                n += 1

        self.group = group
