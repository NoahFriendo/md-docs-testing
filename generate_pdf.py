import subprocess
import os
import re
import shutil

TEMP_DIR = "temp_md"

# Cleanup function to remove the temp_md directory


def cleanup_temp_dir():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


# Initial cleanup in case temp_md exists from a previous run
cleanup_temp_dir()

# Temp directory to store modified markdown files
os.makedirs(TEMP_DIR, exist_ok=True)

all_modified_files = []

# Walk through the docs directory
for root, dirs, files in os.walk("docs"):
    for file in files:
        if file.endswith(".md"):
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()

                # Replace relative image paths with absolute paths
                # Here we assume the markdown uses the format ![alt](path)
                content = re.sub(r'\!\[([^\]]*)\]\(([^)]+)\)',
                                 lambda m: '![{}]({})'.format(
                                     m.group(1),
                                     os.path.abspath(
                                         os.path.join(root, m.group(2))
                                     )
                                 ),
                                 content)

                # Write out to the temporary directory
                new_file_path = os.path.join(TEMP_DIR, file)
                with open(new_file_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(content)

                all_modified_files.append(new_file_path)

# Run pandoc with modified markdown files
command = ["pandoc"] + all_modified_files + \
    ["-o", "site/output.pdf", "--toc", "--pdf-engine=xelatex"]
subprocess.run(command)

# Cleanup the temp_md directory after the PDF is generated
cleanup_temp_dir()
