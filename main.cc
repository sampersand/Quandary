#include "constants.cc"
#include <iostream>
int main(int argc, char const *argv[])
{
    /* code */
    constants* c = new constants();
    std::cout << c->a;
    return 0;
}