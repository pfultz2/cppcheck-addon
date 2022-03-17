void f(int a, int b, int c)
{
    // cppcheck-suppress addon-RedundantConditionalOperator
    bool b1 = a > b ? true : false;
    // cppcheck-suppress addon-RedundantConditionalOperator
    bool b2 = a > b ? false : true;
    (void)b1;
    (void)b2;
}