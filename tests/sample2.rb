def foo (arg1, arg2, arg3)
    a = 42
    b = a / 2
    def barr(arg2)
        b = 99
        return b
    end
    c=barr(b)
    barr(a)
end

def bazz(arg2)
    b = 99
    return b
end