void f(int i) {
    // cppcheck-suppress addon-RedundantCast
    float xx = static_cast<float>(i);
    // cppcheck-suppress addon-RedundantCast
    auto yy = static_cast<float>(i);
}
