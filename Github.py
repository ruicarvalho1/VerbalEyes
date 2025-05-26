import os
import subprocess
import argparse

def get_untracked_files():
    result = subprocess.run(
        ['git', 'ls-files', '--others', '--exclude-standard'],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )
    return [line for line in result.stdout.splitlines() if line]

def chunk_and_commit(files, max_bytes, max_files):
    chunk = []
    chunk_bytes = 0
    commit_num = 1

    for file in files:
        if not os.path.isfile(file):
            continue
        size = os.path.getsize(file)

        # Check if adding this file exceeds chunk limits
        if chunk and (chunk_bytes + size > max_bytes or len(chunk) + 1 > max_files):
            # Commit current chunk
            print(f"Committing chunk {commit_num}: {len(chunk)} files, {chunk_bytes / (1024*1024):.2f} MB")
            subprocess.run(['git', 'add'] + chunk, check=True)
            subprocess.run([
                'git', 'commit', '-m',
                f"Add chunk {commit_num}: {len(chunk)} files, {chunk_bytes / (1024*1024):.2f} MB"
            ], check=True)
            # Push after each commit
            subprocess.run(['git', 'push'], check=True)
            commit_num += 1
            chunk = []
            chunk_bytes = 0

        chunk.append(file)
        chunk_bytes += size

    # Commit any remaining files
    if chunk:
        print(f"Committing chunk {commit_num}: {len(chunk)} files, {chunk_bytes / (1024*1024):.2f} MB")
        subprocess.run(['git', 'add'] + chunk, check=True)
        subprocess.run([
            'git', 'commit', '-m',
            f"Add chunk {commit_num}: {len(chunk)} files, {chunk_bytes / (1024*1024):.2f} MB"
        ], check=True)
        # Push final chunk
        subprocess.run(['git', 'push'], check=True)

    print("All untracked files have been committed and pushed in chunks.")

def main():
    parser = argparse.ArgumentParser(
        description="Commit untracked Git files in chunks by size and count, then push each commit."
    )
    parser.add_argument(
        '--max-bytes', type=int, default=100 * 1024 * 1024,
        help="Maximum total size per commit in bytes (default: 100 MB)"
    )
    parser.add_argument(
        '--max-files', type=int, default=1000,
        help="Maximum number of files per commit (default: 1000)"
    )
    args = parser.parse_args()

    # Ensure we're inside a Git repository
    try:
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: This script must be run inside a Git repository.")
        return

    files = get_untracked_files()
    if not files:
        print("No untracked files to commit and push.")
        return

    chunk_and_commit(files, args.max_bytes, args.max_files)

if __name__ == "__main__":
    main()
