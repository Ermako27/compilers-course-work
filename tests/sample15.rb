def bar(arg)
    result = arg / 2
end
def foo(arg)
    divided = bar(10)
    result = bar(arg) + 2

    complex = (divided * result) + (divided / result)
    return result
end

foo(2)