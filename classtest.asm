.class classtest:Obj
.method $constructor
.local test,seven
    enter
    load test
    const 1
    new Test
    store test
    load seven
    load test
    const 7
    call Test:Seven
    store seven
    load seven
    call Int:print
    return 0
