void f(bool x, bool y)
{
    // cppcheck-suppress addon-CollapsibleIfStatements
    if (x)
    {
        if (y)
        {
            foo();
        }
    }
}
