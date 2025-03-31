# Run the regex engine with different test cases
regex_engine="python main.py"

# Test cases
declare -A tests

tests["hello"]="hello"
tests["^abc$"]="abc abc123 xabc abc\n"
tests["a.c"]="abc aac ac"
tests["[aeiou]"]="e b i"
tests["[a-zA-Z]"]="G 7 _"
tests["\\d"]="5 a"
tests["\\w"]="a _ !"
tests["\\s"]="' ' '	' a"
tests["a*"]=""" aaa b"
tests["a+"]=""" aaa b"
tests["a?"]=""" a aa"
tests["(abc)"]="abc abcd xbc"
tests["(a+)(b*)"]="aabb aa"
tests["cat|dog"]="cat dog bat"
tests["a|b|c"]="a b z"
tests["^([A-Za-z]+)\\s(\\d+)$"]="Alice 123 Bob123"
tests["[a-z]"]="g Z 9"
tests["[0-9]"]="5 a B"

# Run each test case
for pattern in "${!tests[@]}"; do
    echo "Testing pattern: '$pattern'"
    for test_string in ${tests["$pattern"]}; do
        $regex_engine "$pattern" "$test_string"
    done
    echo "--------------------------------"
done
