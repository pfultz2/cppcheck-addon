void f()
{
    try
    {
        int* m= new int[1000];
    }
    // cppcheck-suppress addon-EmptyCatchStatement
    catch(...)
    {
    }
}
