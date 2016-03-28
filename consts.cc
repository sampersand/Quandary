#include <string>
#include <map>
typedef std::string str;
typedef std::map<str, str> smap; //string map
typedef std::map<str, std::map<str, auto>> mmap; //map map
namespace consts
{

    namespace punc {
        str comment[1] = {"#"};
        str escape[1] = {"\\"};
        str linebreak[2] = {";", "\n"};
        str endcomment[3] = {"\n", "\r", "#"};
        str quotes[2] = {"'", "\""};
        str whitespace[4] = {" ", "\n", "\t", "\r"};
        namespace parens {
            str r[] = {"(", "[", "{"};
            str l[] = {")", "]", "}"};
        }
    }
    namespace kws {
        namespace opers {
            namespace assignment {
                // '->'
            }
            // 'assignment': _dict({
            //     '->': _dict({'obj':operobj, 'rank': 13, 'reqs': ((2,), (0,))}),
            //     '<-': _dict({'obj':operobj, 'rank': 13, 'reqs': ((2,), (0,))}),
            // }),
            // 'simple_binary': _dict({
            //     'math': _dict({
            //         '**': _dict({'obj':operobj, 'rank':  3, 'reqs': ((2,), (0,))}),
            //         '*' : _dict({'obj':operobj, 'rank':  4, 'reqs': ((2,), (0,))}),
            //         '/' : _dict({'obj':operobj, 'rank':  4, 'reqs': ((2,), (0,))}),
            //         '%' : _dict({'obj':operobj, 'rank':  4, 'reqs': ((2,), (0,))}),
            //         '+' : _dict({'obj':operobj, 'rank':  5, 'reqs': ((2,), (0,))}),
            //         '-' : _dict({'obj':operobj, 'rank':  5, 'reqs': ((2,), (0,))}),
            //     }),

            //     'bitwise': _dict({
            //         '>>': _dict({'obj':operobj, 'rank':  6, 'reqs': ((2,), (0,))}),
            //         '<<': _dict({'obj':operobj, 'rank':  6, 'reqs': ((2,), (0,))}),
            //         '&' : _dict({'obj':operobj, 'rank':  7, 'reqs': ((2,), (0,))}),
            //         '^' : _dict({'obj':operobj, 'rank':  8, 'reqs': ((2,), (0,))}),
            //         '|' : _dict({'obj':operobj, 'rank':  9, 'reqs': ((2,), (0,))}),
            //     }),
            // }),
            // 'bitwise': _dict({
            //     '~' : _dict({'obj':operobj, 'rank':None,'reqs': (1, 0)}),
            // }),
            // 'logic': _dict({
            //     '=' : _dict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
            //     '<>': _dict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
            //     '<' : _dict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
            //     '<=': _dict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
            //     '>' : _dict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
            //     '>=': _dict({'obj':operobj, 'rank': 10, 'reqs': ((2,), (0,))}),
            //     '&&': _dict({'obj':operobj, 'rank': 11, 'reqs': ((2,), (0,))}),
            //     '||': _dict({'obj':operobj, 'rank': 12, 'reqs': ((2,), (0,))}),
            // }),

            // 'delims': _dict({
            //     ':' : _dict({'obj':operobj, 'rank':  0, 'reqs': ((2,), (0,))}),
            //     '.' : _dict({'obj':operobj, 'rank':  0, 'reqs': ((2, 1), (0,))}),
            //     ',' : _dict({'obj':operobj, 'rank': 14, 'reqs': ((2,), (0,))}),
            //     ';' : _dict({'obj':operobj, 'rank': 15, 'reqs': ((1,), (0,))}),
            // }),
        }
    }
}
