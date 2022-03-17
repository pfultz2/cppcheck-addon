bool f(int a)
{
    if (a == 1)
    {
        cout << "a is 1.";
        return true;
    }
    // cppcheck-suppress addon-UnnecessaryElseStatement
    else
    {
        cout << "a is not 1."
    }
    return false;
}
