import cppcheck

patterns = {
    '%any%': lambda tok: tok,
    '%assign%': lambda tok: tok if tok.isAssignmentOp else None,
    '%comp%': lambda tok: tok if tok.isComparisonOp else None,
    '%name%': lambda tok: tok if tok.isName else None,
    '%op%': lambda tok: tok if tok.isOp else None,
    '%or%': lambda tok: tok if tok.str == '|' else None,
    '%oror%': lambda tok: tok if tok.str == '||' else None,
    '%var%': lambda tok: tok if tok.variable else None,
    '(*)': lambda tok: tok.link if tok.str == '(' else None,
    '[*]': lambda tok: tok.link if tok.str == '[' else None,
    '{*}': lambda tok: tok.link if tok.str == '{' else None,
    '<*>': lambda tok: tok.link if tok.str == '<' and tok.link else None,
}

def match_atom(token, p):
    if not token:
        return None
    if not p:
        return None
    if token.str == p:
        return token
    if p in ['!', '|', '||', '%']:
        return None
    if p in patterns:
        return patterns[p](token)
    if '|' in p:
        for x in p.split('|'):
            t = match_atom(token, x)
            if t:
                return t
    if p.startswith('!'):
        t = match_atom(token, p[1:])
        if not t:
            return token
    return None

def match(token, pattern):
    result = None
    for p in pattern.split(' '):
        t = match_atom(token, p)
        if not t:
            return None
        result = t
        token = t.next
    return result

def forward(token):
    while token:
        yield token
        token = token.next

def backward(token):
    while token:
        yield token
        token = token.previous

def astParents(token):
    while token and token.astParent:
        token = token.astParent
        yield token

def astTop(token):
    top = None
    for parent in astParents(token):
        top = parent
    return top

def tokAt(token, n):
    tl = forward(token)
    if n < 0:
        tl = backward(token)
        n = -n
    for i, t in enumerate(tl):
        if i == n:
            return t

@cppcheck.checker
def AvoidBranchingStatementAsLastInLoop(cfg, data):
    for token in cfg.tokenlist:
        end = match(token, "for|while (*) {*}")
        stmt = tokAt(end, -2)
        if not match(stmt, "%any% ; }"):
            continue
        if not match(stmt, "break|continue"):
            stmt = astTop(stmt)
        if match(stmt, "break|continue|return"):
            cppcheck.reportError(stmt, "style", "Branching statement as the last statement inside a loop is very confusing.")

@cppcheck.checker
def CollapsibleIfStatements(cfg, data):
    for token in cfg.tokenlist:
        if not match(token, "if (*) { if (*) {*} }"):
            continue
        cppcheck.reportError(token, "style", "These two if statements can be collapsed into one.")

