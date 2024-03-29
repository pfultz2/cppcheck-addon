import cppcheck, itertools
from cppcheckdata import simpleMatch, match

def skipTokenMatches(tokens, skip=None):
    for tok in tokens:
        if match(tok, skip):
            continue
        yield tok

def isTokensEqual(xtokens, ytokens, skip=None):
    for x, y in itertools.zip_longest(skipTokenMatches(xtokens, skip), skipTokenMatches(ytokens, skip)):
        if not x:
            return False
        if not y:
            return False
        if x.str != y.str:
            return False
    return True

def getInnerLink(token):
    if not token:
        return []
    if not token.link:
        return []
    return token.next.forward(token.link)

def getVariableDecl(var):
    if not var:
        return []
    end = var.typeEndToken
    if end:
        end = end.next
    return var.typeStartToken.forward(end)

@cppcheck.checker
def AvoidBranchingStatementAsLastInLoop(cfg, data):
    for token in cfg.tokenlist:
        end = match(token, "for|while (*) {*}").end
        if not end:
            continue
        stmt = end.tokAt(-2)
        if not match(stmt, "%any% ; }"):
            continue
        if not match(stmt, "break|continue"):
            stmt = stmt.astTop()
        if match(stmt, "break|continue|return"):
            cppcheck.reportError(stmt, "style", "Branching statement as the last statement inside a loop is very confusing.")

@cppcheck.checker
def CollapsibleIfStatements(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "if (*) { if (*) {*} }"):
            continue
        cppcheck.reportError(token, "style", "These two if statements can be collapsed into one.")

@cppcheck.checker
def ConditionalAssert(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "if (*) { assert (*) ; }"):
            continue
        cppcheck.reportError(token, "style", "The if condition should be included in assert.")

@cppcheck.checker
def EmptyCatchStatement(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "catch (*) { }"):
            continue
        cppcheck.reportError(token, "style", "An empty catch statement.")

@cppcheck.checker
def EmptyDoWhileStatement(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "do { } while ("):
            continue
        cppcheck.reportError(token, "style", "Empty do-while.")

@cppcheck.checker
def EmptyElseBlock(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "else { }"):
            continue
        cppcheck.reportError(token, "style", "Empty else statement can be safely removed.")

@cppcheck.checker
def EmptyForStatement(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "for (*) { }"):
            continue
        cppcheck.reportError(token, "style", "Empty for statement.")

@cppcheck.checker
def EmptyIfStatement(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "if (*) { }"):
            continue
        cppcheck.reportError(token, "style", "Empty if statement.")

@cppcheck.checker
def EmptySwitchStatement(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "switch (*) { }"):
            continue
        cppcheck.reportError(token, "style", "Empty switch statement.")

@cppcheck.checker
def EmptyWhileStatement(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "while (*) { }"):
            continue
        cppcheck.reportError(token, "style", "Empty while statement.")

@cppcheck.checker
def ForLoopShouldBeWhileLoop(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "for ( ; !!;"):
            continue
        # Skip empty for loops
        if match(token, "for (*) { }"):
            continue
        end = token.next.link
        if not match(end.tokAt(-1), "; )"):
            continue
        cppcheck.reportError(token, "style", "For loop should be written as a while loop.")

@cppcheck.checker
def GotoStatement(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "goto"):
            continue
        cppcheck.reportError(token, "style", "Goto considered harmful.")

@cppcheck.checker
def InvertedLogic(cfg, data):
    for token in cfg.tokenlist:
        cond = None
        if match(token, "if (*) {*} else { !!if"):
            cond = token.next.astOperand2
        elif match(token, "?"):
            cond = token.astOperand1
        if not match(cond, "!|!="):
            continue
        cppcheck.reportError(cond, "style", "It is cleaner to invert the logic.")

@cppcheck.checker
def MultipleUnaryOperator(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "+|-|~|!"):
            continue
        if not token.isUnaryOp(token.str):
            continue
        if not match(token.astOperand1, "+|-|~|!"):
            continue
        if not token.astOperand1.isUnaryOp(token.astOperand1.str):
            continue
        cppcheck.reportError(token, "style", "Muliple unary operators used together.")

@cppcheck.checker
def NestedBlocks(cfg, data):
    for token in cfg.tokenlist:
        block = match(token, "if|while|for|switch (*) { {*}@block }").block
        if not block:
            block = match(token, "; { {*}@block break ; }").block
        if not block:
            continue
        cppcheck.reportError(block, "style", "Block directly inside block.")

@cppcheck.checker
def RedundantCast(cfg, data):
    for token in cfg.tokenlist:
        m = match(token, "%var%@decl ; %var%@assign = static_cast <*>@cast (*) ;")
        if not m:
            continue
        if m.decl.varId != m.assign.varId:
            continue
        if not match(token.previous, "auto"):
            if not isTokensEqual(getVariableDecl(m.decl.variable), getInnerLink(m.cast), skip='const|volatile|&|&&|*'):
                continue
        if not match(token, "%var%@decl ; %var%@assign = static_cast <*>@cast (*) ;"):
            continue
        cppcheck.reportError(token, "style", "Static cast is redundant.")

@cppcheck.checker
def RedundantConditionalOperator(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "? true|false : true|false"):
            continue
        cppcheck.reportError(token, "style", "Conditional operator is redundant.")

@cppcheck.checker
def RedundantIfStatement(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "if (*) { return true|false ; } else { return true|false ; }"):
            continue
        cppcheck.reportError(token, "style", "The if statement is redundant.")

@cppcheck.checker
def RedundantLocalVariable(cfg, data):
    for token in cfg.tokenlist:
        m = match(token, "%var%@decl ; %var%@assign = **; return %var%@returned ;")
        if not m:
            continue
        if m.decl.varId != m.assign.varId:
            continue
        if m.decl.varId != m.returned.varId:
            continue
        cppcheck.reportError(m.returned, "style", "Variable is returned immediately after its declaration, can be simplified to just return expression.")

@cppcheck.checker
def UnnecessaryElseStatement(cfg, data):
    for token in cfg.tokenlist:
        m = match(token, "if (*) {*}@block else@else_statement {")
        if not m:
            continue
        stmt = m.block.link.tokAt(-2)
        if not match(stmt, "%any% ; }"):
            continue
        if not match(stmt, "break|continue"):
            stmt = stmt.astTop()
        if not match(stmt, "break|continue|return|throw"):
            continue
        cppcheck.reportError(m.else_statement, "style", "Else statement is not necessary.")

@cppcheck.checker
def UnnecessaryEmptyCondition(cfg, data):
    for token in cfg.tokenlist:
        m = match(token, "if (*)@if_cond { for (*)@for_cond {*} }")
        if not m:
            continue
        cond = m.if_cond.astOperand2
        if match(cond, "!"):
            cond = cond.astOperand1
        if not match(cond.tokAt(-2), ". empty ("):
            continue
        container = cond.tokAt(-2).astOperand1
        if not container.varId:
            continue
        if not match(m.for_cond.astOperand2, ":"):
            continue
        container_iter = m.for_cond.astOperand2.astOperand2
        if container_iter.varId != container.varId:
            continue
        cppcheck.reportError(container, "style", "Unnecessary check for empty before for range loop.")

# @cppcheck.checker
# def useStlAlgorithm(cfg, data):
#     for token in cfg.tokenlist:
#         if not match(token, "for ("):
#             continue
#         cppcheck.reportError(token, "style", "Considering using algorithm instead.")

