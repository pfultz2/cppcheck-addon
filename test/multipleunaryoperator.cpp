void f1(int i)
{
    // cppcheck-suppress addon-MultipleUnaryOperator
    int b = -(+(!(~i)));
    (void)b;
}

void f2(int i)
{
    // cppcheck-suppress addon-MultipleUnaryOperator
    int b = -+!~i;
    (void)b;
}

void f2(int i)
{
    // no warning
    int b = 1 + -i;
    (void)b;
}
