
void f1() {
    for (int i = 0; i < 10; i++) {
        if (foo(i)) {
            continue;
        }
        // cppcheck-suppress addon-AvoidBranchingStatementAsLastInLoop
        break;
    }
}

void f2() {
    for (int i = 0; i < 10; i++) {
        if (foo(i)) {
            continue;
        }
        // cppcheck-suppress addon-AvoidBranchingStatementAsLastInLoop
        continue;
    }
}

int f3() {
    for (int i = 0; i < 10; i++) {
        if (foo(i)) {
            continue;
        }
        // cppcheck-suppress addon-AvoidBranchingStatementAsLastInLoop
        return i + 1;
    }
    return 1;
}
