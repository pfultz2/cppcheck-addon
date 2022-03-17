void f(bool b)
{
    // cppcheck-suppress addon-MultipleUnaryOperator
    int b1 = !!b;
    // cppcheck-suppress addon-MultipleUnaryOperator
    int b2 = ~~b;
    // cppcheck-suppress addon-MultipleUnaryOperator
    int b3 = !(!b);
    // cppcheck-suppress addon-MultipleUnaryOperator
    int b4 = ~(~b);
    (void)b1;
    (void)b2;
    (void)b3;
    (void)b4;
}
