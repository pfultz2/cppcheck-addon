int f(int a)
{
    if (1)
    {
        a++;
    }
    // cppcheck-suppress addon-EmptyElseBlock
    else
    {
    }
    return a;
}
