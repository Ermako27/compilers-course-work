def foo (arg1, arg2, arg3)
    intVar = 42
    dynVar = a / 2
    arrVar = []
    fullArrVar = [9, 8]
    fullArrVar[0] = 5
    strVar = 'hello'
    floatVar = 9.9
    arrayOfVar = [intVar, floatVar]

    def barr(arg2)
        b = 99
        dynVar = a / 2
        arrVar = []
        return b
    end

    funcCallVar = barr(intVar)
    return b
end

def bazz(arg2)
    b = 99
    return b
end