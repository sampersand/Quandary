#include <string>
#include <map>
typedef std::string str;
typedef std::map<str, str> map;
struct consts
{  
    map kws;
    consts(){
        kws = new map();
    }
};