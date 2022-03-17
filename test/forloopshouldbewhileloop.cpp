void f(int a)
{
    // cppcheck-suppress addon-ForLoopShouldBeWhileLoop
    for (; a < 100;)
    {
        foo(a);
    }
}
