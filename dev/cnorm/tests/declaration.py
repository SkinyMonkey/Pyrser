#"extern const unsigned int foo, bar;", # sub_type = declarator -> __variable__
lTest = [
    "int foo;",
    #"unsigned int foo;",
    #"extern unsigned int const foo;",
    #"void* foo;",
    #"void** foo;",
    #"void** const foo;",
    #"void* const* const foo;",
    #"void const foo;",
    #"char tab[];",
    #"char foo;double bar;",
    #"char (*foo)(int, int);",
    #"char (*foo)(int, ...);",
    #"char (*foo)(int, char*);",
    #"char (*foo)(int, char const* const);",
    #"char (*foo[])(int, int);",
    #"union foo bar;",
    #"struct foo bar;",
    "struct foo{char (*ptr)(int);} ;",
    "struct foo{int a;int b;char* str;} ;",
    "union foo{int a: 10;int b;char* str;} ;",
    "enum foo{a,b} ;",
    "int main(){}",
    "int main(int argc){}",
    "int main(char* argv[]){}",
    "int main();",
    "void main(int, char*);",
    "void main(int argc, char* argv[]);",
    "char* foo();",
    "char* (*foo)();",
    "char* foo(int (*foo)(int, int), char*);",
    # this one work, it is just the template output that will not the same:
    #"char* (foo)();",
]
