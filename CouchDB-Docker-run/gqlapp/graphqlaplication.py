
from conect import conectToCouch

client = conectToCouch()
print("overeni jestli existuje spojeni.")
db=client["testingdata"]