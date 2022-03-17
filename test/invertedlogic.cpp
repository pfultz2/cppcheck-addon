int f(int a)
{
    int i;
    // cppcheck-suppress addon-InvertedLogic
    if (a != 0)
    {
        i = 1;
    }
    else
    {
        i = 0;
    }

    // cppcheck-suppress addon-InvertedLogic
    return !i ? -1 : 1;
}
