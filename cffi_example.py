"""

#include <iostream>

class User
{
    std::string name;
    public:
        User(char *name):name(name) {}
        User(std::string &name):name(name) {}

        std::string greet() { return "hello, " + name; }
};

void hello(char *name)
{
    User user(name);
    std::cout << user.greet() << std::endl;
}

int main()
{
    hello((char *) "world");
    return 0;
}

extern "C"
{
    extern void cffi_hello(char *name)
    {
        return hello(name);
    }
}


"""


import cffi


ffi = cffi.FFI()
ffi.cdef("void cffi_hello(char *name);")
C = ffi.dlopen("./libhello.so")


def hello(name):
    C.cffi_hello(name)


if __name__ == "__main__":
    hello("cffi")
