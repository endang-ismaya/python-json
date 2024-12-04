import difflib

text1 = "apple meta google"
text2 = "apple meta microsoft"

differ = difflib.Differ()

result = list(differ.compare(text1.split(), text2.split()))
print(result)
