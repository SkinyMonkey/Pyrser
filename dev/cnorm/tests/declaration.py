working = [
    # variable declaration
    "int foo;",
    "unsigned int foo;",
    "extern unsigned int const foo;",
    "void* foo;",
    "void** foo;",
    "void** const foo;",
    "void* const* const foo;",
    "void const foo;",
    "char tab[];",
    "char foo;double bar;",
    # function pointer declaration
    "char (*foo)(int, int);",
    "char (*foo)(int, ...);",
    "char (*foo)(int, char*);",
    "char (*foo)(int, char const* const);",
    "char (*foo[])(int, int);",
    "char (*foo)(int, int);",
    "char* (*foo)();",
    # type declaration
    "union foo bar;",
    "struct foo bar;",
    "enum foo{a,b} ;",
    "struct foo{char (*ptr)(int);} ;",
    # function decl
    "int main(){}",
    "int main(int argc){}",
    "int main(char* argv[]){}",
    # prototype decl
    "int main();",
    "void main(int, char*);",
    "void main(int argc, char* argv[]);",
    "char* foo();",
]

# "extern const unsigned int foo, bar;", # sub_type = declarator -> __variable__
# FIXME The test in this array are not working
l_test = [
    # type declaration
    "struct foo{int a;int b;char* str;} ;",
    "union foo{int a: 10;int b;char* str;} ;",
    # FIXME : Not working
    # "char* foo(int (*foo)(int, int), char*);",
    # "char* (foo)();", # FIXME : valid?
] + working
