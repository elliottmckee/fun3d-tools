
#!/bin/bash
base_dir=$(pwd)

# Find all directories containing _run_.sh scripts
directories=$(find . -type f -name "*_run_.sh" -exec dirname {} \; | sort -u)
# echo "$directories"

# Loop over each directory, run, cd back
for dir in $directories; do
    echo "Running case: $dir"
    cd $dir
    sh _run_.sh
    cd $base_dir
done
