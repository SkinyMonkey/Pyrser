from .expression import Expression
from .statement import Statement
from .declaration import Declaration

o_root = {}
print((Declaration().parse("int main(){}", o_root, "declaration")))
