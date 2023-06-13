import subprocess
from pathlib import Path
import sys
import random
import csv
import time

SOURCE = "../faial-artifact-cav21/datasets/gpuverify-cav14/all-cuda.txt"
PREFIX = "../faial-artifact-cav21/datasets/gpuverify-cav14/faial/"
LOGICS = ["AUFLIA", "AUFLIRA",
              "AUFNIRA", "LRA",
              "QF_ABV", "QF_AUFBV",
              "QF_AUFLIA", "QF_AX",
              "QF_BV", "QF_BVFP",
              "QF_BVRE", "QF_DT",
              "QF_FP", "QF_FPBV",
              "QF_IDL", "QF_LIA",
              "QF_LRA", "QF_RDL",
              "QF_S", "QF_SLIA",
              "QF_UF", "QF_UFBV",
              "QF_UFIDL", "QF_UFLIA",
              "QF_UFLRA", "UFLRA",
              "UFNIA"]

def load_files(database, prefix):
    files = []
    with open(database) as fp:
        for l in fp:
            l = l.strip()
            orig = l
            l = prefix + l
            if Path(l).exists():
                files.append((orig, l))
    return files

files = load_files(SOURCE, PREFIX)

def run_cmd(cmd, abort_on_fail=True, output=False):
    sys.stdout.flush()
    try:
        if output:
            stdout = None
            stderr = None
        else:
            stdout = stderr = subprocess.DEVNULL
        subprocess.check_call(
            cmd,
            stdout=stdout,
            stderr=stderr,
        )
        return 0
    except subprocess.CalledProcessError as error:
        print()
        print("*" * 80)
        print(" ".join(cmd))
        subprocess.run(cmd)
        if abort_on_fail:
            sys.exit(1)
        return error.returncode

def run(cmd, abort_on_fail=True):
    sys.stdout.flush()
    subprocess.run(cmd)

def bench(logic="AUFNIRA", timeout = 30):
    total = len(files)
    headers = ["file no.", "filename", "status", "logic", "elapsed"]
    failed = []
    checked = 0
    directory = "results/"
    filename = directory + logic + "-results.csv"
    
    with open(filename, 'w') as results:
        writer = csv.writer(results, delimiter=',')
        writer.writerow(headers)
    
    for (orig, l) in files:
        print(total, orig)
        total -= 1
        sys.stdout.flush()
        checked += 1
        # exit status 1: failed
        # exit status 124: timeout
        cmd = ["timeout", timeout, "./faial-drf", "--logic", logic, l]
        elapsed = 0
        start = time.time()
        EXIT_STATUS = run_cmd(cmd, abort_on_fail=False)
        end = time.time()

        elapsed += int((end - start) * 1000)

        match EXIT_STATUS:
            case 0:
                status = "success"
            case 1:
                status = "failed"
            case _:
                status = "timeout"
        
        if EXIT_STATUS == 1:
            failed.append(f"{orig}")
             
        with open(filename, 'a') as results:
            writer = csv.writer(results, delimiter=',')
            writer.writerow([checked, orig, status, logic, elapsed])

    print(f"Checked: {checked - len(failed)}/{len(files)}")
    print(f"=== Failed: {len(failed)} ===\n\n" + "\n".join(failed))

if __name__ == '__main__':
    for idx, logic in enumerate(LOGICS):
        print(f"Benchmarking {logic} ({idx + 1}/{len(LOGICS)})...")
        bench(logic = logic, timeout = 1)