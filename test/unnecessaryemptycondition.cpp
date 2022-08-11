void f1(std::vector<int> v)
{
    // cppcheck-suppress addon-UnnecessaryEmptyCondition
    if (v.empty())
    {
        for(auto&& x:v)
        {
            (void)x;
        }
    }
}

void f2(std::vector<int> v)
{
    // cppcheck-suppress addon-UnnecessaryEmptyCondition
    if (!v.empty())
    {
        for(auto&& x:v)
        {
            (void)x;
        }
    }
}
