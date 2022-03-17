bool f(int a, int b)
{
    // cppcheck-suppress addon-RedundantIfStatement
    if (a == b)
    {
        return true;
    }
    // cppcheck-suppress addon-UnnecessaryElseStatement
    else
    {
        return false;
    }
}
