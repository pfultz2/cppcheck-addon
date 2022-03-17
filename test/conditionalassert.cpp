void f(bool x, bool y) {
    // cppcheck-suppress addon-ConditionalAssert
    if (x) {
        assert(y);
    }
}
