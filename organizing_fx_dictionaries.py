import shutil
import os
from pathlib import Path
import subprocess

def org_bates(source_folder,destination_folder):
    corpus = "bates"
    _count = 0

    for file in (source_folder / "Bates").rglob("*.cha"):
        task = file.parent.name

        if task == "Free20":
            _time = "20"
            _task = "toyplay"
            _other = "0"
            _name = file.stem.lower()
            fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

            shutil.copy(file, destination_folder / fname)

        if task == "Free28":
            _time = "28"
            _task = "toyplay"
            _other = "0"
            _name = file.stem.lower()[:-2]
            fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

            shutil.copy(file, destination_folder / fname)

        if task == "Snack28":
            _time = "28"
            _task = "meal"
            _other = "0"
            _name = file.stem.lower()
            fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

            shutil.copy(file, destination_folder / fname)

        if task == "Story28":
            _time = "28"
            _task = "book"
            _other = "0"
            _name = file.stem.lower()[:-2]
            fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

            shutil.copy(file, destination_folder / fname)

        _count += 1


def org_bernstein(source_folder,destination_folder):
    corpus = "bernstein"
    _count = 0

    for file in (source_folder / "Bernstein").rglob("*.cha"):
        _name = file.parent.name
        _time = "0"
        _task = "toyplay"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_bloom(source_folder,destination_folder):
    corpus = "bloom"
    _count = 0

    for file in (source_folder / "Bloom").rglob("*.cha"):
        _name = file.parent.name
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_braunwald(source_folder,destination_folder):
    corpus = "braunwald"
    _count = 0

    for file in (source_folder / "Braunwald").rglob("*.cha"):
        _name = "L"
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_brown(source_folder,destination_folder):
    corpus = "brown"
    _count = 0

    for file in (source_folder / "Brown").rglob("*.cha"):
        _name = file.parent.name.lower()
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_champaign(source_folder,destination_folder):
    corpus = "champaign"
    _count = 0

    for file in (source_folder / "Champaign").rglob("*.cha"):
        _name = file.stem.lower()
        _time = file.parent.name[0:2]
        _task = "toyplay"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_clark(source_folder,destination_folder):
    corpus = "clark"
    _count = 0

    for file in (source_folder / "Clark").rglob("*.cha"):
        _name = "Shem"
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_demetras1(source_folder,destination_folder):
    corpus = "demetras1"
    _count = 0

    for file in (source_folder / "Demetras1").rglob("*.cha"):
        _name = "trevor"
        _time = "0"
        _task = "toyplay"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_demetras2(source_folder,destination_folder):
    corpus = "demetras2"
    _count = 0

    for file in (source_folder / "Demetras2").rglob("*.cha"):
        _name = file.parent.parent.stem.lower()
        _time = "0"
        _task = "discussion"
        _other = file.parent.stem
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_ehs(source_folder,destination_folder):
    corpus = "ehs"
    _count = 0

    time_dict = {
        "14-mot": ["14", "mot"]
        , "24-mot": ["24", "mot"]
        , "36-mot": ["36", "mot"]
        , "pre-k-book": ["pk", "book"]
        , "pre-K-fat": ["pk", "fat"]
        , "pre-K-mot": ["pk", "mot"]
    }

    for file in (source_folder / "EHS").rglob("*.cha"):
        _name = file.stem.lower()
        _time = time_dict[file.parent.stem][0]
        _task = "multi"
        _other = time_dict[file.parent.stem][1]
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_ellisweismer(source_folder,destination_folder):
    corpus = "ellisweismer"
    _count = 0

    task_dict = {"ec": "toyplay", "pc": "toyplay", "int": "interview", "conv": "interview"}

    for file in (source_folder / "EllisWeismer").rglob("*.cha"):
        _name = file.stem.lower()
        _time = file.parent.stem[:2].lower()
        _task = "everyday"
        _other = task_dict[file.parent.stem[2:]]
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_feldman(source_folder,destination_folder):
    corpus = "feldman"
    _count = 0

    for file in (source_folder / "Feldman").rglob("*.cha"):
        _name = "steven"
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_gleason(source_folder,destination_folder):
    corpus = "gleason"
    _count = 0

    task_dict = {"Dinner": "meal", "Father": "toyplay", "Mother": "toyplay"}

    for file in (source_folder / "Gleason").rglob("*.cha"):
        _name = file.stem.lower()
        _time = "0"
        _task = task_dict[file.parent.stem].lower()
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_hslld(source_folder,destination_folder):
    corpus = "hslld"
    _count = 0

    task_dict = {"BR": "book", "ER": "retell", "MT": "meal", "TP": "toyplay", "ET": "tests", "RE": "book",
                 "LW": "writing", "MD": "other"}

    for file in (source_folder / "HSLLD").rglob(".cha*"):
        _name = file.stem.lower()[:3]
        _time = file.parent.parent.stem.lower()
        _task = task_dict[file.parent.stem].lower()
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_kuczaj(source_folder,destination_folder):
    corpus = "kuczaj"
    _count = 0

    for file in (source_folder / "Kuczaj").rglob("*.cha"):
        _name = "abe"
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_post(source_folder,destination_folder):
    corpus = "post"
    _count = 0

    for file in (source_folder / "Post").rglob("*.cha"):
        _name = file.parent.stem.lower()
        _time = "0"
        _task = "toyplay"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_mccune(source_folder,destination_folder):
    corpus = "mccune"
    _count = 0

    for file in (source_folder / "McCune").rglob("*.cha"):
        _name = file.parent.stem.lower()
        _time = "0"
        _task = "toyplay"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_macwhinney(source_folder,destination_folder):
    corpus = "macwhinney"
    _count = 0

    for file in (source_folder / "MacWhinney").rglob("*.cha"):
        _name = "rossmark"
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_nelson(source_folder,destination_folder):
    pass


