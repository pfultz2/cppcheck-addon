void example()
{
    A:
        a();
    // cppcheck-suppress addon-GotoStatement
    goto A;
}