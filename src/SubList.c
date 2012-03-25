#include <boost/python.hpp>
#include <vector>
#include <string>
#include <algorithm>
#include <boost/unordered_map.hpp>

using namespace std;
using namespace boost;
unordered_map<string,string> strlist;

void load_autocorrections()
{
    FILE *f = fopen("autocorrections","r");
    char tmp1[255]={0}, tmp2[255]={0};

    if(f == NULL)
    {
        printf("Error couldn't open the autocorrections file");
        return;
    }

    while(!feof(f))
    {
        int n = fscanf(f, "\"%[^\"]\" \"%[^\"]\"\n", tmp1, tmp2);
        if(n != 2)
            break;
        strlist[tmp1] = tmp2;
    }

    fclose(f);
}

// Thanks stackoverflow
inline std::string narrow(std::wstring const& text)
{
    std::locale const loc("");
    wchar_t const* from = text.c_str();
    std::size_t const len = text.size();
    std::vector<char> buffer(len + 1);
    std::use_facet<std::ctype<wchar_t> >(loc).narrow(from, from + len, '_', &buffer[0]);
    return std::string(&buffer[0], &buffer[len]);
}

string const match(wstring wordw)
{
    string word = narrow(wordw);

    unordered_map<string,string>::iterator iter;

    iter = strlist.find(word);

    if(iter == strlist.end())
        return "";
    return iter->second;
}

BOOST_PYTHON_MODULE(SubList)
{
    using namespace boost::python;

    def("match", match);

    load_autocorrections();
}