def org_newengland(source_folder,destination_folder):
    corpus = "newengland"
    _count = 0

    for file in (source_folder / "NewEngland").rglob("*.cha"):
        _name = file.stem.lower()
        _time = file.parent.stem.lower()
        _task = "multi"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_newmanratner(source_folder,destination_folder):
    corpus = "newmanratner"
    _count = 0

    for file in (source_folder / "NewmanRatner").rglob("*.cha"):
        _name = file.stem.lower()
        _time = file.parent.stem.lower()
        _task = "toyplay"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_peters(source_folder,destination_folder):
    corpus = "peters"
    _count = 0

    for file in (source_folder / "Peters").rglob("*.cha"):
        _name = "seth"
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_rollins(source_folder,destination_folder):
    corpus = "rollins"
    _count = 0

    for file in (source_folder / "Rollins").rglob("*.cha"):
        if file.stem.lower()[
           0:4] == "jw12": continue  # skipping these because it is unclear whether it is the same kid.

        _name = file.stem.lower()[0:2]
        _time = file.stem.lower()[2:4]
        _task = "toyplay"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_sachs(source_folder,destination_folder):
    corpus = "sachs"
    _count = 0

    for file in (source_folder / "Sachs").rglob("*.cha"):
        _name = "naomi"
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_snow(source_folder,destination_folder):
    pass


def org_suppes(source_folder,destination_folder):
    corpus = "suppes"
    _count = 0

    for file in (source_folder / "Suppes").rglob("*.cha"):
        _name = "nina"
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_vanhouten(source_folder,destination_folder):
    corpus = "vanhouten"
    _count = 0

    task_dict = {"teaching": "tests", "lunch": "meal", "freeplay": "toyplay"}

    for file in (source_folder / "VanHouten").rglob("*.cha"):
        _name = file.stem.lower()[:-1]
        _time = file.parent.parent.stem.lower()
        _task = task_dict[file.parent.stem].lower()
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


def org_weist(source_folder,destination_folder):
    corpus = "weist"
    _count = 0

    for file in (source_folder / "Weist").rglob("*.cha"):
        _name = file.parent.stem.lower()
        _time = "0"
        _task = "everyday"
        _other = "0"
        fname = f"{corpus}_{str(_count)}_{_task}_{_time}_{_other}_{corpus}_{_name}.cha"

        shutil.copy(file, destination_folder / fname)

        _count += 1


#Leave at end
main_dict = {}
main_dict["default"] ={  "Bates":       org_bates
                        ,"Bernstein":   org_bernstein
                        ,"Bloom":       org_bloom
                        ,"Braunwald":   org_braunwald
                        ,"Brown":       org_brown
                        ,"Champaign":   org_champaign
                        ,"Clark":       org_clark
                        ,"Demetras1":   org_demetras1
                        ,"Demetras2":   org_demetras2
                        ,"EHS":         org_ehs
                        ,"EllisWeismer":org_ellisweismer
                        ,"Feldman":     org_feldman
                        ,"Gleason":     org_gleason
                        ,"HSLLD":       org_hslld
                        ,"Kuczaj":      org_kuczaj
                        ,"MacWhinney":  org_macwhinney
                        ,"McCune":      org_mccune
                        ,"Nelson":      org_nelson
                        ,"NewEngland":  org_newengland
                        ,"NewmanRatner":org_newmanratner
                        ,"Peters":      org_peters
                        ,"Post":        org_post
                        ,"Rollins":     org_rollins
                        ,"Sachs":       org_sachs
                        ,"Snow":        org_snow
                        ,"Suppes":      org_suppes
                        ,"VanHouten":   org_vanhouten
                        ,"Weist":       org_weist
                        }

def return_fx_dict(dict_name: str):
    return main_dict[dict_name]