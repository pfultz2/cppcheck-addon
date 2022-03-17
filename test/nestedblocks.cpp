int f1(int x)
{
    if (x) {
        // should warn but cppcheck strips the extra braces
        { return x; }
    }
    return 0;
}
void f2(int x)
{
    switch (x)
    {
        case 1: break;
        case 2: {} break;
        case 3:
        {
            // cppcheck-suppress addon-NestedBlocks
            {
            }
            break;
        }
    }
}