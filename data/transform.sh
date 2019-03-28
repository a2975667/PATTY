for file in *.pkl
    do python -mpickle "$file" > "$file.txt"
done