#!/usr/bin/env python3
"""
전체 프로젝트 - v2_autogolf-project 리포지토리로 Push
모노레포 전체를 origin에 push
"""
import subprocess
import sys
from pathlib import Path

# 설정
REMOTE_URL = 'https://github.com/seojongik/v2_autogolf-project.git'

# 색상 코드
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    print(f"{Colors.BLUE}{Colors.BOLD}▶ {message}{Colors.RESET}")

def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.RESET}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def run_command(cmd, cwd=None, check=True):
    try:
        result = subprocess.run(
            cmd, cwd=cwd, check=check,
            capture_output=True, text=True
        )
        return result.stdout.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        if check:
            print_error(f"명령 실행 실패: {' '.join(cmd)}")
            print_error(f"에러: {e.stderr}")
            raise
        return e.stderr.strip(), e.returncode

def main():
    root = Path(__file__).parent

    print(f"{Colors.BOLD}전체 프로젝트 - v2_autogolf-project 리포지토리로 Push{Colors.RESET}")
    print(f"대상 리포: {REMOTE_URL}")
    print()

    # 변경사항 확인
    print_step("변경사항 확인")
    status_output, _ = run_command(['git', 'status', '--porcelain'], cwd=root, check=False)

    if not status_output:
        print_warning("변경사항이 없습니다.")

        # Push 안된 커밋 확인
        current_branch, _ = run_command(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=root
        )
        ahead_behind, _ = run_command(
            ['git', 'rev-list', '--left-right', '--count', f'origin/{current_branch}...HEAD'],
            cwd=root, check=False
        )

        if ahead_behind:
            parts = ahead_behind.split()
            if len(parts) == 2 and int(parts[1]) > 0:
                print_warning(f"Push되지 않은 커밋이 {parts[1]}개 있습니다.")
                response = input(f"{Colors.YELLOW}Push하시겠습니까? (y/N): {Colors.RESET}").lower()
                if response == 'y':
                    print_step(f"Push 중 (origin/{current_branch})")
                    run_command(['git', 'push', 'origin', current_branch], cwd=root)
                    print_success("Push 완료!")
                sys.exit(0)

        print("할 일이 없습니다.")
        sys.exit(0)

    # 변경된 프로젝트 표시
    print_success("변경사항 발견:")
    for line in status_output.split('\n'):
        if line.startswith(' M') or line.startswith('M '):
            folder = line.split('/')[0].split()[-1] if '/' in line else ''
            print(f"  {line}")
    print()

    # 커밋 메시지 입력
    commit_message = None
    if len(sys.argv) > 1:
        commit_message = sys.argv[1]
    else:
        print(f"{Colors.YELLOW}커밋 메시지를 입력하세요:{Colors.RESET}")
        commit_message = input("> ")

    if not commit_message:
        print_error("커밋 메시지가 비어있습니다.")
        sys.exit(1)

    # 전체 add
    print_step("전체 스테이징")
    run_command(['git', 'add', '.'], cwd=root)
    print_success("스테이징 완료")
    print()

    # 커밋
    print_step("커밋 생성")
    run_command(['git', 'commit', '-m', commit_message], cwd=root)
    print_success(f"커밋 완료: {commit_message}")
    print()

    # Push
    current_branch, _ = run_command(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        cwd=root
    )

    response = input(f"{Colors.YELLOW}v2_autogolf-project에 Push하시겠습니까? (y/N): {Colors.RESET}").lower()
    if response != 'y':
        print_warning("Push를 취소했습니다. 커밋은 로컬에 저장되었습니다.")
        sys.exit(0)

    print_step(f"Push 중 (origin/{current_branch})")
    run_command(['git', 'push', 'origin', current_branch], cwd=root)

    print()
    print_success("전체 Push 완료!")
    print(f"{Colors.GREEN}✓ {REMOTE_URL} 에 전체 프로젝트가 push 되었습니다.{Colors.RESET}")

if __name__ == '__main__':
    main()
