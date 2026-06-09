#!/usr/bin/env python3
"""Run all scenario YAML files through the local malsim CLI and summarize failures."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pexpect

REPO = Path(__file__).resolve().parents[1]
MALSIM = REPO / '.venv' / 'bin' / 'malsim'


def iter_scenarios(root: Path):
    return sorted(
        p for p in root.rglob('*.yml')
        if 'scenario' in p.name.lower()
    )


def run_scenario(path: Path) -> tuple[int, str, bool]:
    cmd = [str(MALSIM), str(path)]
    child = pexpect.spawn(cmd[0], cmd[1:], cwd=REPO, encoding='utf-8', timeout=20)
    child.delaybeforesend = 0

    try:
        idx = child.expect([
            r'Enter action or leave empty to wait:',
            pexpect.EOF,
            pexpect.TIMEOUT,
        ], timeout=20)

        if idx == 0:
            started = True
            # Feed a few interactions to confirm the scenario is interactive and alive,
            # then stop it intentionally so the smoke test does not hang.
            for _ in range(3):
                child.send('0\r')
                next_idx = child.expect([
                    r'Enter action or leave empty to wait:',
                    pexpect.EOF,
                    pexpect.TIMEOUT,
                ], timeout=8)
                if next_idx != 0:
                    break
            child.sendcontrol('c')
            child.expect(pexpect.EOF, timeout=10)
            status = child.exitstatus
            output = str(child.before or '')
            return (0 if status in (0, 130, None) else status), output, started

        child.expect(pexpect.EOF, timeout=30)
        status = child.exitstatus
        output = str(child.before or '')
        return (status if status is not None else 1), output, False
    except pexpect.ExceptionPexpect as exc:
        output = str(child.before or '') + str(exc)
        return 1, output, False


def main() -> None:
    scenarios = iter_scenarios(REPO / 'scenarios')
    failures = []
    succeeded = 0

    for path in scenarios:
        rel = path.relative_to(REPO)
        status, output, started = run_scenario(path)
        if status == 0:
            succeeded += 1
            label = 'OK' if not started else 'OK (interactive stop)'
            print(f'{label:<20} {rel}')
        else:
            failures.append((rel, status, output))
            short = output.strip().splitlines()[-5:]
            print(f'FAIL               {rel} (exit={status})')
            for line in short:
                print('     ' + line)

    print('\nSUMMARY')
    print(f'  total scenarios: {len(list(scenarios))}')
    print(f'  succeeded: {succeeded}')
    print(f'  failed: {len(failures)}')

    if failures:
        sys.exit(1)


if __name__ == '__main__':
    main()
