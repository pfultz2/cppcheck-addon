int f(int a)
{
    int b = a * 2;
    // cppcheck-suppress addon-RedundantLocalVariable
    return b;
}
